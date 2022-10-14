"""Storage.

This module encapsulates the GOB storage.
The API returns GOB data by calling any of the methods in this module.
By using this module the API does not need to have any knowledge about the underlying storage.
"""

import datetime
import re
import warnings

from typing import List
from collections import defaultdict

from sqlalchemy import create_engine, Table, MetaData, func, and_, or_, exc as sa_exc
from sqlalchemy.engine import Row
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import label, functions

from gobcore.model import NotInModelException
from gobcore.model.relations import get_relation_name
from gobcore.model.sa.gob import get_base, get_sqlalchemy_models
from gobcore.model.metadata import PUBLIC_META_FIELDS, PRIVATE_META_FIELDS, FIXED_COLUMNS, FIELD
from gobcore.typesystem import get_gob_type_from_sql_type, get_gob_type_from_info

from gobapi.config import GOB_DB, current_api_base_path
from gobapi.legacy_views.create import create_legacy_views
from gobapi.session import set_session, get_session
from gobapi.auth.auth_query import AuthorizedQuery, SUPPRESSED_COLUMNS, Authority
from gobapi.constants import API_FIELD

from gobapi import gob_model
from gobapi import profiled_query
from gobapi.views import initialise_api_views

session = None
_Base = None
metadata = None


class MigrationLock:
    MIGRATION_LOCK_ID = 184041041  # Random number, but the same for all API instances

    def __init__(self, engine):
        self.engine = engine

    def __enter__(self):
        self.engine.execute(f"SELECT pg_advisory_lock({self.MIGRATION_LOCK_ID})")

    def __exit__(self, exc_type, value, traceback):
        self.engine.execute(f"SELECT pg_advisory_unlock({self.MIGRATION_LOCK_ID})")


def connect():
    """Module initialisation.

    The connection with the underlying storage is initialised.
    Meta information is available via the Base variale.
    Data retrieval is facilitated via the session object

    :return:
    """
    global session, _Base, metadata

    engine = create_engine(URL.create(**GOB_DB), connect_args={'sslmode': 'require'})\
        .execution_options(schema_translate_map={None: "legacy"})
    session = scoped_session(sessionmaker(autocommit=True,
                                          autoflush=False,
                                          bind=engine,
                                          query_cls=AuthorizedQuery))

    with MigrationLock(engine):
        create_legacy_views(gob_model, engine)
        initialise_api_views(engine)  # Can use the legacy views, so should be initialised after the legacy views

    with warnings.catch_warnings():
        # Ignore warnings for unsupported reflection for expression-based indexes
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        _Base = automap_base()
        _Base.prepare(engine, reflect=True, schema="legacy")     # Long running statement !

    Base = get_base()
    Base.metadata.bind = engine  # Bind engine to metadata of the base class
    Base.query = session.query_property()  # Used by graphql to execute queries

    metadata = MetaData(engine)

    set_session(session)
    profiled_query.activate()


def exec_statement(statement):
    engine = session.get_bind()
    return engine.execute(statement)


def _get_table(table_names, table_name):
    """Return the name of the table as it exists in the database.

    The name can possibly be truncated, like in PostgreSQL to 63 characters

    :param table_names:
    :param table_name:
    :return:
    """
    match = sorted([t for t in table_names if t == table_name[:len(t)]],
                   key=lambda s: -len(s))[0]  # take longest match
    if match != table_name:
        print(f"Warning: table\n'{table_name}' is truncated to\n'{match}' in the database")
    return match


def get_table_and_model(catalog_name, collection_name, view=None):
    """Table and Model.

    Utility method to retrieve the Table and Model for a specific collection.
    When a view is provided use the and do not return the GOBModel.

    :param collection_name:
    :param view:
    :return:
    """
    if view:
        return Table(view, metadata, autoload=True), None
    return get_sqlalchemy_models(gob_model)[f'{catalog_name}_{collection_name}'], gob_model[
            catalog_name]['collections'][collection_name]


def _create_reference_link(reference, catalog, collection):
    identificatie = reference.get(FIELD.REFERENCE_ID)
    if identificatie:
        return {'_links': {'self': {
            'href': f'{current_api_base_path()}/{catalog}/{collection}/{identificatie}/'}}}
    return {}


