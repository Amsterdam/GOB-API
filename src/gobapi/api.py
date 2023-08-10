"""API.

This module contains the API endpoints.
Endpoints can use storage methods to retrieve data from the GOB Storage.
Responses are created in a uniform way by using the response module.

The endpoints are defined in the ROUTES variable.
The only public method is get_app() which returns a Flask application object.
The API can be started by get_app().run()
"""

from logging.config import dictConfig

from flask_graphql import GraphQLView
from flask import Flask, request, Response
from flask_cors import CORS
from flask_audit_log.middleware import AuditLogMiddleware

from gobcore.model.metadata import FIELD
from gobcore.views import GOBViews

from gobapi import gob_model
from gobapi.legacy_views.legacy_views import get_all_table_renames
from gobapi.middleware import CustomDirectivesMiddleware
from gobapi.context import set_request_id, set_request_id_header

from gobapi.config import API_BASE_PATH, API_SECURE_BASE_PATH, API_LOGGING
from gobapi.fat_file import fat_file
from gobapi.response import hal_response, not_found, get_page_ref, ndjson_entities, stream_entities
from gobapi.dump.csv import CsvDumper
from gobapi.auth.routes import secure_route, public_route

from gobapi.worker.response import WorkerResponse
from gobapi.worker.api import worker_result, worker_status, worker_end

from gobapi.states import get_states
from gobapi.storage import connect, get_entities, get_entity, query_entities, dump_entities, \
    query_reference_entities, clear_test_dbs
from gobapi.dbinfo.api import get_db_info

from gobapi.graphql.schema import schema
from gobapi.session import shutdown_session
from gobapi.graphql_streaming.api import GraphQLStreamingApi


dictConfig(API_LOGGING)


def _catalogs():
    """Returns the GOB catalogs.

    :return: a list of catalogs (name, href)
    """
    result = {
        '_embedded': {
            'catalogs': [
                {
                    'name': catalog_name,
                    'abbreviation': catalog['abbreviation'],
                    'description': catalog['description'],
                    '_links': {
                        'self': {
                            'href': f'{API_BASE_PATH}/{catalog_name}/'
                        }
                    }
                } for catalog_name, catalog in gob_model.items()
            ]
        }
    }
    return hal_response(result)


def _catalog(catalog_name):
    """Return the details of a specific GOB catalog.

    :param catalog_name: e.g. meetbouten
    :return: the details of the specified catalog {name, href}
    """
    catalog = gob_model.get(catalog_name)
    if catalog:
        result = {
            'name': catalog_name,
            'abbreviation': catalog['abbreviation'],
            'description': catalog['description'],
            'version': catalog['version'],
            'collections': list(catalog['collections'].keys()),
            '_embedded': {
                'collections': [
                    {
                        'name': collection_name,
                        'abbreviation': collection['abbreviation'],
                        '_links': {
                            'self': {
                                'href': f'/gob/{catalog_name}/{collection_name}/'
                            }
                        }
                    } for collection_name, collection in gob_model[catalog_name]['collections'].items()
                ]
            }
        }
        return hal_response(result)
    return not_found(f"Catalog {catalog_name} not found")


def _entities(catalog_name, collection_name, page, page_size, view=None):
    """Returns the entities in the specified catalog collection.

    The page and page_size are used to calculate the offset and number of entities to return.

    A result, links tuple is returned.
    Result is an object containing relevant metadata about the result.
    Links contain the references to any next or previous page.

    :param catalog_name: e.g. meetbouten
    :param collection_name: e.g. meting
    :param page: any page number, page numbering starts at 1
    :param page_size: the number of entities per page
    :param view: the database view that's being used to get the entities, defaults to the entity table
    :return: (result, links)
    """
    assert (gob_model.get(catalog_name) and gob_model[catalog_name]['collections'].get(collection_name))
    assert page >= 1
    assert page_size >= 1

    offset = (page - 1) * page_size

    entities, total_count = get_entities(
        catalog_name, collection_name, offset=offset, limit=page_size, view=view)

    if view:
        # For views always show next page unless no results are returned. Count is slow on large views
        num_pages = page + 1 if len(entities) > 0 else page
    else:
        num_pages = (total_count + page_size - 1) // page_size

    return {
               'total_count': total_count,
               'page_size': page_size,
               'pages': num_pages,
               'results': entities
           }, {
               'next': get_page_ref(page + 1, num_pages),
               'previous': get_page_ref(page - 1, num_pages)
           }


