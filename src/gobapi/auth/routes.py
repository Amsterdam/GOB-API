
from flask import request

from gobapi.auth.auth_query import Authority
from gobcore.secure.request import is_secured_request, extract_roles

# Request args that require authorisation
# SECURE_ARGS = ['view']  # view results are not checked for secure data!
SECURE_ARGS = []


def secure_route(rule, func):
    """
    Secure routes start with API_SECURE_BASE_PATH and are protected by OAuth2 Proxy

    The headers that are used to identify the user and/or role should be present

    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        if is_secured_request(request.headers):
            # Access Token is forwarded by OAuth2 Proxy. Keycloak roles are present in access token.
            setattr(request, 'roles', extract_roles(request.headers))

            if _allows_access(rule, *args, **kwargs):
                return func(*args, **kwargs)
        return "Forbidden", 403

    wrapper.__name__ = f"secure_{func.__name__}"
    return wrapper


def _secure_headers_detected(rule, *args, **kwargs):
    """
    Check if any secure headers are present in the request

    :param rule:
    :param args:
    :param kwargs:
    :return:
    """
    return is_secured_request(request.headers)


def _allows_access(rule, *args, **kwargs):
    """
    Check access to paths with variable catalog/collection names
    """
    catalog_name = kwargs.get('catalog_name')
    collection_name = kwargs.get('collection_name')
    return Authority(catalog_name, collection_name).allows_access()


def _allows_args():
    # Check if a secure parameter is present
    return not [arg for arg in SECURE_ARGS if request.args.get(arg) is not None]


def _issue_fraud_warning(rule, *args, **kwargs):
    """
    Issue a fraud warning

    For now this is printed on stdout (to be found in Kibana)

    In the future this should be connected to an alert mechanism
    """
    print(f"ERROR: FRAUD DETECTED FOR RULE: {rule} => {request.url}", args, kwargs)
    dump_attrs = ['method', 'remote_addr', 'remote_user', 'headers']
    for attr in dump_attrs:
        print(attr, getattr(request, attr))


def public_route(rule, func, *args, **kwargs):
    """
    Public routes start with API_BASE_PATH and are not protected by OAuth2 Proxy

    The headers that are used to identify the user and/or role should NOT be present.
    If any of these headers are present that means that these headers are falsified
    The ip-address and any other identifying information should be reported

    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    def wrapper(*args, **kwargs):
        if _secure_headers_detected(rule, *args, **kwargs):
            # Public route cannot contain secure headers
            _issue_fraud_warning(rule, *args, **kwargs)
            return "Bad request", 400
        elif not (_allows_access(rule, *args, **kwargs) and _allows_args()):
            return "Forbidden", 403
        else:
            return func(*args, **kwargs)

    wrapper.__name__ = f"public_{func.__name__}"
    return wrapper
