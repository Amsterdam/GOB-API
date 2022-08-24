#!/bin/bash

docker-compose exec test_db pg_dump --schema-only -U gobtest -d gobtest
