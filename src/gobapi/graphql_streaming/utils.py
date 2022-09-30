from gobapi import gob_model
from gobapi.utils import to_snake


def resolve_schema_collection_name(schema_collection_name: str):
    """Resolve catalog and collection from schema collection name.

    :param schema_collection_name:
    :return:
    """
    names = to_snake(schema_collection_name).split('.')[-1].split('_')
    for n in range(1, len(names)):
        catalog_name = '_'.join(names[:-n])
        collection_name = '_'.join(names[-n:])
        catalog = gob_model.get(catalog_name)
        if catalog:
            collection = gob_model[catalog_name]['collections'].get(collection_name)
        else:
            collection = None
        if catalog and collection:
            return catalog_name, collection_name
    return None, None
