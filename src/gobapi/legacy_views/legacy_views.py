from collections import defaultdict
from typing import Optional

import yaml

from pydantic import BaseModel
from pathlib import Path


class ViewDefinition(BaseModel):
    table_name: str
    override_columns: Optional[dict[str, str]]

    def get_override_column(self, column_name: str):
        if self.override_columns and column_name in self.override_columns:
            return self.override_columns[column_name]


def _get_view_definitions_path() -> Path:
    return Path(__file__).parent.joinpath("view_definitions")


def _open_view_definition(viewdef_path: Path) -> ViewDefinition:
    with open(viewdef_path, 'r', encoding='utf-8') as f:
        viewdef = yaml.safe_load(f)
        return ViewDefinition.parse_obj(viewdef)


def get_custom_view_definition(table_name: str) -> ViewDefinition:
    viewdef_path = _get_view_definitions_path().joinpath(f"{table_name}.yaml")

    if viewdef_path.exists():
        return _open_view_definition(viewdef_path)


def _catalog_collection_from_tablename(table_name: str):
    catalog, *collection = table_name.split('_')
    return catalog, '_'.join(collection)


def get_all_table_renames() -> dict[str, dict[str, str]]:
    """Returns a mapping from legacy schema to public schema table renames

    """
    path = _get_view_definitions_path()

    result = defaultdict(dict)
    for fpath in path.rglob('*.yaml'):
        viewdef = _open_view_definition(fpath)

        legacy_name = fpath.stem
        if viewdef.table_name and legacy_name != viewdef.table_name:
            legacy_cat, legacy_coll = _catalog_collection_from_tablename(legacy_name)
            _, tablename = _catalog_collection_from_tablename(viewdef.table_name)
            result[legacy_cat][legacy_coll] = tablename
    return result
