# syntax=docker/dockerfile:1
FROM amsterdam/gob_wheelhouse:3.9-buster as wheelhouse
MAINTAINER datapunt@amsterdam.nl


# Application stage.
FROM amsterdam/gob_baseimage:3.9-buster as application
MAINTAINER datapunt@amsterdam.nl
# GOB base image: SQL Server driver.

# Fill the wheelhouse.
COPY --from=wheelhouse /opt/wheelhouse /opt/wheelhouse

# Install ANTLR for build.sh (GraphQL 2 SQL grammar).
RUN apt-get install -y antlr4

# Install gobapi service in /app folder.
WORKDIR /app

# Install required Python packages.
COPY requirements.txt /app/
RUN LIBGDAL_VERSION=$(gdal-config --version) pip install --no-cache-dir \
	--find-links /opt/wheelhouse --requirement requirements.txt
RUN rm requirements.txt
# Wheelhouse cleanup.
RUN rm -rf /opt/wheelhouse

# Copy gobapi module.
COPY gobapi gobapi

# GraphQL 2 SQL grammar build.
COPY build.sh /app
RUN ./build.sh

# OAuth2 Proxy.
COPY ./oauth2-proxy oauth2-proxy
COPY ./oauth2-proxy.cfg oauth2-proxy.cfg
RUN chmod 755 oauth2-proxy
RUN mkdir -p /var/log/oauth2-proxy && chown datapunt /var/log/oauth2-proxy

USER datapunt
CMD uwsgi


# Development.
FROM application as development
USER root
# Install GOB-Core in development mode. Will be overridden with mounts from the developer filesystem.
# Changes made to GOB-Core and will be available immediately.
RUN git clone --depth=1 https://github.com/Amsterdam/GOB-Core.git
RUN LIBGDAL_VERSION=$(gdal-config --version) pip install -e /app/GOB-Core

USER datapunt


# Test.
FROM application as test
USER root
# Remove gobcore tests
RUN rm -rf /app/src/gobcore/tests

# Copy test module and tests.
COPY .flake8 test.sh .coveragerc pytest.ini ./
COPY tests tests

# Wait for PostgreSQL script.
COPY wait-for-postgres.sh wait-for-postgres.sh
RUN chmod +x wait-for-postgres.sh

# Copy Jenkins files.
COPY .jenkins /.jenkins

RUN mkdir -p /app/shared/message_broker && chown datapunt /app/shared
USER datapunt
