# Database container
This database container is used when running tests.
On initialisation, it will:
1. Initialise the GOB database schema (`init/schema.sql`)
2. Initialise the data (`init/initdata.sh`) from the files in `fixtures/`
3. Initialise (refresh) the materialized views (`init/refresh-materialized-views.sql`)


## Update schema (`dumpschema.sh`)
The file `init/schema.sql` contains the database schema that is initialised on first startup of the container. When
the schema is updated, run the following command to update the schema definition in `schema.sql`. Make sure the
database container (`test_db`) is running.

```bash
sh utils/dumpschema.sh > init/schema.sql
```

## Apply alembic migrations to test database (`refresh-materialized-views.sql`)
In a fully running GOB environment, GOB-Upload is responsible for handling database migrations. This means that
sometimes we need to update the database schema in the test database as well. To do this, make sure the `test_db`
container is running and run:

```bash
sh utils/alembic-migrations.sh
```

Note: Make sure you have GOB-Upload checked out locally at the same level as GOB-API (as any development installation
should have).

After having applied the alembic migrations to the running container, use the `dumpschema.sh` script (see above) to
update the schema definition that is used to initialise the container on a fresh run. Also, update the alembic version
in the `fixtures/alembic_version.csv` fixture.

## Initialising data
The data in `fixtures/` is automatically imported when a new instance of the database container is created. File names
in the `fixtures` directory should match the table name.

To add new fixtures, create the new CSV fixture file with the Postgres COPY command with 'csv header' arguments from
the source database (e.g. your local running GOB database). For example:

```bash
# From running gob database container, export first 5 lines. Change the SELECT query as you wish
psql -U gob -d gob -c "COPY (SELECT * FROM nap_peilmerken ORDER BY _gobid LIMIT 5) TO '/tmp/nap_peilmerken.csv' csv header"
```

Move the resulting data to the `fixtures` directory and that's it. This data will now be imported when the container
is initialised for the first time again.

Note: When structural changes occur in the GOB database schema, the existing fixtures may not be valid anymore. We
could use the same psql export command above to export the migrated data to CSV. Just make sure the data is first
imported, then run the alembic migrations and replace the fixtures files with the newly exported data. It may prove
useful to write a script for that if that time comes.
