#!/bin/bash

docker-compose -f src/.jenkins/test/docker-compose.yml -f src/.jenkins/test/docker-compose.migrate.yml run --rm migrate
