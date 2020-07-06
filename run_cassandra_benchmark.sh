#!/bin/bash

docker-compose -f cassandra-benchmark.yml build

docker-compose -f cassandra-benchmark.yml up