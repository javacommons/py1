import logging
import queue
import threading


class CommonThread(threading.Thread):

    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.inq = queue.Queue()
        self.outq = queue.Queue()

    @classmethod
    def some_are_active(cls):
        for thread in threading.enumerate():
            if isinstance(thread, CommonThread):
                # print('thread.name={}'.format(thread.name))
                return True
        return False

    @classmethod
    def log_active_threads(cls):
        for thread in threading.enumerate():
            if not isinstance(thread, CommonThread):
                continue
            while not thread.outq.empty():
                logging.debug(thread.outq.get())


class WorkerThread(CommonThread):
    def __init__(self, worker_function, *args):
        CommonThread.__init__(self, *args)
        self.worker_function = worker_function

    def run(self):
        self.worker_function(*self.args)
        return None
