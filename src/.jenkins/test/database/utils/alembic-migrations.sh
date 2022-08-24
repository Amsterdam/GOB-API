#!/bin/bash

docker-compose -f ../docker-compose.yml -f ../docker-compose.migrate.yml build
docker-compose -f ../docker-compose.yml -f ../docker-compose.migrate.yml run --rm migrate