def _format_reference(reference, catalog, collection, spec):
    link = _create_reference_link(reference, catalog, collection)

    if spec.get('secure', {}).get(FIELD.SOURCE_VALUE):
        # Original bronwaarde was secured, decrypt if possible
        gob_type = get_gob_type_from_info(spec)

        # Actual input to from_value is not the original value, but it is a dict with a bronwaarde key, so the
        # bronwaarde key is decrypted as the original input would have been.
        reference = gob_type.from_value(reference, secure=spec.get('secure')).to_value

    return {
        **reference,
        **link,
    }


def _create_external_reference_link(entity, field, entity_catalog, entity_collection):
    identificatie = getattr(entity, FIELD.ID)
    field_path = field.replace('_', '-')
    return {'href':
            f'{current_api_base_path()}/{entity_catalog}/{entity_collection}/{identificatie}/{field_path}/'}


def _create_reference_view(entity, field, spec):
    # Get the dict or array of dicts from a (Many)Reference field
    embedded = _to_gob_value(entity, field, spec).to_db

    if embedded is not None and spec['ref'] is not None:
        catalog, collection = spec['ref'].split(':')
        if spec['type'] == 'GOB.ManyReference':
            embedded = [_format_reference(reference, catalog, collection, {}) for reference in embedded]
        else:
            ref = _format_reference(embedded, catalog, collection, {})
            gob_type = get_gob_type_from_info(spec)
            embedded = gob_type.from_value(ref, secure=spec.get('secure'))

    return embedded


def _create_reference(entity, field, spec, entity_catalog=None, entity_collection=None):
    """Create an embedded reference.

    :param entity: The entity
    :param field: The field a reference is being created for
    :param spec: The field specification
    :param entity_catalog: The catalog of the entity -- not used
    :param entity_collection: The collection of the entity -- not used
    :return:
    """
    if spec['ref'] is not None:
        catalog, collection = spec['ref'].split(':')

        references = getattr(entity, field) or []

        if isinstance(references, dict):
            references = [references]

        # reference is a dict of the form {'bronwaarde': X, 'id': Y}
        return [_format_reference(reference, catalog, collection, spec) for reference in references]

    return {}


def _to_gob_value(entity, field, spec, resolve_secure=False):
    """Transforms a entity field value into a GOB type value.

    Attention:
    Resolve secure is normally False as this is all handled by the Authority classes.
    For enhanced views however, this is not possible.
    These queries are based upon a view and cannot directly be related to a GOB Model.
    If the field names of the view are properly named the decryption will be handled here.

    :param entity:
    :param field:
    :param spec:
    :param resolve_secure:
    :return:
    """
    entity_value = getattr(entity, field, None)
    if isinstance(spec, dict):
        gob_type = get_gob_type_from_info(spec)
        if resolve_secure and Authority.is_secure_type(spec):
            # Transform the value into a secure type value
            secure_type = Authority.get_secure_type(gob_type, spec, entity_value)
            # Return decrypted value
            return Authority.get_secured_value(secure_type)
        return gob_type.from_value(entity_value, **spec)
    gob_type = get_gob_type_from_sql_type(spec)
    return gob_type.from_value(entity_value)


def _get_convert_for_state(collection, fields=None, private_attributes=False):
    """Get the entity to dict convert function for GOBModels with state.

    The collection model is used to extract only the public attributes of the entity,
    fields can be used to only select certain attributes.

    :param collection:
    :param fields:
    :return:
    """
    def convert(entity):
        hal_entity = {k: _to_gob_value(entity, k, v) for k, v in items}
        return hal_entity

    fields = fields or []

    # Select all attributes except if it's a reference, unless a specific list was passed
    if not fields:
        fields = [field for field in collection['fields'].keys()
                  if field not in collection['references'].keys()
                  and (not field.startswith('_') or private_attributes)]
    attributes = {k: v for k, v in collection['fields'].items() if k in fields}
    items = list(attributes.items())
    return convert


