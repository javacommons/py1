import argparse
import logging
import queue
import threading


class CommonThread(threading.Thread):

    def __init__(self, *params):
        threading.Thread.__init__(self)
        self.params = params
        self.inq = queue.Queue()
        self.outq = queue.Queue()
        self.parser = argparse.ArgumentParser()
        self.args = None

    def parse(self):
        self.args = self.parser.parse_args(self.params)

    @classmethod
    def set_basic_logging(cls, level=logging.DEBUG, format='%(threadName)s: %(message)s'):
        logging.basicConfig(level=level, format=format)

    @classmethod
    def some_are_active(cls):
        for thread in threading.enumerate():
            if isinstance(thread, CommonThread):
                return True
        return False

    @classmethod
    def collect_threads_output(cls):
        result = []
        for thread in threading.enumerate():
            if not isinstance(thread, CommonThread):
                continue
            while not thread.outq.empty():
                result.append(thread.outq.get())
        return result

    @classmethod
    def log_threads_output(cls, use_print=False):
        msg_list = CommonThread.collect_threads_output()
        for msg in msg_list:
            if use_print:
                print(msg)
            else:
                logging.debug(msg)


class WorkerThread(CommonThread):

    def __init__(self, worker_function, *params):
        CommonThread.__init__(self, *params)
        self.worker_function = worker_function

    def run(self):
        self.worker_function(self, *self.params)
        return None
