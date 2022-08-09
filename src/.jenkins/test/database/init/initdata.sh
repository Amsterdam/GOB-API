#!/bin/sh

set -e
set -u

FIXTURES_DIR=/fixtures
FILES=$(ls $FIXTURES_DIR)

for f in $FILES
do
  FILEPATH=$FIXTURES_DIR/$f
  TABLENAME="$(basename $FILEPATH .csv)"

  echo "Loading fixture for $TABLENAME"
  psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\copy $TABLENAME FROM '$FILEPATH' csv header"
done
