# cassandra-vs-aerospike-benchmark
Small benchmark to compare read/write performance of Cassandra and Aerospike Databases

## Benchmark Summary

In this benchmark I tested 100K reads and 100K writes of user profiles. Operations were done concurrently by 10 reader threads and 10 writer threads.
Meausurement were done with a single node for both databases, however this benchmark can be extended to add more nodes to the cluster, and perform more operations.

In the end of the benchmark execution, a score will be presented in meanse of read/write latency (in microseconds) and throughput (in operations per second).

## Results

|        Database         |         Read Results          |         Write Results         |
| ----------------------- | ----------------------------- | ----------------------------- |
|                         | Latency[us] | Throughput[OPS] | Latency[us] | Throughput[OPS] |
| ----------------------- | ----------- | --------------- | ----------- | --------------- |
| Aerospike 5.0.0.7       |   1099.06   |     8966.75     |   1098.12   |     8873.31     |
| ----------------------- | ----------- | --------------- | ----------- | --------------- | 
| Apache Cassandra 3.24.0 |   9939.06   |     1003.64     |   7629.58   |     1303.78     |
| ----------------------- | ----------- | --------------- | ----------- | --------------- | 
|       Result            | x9.04 to AS |   x8.93 to AS   | x6.95 to AS |    x6.8 to AS   |
| ----------------------- | ----------- | --------------- | ----------- | --------------- | 


## Requirements

Docker and Docker Compose are required to run this benchmark