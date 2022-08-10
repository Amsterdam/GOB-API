#!/bin/sh
# wait-for-postgres.sh

set -e

host="$1"
shift

max=60
current=0

until PGPASSWORD=$DATABASE_PASSWORD psql -h "$host" -U "$DATABASE_USER" -p $DATABASE_PORT_OVERRIDE -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1

  if [ $((current++)) -ge $max ]; then
    >&2 echo "Timed out waiting for Postgres"
    exit 1
  fi

done

>&2 echo "Postgres is up - executing command"
exec "$@"
