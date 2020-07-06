
import glob
import threading
import json

from abc import abstractmethod, ABCMeta
from results import Results

class BenchmarkDriver(object):

    __metaclass__ = ABCMeta

    def __init__(self, readers_count, writers_count):
        self.readers_count = readers_count
        self.writers_count = writers_count

    
    def get_readers_count(self):
        return self.readers_count


    def read(self, results, thread_id):
        print('Thread ' + thread_id + ' is querying profiles...')

        for i in range(0, 10000):
            start_time = results.get_time_micro()
            try:
                self.exec_read_from_db()
                results.operation_finished(results.get_time_micro() - start_time)
            except Exception as e:
                print('Read error: {0}'.format(e))    
    
        results.thread_finished()
        print('Thread ' + thread_id + ' finished.')   


    def write(self, results, profile_files, thread_id):

        for profiles_json in profile_files:
            print('Thread ' + thread_id + ' is inserting profiles from ' + profiles_json)
            with open(profiles_json) as mf:
                profiles = json.load(mf)

            for prof in profiles:
                start_time = results.get_time_micro()

                try:
                    self.exec_write_to_db(prof)
                    results.operation_finished(results.get_time_micro() - start_time)
                except Exception as e:
                    print('Write error: {0}'.format(e))

            print('Thread ' + thread_id + ' completed inserting profiles from ' + profiles_json)

        results.thread_finished()
        print('Thread ' + thread_id + ' finished.') 

    
    @abstractmethod
    def exec_read_from_db(self):
        pass


    @abstractmethod
    def exec_write_to_db(self, profile_data):
        pass

   
    def run(self):
        profile_files = glob.glob('profiles/*.json')
        max_profile_files = len(profile_files)

        if (self.writers_count > max_profile_files):
            self.writers_count = max_profile_files
         
        writer_threads = []
        write_results = Results(self.writers_count)  

        start_index = 0 

        for i in range(self.writers_count):
            slice = []
            slice_size = min(int(max_profile_files / self.writers_count), max_profile_files - i)

            for j in range(start_index, start_index + slice_size):
                slice.append(profile_files[j])                              

            start_index += slice_size
            thread = threading.Thread(target=self.write, args=(write_results, slice, 'writer-' + str(i)))
            thread.start()
            writer_threads.append(thread)
    
        for i in range(self.writers_count):
            writer_threads[i].join()

        print('####   Write Benchmark Completed   ####')
        print('Results:')
        print('Write Latency: {:.2f} us'.format(write_results.get_latency()))
        print('Write Throughput: {:.2f} Ops/Sec'.format(write_results.get_throughput()))

        reader_threads = []
        read_results = Results(self.get_readers_count())

        for i in range(self.get_readers_count()):
            thread = threading.Thread(target=self.read, args=(read_results, 'reader-' + str(i)))
            thread.start()
            reader_threads.append(thread)

        for i in range(self.get_readers_count()):
            reader_threads[i].join()

        print('####   Read Benchmark Completed   ####')
        print('Results:')
        print('Read Latency: {:.2f} us'.format(read_results.get_latency()))
        print('Read Throughput: {:.2f} Ops/Sec'.format(read_results.get_throughput()))

        print('Finished.')





