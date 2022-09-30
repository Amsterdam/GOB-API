from unittest import TestCase, mock

from gobapi.graphql_streaming.utils import resolve_schema_collection_name


class TestUtils(TestCase):

    @mock.patch('gobapi.graphql_streaming.utils.gob_model', spec_set=True)
    def test_resolve_schema_collection_name(self, mock_model):
        data = {}
        mock_model.get.side_effect = data.get
        result = resolve_schema_collection_name("catalogCollection")
        mock_model.get.assert_called_with('catalog')
        self.assertEqual(result, (None, None))

        data = {'catalog': {'collections': {}}}
        mock_model.get.side_effect = data.get
        mock_model.__getitem__.side_effect = data.__getitem__
        result = resolve_schema_collection_name("catalogCollection")
        mock_model.__getitem__.assert_called_with('catalog')
        self.assertEqual(result, (None, None))

        data = {'catalog': {'collections': {'collection': {'attributes': {}}}}}
        mock_model.get.side_effect = data.get
        mock_model.__getitem__.side_effect = data.__getitem__
        result = resolve_schema_collection_name("catalogCollection")
        mock_model.__getitem__.assert_called_with('catalog')
        self.assertEqual(result, ('catalog', 'collection'))

        data = {'catalog_ext': {'collections': {'collection': {'attributes': {}}}}}
        mock_model.get.side_effect = data.get
        mock_model.__getitem__.side_effect = data.__getitem__
        result = resolve_schema_collection_name("catalogExtCollection")
        mock_model.__getitem__.assert_called_with('catalog_ext')
        self.assertEqual(result, ('catalog_ext', 'collection'))

        data = {'catalog': {'collections': {'ext_collection': {'attributes': {}}}}}
        mock_model.get.side_effect = data.get
        mock_model.__getitem__.side_effect = data.__getitem__
        result = resolve_schema_collection_name("catalogExtCollection")
        mock_model.__getitem__.assert_called_with('catalog')
        self.assertEqual(result, ('catalog', 'ext_collection'))
