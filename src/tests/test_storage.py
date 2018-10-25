"""Storage Unit tests

The unit tests for the storage module.
As it is a unit test all external dependencies are mocked

"""
import importlib
import sqlalchemy


class MockClasses:
    def __init__(self):
        self.collection1 = 'collection1'


class MockBase:
    def prepare(self, engine, reflect):
        return None

    classes = MockClasses()


class MockEntity:
    def __init__(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MockEntities:
    all_entities = []
    one_entity = {}

    def count(self):
        return len(self.all_entities)

    def offset(self, offset):
        return self

    def limit(self, limit):
        return self

    def all(self):
        return self.all_entities

    def filter_by(self, **kwargs):
        return self

    def order_by(self, order_by):
        return self

    def one_or_none(self):
        return self.one_entity


class MockColumn:

    def __init__(self, name):
        self.name = name
    type = sqlalchemy.types.VARCHAR()

class MockTable():

    def __init__(self, *args, **kwargs):
        pass

    columns = [MockColumn('id'), MockColumn('attribute'), MockColumn('meta')]


class MockSession:
    def __init__(self, engine):
        pass

    def query(self, table):
        return MockEntities()


def mock_create_engine(url):
    return 'engine'


def mock_automap_base():
    return MockBase()


mock_PUBLIC_META_FIELDS = {
    "meta": {
        "type": "GOB.String",
        "description": "metadescription"
    }
}


def mock_get_gobmodel():
    class model:
        def get_model(self, name):
            return {
                'collection1': {
                    'entity_id': 'id',
                    'attributes': {
                        'id': {
                            'type': 'GOB.String',
                            'description': 'Unique id of the collection'
                        },
                        'attribute': {
                            'type': 'GOB.String',
                            'description': 'Some attribute'
                        }
                    },
                    'fields': {
                        'id': {
                            'type': 'GOB.String',
                            'description': 'Unique id of the collection'
                        },
                        'attribute': {
                            'type': 'GOB.String',
                            'description': 'Some attribute'
                        }
                    }
                }
            }[name]

    return model()

def before_each_storage_test(monkeypatch):
    import sqlalchemy
    importlib.reload(sqlalchemy)
    import sqlalchemy.ext.automap
    importlib.reload(sqlalchemy.ext.automap)
    import sqlalchemy.orm
    importlib.reload(sqlalchemy.orm)

    import gobapi.config
    importlib.reload(gobapi.config)

    import gobcore.model
    importlib.reload(gobapi.config)

    monkeypatch.setattr(sqlalchemy, 'create_engine', mock_create_engine)
    monkeypatch.setattr(sqlalchemy, 'Table', MockTable)
    monkeypatch.setattr(sqlalchemy.ext.automap, 'automap_base', mock_automap_base)
    monkeypatch.setattr(sqlalchemy.orm, 'Session', MockSession)

    monkeypatch.setattr(gobcore.model, 'GOBModel', mock_get_gobmodel)
    monkeypatch.setattr(gobcore.model.metadata, 'PUBLIC_META_FIELDS', mock_PUBLIC_META_FIELDS)

    import gobapi.storage
    importlib.reload(gobapi.storage)

    from gobapi.storage import connect
    connect()


def test_entities(monkeypatch):
    before_each_storage_test(monkeypatch)

    from gobapi.storage import get_entities
    MockEntities.all_entities = []
    assert(get_entities('collection1', 0, 1) == ([], 0))

    mockEntity = MockEntity({'id': 'id', 'attribute': 'attribute'})
    MockEntities.all_entities = [
        mockEntity
    ]
    assert(get_entities('collection1', 0, 1) == ([{'attribute': 'attribute', 'id': 'id'}], 1))

    mockEntity = MockEntity({'id': 'id', 'attribute': 'attribute', 'non_existing_attribute': 'non_existing_attribute'})
    MockEntities.all_entities = [
        mockEntity
    ]
    assert(get_entities('collection1', 0, 1) == ([{'attribute': 'attribute', 'id': 'id'}], 1))


def test_entities_with_ordering(monkeypatch):
    before_each_storage_test(monkeypatch)

    from gobapi.storage import get_entities
    mockEntity1 = MockEntity({'id': 'id1', 'attribute': 'attribute'})
    mockEntity2 = MockEntity({'id': 'id2', 'attribute': 'attribute'})
    MockEntities.all_entities = [
        mockEntity1,
        mockEntity2,
    ]
    assert(get_entities('collection1', 0, 1) == ([{'attribute': 'attribute', 'id': 'id1'}, {'attribute': 'attribute', 'id': 'id2'}], 2))

    # Test that both asc as desc are accepted as input
    assert(get_entities('collection1', 0, 1, order_by='id') == ([{'attribute': 'attribute', 'id': 'id1'}, {'attribute': 'attribute', 'id': 'id2'}], 2))
    assert(get_entities('collection1', 0, 1, order_by='-id') == ([{'attribute': 'attribute', 'id': 'id1'}, {'attribute': 'attribute', 'id': 'id2'}], 2))


def test_entities_with_view(monkeypatch):
    before_each_storage_test(monkeypatch)

    from gobapi.storage import get_entities
    MockEntities.all_entities = []
    assert(get_entities('collection1', 0, 1, view='enhanced') == ([], 0))

    mockEntity = MockEntity({'id': 'id', 'attribute': 'attribute'})
    MockEntities.all_entities = [
        mockEntity
    ]
    assert(get_entities('collection1', 0, 1, view='enhanced') == ([{'attribute': 'attribute', 'id': 'id'}], 1))

    mockEntity = MockEntity({'id': 'id', 'attribute': 'attribute', 'non_existing_attribute': 'non_existing_attribute'})
    MockEntities.all_entities = [
        mockEntity
    ]
    assert(get_entities('collection1', 0, 1, view='enhanced') == ([{'attribute': 'attribute', 'id': 'id'}], 1))


def test_entity(monkeypatch):
    before_each_storage_test(monkeypatch)

    from gobapi.storage import get_entity
    assert(get_entity('collection1', 'id') == None)

    mockEntity = MockEntity({'id': 'id', 'attribute': 'attribute', 'meta': 'meta'})
    MockEntities.one_entity = mockEntity
    assert(get_entity('collection1', 'id') == {'attribute': 'attribute', 'id': 'id', 'meta': 'meta'})


def test_entity_with_view(monkeypatch):
    before_each_storage_test(monkeypatch)

    MockEntities.one_entity = None
    from gobapi.storage import get_entity
    assert(get_entity('collection1', 'id', 'enhanced') == None)

    mockEntity = MockEntity({'id': 'id', 'attribute': 'attribute', 'meta': 'meta'})
    MockEntities.one_entity = mockEntity
    assert(get_entity('collection1', 'id', 'enhanced') == {'attribute': 'attribute', 'id': 'id', 'meta': 'meta'})
