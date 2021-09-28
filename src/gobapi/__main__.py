"""__main__

This module is the main module for the API server.

On startup the api is instantiated.

"""
import os
from uuid import uuid4
from flask import request
from gobapi.api import get_app

app = get_app()


@app.before_request
def set_request_id():
    """Set a request id to be able to group logging in a request.

    Responses may also include this request id in the header.
    """
    request.request_id = uuid4()  # pragma: no cover


app.run(port=os.getenv("GOB_API_PORT", 8141))