def _add_relation_dates_to_manyreference(entity_reference, relation_dates):
    for item in entity_reference:
        for relation_date in relation_dates:
            if item[FIELD.SOURCE_VALUE] == relation_date[FIELD.SOURCE_VALUE]:
                item.update({
                    API_FIELD.START_VALIDITY_RELATION: relation_date.get(API_FIELD.START_VALIDITY_RELATION),
                    API_FIELD.END_VALIDITY_RELATION: relation_date.get(API_FIELD.END_VALIDITY_RELATION),
                })
    return entity_reference


def _flatten_join_result(result):
    entity = result[0]
    Base = get_base()

    for key, value in result._asdict().items():
        if isinstance(value, Base):
            # First item is Base object
            continue
        # Other items are of the form { 'ref:ligt_in_wijk': [{'bronwaarde': X, 'id': Y}] }
        _, reference = key.split(':')
        setattr(entity, reference, value)

    return entity


def _get_convert_for_model(catalog, collection, model, meta=None, private_attributes=False):
    """Get the entity to dict convert function for GOBModels.

    The model is used to extract only the public attributes of the entity.

    :param entity:
    :param model:
    :return:
    """
    def convert(result: Row):
        entity = _flatten_join_result(result) if isinstance(result, (tuple, Row)) else result

        deleted = getattr(entity, SUPPRESSED_COLUMNS, [])
        hal_entity = {k: _to_gob_value(entity, k, v) for k, v in items if k not in deleted}

        # Add link to self in each entity
        id = getattr(entity, '_id')
        hal_entity['_links'] = {
            'self': {'href': f'{current_api_base_path()}/{catalog}/{collection}/{id}/'}
        }
        # Add references to other entities, exclude private_attributes unless specifically requested
        if model['references']:
            hal_entity['_embedded'] = {k: _create_reference(entity, k, v, catalog, collection)
                                       for k, v in model['references'].items()
                                       if k not in deleted
                                       and k not in model.get('very_many_references', {}).keys()
                                       and ((not k.startswith('_') and not v.get('hidden')) or private_attributes)}

            # Delete embedded from the entity if no references are added
            if not hal_entity['_embedded']:
                del hal_entity['_embedded']

        if model.get('very_many_references'):
            hal_entity['_links'].update({k: _create_external_reference_link(entity, k, catalog, collection)
                                        for k, v in model['very_many_references'].items()})

        return hal_entity

    # Get the attributes which are not a reference, exclude private_attributes unless specifically requested
    attributes = {k: v for k, v in model['fields'].items()
                  if (not k.startswith('_') or private_attributes)
                  and not v.get('hidden')}
    attributes.update(meta or {})
    hal_attributes = {k: v for k, v in attributes.items() if k not in model['references'].keys()}
    items = list(hal_attributes.items())
    return convert


def _add_resolve_attrs_to_columns(columns):
    """Adds attributes to columns necessary to resolve model attributes from a view.

    Looks for attributes of the form brk:sjt:heeft_bsn_voor, and will try to find the attribute
    heeft_bsn_voor in the catalog brk and collection sjt.

    Adds attribute, authority and public_name (heeft_bsn_voor in this case) to columns matching
    the pattern above.
    """
    resolve_attr_pattern = re.compile(r"^(\w+):(\w+):(\w+)$")

    for column in columns:
        match = re.match(resolve_attr_pattern, column.name)
        if not match:
            continue

        catalog_abbreviation, collection_abbreviation, attribute_name = match.groups()

        try:
            _, collection = gob_model.get_catalog_collection_from_abbr(
                catalog_abbreviation,
                collection_abbreviation
            )
            attribute = collection['attributes'][attribute_name]
        except (NotInModelException, KeyError):
            continue

        setattr(column, 'attribute', attribute)
        setattr(column, 'public_name', attribute_name)


