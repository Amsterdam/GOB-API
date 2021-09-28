"""This module is the main module for the API *development* server.

On startup the api is instantiated.
"""
import os
from gobapi.api import get_app

app = get_app()

app.run(port=os.getenv("GOB_API_PORT", 8141))
