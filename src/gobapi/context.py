"""Module which sets and gets request context.

If required, other app context related stuff should be added here as well.

There is no coverage for this, as it requires a properly setup app-mock, which
is not available unfortunately.
"""
from typing import Optional
from uuid import uuid4

from flask import request, Response


def get_request_id() -> Optional[str]:  # pragma: no cover
    """Get the request_id from the request object, if available.

    The request_id object should be set by 'set_request_id' which is registered by app.before_request.
    """
    return getattr(request, "request_id", None)


def set_request_id() -> None:  # pragma: no cover
    """Set a request id to be able to group logging in a request.

    Responses may also include this request id in the header.
    """
    request.request_id = uuid4()


def set_request_id_header(response: Response) -> Response:  # pragma: no cover
    response.headers["X-Request-ID"] = get_request_id()
    return response