def _get_convert_for_table(table, filter=None):
    """Get the entity to dict convert function for database Tables or Views.

    The table columns are used to extract only the public attributes of the entity.

    :return:
    """
    def convert(entity):
        def resolve_column(column):
            """Resolves the name and value of the given column for entity using _to_gob_value.
            Uses attributes set by _add_resolve_attrs_to_columns to determine how values are resolved.

            If 'attribute' is set on column, pass 'attribute' to _to_gob_value, in which case the
            GOB type will be used. Otherwise, pass SQL type of the column.
            """
            value = _to_gob_value(
                entity,
                column.name,
                getattr(column, 'attribute', type(column.type)),
                resolve_secure=True
            )
            # If 'public_name' is set, replace column name (for example brk:sjt:heeft_bsn_voor) with 'public_name',
            # (for example heeft_bsn_voor). Set by _add_resolve_attrs_to_columns
            name = getattr(column, 'public_name', column.name)

            return name, value

        hal_entity = dict([resolve_column(column) for column in columns])

        # Add references to other entities
        if references:
            hal_entity['_embedded'] = {
                v['attribute_name']: _create_reference_view(entity, k, v) for k, v in references.items()
            }
        return hal_entity

    filter = filter or {}
    # Get all metadata or reference fields and filter them from the columns returned by the database view
    metadata_column_list = list(filter.keys())
    columns = [c for c in table.columns
               if c.name not in metadata_column_list
               and not isReference(c.name)]
    reference_columns = [c for c in table.columns if isReference(c.name)]

    # Create the list of references
    references = {}
    for c in reference_columns:
        '''
        Column name is in the form of '_ref_attribute_name_ctg_cln'
        We need to get the type of reference (ref or mref), the attribute name and
        the reference based on abbreviation. Abbreviations were used to escape the
        column name limit in SQL. The original column name is stored to
        be able to get the data from the row.

        For example: _ref_ligt_in_buurt_gdb_brt will result in:
        attribute_name: ligt_in_buurt
        catalog_abbreviation: gdb
        collection_abbreviation: brt
        ref: gebieden:buurt
        gob_type: GOB.Reference

        This will be used to create an embedded reference in the HAL JSON output
        '''
        # This will result in an array of e.g ['', 'ref', 'ligt', 'in', 'buurt', 'gbd', 'brt']
        column_name_array = c.name.split('_')

        # Join elements that make up the attribute name, position 2 until the third last (e.g. ligt_in_buurt)
        attribute_name = '_'.join(column_name_array[2:-2])

        # Get the abbreviation of the catalog (e.g. gbd) and collection (e.g. brt)
        catalog_abbreviation = str(column_name_array[-2])
        collection_abbreviation = str(column_name_array[-1])

        # Get a reference string by abbreviation (e.g. gebieden:buurten)
        ref = gob_model.get_reference_by_abbreviations(catalog_abbreviation, collection_abbreviation)
        gob_type = 'GOB.ManyReference' if c.name.startswith('_mref') else 'GOB.Reference'

        # Create the reference specification
        references[c.name] = {
            'attribute_name': attribute_name,
            'type': gob_type,
            'ref': ref
        }

    _add_resolve_attrs_to_columns(columns)
    return convert


def isReference(column_name):
    """isReference.

    Receives a table column_name and checks if it's a reference or many reference based on the
    column name.

    Returns a boolean.

    :param column_name:
    :return: boolean
    """
    return column_name.startswith(('_ref', '_mref'))


def get_entities(catalog, collection, offset, limit, view=None, reference_name=None, src_id=None):
    """Entities.

    Returns the list of entities within a collection.
    Starting at offset (>= 0) and limiting the result to <limit> items.

    :param collection:
    :param offset:
    :param limit:
    :param view: optional view for the collection
    :param reference_name: optional reference_name, will return entities for a specific relation
    :param src_id: optional e.g. 1234
    :return:
    """
    all_entities, entity_convert = query_reference_entities(catalog, collection, reference_name, src_id) \
        if reference_name else query_entities(catalog, collection, view)

    all_entities.set_catalog_collection(catalog, collection)

    # For views count is slow on large views
    all_count = all_entities.count() if view is None else None

    # Limit and offset for pagination
    page_entities = all_entities.offset(offset).limit(limit).all()

    entities = [entity_convert(entity) for entity in page_entities]
    return entities, all_count


