"""
Dump GOB

Dumps of catalog collections in sql format
"""
import re

from gobcore.typesystem.gob_types import String
from gobcore.typesystem import fully_qualified_type_name
from gobcore.model.metadata import FIELD

from gobapi import gob_model
from gobapi.auth.auth_query import Authority
from gobapi.dump.config import DELIMITER_CHAR, JSON_TYPES
from gobapi.dump.config import UNIQUE_ID, REFERENCE_TYPES, get_reference_fields
from gobapi.dump.config import SQL_TYPE_CONVERSIONS, SQL_QUOTATION_MARK

from gobapi.dump.config import get_field_specifications, joined_names, get_field_order


def _quote(name):
    """
    Quote all SQL identifiers (schema, table, column names)
    to prevent weird errors with SQL keywords accidentally being used in identifiers.

    Note that quotation marks may differ per database type.
    Current escape char works for PostgreSQL

    :param name:
    :return:
    """
    QUOTE_CHAR = '"'
    return f"{QUOTE_CHAR}{name}{QUOTE_CHAR}"


def _create_schema(name):
    """
    Returns a SQL statement to create a schema with the given name

    :param name:
    :return:
    """
    return f"""
-- DROP SCHEMA {name} CASCADE;
CREATE SCHEMA IF NOT EXISTS {_quote(name)};
COMMIT;
"""


def _create_field(name, type, description):
    """
    Create a database field

    :param name:
    :param type:
    :param description:
    :return: dict containing database field properties
    """
    return {
        'name': _quote(name),
        'type': SQL_TYPE_CONVERSIONS[type],
        'description': description
    }


def to_sql_string_value(s):
    """
    Convert a python string into an SQL string ('...') value
    :param s:
    :return:
    """
    # Escape any single quotes as they are used to start and terminate a string value
    return f"'{quote_sql_string(s)}'"


def quote_sql_string(s):
    """
    Quote sql string by replacing sql quotation marks by 2 quotation marks, eg ' => ''
    :param s:
    :return:
    """
    return s.replace(SQL_QUOTATION_MARK, 2 * SQL_QUOTATION_MARK)


def _quoted_tablename(schema, table_name):
    return f"{_quote(schema)}.{_quote(table_name)}"


def _delete_table(schema, name):
    """
    Delete table with the given name in the given schema

    :param schema:
    :param name:
    :return:
    """
    table = _quoted_tablename(schema, name)
    return f"DROP TABLE IF EXISTS {table} CASCADE"


def _insert_into_table(schema, src_name, dst_name):
    """
    Truncates the dst_table and copy the data from src_table in the given schema to dst_name in the same schema

    :param schema:
    :param src_name:
    :param dst_name:
    :return:
    """
    src_table = _quoted_tablename(schema, src_name)
    dst_table = _quoted_tablename(schema, dst_name)
    return f"""
TRUNCATE TABLE {dst_table};
INSERT INTO {dst_table} SELECT * FROM {src_table}
"""


def _create_indexes(model):
    indexes = []
    for field, spec in get_field_specifications(model).items():
        if field == model['entity_id'] or re.compile(r"(^|.+_)ref$").match(field) or field == FIELD.LAST_EVENT:
            indexes.append(
                {'field': field})  # Plain entity id, full entity id (ref) or rel. foreign key (eg dst_ref)
        elif "GOB.Geo" in spec['type']:
            indexes.append({'field': field, 'method': "gist"})  # Spatial index
        elif spec['type'] == "GOB.Reference" and "ref" in get_reference_fields(spec):
            indexes.append({'field': f"{field}_ref"})  # Foreign key index

    return indexes


def _create_index(schema, collection_name, field, method="btree"):
    """
    Create an index for the table with the given collection_name in the given schema on the given field.

    :param schema:
    :param collection_name:
    :param field:
    :param method:
    :return:
    """
    table = _quoted_tablename(schema, collection_name)
    return f"""
CREATE INDEX IF NOT EXISTS {collection_name}_{field} ON {table} USING {method} ({field})
"""


def get_max_eventid(schema, collection_name):
    table_name = _quoted_tablename(schema, collection_name)
    return f"SELECT max({FIELD.LAST_EVENT}) FROM {table_name}"


