from unittest import TestCase, mock
from unittest.mock import patch, MagicMock

from gobapi.auth.auth_query import Authority, AuthorizedQuery, GOB_AUTH_SCHEME, gob_types
from gobapi.auth.auth_query import gob_secure_types, _handle_secure_columns, set_suppressed_columns

role_a = "a"
role_b = "b"
role_c = "c"

mock_scheme = {
    "any catalog": {
        "collections": {
            "any collection": {
                "attributes": {
                    "any attribute": {
                        "roles": [role_a, role_b]
                    }
                }
            }
        }
    },
    "secure catalog": {
        "roles": [role_a, role_b]
    },
    "secure catalog collection": {
        "collections": {
            "secure collection": {
                "roles": [role_a, role_b]
            }
        }
    },
}


class MockEntity:

    def __init__(self):
        self.a = "value a"
        self.b = "value b"
        self.c = "value c"


class MockRequest:
    headers = {}


mock_request = MockRequest()


@patch("gobapi.auth.auth_query.super", MagicMock)
class TestAuthorizedQuery(TestCase):

    def test_create(self):
        q = AuthorizedQuery()
        self.assertIsNone(q._authority)

    def test_set_catalog_collection(self):
        q = AuthorizedQuery()
        q.set_catalog_collection("any catalog", "any collection")
        self.assertEqual(q._authority._catalog, "any catalog")
        self.assertEqual(q._authority._collection, "any collection")
        self.assertEqual(q._authority._auth_scheme, GOB_AUTH_SCHEME)

    def test_get_roles(self):
        mock_req = MagicMock()
        delattr(mock_req, 'roles')

        with patch("gobapi.auth.auth_query.request", mock_req):
            q = AuthorizedQuery()
            q.set_catalog_collection('any catalog', 'any collection')
            self.assertEqual([], q._authority.get_roles())

            mock_req.roles = ['role1', 'role2']
            self.assertEqual(['role1', 'role2'], q._authority.get_roles())

    @patch("gobapi.auth.auth_query.request", mock_request)
    @patch("gobapi.auth.auth_query.GOB_AUTH_SCHEME", mock_scheme)
    def test_get_suppressed_columns(self):
        q = AuthorizedQuery()
        q.set_catalog_collection("any catalog", "any collection")

        q._authority.get_roles = lambda: [role_a]
        self.assertEqual(q._authority.get_suppressed_columns(), [])

        q._authority.get_roles = lambda: [role_b]
        self.assertEqual(q._authority.get_suppressed_columns(), [])

        q._authority.get_roles = lambda: [role_c]
        self.assertEqual(q._authority.get_suppressed_columns(), ['any attribute'])

        q._authority.get_roles = lambda: [role_a]

        q.set_catalog_collection("some other catalog", "any collection")
        self.assertEqual(q._authority.get_suppressed_columns(), [])

        q.set_catalog_collection("any catalog", "some other collection")
        self.assertEqual(q._authority.get_suppressed_columns(), [])

        q.set_catalog_collection("secure catalog collection", "secure collection")
        q._authority.get_roles = lambda: [role_a]
        q._authority._attributes = 'all attributes'
        self.assertEqual(q._authority.get_suppressed_columns(), [])

        q.set_catalog_collection("secure catalog collection", "secure collection")
        q._authority.get_roles = lambda: []
        q._authority._attributes = 'all attributes'
        self.assertEqual(q._authority.get_suppressed_columns(), 'all attributes')

    @patch("gobapi.auth.auth_query.Authority")
    def test__handle_secure_columns(self, mock_authority):
        mock_authority.exposed_value.return_value = 'exposed value'

        entity = None
        _handle_secure_columns(entity, {})
        self.assertEqual(entity, None)

        class Entity:
            def __init__(self):
                self.col1 = 'value1'
                self.col2 = 'value2'

        entity = Entity()
        _handle_secure_columns(entity, {'col1': 'info1'})
        self.assertEqual(entity.col1, 'exposed value')
        self.assertEqual(entity.col2, 'value2')

        # Do not crash on unknown columns
        _handle_secure_columns(entity, {'col1': 'info1', 'unknown col': 'unknown value'})
        self.assertEqual(entity.col1, 'exposed value')
        self.assertEqual(entity.col2, 'value2')


