import json
from typing import Optional

from flask import request, jsonify
from sqlalchemy.sql import text

from gobapi.graphql_streaming.graphql2sql.graphql2sql import (
    GraphQL2SQL,
    NoAccessException, InvalidQueryException)
from gobapi.graphql_streaming.response_custom import \
    GraphQLCustomStreamingResponseBuilder
from gobapi.logger import get_logger
from gobapi.session import get_session
from gobapi.utils import get_request_id
from gobapi.worker.response import WorkerResponse

logger = get_logger(__name__)


class GraphQLStreamingApi:
    """Returns data on a long living open connection."""

    def _get_query(self) -> Optional[str]:
        query = request.args.get('query')
        if query:
            return query

        if request.data:
            # Compatible with existing GOB export code
            request_data = json.loads(request.data.decode('utf-8'))
            return request_data['query']

        return None

    def entrypoint(self):
        query = self._get_query()
        if not query:
            logger.warning("No query passed in")
            return jsonify({'error': str("no query given")}), 400

        logger.info(f"Running GraphQL for {get_request_id()}: {query}")
        graphql2sql = GraphQL2SQL(query)
        try:
            sql = graphql2sql.sql()
        except NoAccessException:
            return jsonify({'error': 'Forbidden'}), 403
        except InvalidQueryException as e:
            return jsonify({'error': str(e)}), 400
        session = get_session()
        # use an ad-hoc Connection and stream results (instead of pre-buffered)
        result_rows = session.connection().execution_options(stream_results=True).execute(text(sql))

        response_builder = \
            GraphQLCustomStreamingResponseBuilder(result_rows,
                                                  graphql2sql.relations_hierarchy,
                                                  graphql2sql.selections,
                                                  request_args=request.args)

        return WorkerResponse.stream_with_context(response_builder, mimetype='application/x-ndjson')
