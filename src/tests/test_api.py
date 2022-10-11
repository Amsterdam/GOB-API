""""API Unit tests.

The unit tests for the API module.
As it is a unit test all external dependencies are mocked.
"""

from unittest import TestCase
from unittest.mock import patch

import gobapi.api
from gobapi.api import _collection, _reference_collection, _clear_tests

def noop(*args):
    pass


class MockFlask:
    running = False
    config = {}

    def __init__(self, name):
        pass

    def route(self, rule, **kwargs):
        return noop

    def add_url_rule(self, rule, **kwargs):
        return noop

    def before_request(self, *args, **kwargs):
        pass

    def after_request(self, *args, **kwargs):
        pass

    def teardown_appcontext(self, func):
        return None

    def run(self):
        self.running = True


class MockCORS:
    def __init__(self, app):
        pass


class MockRequest:
    args = {}
    path = 'path'

mockRequest = MockRequest()


class MockGOBViews:
    views = {}

    def get_views(self, catalog, collection):
        return self.views

    def get_view(self, catalog, collection, view_name):
        return self.views.get(view_name)


def mock_entities(catalog, collection, offset, limit, view=None, reference_name=None, src_id=None):
    entities = []
    return entities, len(entities)


catalogs = {}
catalog = {}

class MockModel:
    def __init__(self):
        pass

    def __getitem__(self, catalog_name):
        return catalog

    def get(self, catalog_name):
        return catalog

    def items(self):
        return catalogs.items()


def before_each_api_test(monkeypatch):
    global catalogs, catalog
    global entity

    catalogs = {}
    catalog = {}
    entity = None

    monkeypatch.setattr(gobapi.config, 'API_INFRA_SERVICES', "")

    monkeypatch.setattr(gobapi.api, 'Flask', MockFlask)
    monkeypatch.setattr(gobapi.api, 'CORS', MockCORS)

    monkeypatch.setattr(gobapi.api, 'request', mockRequest)

    monkeypatch.setattr(gobapi.api, 'hal_response',
            lambda data, links=None: ((data, links), 200, {'Content-Type': 'application/json'}))
    monkeypatch.setattr(gobapi.api, 'not_found', lambda msg: msg)

    monkeypatch.setattr(gobapi.api, 'GOBViews', MockGOBViews)

    monkeypatch.setattr(gobapi.api, 'connect', noop)
    monkeypatch.setattr(gobapi.api, 'get_entities', mock_entities)
    monkeypatch.setattr(gobapi.api, 'get_entity',
            lambda catalog, collection, id, view=None: entity)

    monkeypatch.setattr(gobapi.api, 'get_states',
            lambda collections, offset, limit: ([{'id': '1', 'attribute': 'attribute'}], 1))

    monkeypatch.setattr(gobapi.api, 'gob_model', MockModel())

    monkeypatch.setattr(
        gobapi.api, 'AuditLogMiddleware',
        type('MockAuditLogMiddleware', (), {'__init__': lambda *args: None})
    )


@patch("gobapi.services.threaded_service")
def test_app(Mock, monkeypatch):
    before_each_api_test(monkeypatch)
    from gobapi.api import get_app

    app = get_app()
    assert not app == None
    app.run()
    # assert len(app._infra_threads) == 0


def test_catalogs(monkeypatch):
    global catalogs

    before_each_api_test(monkeypatch)
    from gobapi.api import _catalogs

    catalogs = {}
    assert _catalogs() == (({'_embedded': {'catalogs':[] }}, None), 200, {'Content-Type': 'application/json'})

    catalogs = {'catalog': {'description': 'catalog', 'abbreviation': 'cat'}}
    assert _catalogs() == (
        (
            {
                '_embedded': {
                    'catalogs': [
                        {
                            '_links': {'self': {'href': '/gob/public/catalog/'}},
                            'name': 'catalog',
                            'abbreviation': 'cat',
                            'description': 'catalog'
                        }
                    ]}}, None), 200, {'Content-Type': 'application/json'})


def test_catalog(monkeypatch):
    global catalog

    before_each_api_test(monkeypatch)
    from gobapi.api import _catalog

    catalog = {}
    assert _catalog('catalog_name') == 'Catalog catalog_name not found'

    catalog = {
        'description': 'description',
        'abbreviation': 'abbr',
        'version': 'v1',
        'collections': {}
    }
    assert _catalog('catalog_name') == (
        (
            {
                '_embedded': {
                    'collections': []
                },
                'name': 'catalog_name',
                'abbreviation': 'abbr',
                'description': 'description',
                'version': 'v1',
                'collections': []
            }, None), 200, {'Content-Type': 'application/json'})