class TestAuthorizedQueryIter(TestCase):

    @patch("gobapi.auth.auth_query.super")
    def test_iter(self, mock_super):
        mock_super.session = MagicMock()
        mock_super.return_value = iter([MockEntity(), MockEntity()])

        q = AuthorizedQuery()
        q._authority = MagicMock()
        q._authority.get_suppressed_columns = lambda: ["a", "b", "some other col"]
        q.session = MagicMock()

        for result in q:
            self.assertIsNone(result.a)
            self.assertIsNone(result.b)
            self.assertFalse(hasattr(result, "some other col"))
            self.assertIsNotNone(result.c)

        # Do not fail on set suppressed columns
        set_suppressed_columns(None, ["a"])

        mock_super.return_value = iter([(MockEntity(),), (MockEntity(),)])
        q = AuthorizedQuery()
        q._authority = mock.MagicMock()
        q._authority.get_suppressed_columns = lambda: ["a", "b", "some other col"]
        q.session = MagicMock()

        for result in q:
            self.assertIsNone(result[0].a)
            self.assertIsNone(result[0].b)
            self.assertFalse(hasattr(result[0], "some other col"))
            self.assertIsNotNone(result[0].c)

    @patch("gobapi.auth.auth_query.super")
    def test_iter_expire_per(self, mock_super):
        mock_super.session = MagicMock()
        mock_super.return_value = iter([MockEntity(), MockEntity()])

        q = AuthorizedQuery()
        q._authority = MagicMock()
        q._authority.get_suppressed_columns = lambda: ["a", "b", "some other col"]
        q.session = MagicMock()
        q.expire_per(1)

        for _ in q:
            continue

        # assert expire_all is called every iteration + once at the end
        self.assertEqual(q.session.expire_all.call_count, 3)

    @patch("gobapi.auth.auth_query.super")
    def test_iter_unauthorized(self, mock_super):
        mock_super.return_value = iter([MockEntity(), MockEntity()])
        q = AuthorizedQuery()
        q.session = MagicMock()

        for result in q:
            for attr in ["a", "b", "c"]:
                self.assertTrue(hasattr(result, attr))


