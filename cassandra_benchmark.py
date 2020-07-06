from __future__ import print_function
import json
import time
import sys

import cassandra
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from benchmark_driver import BenchmarkDriver


def create_schema(session):
    session.execute("CREATE KEYSPACE IF NOT EXISTS benchmark WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1' }")
    session.set_keyspace('benchmark')
    session.execute(('CREATE TABLE IF NOT EXISTS profiles (id uuid, first_name text, last_name text, gender text, company text, email text, phone text,' 
                            'street text, city text, state text, zip smallint, PRIMARY KEY (id, first_name, last_name, email, gender))'))


class CassandraBenchmark(BenchmarkDriver):

    def __init__(self, session, readers_count, writers_count):
        super(CassandraBenchmark, self).__init__(readers_count, writers_count)
        self.session = session
        self.insert_stmt = self.session.prepare("INSERT INTO profiles JSON ?")


    def exec_read_from_db(self):
        self.session.execute(self.get_query())    


    def get_query(self):
        return "SELECT id, first_name, last_name FROM profiles WHERE id = 78501211-5e55-4e58-b152-a4e1f0f6fece"


    def exec_write_to_db(self, profile_data):
        self.session.execute(self.insert_stmt, [json.dumps(profile_data)])



def main():
    print('Testing Apache Cassandra ' + cassandra.__version__)
    
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')

    # Waiting for cassandra database to initialize... 
    connect_success = False
    max_attempts = 15
    attempts = 0
    
    while (not connect_success) and (attempts < max_attempts):
        print('Waiting for Cassandra to init, attempt #' + str(attempts+1))
        try:
            cluster = Cluster(['cassandra'], port=9042, auth_provider=auth_provider)
            session = cluster.connect()
            connect_success = True
        except Exception as e:
            last_error = e
            time.sleep(5)
            
        attempts += 1

    if not connect_success:
        print('Failed to connect to Cassandra, error: {0}'.format(last_error), file=sys.stderr)
        exit(1)

    print('Connection to Cassandra established.')

    create_schema(session)

    benchmark = CassandraBenchmark(session, 10, 10)
    
    benchmark.run()


if __name__ == '__main__':
    main()