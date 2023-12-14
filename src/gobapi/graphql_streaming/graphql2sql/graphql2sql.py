import re
from typing import List, Optional

from antlr4 import CommonTokenStream, InputStream

from gobcore.model.metadata import FIELD
from gobcore.model.relations import get_relation_name
from gobcore.typesystem import gob_types, is_gob_geo_type

from gobapi import gob_model
from gobapi.auth.auth_query import Authority
from gobapi.constants import API_FIELD
from gobapi.graphql_streaming.graphql2sql.grammar.GraphQLLexer import GraphQLLexer
from gobapi.graphql_streaming.graphql2sql.grammar.GraphQLParser import GraphQLParser
from gobapi.graphql_streaming.graphql2sql.grammar.GraphQLVisitor import GraphQLVisitor as BaseVisitor
from gobapi.graphql_streaming.resolve import CATALOG_NAME, COLLECTION_NAME
from gobapi.graphql_streaming.utils import resolve_schema_collection_name
from gobapi.utils import to_snake


class GraphQLVisitor(BaseVisitor):
    """Visitor for ANTLR4 GraphQL parse tree, generated with the GraphQL.g4 grammar.

    Visitor uses a relationStack to keep track of to which relation the visited selects and arguments
    belong. Visitor also puts the parent of each relation in the relationParents dict.

    Note: This visitor does not implement the full parse tree. The current implementation is the minimal
    implementation to support parsing of the GraphQL queries GOB currently sends to the endpoint.
    NotImplementedErrors are raised to avoid unexpected behaviour in not-implemented parts of the parse tree.
    """

    def __init__(self):
        self.relationStack = []
        self.selects = {}
        self.relationParents = {}
        self.relationAliases = {}
        self.arguments = {}

    def pushRelationStack(self, relation: str, alias: str):
        """Pushes relation to stack.

        :param relation:
        :return:
        """
        self.relationParents[alias] = self.relationStack[-1] if len(self.relationStack) else None
        self.relationStack.append(alias)
        self.relationAliases[alias] = relation

        if relation not in self.selects:
            self.selects[alias] = {
                'fields': [],
                'arguments': self.arguments,
            }
            self.arguments = {}

    def popRelationStack(self):
        return self.relationStack.pop()

    def addSelectField(self, fieldname: str):
        self.selects[self.relationStack[-1]]['fields'].append(fieldname)

    def addArgument(self, key, value):
        self.arguments[key] = value

    def visitDirective(self, ctx: GraphQLParser.DirectiveContext):
        if str(ctx.NAME()) == "formatdate":
            # Ignore this one for now
            pass
        else:  # pragma: no cover
            raise NotImplementedError(f"Not implemented directive {ctx.NAME()}")

    def visitField(self, ctx: GraphQLParser.FieldContext):
        if ctx.arguments():
            self.visitArguments(ctx.arguments())

        if ctx.directives():
            self.visitDirectives(ctx.directives())

        # Alias is ignored for now
        field_name, alias = self.visitFieldName(ctx.fieldName())

        if ctx.selectionSet():
            # Relation
            if field_name in ['edges', 'node']:
                # Ignore stack, just visit
                self.visitSelectionSet(ctx.selectionSet())
            elif field_name == 'pageInfo':
                # Ignore pageInfo
                pass
            else:
                self.pushRelationStack(field_name, alias)
                self.visitSelectionSet(ctx.selectionSet())
                self.popRelationStack()
        else:
            # Normal field
            self.addSelectField(field_name)

    def visitArgument(self, ctx: GraphQLParser.ArgumentContext):

        if ctx.valueOrVariable():
            value = self.visitValueOrVariable(ctx.valueOrVariable())
            name = str(ctx.NAME())
            self.addArgument(name, value)
        elif ctx.SORT():
            if ctx.nameArray():
                value = self.visitNameArray(ctx.nameArray())
                self.addArgument('sort', value)
            else:
                value = str(ctx.NAME())
                self.addArgument('sort', [value])
        else:  # pragma: no cover
            raise NotImplementedError(f"Not implemented argument {ctx}")

    def visitNameArray(self, ctx: GraphQLParser.NameArrayContext):
        return [str(n) for n in ctx.NAME()]

    def visitValueOrVariable(self, ctx: GraphQLParser.ValueOrVariableContext):
        if ctx.value():
            if isinstance(ctx.value(), GraphQLParser.StringValueContext):
                return self.visitStringValue(ctx.value())
            if isinstance(ctx.value(), GraphQLParser.NumberValueContext):
                return self.visitNumberValue(ctx.value())
            if isinstance(ctx.value(), GraphQLParser.BooleanValueContext):
                return self.visitBooleanValue(ctx.value())
            raise NotImplementedError(f"Not implemented value type {type(ctx.value())}")  # pragma: no cover
        if ctx.variable():
            return self.visitVariable(ctx.variable())

    def visitStringValue(self, ctx: GraphQLParser.StringValueContext):
        return str(ctx.STRING())

    def visitNumberValue(self, ctx: GraphQLParser.NumberValueContext):
        return str(ctx.NUMBER())

    def visitBooleanValue(self, ctx: GraphQLParser.BooleanValueContext):
        return str(ctx.BOOLEAN()) != 'false'

    def visitFieldName(self, ctx: GraphQLParser.FieldNameContext):
        """

        :param ctx:
        :return: fieldname, alias
        """
        if ctx.alias():
            return self.visitAlias(ctx.alias())

        return ctx.NAME().getText(), ctx.NAME().getText()

    def visitAlias(self, ctx: GraphQLParser.AliasContext):
        """

        :param ctx:
        :return: fieldname, alias
        """
        return ctx.NAME(1).getText(), ctx.NAME(0).getText()