def _clear_tests():
    clear_test_dbs()
    return "", 200


def _reference_entities(src_catalog_name, src_collection_name, reference_name, src_id, page, page_size):
    """Returns the entities for a reference with specified source entity.

    The page and page_size are used to calculate the offset and number of entities to return.

    A result, links tuple is returned.
    Result is an object containing relevant metadata about the result.
    Links contain the references to any next or previous page

    :param src_catalog_name: e.g. meetbouten
    :param src_collection_name: e.g. metingen
    :param reference_name: e.g. ligt_in_buurt
    :param src_id: e.g. 1234
    :param page: any page number, page numbering starts at 1
    :param page_size: the number of entities per page
    :return: (result, links)
    """
    assert (gob_model[src_catalog_name]['collections'][
        src_collection_name]['references'].get(reference_name))
    assert page >= 1
    assert page_size >= 1

    offset = (page - 1) * page_size

    entities, total_count = get_entities(src_catalog_name, src_collection_name, offset=offset, limit=page_size,
                                         view=None, reference_name=reference_name, src_id=src_id)

    num_pages = (total_count + page_size - 1) // page_size

    return {
               'total_count': total_count,
               'page_size': page_size,
               'pages': num_pages,
               'results': entities
           }, {
               'next': get_page_ref(page + 1, num_pages),
               'previous': get_page_ref(page - 1, num_pages)
           }


def _get_legacy_collection_name(catalog_name, collection_name):
    """Returns the legacy collection name for given catalog, collection combination.

    The collection_name may already be in 'legacy' format, in which case the collection_name is returned.

    Used for renamed collection names; this happens (currently) only for the rel catalog.
    """
    renamed = [k for k, v in get_all_table_renames().get(catalog_name, {}).items() if v == collection_name]

    if renamed:
        return renamed[0]
    return collection_name


def _dump(catalog_name, collection_name):
    """Dump all entities in the requested format. Currently only csv.

    :param catalog_name:
    :param collection_name:
    :return: Streaming response of all entities in csv format with header
    """
    # Because the dump job only knows the current name in public. Transform to legacy name.
    collection_name = _get_legacy_collection_name(catalog_name, collection_name)

    format = request.args.get('format')
    exclude_deleted = request.args.get('exclude_deleted') == 'true'

    filter = (lambda table: getattr(table, FIELD.DATE_DELETED).is_(None)) if exclude_deleted else None
    entities, model = dump_entities(catalog_name, collection_name, filter=filter)

    if format == "csv":
        result = CsvDumper(entities, model=model)
        return WorkerResponse.stream_with_context(result, mimetype='text/csv')
    return f"Unrecognised format parameter '{format}'" if format else "Format parameter not set", 400


def _collection(catalog_name, collection_name):
    """Returns the list of entities within the specified collection.

    A list of entities is returned. This output is paged, default page 1 page size 100.

    :param catalog_name: e.g. meetbouten
    :param collection_name: e.g. meting
    :return:
    """
    if gob_model.get(catalog_name) and gob_model[catalog_name]['collections'].get(collection_name):
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 100))

        view = request.args.get('view', None)

        stream = request.args.get('stream', None) == "true"
        ndjson = request.args.get('ndjson', None) == "true"

        # If a view is requested and doesn't exist return a 404
        if view and not GOBViews().get_view(catalog_name, collection_name, view):
            return not_found(f'{catalog_name}.{collection_name}?view={view} not found')

        view_name = GOBViews().get_view(catalog_name, collection_name, view)['name'] if view else None

        if stream:
            entities, convert = query_entities(catalog_name, collection_name, view_name)
            result = stream_entities(entities, convert)
            return WorkerResponse.stream_with_context(result, mimetype='application/json')
        if ndjson:
            entities, convert = query_entities(catalog_name, collection_name, view_name)
            result = ndjson_entities(entities, convert)
            return WorkerResponse.stream_with_context(result, mimetype='application/x-ndjson')
        else:
            result, links = _entities(catalog_name, collection_name, page, page_size, view_name)
            return hal_response(data=result, links=links)
    return not_found(f'{catalog_name}.{collection_name} not found')