def delete_entities_with_source_ids(schema, collection_name, source_ids):
    table_name = _quoted_tablename(schema, collection_name)
    source_ids_sql = ",".join([to_sql_string_value(source_id) for source_id in source_ids])
    return f"DELETE FROM {table_name} WHERE {FIELD.SOURCE_ID} IN ({source_ids_sql})"


def get_count(schema, collection_name):
    """
    Returns the SQL statement that returns the number of rows in the given table (schema.collection)

    :param schema:
    :param collection_name:
    :return:
    """
    table_name = _quoted_tablename(schema, collection_name)
    return f"SELECT count(*) FROM {table_name}"


def _autorized_order(order, catalog_name, collection_name):
    """
    Filter the order (list of columns) on columns that are not suppressed given the current request
    """
    authority = Authority(catalog_name, collection_name)
    suppress_columns = authority.get_suppressed_columns()
    return [o for o in order if o not in suppress_columns]


def _create_table(schema, catalog_name, collection_name, model, tablename=None):
    """
    Returns a SQL statement to create a table in a schema
    The table fields are constructed from the specs

    :param schema:
    :param collection_name:
    :param specs:
    :param tablename: if None, collection_name is used
    :return:
    """
    specs = get_field_specifications(model)
    order = _autorized_order(get_field_order(model), catalog_name, collection_name)
    catalog = gob_model[catalog_name]
    catalog_description = quote_sql_string(catalog['description'])
    fields = []
    for field_name in order:
        field_spec = specs[field_name]
        field_description = quote_sql_string(field_spec['description'])
        if field_spec['type'] in REFERENCE_TYPES:
            for reference_field in get_reference_fields(field_spec):
                name = joined_names(field_name, reference_field)
                fields.append(_create_field(name, fully_qualified_type_name(String),
                                            f"{field_description} ({reference_field})"))
        elif field_spec['type'] in JSON_TYPES:
            for field, spec in field_spec['attributes'].items():
                name = joined_names(field_name, field)
                # Make all JSON attribute columns of type String (in case the resulting values are merged into a list)
                fields.append(_create_field(name, fully_qualified_type_name(String), f"{field_description} ({field})"))
        else:
            fields.append(_create_field(field_name, field_spec['type'], field_description))

    field_lengths = [len(field['name']) for field in fields]
    max_length = max(field_lengths) if field_lengths else 1

    table_name = (f"{_quote(schema)}.{_quote(tablename or collection_name)}")
    table_fields = ",\n  ".join([f"{field['name']:{max_length}} {field['type']}" for field in fields])

    comments = ";\n".join([
        f"COMMENT ON COLUMN {table_name}.{field['name']:{max_length}} "
        f"IS {SQL_QUOTATION_MARK}{field['description']}{SQL_QUOTATION_MARK}" for field in fields
    ])

    primary_key = f",PRIMARY KEY ({UNIQUE_ID})" if UNIQUE_ID in order else ""

    return f"""
CREATE TABLE IF NOT EXISTS {table_name}
(
  {table_fields}
  {primary_key}
);
COMMIT;

-- Table and Column comments
COMMENT ON TABLE  {table_name} {'':{max_length}} IS {SQL_QUOTATION_MARK}{catalog_description}{SQL_QUOTATION_MARK};
{comments}
"""


def _import_csv(schema, collection_name, csv_file):
    """
    Returns a SQL statement to import a collection into a table

    :param schema:
    :param collection_name:
    :param specs:
    :param csv_file:
    :return:
    """
    table_name = _quoted_tablename(schema, collection_name)
    return f"\\COPY {table_name} FROM '{csv_file}' DELIMITER '{DELIMITER_CHAR}' CSV HEADER;"


def sql_entities(catalog_name, collection_name, model):
    """
    Returns a SQL statement to create a schema, table for the given model

    :param catalog_name:
    :param collection_name:
    :param entities:
    :param model:
    :return:
    """
    schema = catalog_name
    indexes = _create_indexes(model)
    create_indexes = "".join([_create_index(schema, collection_name, **index) for index in indexes])

    return f"""
-- Create schema
{_create_schema(schema)}

-- Create table
{_create_table(schema, catalog_name, collection_name, model)}

-- Import data from csv
{_import_csv(schema, collection_name, f"{collection_name}.csv")}

-- Create indexes
{create_indexes}
"""