class TestAuthority(TestCase):

    def test_create(self):
        authority = Authority('cat', 'col')
        self.assertEqual(authority._catalog, 'cat')
        self.assertEqual(authority._collection, 'col')
        self.assertEqual(authority._auth_scheme, GOB_AUTH_SCHEME)

    @patch("gobapi.auth.auth_query.request", mock_request)
    def test_filter_row(self):
        authority = Authority('cat', 'col')
        authority.get_suppressed_columns = lambda: ['b', 'd']
        row = {'a': 1, 'b': 2, 'c': 3}
        authority.filter_row(row)
        self.assertEqual(row, {'a': 1, 'b': None, 'c': 3})

        authority.allows_access = lambda: False
        row = {'a': 1, 'b': 2, 'c': 3}
        authority.filter_row(row)
        self.assertEqual(row, {'a': None, 'b': None, 'c': None})

    @patch("gobapi.auth.auth_query.User")
    def test_secured_value(self, mock_user):
        mock_request = MagicMock()
        with patch("gobapi.auth.auth_query.request", mock_request):

            authority = Authority('cat', 'col')
            mock_user.return_value = "any user"
            mock_secure_type = mock.MagicMock()
            result = authority.get_secured_value(mock_secure_type)
            mock_user.assert_called_with(mock_request)
            mock_secure_type.get_value.assert_called_with("any user")

    @patch("gobapi.auth.auth_query.GOB_AUTH_SCHEME", mock_scheme)
    def test_is_secured(self):
        testcases = [
            ('any catalog', 'any collection', True),
            ('secure catalog', 'any collection', True),
            ('any catalog', 'some other collection', False),
            ('open catalog', 'collection', False),
        ]

        for cat, coll, result in testcases:
            authority = Authority(cat, coll)
            self.assertEqual(result, authority.is_secured())

    @patch("gobapi.auth.auth_query.request", mock_request)
    @patch("gobapi.auth.auth_query.GOB_AUTH_SCHEME", mock_scheme)
    def test_allows_access(self):
        authority = Authority('secure catalog', 'any col')
        authority.get_roles = lambda : []
        self.assertFalse(authority.allows_access())

        authority.get_roles = lambda : [role_b]
        self.assertTrue(authority.allows_access())

        authority._catalog = "secure catalog collection"
        authority._collection = "secure collection"
        authority.get_roles = lambda : []
        self.assertFalse(authority.allows_access())

        authority.get_roles = lambda : [role_b]
        self.assertTrue(authority.allows_access())

        authority._collection = "any collection"
        authority.get_roles = lambda : []
        self.assertTrue(authority.allows_access())

    @patch("gobapi.auth.auth_query.gob_model")
    @patch("gobapi.auth.auth_query.get_gob_type_from_info", lambda spec: gob_secure_types.SecureString)
    def test_get_secured_columns(self, mock_model):
        mock_model.__getitem__.return_value = {
            'collections': {
                'any col': {
                    'fields': {'secure column': 'any spec'}
                }
            }
        }

        authority = Authority('secure catalog', 'any col')
        secure_columns = authority.get_secured_columns()
        self.assertEqual(
            secure_columns,
            {'secure column': {'gob_type': gob_secure_types.SecureString, 'spec': 'any spec'}})

        authority = Authority('secure catalog', 'missing col')
        secure_columns = authority.get_secured_columns()
        self.assertEqual(secure_columns, {})

    @patch("gobapi.auth.auth_query.gob_model")
    def test_get_secured_json_columns(self, mock_model):
        mock_model.__getitem__.return_value = {
            'collections': {
                'any col': {
                    'fields': {
                        'secure column': {
                            'type': 'GOB.JSON',
                            'attributes': {
                                'attr1': {
                                    'type': 'GOB.SecureString'
                                },
                                'attr2': {
                                    'type': 'GOB.String'
                                }
                            }
                        }
                    }
                }
            }
        }
        authority = Authority('secure catalog', 'any col')
        secure_columns = authority.get_secured_columns()
        expect = {
            'secure column': {
                'gob_type': gob_types.JSON,
                'spec': {
                    'type': 'GOB.JSON',
                    'gob_type': gob_types.JSON,
                    'attributes': {
                        'attr1': {
                            'type': 'GOB.SecureString',
                            'gob_type': gob_secure_types.SecureString
                        },
                        'attr2': {
                            'type': 'GOB.String',
                            'gob_type': gob_types.String
                        }
                    },
                }
            }
        }
        print(secure_columns)
        self.assertEqual(secure_columns, expect)

    def test_is_secure_type(self):
        authority = Authority('secure catalog', 'any col')

        spec = {
            "type": "GOB.String"
        }
        self.assertFalse(authority.is_secure_type(spec))

        spec = {
            "type": "GOB.SecureString"
        }
        self.assertTrue(authority.is_secure_type(spec))

        spec = {
            "type": "GOB.JSON",
            "attributes": {
                "attr": {
                    "type": "GOB.String"
                }
            }
        }
        self.assertFalse(authority.is_secure_type(spec))

        spec = {
            "type": "GOB.JSON",
            "attributes": {
                "attr": {
                    "type": "GOB.SecureString"
                }
            }
        }
        self.assertTrue(authority.is_secure_type(spec))

    def test_handle_secured_columns(self):
        authority = Authority('secure catalog', 'any col')
        authority.get_secured_columns = lambda : {'col': 'any info'}
        authority.exposed_value = lambda value, info: 'exposed value'

        row = {}
        authority._handle_secured_columns({}, row)
        self.assertEqual(row, {})

        row = {'col': 'any value', 'any other col': 'any value'}
        authority._handle_secured_columns({}, row)
        self.assertEqual(row, {'col': 'exposed value', 'any other col': 'any value'})

        row = {'mapped col': 'any value', 'any other col': 'any value'}
        mapping = {'col': 'mapped col'}
        authority._handle_secured_columns(mapping, row)
        self.assertEqual(row, {'mapped col': 'exposed value', 'any other col': 'any value'})

    @patch("gobapi.auth.auth_query.User", MagicMock())
    def test_exposed_value(self):
        mock_type = MagicMock()
        mock_type.get_value = lambda user: 'protected value'
        mock_type.from_value_secure = lambda value, spec: mock_type
        info = {
            'gob_type': mock_type,
            'spec': 'any spec'
        }
        value = Authority.exposed_value('any value', info)
        self.assertEqual(value, 'protected value')

        value = Authority.exposed_value(None, info)
        self.assertEqual(value, None)

    def test_get_secure_type(self):
        mock_gob_type = mock.MagicMock()
        mock_gob_type.from_value_secure.return_value = "secure GOB type"

        result = Authority.get_secure_type(mock_gob_type, 'any spec', 'any value')
        self.assertEqual(result, "secure GOB type")
        mock_gob_type.from_value_secure.assert_called_with('any value', 'any spec')