class NoAccessException(Exception):
    pass


class InvalidQueryException(Exception):
    pass


class SqlGenerator:
    """SqlGenerator generates SQL from the GraphQLVisitor output."""
    CURSOR_ID = "cursor"
    SCHEMA = "legacy"

    # Attributes to ignore in the query on attributes.
    srcvalues_attributes = [FIELD.SOURCE_VALUE, FIELD.SOURCE_INFO]
    relvalues_attributes = [API_FIELD.START_VALIDITY_RELATION, API_FIELD.END_VALIDITY_RELATION]

    def __init__(self, visitor: GraphQLVisitor):
        """SqlGenerator initialisation.

        :param visitor:
        """
        self.visitor = visitor
        self.selects = visitor.selects
        self.relation_parents = visitor.relationParents
        self.relation_aliases = visitor.relationAliases
        self.relation_info = {}

    def _get_arguments_with_defaults(self, arguments: dict) -> dict:
        args = {
            'active': True,
        }
        args.update(arguments)
        return args

    def _get_filter_arguments(self, arguments: dict) -> dict:
        """Returns filter arguments from arguments dict.

        Changes GraphQL strings with double quotes to single quotes for Postgres.

        :param arguments:
        :return:
        """
        ignore = ['first', 'last', 'before', 'after', 'sort', 'active']

        def change_quotation(value):
            strval = str(value)
            double_quote = '"'
            if strval[0] == double_quote and strval[-1] == double_quote:
                return "'" + strval[1:-1] + "'"
            return value

        return {to_snake(k): change_quotation(v) for k, v in arguments.items() if
                k not in ignore and
                not k.endswith('_desc') and
                not k.endswith('_asc')
                }

    def _reset(self):
        self.aliased_select_expressions = {}
        self.unaliased_select_expressions = []
        self.joins = []
        self.relation_info = {}

    def _collect_relation_info(self, relation_name: str, schema_collection_name: str):
        catalog_name, collection_name = resolve_schema_collection_name(schema_collection_name)

        if not (catalog_name and collection_name):
            raise InvalidQueryException(f"{schema_collection_name} is not a valid entity")

        collection = gob_model[catalog_name]['collections'][collection_name]
        abbr = collection['abbreviation'].lower()
        abbr_cnt = len([item for item in self.relation_info.values() if item['abbr'] == abbr])

        self.relation_info[relation_name] = {
            'abbr': abbr,
            'collection_name': collection_name,
            'catalog_name': catalog_name,
            'tablename': gob_model.get_table_name(catalog_name, collection_name),
            'alias': f'{abbr}_{abbr_cnt}',
            'has_states': collection.get('has_states', False),
            'collection': collection,
            'attributes': collection['attributes'],
            'all_fields': collection['all_fields'],
        }

        return self.relation_info[relation_name]

    def _get_relation_info(self, relation_alias: str):
        return self.relation_info[relation_alias]

    def _validate_attributes(self, relation_info: dict, attributes: List[str], relation_name: str):
        for attribute in attributes:
            self._validate_attribute(relation_info, attribute, relation_name)

    def _validate_attribute(self, relation_info: dict, attribute: str, relation_name: str):
        if to_snake(attribute) not in list(relation_info['all_fields']) + [
                FIELD.SOURCE_VALUE, FIELD.SOURCE_INFO,
                API_FIELD.START_VALIDITY_RELATION, API_FIELD.END_VALIDITY_RELATION]:
            raise InvalidQueryException(f"Attribute {attribute} does not exist for {relation_name}")

    def _geometry_as_text(self, geometry: str):
        return f"ST_AsText({geometry})"

    def _select_expression(self, relation: dict, field: str) -> tuple[str, Optional[str]]:
        """Returns the select expression for the given field, with the alias as a tuple."""
        if field == self.CURSOR_ID:
            return (f"{relation['alias']}.{FIELD.GOBID}", self.CURSOR_ID)

        field_snake = to_snake(field)
        expression = f"{relation['alias']}.{field_snake}"

        self._validate_attribute(relation, field, relation['collection_name'])

        # If geometry field, transform to WKT
        if field_snake in relation['attributes'] and is_gob_geo_type(relation['attributes'][field_snake]['type']):
            return self._geometry_as_text(expression), field_snake

        return expression, None

    def _current_filter_expression(self, table_id: str = None):
        table = f"{table_id}." if table_id else ""

        return f"(COALESCE({table}{FIELD.EXPIRATION_DATE}, '9999-12-31'::timestamp without time zone) > NOW())"

    def _full_table_name(self, table_name: str):
        return f"{self.SCHEMA}.{table_name}"

    def _build_from_table(self, arguments: dict, table_name: str, table_alias: str):
        """Builds from table expression for base relation with :table_name: and :arguments:

        :param arguments:
        :param table_name:
        :return:
        """
        conditions = []

        if arguments['active']:
            conditions.append(self._current_filter_expression())

        if 'after' in arguments:
            conditions.append(f"{FIELD.GOBID} > {arguments['after']}")

        # Add non-keyword filter arguments
        filter_args = self._get_filter_arguments(arguments)
        conditions.extend([f"{k} = {v}" for k, v in filter_args.items()])
        conditions.append(f"{FIELD.DATE_DELETED} IS NULL")

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        limit = f"LIMIT {arguments['first']}" if 'first' in arguments else ""

        order_by_fields = []
        for s in arguments.get('sort', []):
            if s.endswith('_desc'):
                f = s.replace('_desc', '')
                order_by_fields.append(f"{f} DESC")
            else:
                f = s.replace('_asc', '')
                order_by_fields.append(f"{f} ASC")

        if not len(order_by_fields):
            order_by_fields.append(FIELD.GOBID)

        order = f"ORDER BY {','.join(order_by_fields)}"

        return f"""FROM (
    SELECT *
    FROM {self._full_table_name(table_name)}
    {where}
    {order}
    {limit}
) {table_alias}"""

    def sql(self):
        self._reset()

        # Relation without parent is main relation
        base_collection = [k for k, v in self.relation_parents.items() if v is None][0]

        self._collect_relation_info(base_collection, base_collection)
        base_info = self._get_relation_info(base_collection)

        select_fields = [self._select_expression(base_info, field)
                         for field in [FIELD.GOBID] + self.selects[base_collection]['fields']]

        self._add_select_expressions(select_fields)

        # Add catalog and collection to allow for value resolution
        self._add_select_expressions([
            (f"'{base_info['catalog_name']}'", CATALOG_NAME),
            (f"'{base_info['collection_name']}'", COLLECTION_NAME),
        ])

        authority = Authority(base_info['catalog_name'], base_info['collection_name'])
        if not authority.allows_access():
            raise NoAccessException

        arguments = self._get_arguments_with_defaults(self.selects[base_collection]['arguments'])

        self.joins.append(self._build_from_table(arguments, base_info['tablename'], base_info['alias']))

        del self.selects[base_collection]

        self._join_relations(self.selects)

        select = self._select_expressions_as_string()
        table_select = '\n'.join(self.joins)
        order_by = f"ORDER BY {base_info['alias']}.{FIELD.GOBID}"

        query = f"SELECT\n{select}\n{table_select}\n{order_by}"

        return query

    def _add_select_expression(self, expression: str, alias: Optional[str] = None):
        if alias is None:
            self.unaliased_select_expressions.append(expression)
        else:
            self.aliased_select_expressions[alias] = expression

    def _add_select_expressions(self, select_expressions: list[tuple[str, Optional[str]]]):
        for expression, alias in select_expressions:
            self._add_select_expression(expression, alias)

    def _select_expressions_as_string(self):
        return ",\n".join(self.unaliased_select_expressions + [f"{v} AS {k}"
                                                               for k, v in self.aliased_select_expressions.items()])

    def _get_formatted_filter_arguments(self, arguments: dict, base_alias: str):
        result = []
        filter_args = self._get_filter_arguments(arguments)

        for k, v in filter_args.items():
            result.append(f"{base_alias}.{k} = {v}")
        return result

    def _is_many(self, gobtype: str):
        return gobtype == f"GOB.{gob_types.ManyReference.name}"

    def _join_relations(self, relations: dict):
        self.relcnt = 0
        for relation_alias, select in relations.items():
            arguments = self._get_arguments_with_defaults(select['arguments'])
            select_fields = [FIELD.GOBID] + select['fields']

            relation_unaliased = self.relation_aliases[relation_alias]

            if relation_unaliased.startswith('inv'):
                self._join_inverse_relation(relation_alias, select_fields, arguments)
            else:
                self._join_relation(relation_alias, select_fields, arguments)
            self.relcnt += 1

    def _add_srcvalue_selection(self, src_relation: dict, src_attr_name: str, is_many: bool):
        """Add _src_* selection to query.

        Returns the field containing the bronwaarde for this row as string so that the remainder
        of the query can match on this bronwaarde.

        :param src_relation:
        :param src_attr_name:
        :param is_many:
        :return:
        """
        src_alias = f"_src_{src_attr_name}"
        jsonb_alias = f"rel_bw_{self.relcnt}"

        if is_many:
            src_values_join = f"LEFT JOIN jsonb_array_elements({src_relation['alias']}.{src_attr_name}) " \
                              f"{jsonb_alias}(item) ON {jsonb_alias}.item->>'{FIELD.SOURCE_VALUE}' IS NOT NULL"

            match_src_value = f"{jsonb_alias}.item->>'{FIELD.SOURCE_VALUE}'"

            self.joins.append(src_values_join)
            self._add_select_expression(f"{jsonb_alias}.item", src_alias)
        else:
            match_src_value = f"{src_relation['alias']}.{src_attr_name}->>'{FIELD.SOURCE_VALUE}'"
            self._add_select_expression(f"{src_relation['alias']}.{src_attr_name}", src_alias)

        return match_src_value

    def _relation_table_name(self, relation_name: str):
        table_name = f"mv_{relation_name}"
        return self._full_table_name(table_name)

    def _join_relation_table(self, src_relation: dict, dst_relation: dict, relation_name: str, rel_table_alias: str,
                             arguments: dict, src_value_requested: bool, src_attr_name: str, is_many: bool,
                             is_inverse: bool):
        """Generates the SQL for the relation table join, see _add_relation_joins.

        :param src_relation:
        :param relation_name:
        :param rel_table_alias:
        :param arguments:
        :param src_value_requested:
        :param src_attr_name:
        :param is_many:
        :param is_inverse:
        :return:
        """
        rel_left = 'src' if not is_inverse else 'dst'
        rel_right = 'dst' if not is_inverse else 'src'
        relation_table = self._relation_table_name(relation_name)

        def join_reltable(reltable_alias: str, reltable_side=rel_left, join_with_table='src'):
            join_relation = src_relation if join_with_table == 'src' else dst_relation

            filters = [
                f"{reltable_alias}.{reltable_side}_id = {join_relation['alias']}.{FIELD.ID}"
            ]

            if not is_inverse and src_value_requested:
                match_src_value_with = self._add_srcvalue_selection(join_relation, src_attr_name, is_many)
                filters.append(f"{reltable_alias}.{FIELD.SOURCE_VALUE} = {match_src_value_with}")

            if join_relation['has_states']:
                filters.append(f"{reltable_alias}.{reltable_side}_volgnummer = {join_relation['alias']}.{FIELD.SEQNR}")

            return " AND ".join(filters)

        if arguments.get('first'):
            if arguments.get('sort'):
                sort = [s.replace('_desc', ' DESC')
                        if s.endswith('_desc')
                        else s.replace('_asc', ' ASC')
                        for s in arguments['sort']]
            else:
                sort = [FIELD.GOBID]
            order_by = ', '.join([f"{dst_relation['alias']}.{s}" for s in sort])

            first = int(arguments['first'])
            match_row_number = f"{rel_table_alias}.row_number <= {first}" if first > 1 \
                else f"{rel_table_alias}.row_number = 1"

            select_exprs = [
                "rel.src_id AS src_id",
                "rel.dst_id AS dst_id",
            ]
            select_exprs += ["rel.src_volgnummer AS src_volgnummer"] if src_relation['has_states'] else []
            select_exprs += ["rel.dst_volgnummer AS dst_volgnummer"] if dst_relation['has_states'] else []

            select_exprs_str = ",\n        ".join(select_exprs)
            join_relation_table = f"""
LEFT JOIN (
    SELECT
        {select_exprs_str},
        ROW_NUMBER() OVER (
            PARTITION BY rel.dst_id ORDER BY {order_by}
        ) AS row_number
    FROM {relation_table} rel
    JOIN {self._full_table_name(dst_relation['tablename'])} {dst_relation['alias']}
    ON {join_reltable('rel', rel_right, 'dst')}
) {rel_table_alias} ON {join_reltable(rel_table_alias, rel_left)} AND {match_row_number}"""
        else:
            join_relation_table = f"LEFT JOIN {relation_table} {rel_table_alias} " \
                                  f"ON {join_reltable(rel_table_alias)}"

        return join_relation_table

    def _join_dst_table(self, dst_relation: dict, rel_table_alias: str, arguments: dict, is_inverse: bool):
        """Generates the SQL for the destination table join part of a relation:

        A -> B -> C, where A is the src_relation, B the relation_table join and C the dst_relation.
        See _add_relation_joins

        :param dst_relation:
        :param rel_table_alias:
        :param arguments:
        :param is_inverse:
        :return:
        """
        filter_args = self._get_formatted_filter_arguments(arguments, dst_relation['alias'])
        rel_right = 'dst' if not is_inverse else 'src'

        join_dst_table = f"LEFT JOIN {self._full_table_name(dst_relation['tablename'])} {dst_relation['alias']} " \
                         f"ON {rel_table_alias}.{rel_right}_id = {dst_relation['alias']}.{FIELD.ID}"

        if dst_relation['has_states']:
            join_dst_table += f" AND {rel_table_alias}.{rel_right}_volgnummer = {dst_relation['alias']}.{FIELD.SEQNR}"

        if filter_args:
            join_dst_table += f" AND ({') AND ('.join(filter_args)})"

        if arguments['active']:
            join_dst_table += f" AND {self._current_filter_expression(dst_relation['alias'])}"

        return join_dst_table

    def _add_relation_joins(self, src_relation: dict, dst_relation: dict, relation_name: str, arguments: dict,
                            src_value_requested: bool = False, src_attr_name: str = None,
                            is_many: bool = False, is_inverse=False):
        """Joins dst_relation to src_relation using relation_table.

        Resulting SQL will create a join of the form A -> B -> C, where:
        A is the src_relation
        B is the relation_table, and
        C is the dst_relation

        If A contains the attribute pointing to C, A is the owner of the relation, and A will be referred to as 'src'
        in the relation_table B. Otherwise, C is the owner of the relation and C will be referred to as 'src' in the
        relation_table B.

        In case the dst_relation C is the owner of the relation (C has a relation defined to A), this join is said to
        be 'inversed'. Inversed relations never have a requested src_value (bronwaarde), as the src_value is always
        part of the 'owner' of the relation. This is also true for the src_attr_name, as the src_attr_name is always
        defined on the owning side of the relation. That same way, is_many is also only necessary to define for the
        when src_relation A is the owning side of the relation, as is_many is only important when src_value is
        requested (and we will have to unpack the json containing the src_value)

        :param src_relation: The main relation
        :param dst_relation: The relation to join
        :param relation_name:
        :param arguments: A dict with arguments passed in GraphQL to this relation
        :param src_value_requested: boolean. Only applicable if is_inverse == False
        :param src_attr_name: The name of the attribute in the src relation. Only applicable if is_inverse == False
        :param is_many: boolean. Only applicable if is_inverse == False
        :param is_inverse: boolean value indicating if src_relation is the owner of the relation (is_inverse = False),
        or that the relation is owned by dst_relation (is_inverse = True).
        :return:
        """
        rel_table_alias = f"rel_{self.relcnt}"

        join_relation_table = self._join_relation_table(src_relation, dst_relation, relation_name, rel_table_alias,
                                                        arguments, src_value_requested, src_attr_name, is_many,
                                                        is_inverse)
        join_dst_table = self._join_dst_table(dst_relation, rel_table_alias, arguments, is_inverse)

        self.joins.append(join_relation_table)
        self.joins.append(join_dst_table)

    def _is_srcvalue_requested(self, attributes: list):
        return any(to_snake(attr) in self.srcvalues_attributes for attr in attributes)

    def _is_relvalue_requested(self, attributes: list):
        return any(to_snake(attr) in self.relvalues_attributes for attr in attributes)

    def _join_relation(self, relation_alias: str, attributes: list, arguments: dict):
        parent = self.relation_parents[relation_alias]
        parent_info = self._get_relation_info(parent)
        relation_attr_name = to_snake(self.relation_aliases[relation_alias])

        self._validate_attribute(parent_info, relation_attr_name, parent)

        dst_catalog_name, dst_collection_name = gob_model.get_catalog_collection_names_from_ref(
            parent_info['collection']['attributes'][relation_attr_name]['ref']
        )

        dst_info = self._collect_relation_info(relation_alias,
                                               f'{dst_catalog_name}_{dst_collection_name}')
        self._validate_attributes(dst_info, attributes, relation_alias)

        relation_name = get_relation_name(
            gob_model,
            parent_info['catalog_name'],
            parent_info['collection_name'],
            relation_attr_name
        )

        self._add_relation_joins(parent_info, dst_info, relation_name, arguments,
                                 self._is_srcvalue_requested(attributes), relation_attr_name,
                                 self._is_many(parent_info['collection']['attributes'][relation_attr_name]['type']))

        self._add_relation_join_attributes_to_select_expressions(
            attributes,
            dst_catalog_name,
            dst_collection_name,
            dst_info['alias'],
            relation_alias
        )

    def _join_inverse_relation(self, relation_alias: str, attributes: list, arguments: dict):
        parent = self.relation_parents[relation_alias]
        parent_info = self._get_relation_info(parent)

        relation_unaliased = self.relation_aliases[relation_alias]
        relation_name_snake = to_snake(relation_unaliased).split('_')

        assert relation_name_snake[0] == 'inv'

        relation_attr_name = '_'.join(relation_name_snake[1:-2])
        dst_catalog_name = relation_name_snake[-2]
        dst_collection_name = relation_name_snake[-1]
        dst_model_name = gob_model.get_table_name(dst_catalog_name, dst_collection_name)
        dst_info = self._collect_relation_info(relation_alias, f'{dst_model_name}')
        self._validate_attributes(dst_info, attributes, relation_alias)

        self._validate_attribute(dst_info, relation_attr_name, dst_collection_name)
        relation_name = get_relation_name(
            gob_model,
            dst_info['catalog_name'],
            dst_info['collection_name'],
            relation_attr_name
        )

        self._add_relation_joins(parent_info, dst_info, relation_name, arguments, is_inverse=True)

        self._add_relation_join_attributes_to_select_expressions(
            attributes,
            dst_catalog_name,
            dst_collection_name,
            dst_info['alias'],
            relation_alias
        )

    def _json_build_attrs(self, attributes: list, join_alias: str):
        """Create the list of attributes to be used in json_build_object( ) for attributes in relation_name

        :param attributes:
        :param join_alias:
        :return:
        """
        snake_attrs = [to_snake(attr) for attr in attributes]

        json_attrs = ",".join([f"'{attr}', {join_alias}.{attr}" for attr in snake_attrs
                               if attr not in self.srcvalues_attributes + self.relvalues_attributes])

        if self._is_relvalue_requested(attributes):
            rel_attrs = ",".join([f"'{attr}', rel_{self.relcnt}.{attr.replace('_relatie', '')}"
                                  for attr in snake_attrs if attr in self.relvalues_attributes])
            json_attrs = f"{json_attrs}, {rel_attrs}"

        return json_attrs

    def _add_relation_join_attributes_to_select_expressions(
            self,
            attributes: list,
            dst_catalog_name: str,
            dst_collection_name: str,
            join_alias: str,
            relation_attr_name: str
    ):
        json_attrs = self._json_build_attrs(attributes, join_alias)
        json_attrs = f"{json_attrs}, '_catalog', '{dst_catalog_name}', '_collection', '{dst_collection_name}'"
        alias = to_snake(f"_{relation_attr_name}")
        self._add_select_expression(f"json_build_object({json_attrs})", alias)


class GraphQL2SQL:
    """GraphQL2SQL class. Parses the input graphql_query and outputs an SQL-equivalent for Postgres.

    Current implementation does not implement the full GraphQL grammar and a this implementation is
    very specific to the GOB use and data model.
    """

    def __init__(self, graphql_query: str):
        self.query = graphql_query
        # Remove any GraphQL comments
        self.query = re.sub(r'#[^\s]*', '', self.query)
        self.relations_hierarchy = None
        self.selections = None

    def sql(self, generator: SqlGenerator = None, visitor: GraphQLVisitor = None):
        """Returns a tuple (sql, relation_parents), where sql is the generated sql and relation_parents is a dict
        containing the hierarchy of the relations in this query, so that the result set can be reconstructed as one
        object with nested relations.

        :param graphql_query:
        :return:
        """
        input_stream = InputStream(self.query)
        lexer = GraphQLLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = GraphQLParser(stream)
        tree = parser.document()

        visitor = visitor or GraphQLVisitor()
        visitor.visit(tree)
        generator = generator or SqlGenerator(visitor)

        self.relations_hierarchy = visitor.relationParents
        self.selections = visitor.selects

        return generator.sql()
