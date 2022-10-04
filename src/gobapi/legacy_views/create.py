from sqlalchemy.engine import Engine
from sqlalchemy.exc import ProgrammingError
from psycopg2.errors import InvalidTableDefinition

from gobcore.model import GOBModel, relations
from gobapi.legacy_views.legacy_views import ViewDefinition, get_custom_view_definition


def _get_tables(gob_model: GOBModel):
    for catalog_name, catalog in gob_model.items():
        for collection_name in catalog['collections']:
            yield catalog_name, collection_name, gob_model.get_table_name(catalog_name, collection_name)


def _default_view_query(table_name: str):
    return f"SELECT * FROM public.{table_name}"


def _get_custom_view_query(
        viewdef: ViewDefinition, gob_model: GOBModel, catalog_name: str, collection_name: str):
    collection = gob_model[catalog_name]['collections'][collection_name]

    def get_field_def(field_name: str):
        override_column = viewdef.get_override_column(field_name)
        if override_column:
            return f"{override_column} as {field_name}"
        return field_name

    fields = [get_field_def(field) for field in collection['all_fields'].keys()]
    from_table_name = viewdef.table_name

    fields_formatted = ",\n  ".join(fields)

    return f"SELECT\n  {fields_formatted}\nFROM public.{from_table_name}"


def _create_view_with_drop_fallback(view_name: str, query: str, connection):
    create_view_query = f"CREATE OR REPLACE VIEW legacy.{view_name} AS {query}"

    try:
        connection.execute(create_view_query)
    except ProgrammingError as exc:
        if isinstance(exc.orig, InvalidTableDefinition):
            # View definition does not match existing view. Drop old and create new
            connection.execute(f"DROP VIEW legacy.{view_name} CASCADE")
            connection.execute(create_view_query)
        else:
            raise exc


def _create_views_for_object_tables(gob_model: GOBModel, connection):
    for catalog_name, collection_name, table_name in _get_tables(gob_model):
        view_definition = get_custom_view_definition(table_name)

        if view_definition:
            print(f"Have custom view for {table_name} ({catalog_name} {collection_name})")
            query = _get_custom_view_query(view_definition, gob_model, catalog_name, collection_name)
            _create_view_with_drop_fallback(table_name, query, connection)
        else:
            query = _default_view_query(table_name)
            _create_view_with_drop_fallback(table_name, query, connection)


def _create_views_for_materialized_views(gob_model: GOBModel, connection):
    for relation_name in relations.get_relations(gob_model)['collections'].keys():
        table_name = f"rel_{relation_name}"
        view_definition = get_custom_view_definition(table_name)

        if view_definition:
            mv_name_in_public = view_definition.table_name.replace("rel_", "mv_", 1)
            mv_name = table_name.replace("rel_", "mv_", 1)
            query = f"SELECT * FROM public.{mv_name_in_public}"
        else:
            mv_name = f"mv_{relation_name}"
            query = _default_view_query(mv_name)

        connection.execute(f"CREATE OR REPLACE VIEW legacy.{mv_name} AS {query}")


def create_legacy_views(gob_model: GOBModel, engine: Engine):
    """Creates views in legacy schema that maps the AMS Schema model in public to the
    legacy GOB Model so that the API still exposes the GOB Model.
    """
    print("Initialising legacy schema")

    with engine.connect() as connection:
        connection.execute("CREATE SCHEMA IF NOT EXISTS legacy")

        _create_views_for_object_tables(gob_model, connection)
        _create_views_for_materialized_views(gob_model, connection)

    print("Done initialising legacy schema")