def dump_entities(catalog, collection, filter=None, order_by=None):
    """Get all entities in the given catalog collection.

    :param catalog:
    :param collection:
    :param filter: function that returns a filter expression with the table as input
    :param order_by: column to order by

    example of filter parameter:
    filter = lambda table: getattr(table, FIELD.LAST_EVENT) > max_eventid

    :return: (all collection entities, the collection model)
    """
    assert _Base
    _session = get_session()

    yield_per = 10_000

    table, model = get_table_and_model(catalog, collection)

    # Register the meta data in the model
    model['catalog'] = catalog
    model['collection'] = collection

    entities = _session.query(table)

    if filter:
        entities = entities.filter(filter(table))

    if order_by:
        entities = entities.order_by(getattr(table, order_by))

    entities.set_catalog_collection(catalog, collection)
    entities.expire_per(yield_per)

    return entities.yield_per(yield_per), model


def get_id_columns(catalog, collection):
    """Get the id columns of the given catalog and collection.

    :param catalog:
    :param collection:
    :return:
    """
    table, _ = get_table_and_model(catalog, collection)

    if catalog == "rel":
        # src_id, src_volgnummer, dst_id, dst_volgnummer
        columns = [f"{src_dst}_{column}" for src_dst in ["src", "dst"] for column in ["id", FIELD.SEQNR]]
    else:
        # id, volgnummer
        columns = [FIELD.ID, FIELD.SEQNR]
    return [getattr(table, column) for column in columns if hasattr(table, column)]


def get_entity_refs_after(catalog: str, collection: str, last_eventid: int) -> List[str]:
    """Returns refs of entities with _last_event greater than last_eventid.

    :param catalog:
    :param collection:
    :param last_eventid:
    """
    assert _Base
    session = get_session()

    table, _ = get_table_and_model(catalog, collection)

    id_columns = []
    for index, column in enumerate(get_id_columns(catalog, collection)):
        if index > 0:
            id_columns.append('_')
        id_columns.append(column)
    id = functions.concat(*id_columns)
    query = session.query(id).filter(getattr(table, FIELD.LAST_EVENT) > last_eventid)
    query.set_catalog_collection(catalog, collection)
    return [row[0] for row in query.all()]


def get_count(catalog: str, collection: str) -> int:
    """Returns the number of entities present in the object table for given catalog and collection.

    :param catalog:
    :param collection:
    :return:
    """
    assert _Base
    session = get_session()

    table, _ = get_table_and_model(catalog, collection)

    query = session.query(table)
    query.set_catalog_collection(catalog, collection)
    return query.count()


def get_max_eventid(catalog: str, collection: str) -> int:
    """Returns max eventid present in the object table for given catalog and collection.

    :param catalog:
    :param collection:
    :return:
    """
    assert _Base
    session = get_session()

    table, _ = get_table_and_model(catalog, collection)

    query = session.query(func.max(getattr(table, FIELD.LAST_EVENT)))
    query.set_catalog_collection(catalog, collection)
    return query.scalar()


def _add_relations(query, catalog_name, collection_name):
    collection = gob_model[catalog_name]['collections'][collection_name]
    has_states = collection.get('has_states', False)

    src_table, _ = get_table_and_model(catalog_name, collection_name)

    for reference in collection['references']:
        relation_name = get_relation_name(gob_model, catalog_name, collection_name, reference)

        if not relation_name:
            continue

        rel_table, _ = get_table_and_model('rel', relation_name)

        select_attrs = [
            getattr(rel_table, 'src_id'),
            getattr(rel_table, 'src_volgnummer'),
        ] if has_states else [
            getattr(rel_table, 'src_id'),
        ]

        subselect = session \
            .query(
                *select_attrs,
                func.json_agg(
                    func.json_build_object(
                        FIELD.SOURCE_VALUE, getattr(rel_table, FIELD.SOURCE_VALUE),
                        FIELD.REFERENCE_ID, getattr(rel_table, 'dst_id')
                    )
                ).label('source_values')
            ).filter(
                and_(
                    getattr(rel_table, FIELD.DATE_DELETED).is_(None),
                    or_(
                        getattr(rel_table, FIELD.EXPIRATION_DATE).is_(None),
                        getattr(rel_table, FIELD.EXPIRATION_DATE) > func.now()
                    )
                )
            ).group_by(
                *select_attrs
            ).subquery()

        join_clause = [
            getattr(src_table, FIELD.ID) == getattr(subselect.c, 'src_id'),
            getattr(src_table, FIELD.SEQNR) == getattr(subselect.c, 'src_volgnummer')
        ] if has_states else [
            getattr(src_table, FIELD.ID) == getattr(subselect.c, 'src_id'),
        ]

        query = query.join(subselect, and_(*join_clause), isouter=True) \
            .add_columns(
            getattr(subselect.c, 'source_values').label(f"ref:{reference}")
        )

    return query


