
import threading
import time

class Results:

    def __init__(self, num_of_threads):
        self.lock = threading.Lock()
        self.ops_count = 0
        self.total_ops_time = 0
        self.ops_start_time = self.get_time_seconds()
        self.need_to_finish = num_of_threads


    def get_throughput(self):
        return float(self.ops_count / (self.ops_end_time - self.ops_start_time)) if hasattr(self, 'ops_end_time') else 0


    def get_latency(self):
        return float(self.total_ops_time / self.ops_count) if self.ops_count > 0 else 0;        


    def operation_finished(self, time):
        self.lock.acquire()
        try:
            self.total_ops_time += time
            self.ops_count += 1
        finally:
            self.lock.release()

    
    def thread_finished(self):
        self.lock.acquire()
        try:
            self.need_to_finish -= 1
            #if (self.need_to_finish == 0):
            self.ops_end_time = self.get_time_seconds()
        finally:
            self.lock.release()               

    
    def get_time_micro(self):
        return float(time.time() * 1000 * 1000)

    
    def get_time_seconds(self):
        return float(time.time())
