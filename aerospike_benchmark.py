
from __future__ import print_function

import sys
import json
import random
import time
import aerospike

from benchmark_driver import BenchmarkDriver


keys = []
keys.append('d084b15b-7229-486f-a808-b28f3600902b')
keys.append('cb23e4d9-6e73-403a-95dd-2bb30fd56457')
keys.append('0c0a73e9-0f2c-4df1-a4a6-e3edbbb17815')
keys.append('ae9aaebe-8247-4a57-8ba6-c9e9dfea9ee8')
keys.append('9da02eac-bbcf-4110-a24f-72ef999c9afe')
keys.append('65979f7e-8c43-46b6-9693-82074821eeef')


class AerospikeBenchmark(BenchmarkDriver):

    def __init__(self, client, readers_count, writers_count):
        super(AerospikeBenchmark, self).__init__(readers_count, writers_count)
        self.client = client


    def exec_read_from_db(self):
        self.client.get(self.get_key())


    def exec_write_to_db(self, profile_data):
        key = ('test', 'profiles', str(profile_data['id'])) 
        self.client.put(key, profile_data)


    def get_key(self):
        return ('test', 'profiles', keys[random.randint(0, 5)])



def main():
    print('Testing Aerospike Database')
    
    config = {
        'hosts': [
            ('aerospike', 3000)
        ],
        'policies': {
            'timeout': 1000
        }
    }

    # Waiting for Aerospike database to initialize... 
    connect_success = False
    max_attempts = 15
    attempts = 0
    
    while (not connect_success) and (attempts < max_attempts):
        print('Waiting for Aerospike to init, attempt #' + str(attempts+1))
        try:
            client = aerospike.client(config)
            client.connect()
            connect_success = True
        except Exception as e:
            last_error = e
            time.sleep(5)
            
        attempts += 1

    if not connect_success:
        print('Failed to connect to Aerospike, error: {0}'.format(last_error), file=sys.stderr)
        exit(1)

    time.sleep(10)

    print('Connection to Aerospike established.')

    client = aerospike.client(config).connect()
    try:
        benchmark = AerospikeBenchmark(client, 10, 10)
    
        benchmark.run()
    finally:
        client.close()


if __name__ == '__main__':
    main()