def test_entities(monkeypatch):
    global catalog

    before_each_api_test(monkeypatch)
    from gobapi.api import _entities

    catalog = {'collections': {
        'collection': {'key': 'value'}
        }}
    assert _entities('catalog', 'collection', 1, 1) == ({
        'page_size': 1, 'pages': 0, 'results': [], 'total_count': 0}, {'next': None, 'previous': None})


def test_entities_with_view(monkeypatch):
    global catalog

    before_each_api_test(monkeypatch)
    from gobapi.api import _entities

    catalog = {'collections': {
        'collection': {'key': 'value'}
        }}
    assert _entities('catalog', 'collection', 1, 1, 'enhanced') == ({
        'page_size': 1, 'pages': 1, 'results': [], 'total_count': 0}, {'next': None, 'previous': None})


def test_reference_entities(monkeypatch):
    global catalog

    before_each_api_test(monkeypatch)
    from gobapi.api import _reference_entities

    catalog = {'collections': {
        'collection': {'references': {'reference': True}}
        }}
    assert _reference_entities('catalog', 'collection', 'reference', 1, 1, 1) == ({
        'page_size': 1, 'pages': 0, 'results': [], 'total_count': 0}, {'next': None, 'previous': None})


def test_entity(monkeypatch):
    global catalog, entity

    before_each_api_test(monkeypatch)
    from gobapi.api import _entity

    catalog = {}
    assert _entity('catalog', 'collection', '1') == 'catalog not found'

    catalog = {'collections': {}}
    assert _entity('catalog', 'collection', '1') == 'catalog.collection not found'

    catalog = {'collections': {
        'collection': {'key': 'value'}
        }}

    entity = None
    assert _entity('catalog', 'collection', '1') == 'catalog.collection:1 not found'

    entity = {'id': 1}
    assert _entity('catalog', 'collection', 1) == ((entity, None), 200, {'Content-Type': 'application/json'})


def test_entity_with_view(monkeypatch):
    global catalog, entity

    before_each_api_test(monkeypatch)
    from gobapi.api import _entity

    mockRequest.args = {
        'view': 'enhanced'
    }

    catalog = {}
    assert _entity('catalog', 'collection', '1') == 'catalog not found'

    catalog = {'collections': {}}
    assert _entity('catalog', 'collection', '1') == 'catalog.collection not found'

    catalog = {'collections': {
        'collection': {'key': 'value'}
        }}

    entity = None
    assert _entity('catalog', 'collection', '1') == 'catalog.collection?view=enhanced not found'

    MockGOBViews.views = {
        'enhanced': {
            'name': 'the_view_name'
        }
    }
    assert _entity('catalog', 'collection', '1') == 'catalog.collection:1 not found'

    entity = {'id': 1}
    assert _entity('catalog', 'collection', 1) == ((entity, None), 200, {'Content-Type': 'application/json'})


def test_collection(monkeypatch):
    global catalog

    before_each_api_test(monkeypatch)
    from gobapi.api import _collection

    catalog = {'collections': {}}
    assert _collection('catalog', 'collection') == 'catalog.collection not found'

    catalog = {'collections': {
        'collection': {'key': 'value'}
        }}

    mockRequest.args = {}
    assert _collection('catalog', 'collection') == (
        ({
             'page_size': 100,
             'pages': 0,
             'results': [],
             'total_count': 0
         },{
             'next': None,
            'previous': None}
        ), 200, {'Content-Type': 'application/json'})

    mockRequest.args = {
        'page': 5,
        'page_size': 10
    }
    assert _collection('catalog', 'collection') == (
        ({
             'page_size': 10,
             'pages': 0,
             'results': [],
             'total_count': 0
         },{
             'next': None,
             'previous': None}
        ), 200, {'Content-Type': 'application/json'})


def test_collection_with_view(monkeypatch):
    global catalog

    before_each_api_test(monkeypatch)
    from gobapi.api import _collection

    catalog = {'collections': {}}
    assert _collection('catalog', 'collection') == 'catalog.collection not found'

    catalog = {'collections': {
        'collection': {'key': 'value'}
        }}

    mockRequest.args = {
        'view': 'enhanced'
    }
    MockGOBViews.views = {}
    assert _collection('catalog', 'collection') == 'catalog.collection?view=enhanced not found'

    MockGOBViews.views = {
        'enhanced': {
            'name': 'the_view_name'
        }
    }
    # Views always show 1 page extra because count is slow on large views
    assert _collection('catalog', 'collection') == (
        ({
             'page_size': 100,
             'pages': 1,
             'results': [],
             'total_count': 0
         },{
             'next': None,
             'previous': None}
        ), 200, {'Content-Type': 'application/json'})


