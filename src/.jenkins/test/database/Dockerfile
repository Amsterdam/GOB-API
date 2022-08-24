FROM amsterdam/postgres11

RUN mkdir /fixtures
COPY fixtures /fixtures

# Init scripts. Start with z so that they run after the existing init-extensions script
COPY ./init/schema.sql /docker-entrypoint-initdb.d/z1-schema.sql
COPY ./init/initdata.sh /docker-entrypoint-initdb.d/z2-initdata.sh
COPY ./init/refresh-materialized-views.sql /docker-entrypoint-initdb.d/z3-refresh-materialized-views.sql
