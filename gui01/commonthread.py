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

    @classmethod
    def some_are_active(cls):
        for thread in threading.enumerate():
            if isinstance(thread, CommonThread):
                return True
        return False

    @classmethod
    def log_active_threads(cls):
        for thread in threading.enumerate():
            if not isinstance(thread, CommonThread):
                continue
            while not thread.outq.empty():
                logging.debug(thread.outq.get())


class WorkerThreadParams:

    def __init__(self, inq, outq):
        self.inq = inq
        self.outq = outq


class WorkerThread(CommonThread):

    def __init__(self, worker_function, *params):
        CommonThread.__init__(self, *params)
        self.worker_function = worker_function

    def run(self):
        o = WorkerThreadParams(self.inq, self.outq)
        self.worker_function(o, *self.params)
        return None


class ArgParserThread(CommonThread):

    def __init__(self, *params):
        CommonThread.__init__(self, *params)
        self.parser = argparse.ArgumentParser()
        self.args = None

    def parse(self):
        self.args = self.parser.parse_args(self.params)
