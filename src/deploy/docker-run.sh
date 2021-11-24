#!/usr/bin/env bash
set -u   # crash on missing env variables
set -e   # stop on any error
set -x

# Start uWSGI with the GOB application and oauth2-proxy
exec uwsgi