def test_reference_collection(monkeypatch):
    global catalog, entity

    before_each_api_test(monkeypatch)
    from gobapi.api import _reference_collection

    catalog = {}
    assert _reference_collection('catalog', 'collection', '1234', 'reference') == 'catalog not found'

    catalog = {'collections': {}}
    assert _reference_collection('catalog', 'collection', '1234', 'reference') == 'catalog.collection not found'

    catalog = {'collections': {
        'collection': {'references': {'reference': True}}
        }
    }
    mockRequest.args = {}
    assert _reference_collection('catalog', 'collection', '1234', 'reference') == 'catalog.collection:1234 not found'

    catalog = {'collections': {
        'collection': {'references': {'reference': False}}
        }}
    mockRequest.args = {
        'page': 5,
        'page_size': 10
    }
    entity = {'id': '1234'}
    assert _reference_collection('catalog', 'collection', '1234', 'reference') == 'catalog.collection:1234:reference not found'

    catalog = {'collections': {
        'collection': {'references': {'reference': True}}
        }}
    assert _reference_collection('catalog', 'collection', '1234', 'reference') == (
        ({
             'page_size': 10,
             'pages': 0,
             'results': [],
             'total_count': 0
         },{
             'next': None,
             'previous': None}
        ), 200, {'Content-Type': 'application/json'})


def test_states(monkeypatch):
    before_each_api_test(monkeypatch)
    from gobapi.api import _states

    assert _states() == 'No collections requested'

    mockRequest.args = {
        'collections': 'catalog:collection'
    }
    assert _states() == (
        ({
             'page_size': 100,
             'pages': 1,
             'results': [{'id': '1', 'attribute': 'attribute'}],
             'total_count': 1
         },{
             'next': None,
            'previous': None}
        ), 200, {'Content-Type': 'application/json'})


def test_health(monkeypatch):
    before_each_api_test(monkeypatch)
    from gobapi.api import _health

    assert _health() == 'Connectivity OK'


def test_wsgi(monkeypatch):
    before_each_api_test(monkeypatch)
    from gobapi.wsgi import application

    assert not application == None


@patch('gobapi.api.WorkerResponse.stream_with_context', lambda f, mimetype: f)
class TestStreams(TestCase):

    @patch('gobapi.api.request', mockRequest)
    @patch('gobapi.api.ndjson_entities')
    @patch('gobapi.api.stream_entities')
    @patch('gobapi.api.query_entities')
    @patch('gobapi.api.gob_model', spec_set=True)
    def test_collection(self, mock_gobmodel, mock_query, mock_stream, mock_ndjson):
        data = {'catalog': {
            'collections': {
                'collection': {'key': 'value'}
                }
            }
        }
        mock_gobmodel.get.side_effect = data.get
        mock_gobmodel.__getitem__.side_effect = data.__getitem__
        mock_query.side_effect = lambda cat, col, view: ([], lambda e: e)

        mockRequest.args = {
            'stream': 'true'
        }
        result = _collection('catalog', 'collection')
        mock_gobmodel.__getitem__.assert_called_with("catalog")
        mock_stream.assert_called()

        mockRequest.args = {
            'ndjson': 'true'
        }
        result = _collection('catalog', 'collection')
        mock_ndjson.assert_called()

    @patch('gobapi.api.request', mockRequest)
    @patch('gobapi.api.ndjson_entities')
    @patch('gobapi.api.stream_entities')
    @patch('gobapi.api.query_reference_entities')
    @patch('gobapi.api.get_entity')
    @patch('gobapi.api.gob_model', spec_set=True)
    def test_reference_collection(self, mock_gobmodel, mock_entity, mock_query, mock_stream, mock_ndjson):
        data = {'catalog': {
            'collections': {
                'collection': {'references': {'reference': True}}
                }
            }
        }
        mock_gobmodel.get.side_effect = data.get
        mock_gobmodel.__getitem__.side_effect = data.__getitem__
        mock_entity.return_value = {'id': 'reference'}
        mock_query.side_effect = lambda cat, col, ref, entity_id: ([], lambda e: e)

        mockRequest.args = {
            'stream': 'true'
        }
        result = _reference_collection('catalog', 'collection', 'entity_id', 'reference')
        mock_gobmodel.get.assert_called_with("catalog")
        mock_entity.assert_called_with("catalog", 'collection', 'entity_id')
        mock_query.assert_called_with("catalog", 'collection', 'reference', 'entity_id')
        mock_stream.assert_called()

        mockRequest.args = {
            'ndjson': 'true'
        }
        result = _reference_collection('catalog', 'collection', 'entity_id', 'reference')
        mock_ndjson.assert_called()

class TestClearTest(TestCase):

    @patch("gobapi.api.clear_test_dbs")
    def test_clear_test_dbs(self, mock_clear_test_dbs):
        result = _clear_tests()
        mock_clear_test_dbs.assert_called()
        self.assertEqual(result, ('', 200))
