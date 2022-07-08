from gobcore.model import GOBModel, relations
from sqlalchemy.engine import Engine


def _get_tables(model: GOBModel):
    for catalog_name, catalog in model.get_catalogs().items():
        for collection_name, collection in model.get_collections(catalog_name).items():
            yield model.get_table_name(catalog_name, collection_name)


def _create_or_replace_default(table_name: str):
    return f"CREATE OR REPLACE VIEW legacy.{table_name} AS SELECT * FROM public.{table_name}"


def _create_views_for_object_tables(model: GOBModel, connection):
    for table_name in _get_tables(model):
        connection.execute(_create_or_replace_default(table_name))


def _create_views_for_materialized_views(model: GOBModel, connection):
    for relation_name in relations.get_relations(model)['collections'].keys():
        mv_name = f"mv_{relation_name}"
        connection.execute(_create_or_replace_default(mv_name))


def _create_views_for_special_tables(connection):
    # These won't be used, but model initialisation needs these
    tables = ["spatial_ref_sys", "alembic_version", "events"]
    for table_name in tables:
        connection.execute(_create_or_replace_default(table_name))


def create_legacy_views(model: GOBModel, engine: Engine):
    """Creates views in legacy schema that maps the AMS Schema model in public to the legacy GOB Model so that the
    API still exposes the GOB Model.
    """

    print("Initialising legacy views")

    with engine.connect() as connection:
        connection.execute("CREATE SCHEMA IF NOT EXISTS legacy")

        _create_views_for_object_tables(model, connection)
        _create_views_for_materialized_views(model, connection)
        _create_views_for_special_tables(connection)
