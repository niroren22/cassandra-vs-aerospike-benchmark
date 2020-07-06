#!/bin/bash

docker-compose cassandra-benchmark.yml -t cassandra-benchmark:latest build

docker-compose cassandra-benchmark:latest up