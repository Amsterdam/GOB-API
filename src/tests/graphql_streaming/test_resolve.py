from unittest import TestCase, mock

from gobapi.graphql_streaming.resolve import Resolver


class TestResolve(TestCase):

    def testResolver(self):
        resolver = Resolver()
        self.assertIsNotNone(resolver)
        self.assertEqual(resolver._attributes, {})

    @mock.patch('gobapi.graphql_streaming.resolve.Authority', spec_set=True)
    @mock.patch('gobapi.graphql_streaming.resolve.gob_model', spec_set=True)
    @mock.patch('gobapi.graphql_streaming.resolve._SEC_TYPES', ['GOB.SecureString', 'GOB.SecureDateTime'])
    def testResolverWithAttributes(self, mock_model, mock_authority_class):
        mock_authority = mock.MagicMock()
        mock_authority.get_secured_value.return_value = "resolved value"
        mock_authority_class.return_value = mock_authority
        attributes = {
            'attributes': {
                'a_b': {
                    'type': 'GOB.SecureString'
                },
                'c_d': {
                    'type': 'GOB.SecureDateTime'
                },
                'e_f': {
                    'type': 'some type'
                }
            }
        }
        mock_model.__getitem__.return_value = {
            'collections': {'col': attributes}
        }
        resolver = Resolver()
        row = {
            '_catalog': 'cat',
            '_collection': 'col',
            'aB': 'aB value',
            'cD': 'cD value',
            'eF': 'eF value',
            'attr': 'value'
        }
        result = {}

        resolver.resolve_row(row, result)
        mock_authority_class.assert_called_with('cat', 'col')
        self.assertEqual(mock_authority.filter_row.call_count, 2)  # for row and for result
        mock_model.__getitem__.assert_called_with('cat')
        self.assertEqual(
            resolver._attributes, {'cat': {'col': {'a_b': 'aB', 'c_d': 'cD', 'e_f': 'eF'}}})

    @mock.patch('gobapi.graphql_streaming.resolve.gob_model', spec_set=True)
    def test_init_catalog_collection(self, mock_model):
        attributes = {
            'attributes': {
                'a_b': 1,
                'b_c': 2
            }
        }
        mock_model.__getitem__.return_value = {
            'collections': {'col': attributes}
        }

        resolver = Resolver()
        resolver._init_catalog_collection(None, None)
        self.assertEqual(resolver._attributes, {None: {None: {}}})

        resolver = Resolver()
        resolver._init_catalog_collection('cat', 'col')
        self.assertEqual(resolver._attributes, {'cat': {'col': {'a_b': 'aB', 'b_c': 'bC'}}})

        resolver._init_catalog_collection('cat', 'col')
        self.assertEqual(resolver._attributes, {'cat': {'col': {'a_b': 'aB', 'b_c': 'bC'}}})

        resolver._init_catalog_collection('cat', None)
        self.assertEqual(resolver._attributes, {'cat': {None: {}, 'col': {'a_b': 'aB', 'b_c': 'bC'}}})
