import json

from unittest import TestCase
from unittest.mock import patch, MagicMock

from gobapi.graphql_streaming.api import GraphQLStreamingApi, NoAccessException, InvalidQueryException


@patch("gobapi.graphql_streaming.api.WorkerResponse.stream_with_context", lambda f, mimetype: f)
class TestGraphQLStreamingApi(TestCase):

    def setUp(self) -> None:
        self.api = GraphQLStreamingApi()

    @patch("gobapi.graphql_streaming.api.get_session")
    @patch("gobapi.graphql_streaming.api.GraphQL2SQL")
    @patch("gobapi.graphql_streaming.api.GraphQLCustomStreamingResponseBuilder")
    @patch("gobapi.graphql_streaming.api.text", lambda x: 'text_' + x)
    def test_entrypoint(self, mock_response_builder, mock_graphql2sql, mock_get_session):
        mock_request = MagicMock()
        mock_request.data.decode.return_value = '{"query": "some query"}'
        mock_request.args.get.return_value = ''
        graphql2sql_instance = mock_graphql2sql.return_value
        graphql2sql_instance.sql.return_value = 'parsed query'

        with patch("gobapi.graphql_streaming.api.request", mock_request):
            result = self.api.entrypoint()
            mock_graphql2sql.assert_called_with("some query")
            mock_get_session.return_value.connection.assert_called()
            mock_get_session.return_value.connection.return_value.execution_options.assert_called_with(stream_results=True)
            execute = mock_get_session.return_value.connection.return_value.execution_options.return_value.execute
            execute.assert_called_with('text_parsed query')
            mock_response_builder.assert_called_with(execute.return_value,
                                                     graphql2sql_instance.relations_hierarchy,
                                                     graphql2sql_instance.selections,
                                                     request_args=mock_request.args)
            self.assertEqual(result, mock_response_builder.return_value)

    @patch("gobapi.graphql_streaming.api.jsonify", lambda x: json.dumps(x))
    @patch("gobapi.graphql_streaming.api.GraphQL2SQL")
    @patch("gobapi.graphql_streaming.api.text", lambda x: 'text_' + x)
    def test_entrypoint_no_access(self, mock_graphql2sql):
        mock_request = MagicMock()

        def no_access():
            raise NoAccessException

        def invalid_query():
            raise InvalidQueryException("Some error message")

        with patch("gobapi.graphql_streaming.api.request", mock_request):
            mock_request.data.decode.return_value = '{"query": "some query"}'
            mock_request.args.get.return_value = None
            graphql2sql_instance = mock_graphql2sql.return_value
            graphql2sql_instance.sql = no_access

            result = self.api.entrypoint()
            self.assertEqual(result, ('{"error": "Forbidden"}', 403))

            graphql2sql_instance.sql = invalid_query

            result = self.api.entrypoint()
            self.assertEqual(result, ('{"error": "Some error message"}', 400))

