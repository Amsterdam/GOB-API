from typing import Optional

import yaml

from gobcore.model import GOBModel, relations
from pydantic import BaseModel
from sqlalchemy.engine import Engine
from pathlib import Path


class ViewDefinition(BaseModel):
    table_name: str
    override_columns: Optional[dict[str, str]]

    def get_override_column(self, column_name: str):
        if self.override_columns and column_name in self.override_columns:
            return self.override_columns[column_name]


def _get_tables(model: GOBModel):
    for catalog_name, catalog in model.get_catalogs().items():
        for collection_name, collection in model.get_collections(catalog_name).items():
            yield catalog_name, collection_name, model.get_table_name(catalog_name, collection_name)


def _create_or_replace_default_view_query(table_name: str):
    return f"CREATE OR REPLACE VIEW legacy.{table_name} AS SELECT * FROM public.{table_name}"


def _get_custom_view_definition(table_name: str) -> ViewDefinition:
    viewdef_path = Path(__file__).parent.joinpath(f"view_definitions/{table_name}.yaml")

    if viewdef_path.exists():
        with open(viewdef_path, 'r') as f:
            viewdef = yaml.safe_load(f)
            return ViewDefinition.parse_obj(viewdef)


def _get_custom_view_query(viewdef: ViewDefinition, model: GOBModel, catalog_name: str, collection_name: str):
    collection = model.get_collection(catalog_name, collection_name)

    def get_field_def(field_name: str):
        override_column = viewdef.get_override_column(field_name)
        if override_column:
            return f"{override_column} as {field_name}"
        return field_name

    fields = [get_field_def(field) for field in collection['all_fields'].keys()]
    view_name = model.get_table_name(catalog_name, collection_name)
    from_table_name = viewdef.table_name

    fields_formatted = ",\n  ".join(fields)

    return f"CREATE OR REPLACE VIEW legacy.{view_name} AS SELECT\n  {fields_formatted}\nFROM public.{from_table_name}"


def _create_views_for_object_tables(model: GOBModel, connection):

    for catalog_name, collection_name, table_name in _get_tables(model):
        view_definition = _get_custom_view_definition(table_name)

        if view_definition:
            print(f"Have custom view for {table_name} ({catalog_name} {collection_name})")
            query = _get_custom_view_query(view_definition, model, catalog_name, collection_name)
            connection.execute(query)
        else:
            connection.execute(_create_or_replace_default_view_query(table_name))


def _create_views_for_materialized_views(model: GOBModel, connection):
    for relation_name in relations.get_relations(model)['collections'].keys():
        mv_name = f"mv_{relation_name}"

        if view_definition := _get_custom_view_definition(f"rel_{relation_name}"):
            mv_name_in_public = view_definition.table_name.replace("rel_", "mv_", 1)

            query = f"CREATE OR REPLACE VIEW legacy.{mv_name} AS SELECT * FROM public.{mv_name_in_public}"
            connection.execute(query)
        else:
            connection.execute(_create_or_replace_default_view_query(mv_name))


def create_legacy_views(model: GOBModel, engine: Engine):
    """Creates views in legacy schema that maps the AMS Schema model in public to the legacy GOB Model so that the
    API still exposes the GOB Model.
    """

    print("Initialising legacy schema")

    with engine.connect() as connection:
        connection.execute("CREATE SCHEMA IF NOT EXISTS legacy")

        _create_views_for_object_tables(model, connection)
        _create_views_for_materialized_views(model, connection)

    print("Done initialising legacy schema")