def _apply_filters(query, filters, model):
    for filter_ in filters:
        if filter_.get('op') == '==':
            query = query.filter(getattr(model, filter_['field']) == filter_['value'])
        else:
            raise NotImplementedError(f"Filter operator '{filter_.get('op', '')}' not implemented")

    return query


def query_entities(catalog, collection, view):
    assert _Base
    _session = get_session()

    table, model = get_table_and_model(catalog, collection, view)

    query = _session.query(table)
    query.set_catalog_collection(catalog, collection)

    # Only add relations if we're querying a catalog/collection
    if view is None:
        query = _add_relations(query, catalog, collection)

    # Exclude all records with date_deleted
    all_entities = filter_deleted(query, table)

    if view is None:
        # The default result is where expiration date is in the future or empty
        all_entities = filter_active(all_entities, table)

    # Apply filters if defined in model
    try:
        filters = model['api']['filters']
    except (KeyError, TypeError):
        pass
    else:
        all_entities = _apply_filters(all_entities, filters, table)

    if view:
        entity_convert = _get_convert_for_table(table,
                                                {**PUBLIC_META_FIELDS, **PRIVATE_META_FIELDS, **FIXED_COLUMNS})
    else:
        entity_convert = _get_convert_for_model(catalog, collection, model)

    return all_entities.yield_per(10000), entity_convert


def query_reference_entities(catalog, collection, reference_name, src_id):
    assert _Base
    _session = get_session()

    rel_catalog_name = 'rel'
    rel_collection_name = get_relation_name(gob_model, catalog, collection, reference_name)

    rel_table, _ = get_table_and_model(rel_catalog_name, rel_collection_name)

    dst_catalog_name, dst_collection_name = gob_model[catalog]['collections'][
        collection]['references'][reference_name]['ref'].split(':')

    # Destination table and model
    dst_table, dst_model = get_table_and_model(dst_catalog_name, dst_collection_name)

    query = _session.query(dst_table) \
                    .join(rel_table, dst_table._id == rel_table.dst_id) \
                    .filter(rel_table.src_id == src_id)

    # Exclude all records with date_deleted
    all_entities = filter_deleted(query, dst_table)

    # The default result is where expiration date is in the future or empty
    all_entities = filter_active(all_entities, dst_table)

    entity_convert = _get_convert_for_model(dst_catalog_name, dst_collection_name, dst_model)

    return all_entities, entity_convert


def get_collection_states(catalog, collection):
    """States.

    Returns all entities with state from the specified collection.

    :param catalog:
    :param collection:
    :return states: A dict containing all entities by _id for easy lookup
    """
    assert _Base
    _session = get_session()

    entity, _ = get_table_and_model(catalog, collection)

    # Get the max sequence number for every id + start validity combination
    sub = _session.query(getattr(entity, FIELD.ID),
                         getattr(entity, FIELD.START_VALIDITY),
                         label("max_seqnr", func.max(getattr(entity, FIELD.SEQNR)))
                         )\
        .group_by(FIELD.ID, FIELD.START_VALIDITY)\
        .subquery()

    # Filter the entities to only the highest volgnummer per id + start validity combination
    all_entities = _session.query(entity)
    all_entities.set_catalog_collection(catalog, collection)
    all_entities = all_entities \
        .join(sub, and_(getattr(sub.c, FIELD.ID) == getattr(entity, FIELD.ID),
                        getattr(sub.c, FIELD.START_VALIDITY) == getattr(entity, FIELD.START_VALIDITY),
                        sub.c.max_seqnr == getattr(entity, FIELD.SEQNR)))\
        .all()

    states = defaultdict(list)

    if not all_entities:
        return states

    for entity in all_entities:
        states[entity._id].append(entity)
    return states