def _entity(catalog_name, collection_name, entity_id, view=None):
    """Returns the entity within the specified collection with the specified id.

    An individual entity is returned.

    :param catalog_name: e.g. meetbouten
    :param collection_name: e.g. meting
    :param entity_id: unique identifier of the entity
    :param view: the database view that's being used to get the entity, defaults to the entity table
    :return:
    """
    if not gob_model.get(catalog_name):
        return not_found(f'{catalog_name} not found')

    if gob_model[catalog_name]['collections'].get(collection_name):
        view = request.args.get('view', None)

        # If a view is requested and doesn't exist return a 404
        if view and not GOBViews().get_view(catalog_name, collection_name, view):
            return not_found(f'{catalog_name}.{collection_name}?view={view} not found')

        view_name = GOBViews().get_view(catalog_name, collection_name, view)['name'] if view else None

        result = get_entity(catalog_name, collection_name, entity_id, view_name)
        return hal_response(result) if result is not None else not_found(
            f'{catalog_name}.{collection_name}:{entity_id} not found')
    return not_found(f'{catalog_name}.{collection_name} not found')


def _reference_collection(catalog_name, collection_name, entity_id, reference_path):
    """Returns the (very many) references from an entity within the specified collection
    with the specified id.

    An list of references is returned.

    :param catalog_name: e.g. meetbouten
    :param collection_name: e.g. meting
    :param entity_id: unique identifier of the entity
    :param reference: unique identifier of the reference attribute e.g. ligt_in_buurt
    :param view: the database view that's being used to get the entity, defaults to the entity table
    :return:
    """
    if not gob_model.get(catalog_name):
        return not_found(f'{catalog_name} not found')

    collection = gob_model[catalog_name]['collections'].get(collection_name)
    if collection:
        # Get the reference
        reference_name = reference_path.replace('-', '_')
        reference = collection['references'].get(reference_name)
        # Check if the source entity exists
        entity = get_entity(catalog_name, collection_name, entity_id)

        if entity and reference:
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 100))

            stream = request.args.get('stream', None) == "true"
            ndjson = request.args.get('ndjson', None) == "true"

            if stream:
                entities, convert = query_reference_entities(
                    catalog_name, collection_name, reference_name, entity_id)
                return Response(stream_entities(entities, convert), mimetype='application/json')
            if ndjson:
                entities, convert = query_reference_entities(
                    catalog_name, collection_name, reference_name, entity_id)
                return Response(ndjson_entities(entities, convert), mimetype='application/x-ndjson')
            result, links = _reference_entities(
                catalog_name, collection_name, reference_name, entity_id, page, page_size)
            return hal_response(data=result, links=links)

        response = not_found(
                f'{catalog_name}.{collection_name}:{entity_id} not found') if not entity else not_found(
                f'{catalog_name}.{collection_name}:{entity_id}:{reference_name} not found')
        return response
    return not_found(f'{catalog_name}.{collection_name} not found')


def _states():
    """Returns the states for the supplied list of collections.

    All states for a collection with the related collections are returned.
    The list of collections can be passed as an URL parameter:

    ?collections=gebieden:wijken,gebieden:stadsdelen

    :return:
    """
    collection_names = request.args.get('collections')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 100))
    offset = (page - 1) * page_size

    if collection_names:
        collections = []
        for col in collection_names.split(','):
            collections.append(col.split(':'))

        entities, total_count = get_states(collections, offset=offset, limit=page_size)

        num_pages = (total_count + page_size - 1) // page_size

        result = {
            'total_count': total_count,
            'page_size': page_size,
            'pages': num_pages,
            'results': entities
        }
        links = {
            'next': get_page_ref(page + 1, num_pages),
            'previous': get_page_ref(page - 1, num_pages)
            }
        return hal_response(result, links)
    return not_found('No collections requested')


