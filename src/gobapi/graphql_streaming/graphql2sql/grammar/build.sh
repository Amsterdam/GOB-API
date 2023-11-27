#!/bin/bash

ANTLR=${ANTLR_CMD:-antlr4}

${ANTLR} -Dlanguage=Python3 GraphQL.g4 -visitor -no-listener
