# GOB-API

GOB API provides for a HAL JSON and GraphQL view on the GOB catalogs, collections and entities.

The root endpoint provides for all GOB catalogs.
Every endpoint contains the links to explore the data in more detail.

The endpoints prefixed with `/gob/public` are public, the `/gob` endpoints are protected.

# Requirements

* docker compose >= 1.25
* Docker CE >= 18.09
* Python >= 3.9

# Installation

## Secure data

Secure data in GOB is protected by:
- [OAuth2 Proxy](https://oauth2-proxy.github.io/oauth2-proxy/) (protected access points)
- [Keycloak](https://www.keycloak.org) (authentication)
- authorisation schemes (match Keycloak roles on GOB access)
- encryption (for confidential attributes)

In order to access secure data you need to define environment variables:
- `SECURE_SALT` and `SECURE_PASSWORD`
  - shared with [GOB Import](https://github.com/Amsterdam/GOB-Import) (symmetrical encryption).
    GOB Import is responsable for the encryption and GOB API uses the secrets for decryption
- OAuth2 Proxy configuration
  - `OAUTH2_PROXY_CLIENT_ID`
  - `OAUTH2_PROXY_CLIENT_SECRET`
  - `OAUTH2_PROXY_COOKIE_SECRET`
  - `OAUTH2_PROXY_OIDC_ISSUER_URL`
  - `OAUTH2_PROXY_REDIRECT_URL`

In order to activate OAuth2 Proxy and Keycloak locally see the comments in `docker-compose.yml`.

## Local

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r src/requirements.txt
```

Or activate the previously created virtual environment:

```bash
source venv/bin/activate
```

A running [GOB infrastructure](https://github.com/Amsterdam/GOB-Infra) is required to run this component.

Optional: Set environment if GOB-API should connect to remote data sources:

```bash
export $(cat .env | xargs)  # Copy from .env.example if missing
```

Start the API:

```bash
cd src
python -m gobapi
```

The API is exposed at:
- HAL JSON: http://127.0.0.1:8141/gob/
- GraphQL: http://localhost:8141/gob/graphql/

The IP address of the server is also reported at stdout when starting the API from the command line.

### Streaming output

Instead of having the API compute the result and return it as a whole or in paged format,
data can also be retrieved streaming. This not only limits the memory usage of the API
but also allows for more easy processing of the data.

- Streaming HAL JSON output can be obtained by using `?streaming=true` or `?ndjson=true` as URL parameter.
- Streaming GraphQL output can be obtained by using the endpoint `.../graphql/streaming`.

### Tests

```bash
cd src
sh test.sh
```

## Docker

```bash
docker compose build
docker compose up -d
```

The API is exposed at the same address as for the local installation.

### Tests

```bash
docker compose -f src/.jenkins/test/docker-compose.yml build
docker compose -f src/.jenkins/test/docker-compose.yml run --rm test
```

#### Test database
The API test suit runs a database to test the legacy views. This database is automatically initialised with the test
data.
For information on how to update the data and/or schema in this database, refer to [the database README](src/.jenkins/test/database/README.md).