def clear_test_dbs():
    """Clear the GOB test databases.

    :return:
    """
    # Test data is contained in the test_catalog and relation catalog
    test_catalog = "test_catalogue"
    rel_catalog = "rel"

    # Collect names of all test tables and entities
    tables = []
    test_entities = []
    rel_entities = []

    for collection_name in gob_model[test_catalog]['collections']:
        tables.append(gob_model.get_table_name(test_catalog, collection_name))
        test_entities.append(collection_name)

        collection = gob_model[test_catalog]['collections'][collection_name]
        refs = {
            **collection['references'],
            **collection['very_many_references']
        }
        for ref in refs:
            ref_name = get_relation_name(gob_model, test_catalog, collection_name, ref)
            tables.append(gob_model.get_table_name(rel_catalog, ref_name))
            rel_entities.append(ref_name)

    # Nicely format the SQL statement
    indent = ",\n" + ' ' * 17
    table_length = max(len(table) for table in tables)

    # Provide for SQL statements
    truncate_tables = ";\n".join([f"TRUNCATE TABLE {table:{table_length}} CASCADE" for table in tables])
    test_entity_list = indent.join([f"'{e}'" for e in test_entities])
    rel_entity_list = indent.join([f"'{e}'" for e in rel_entities])

    # Construct SQL statement
    statement = f"""
-- Truncate test tables
{truncate_tables};

-- Delete test entity events
DELETE
FROM events
WHERE catalogue = '{test_catalog}'
  AND entity IN ({test_entity_list});

-- Delete test relation events
DELETE FROM events
WHERE catalogue = '{rel_catalog}'
  AND entity IN ({rel_entity_list});

-- Commit all changes
COMMIT;
"""
    exec_statement(statement)


def get_entity(catalog, collection, id, view=None):
    """Entity.

    Returns the entity from the specified collection or the view identied by the id parameter.
    If the entity cannot be found, None is returned.

    :param id:
    :param view:
    :return:
    """
    assert _Base
    _session = get_session()

    _filter = {
        "_id": id,
    }

    table, model = get_table_and_model(catalog, collection, view)

    query = _session.query(table).filter_by(**_filter)
    query.set_catalog_collection(catalog, collection)

    query = _add_relations(query, catalog,  collection)

    # Exclude all records with date_deleted
    entity = filter_deleted(query, table)

    if view is None:
        # The default result is without deleted items
        entity = filter_active(entity, table)

    # Apply filters if defined in model
    try:
        filters = model['api']['filters']
    except (KeyError, TypeError):
        pass
    else:
        entity = _apply_filters(entity, filters, table)

    entity = entity.one_or_none()
    if view:
        entity_convert = _get_convert_for_table(
            table, {**PRIVATE_META_FIELDS, **FIXED_COLUMNS})
    else:
        entity_convert = _get_convert_for_model(
            catalog, collection, model, meta=PUBLIC_META_FIELDS, private_attributes=True)

    return entity_convert(entity) if entity else None


def filter_deleted(query, model):
    """Filter a query to exclude records with date deleted.

    :param query:
    :param model: The SQLAlchemy model
    :return: query
    """
    # The table can also be a view on a table and doesn't always have _date_deleted
    try:
        query = query.filter(getattr(model, FIELD.DATE_DELETED) == None)  # noqa: E711 (== None)
    except AttributeError:
        pass
    return query


def filter_active(query, model):
    """Filter a query to return only the active records.

    :param query:
    :param model: The SQLAlchemy model
    :return: query
    """
    return query.filter(or_(
        getattr(model, FIELD.EXPIRATION_DATE) > datetime.datetime.now(),
        getattr(model, FIELD.EXPIRATION_DATE) == None  # noqa: E711 (== None)
    ))
