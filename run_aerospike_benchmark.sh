#!/bin/bash

docker-compose -f aerospike-benchmark.yml build

docker-compose -f aerospike-benchmark.yml up