def _health():
    return 'Connectivity OK'


def _add_route(app, paths, rule, view_func, methods):
    """For every rule add a public and a secure endpoint.

    Both the public and the secure endpoints are protected.
    The secure endpoint expects the Keycloak headers to be present and the endpoint is protected by OAuth2 Proxy.
    The public endpoint assures that none of the Keycloak headers is present.

    :param app:
    :param rule:
    :param view_func:
    :param methods:
    :return:
    """
    wrappers = {
        API_BASE_PATH: public_route,
        API_SECURE_BASE_PATH: secure_route
    }
    for path in paths:
        wrapper = wrappers[path]
        wrapped_rule = f"{path}{rule}"
        app.add_url_rule(rule=wrapped_rule, methods=methods, view_func=wrapper(wrapped_rule, view_func))


def get_app():
    """Returns a Flask application object.

    The rules are maintained in the ROUTES variable (Note: By default a rule just listens for GET).

    CORS is used to allow CORS for all domains on all routes.

    :return: a Flask application object
    """
    connect()

    graphql = GraphQLView.as_view(
        'graphql',
        schema=schema,
        middleware=[CustomDirectivesMiddleware()],
        graphiql=True  # for having the GraphiQL interface
    )
    graphql_streaming = GraphQLStreamingApi()

    app = Flask(__name__)
    CORS(app)

    # Exclude all non-secure urls fot the audit log and provide the callable to get the user from the request
    app.config['AUDIT_LOG'] = {
        'EXEMPT_URLS': [fr'^(?!{API_SECURE_BASE_PATH}).+'],
        'LOG_HANDLER_CALLABLE_PATH': 'gobapi.util.audit_log.get_log_handler',
        'USER_FROM_REQUEST_CALLABLE_PATH': 'gobapi.util.audit_log.get_user_from_request',
    }

    # Add the AuditLogMiddleware
    AuditLogMiddleware(app)

    # Health check route
    app.route(rule='/status/health/')(_health)

    # Application routes
    PUBLIC = [API_BASE_PATH, API_SECURE_BASE_PATH]
    # SECURE = [API_SECURE_BASE_PATH]
    ROUTES = [
        (PUBLIC, '/', _catalogs, ['GET']),
        (PUBLIC, '/<catalog_name>/', _catalog, ['GET']),
        (PUBLIC, '/<catalog_name>/<collection_name>/', _collection, ['GET']),
        (PUBLIC, '/<catalog_name>/<collection_name>/<entity_id>/', _entity, ['GET']),
        (PUBLIC, '/<catalog_name>/<collection_name>/<entity_id>/<reference_path>/', _reference_collection, ['GET']),
        (PUBLIC, '/alltests/', _clear_tests, ['DELETE']),
        (PUBLIC, '/toestanden/', _states, ['GET']),
        (PUBLIC, '/graphql/', graphql, ['GET', 'POST']),
        (PUBLIC, '/graphql/streaming/', graphql_streaming.entrypoint, ['POST']),
        (PUBLIC, '/dump/<catalog_name>/<collection_name>/', _dump, ['GET']),
        (PUBLIC, '/worker/<worker_id>', worker_result, ['GET']),
        (PUBLIC, '/worker/end/<worker_id>', worker_end, ['DELETE']),
        (PUBLIC, '/worker/status/<worker_id>', worker_status, ['GET']),
        (PUBLIC, '/fat_file/<gbs>', fat_file, ['GET']),
        (PUBLIC, '/info/<info_type>/', get_db_info, ['GET'])
    ]
    for paths, rule, view_func, methods in ROUTES:
        _add_route(app, paths, rule, view_func, methods)

    app.teardown_appcontext(shutdown_session)

    app.before_request(set_request_id)
    app.after_request(set_request_id_header)

    return app
