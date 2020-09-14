import sys
import PySimpleGUI as sg
from sgui_util import *
from task_util import *


def gui_main():
    layout = [
        [sg.Button('読込', key='-READ_BTN-'), sg.Text(size=(80, 1), key='-FILE-')],
        [sg.Button('名前を付けて保存', key='-SAVE_AS_BTN-'), sg.Text(size=(80, 1), key='-FILE_TO_SAVE-')],
        [sg.Button('フォルダ選択', key='-FOLDER_BTN-'), sg.Text(size=(80, 1), key='-FOLDER-')]
    ]

    window = sg.Window('File Browser', layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event is None or event == 'Exit':
            break
        if event == '-READ_BTN-':
            # filename = get_file_name_to_open(window, width=50)
            filename = sgui_get_file_name_to_open(
                pattern='*.txt;*.bxproj', width=60, verb='処理する', old_value=window.FindElement('-FILE-').Get())
            print('filename={}'.format(filename))
            if filename:
                window.FindElement('-FILE-').Update(filename)
            else:
                window.FindElement('-FILE-').Update('')
        if event == '-SAVE_AS_BTN-':
            filename = sgui_get_file_name_to_save(
                pattern='*.txt;*.log', old_value=window.FindElement('-FILE_TO_SAVE-').Get())
            print(filename)
            if filename:
                window.FindElement('-FILE_TO_SAVE-').Update(filename)
            else:
                window.FindElement('-FILE_TO_SAVE-').Update('')
        if event == '-FOLDER_BTN-':
            filename = sgui_get_folder_name(old_value=window.FindElement('-FOLDER-').Get())
            print(filename)
            if filename:
                window.FindElement('-FOLDER-').Update(filename)
            else:
                window.FindElement('-FOLDER-').Update('')

    window.Close()

    import os, time, sys, subprocess

    # task_subprocess_run1(__file__, ['-h'])
    # task_subprocess_run1(__file__, ['install', '-s', '{type=msys32, font_size=14}', '11', '22'])
    # task_subprocess_run1(__file__, ['install', '-w', '-s={type=msys32, font_size=14}', '11', '22'])


def console_main():
    import argparse
    parser = argparse.ArgumentParser(description='description of this program')
    parser.add_argument('--argX')
    parser.add_argument('-w', action='store_true')
    parser.add_argument('operation', choices=['install', 'uninstall', 'update'], help='type of operation')
    parser.add_argument('--spec', '-s', required=True)
    parser.add_argument('inst_dir', help='installation directory')
    parser.add_argument('rest', nargs='*', help='file or directory')

    args = parser.parse_args()
    # print('arg1={}'.format(args.arg1))
    # print('arg2={}'.format(args.arg2))
    print('operation={}'.format(args.operation))
    print('spec={}'.format(args.spec))
    print('inst_dir={}'.format(args.inst_dir))
    print('argX={}'.format(args.argX))
    print('w={}'.format(args.w))
    print('rest={}'.format(args.rest))

    # args2 = parser.parse_args(['uninstall', '-w', '-s={type=msys32, font_size=14}', '123', '456'])
    # print('operation={}'.format(args2.operation))
    # print('spec={}'.format(args2.spec))
    # print('inst_dir={}'.format(args2.inst_dir))
    # print('argX={}'.format(args2.argX))
    # print('w={}'.format(args2.w))
    # print('rest={}'.format(args2.rest))


if __name__ == '__main__':
    print(len(sys.argv))

    gui_main()

    # if len(sys.argv) <= 1:
    #     gui_main()
    # else:
    #     console_main()
    #
    # print('end')

    import logging
    import threading
    import time
    import queue

    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

    q = queue.Queue()

    def worker1():
        # thread の名前を取得
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')

    def worker2(q, y=1, argv=[]):
        logging.debug('start')
        logging.debug(q)
        logging.debug(y)
        logging.debug('argv={}'.format(argv))
        q.put('q-1')
        time.sleep(5)
        logging.debug('end')

    class CommonThread(threading.Thread):
        # all_threads = []

        def __init__(self, *args):
            threading.Thread.__init__(self)
            # super(CommonThread, self).__init__(self)
            self.args = args
            self.inq = queue.Queue()
            self.outq = queue.Queue()
            # CommonThread.all_threads.append(self)

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

    class MyThread(CommonThread):
        def __init__(self, *args):
            # CommonThread.__init__(self, *args)
            super(MyThread, self).__init__(self, *args)

        def run(self):
            logging.debug('Starting Thread named {}, args={} inq={}, outq={}'.format(
                self.name, self.args, self.inq, self.outq))
            for i in self.args:
                logging.debug(i)
                self.outq.put(i)
            time.sleep(5)
            logging.debug('end')

    logging.debug('starting')
    t0 = MyThread('ONE', 'TWO', 'THREE')
    t0.start()
    # スレッドに workder1 関数を渡す
    t1 = threading.Thread(name='Thread-A', target=worker1)
    t2 = threading.Thread(target=worker2, args=(q,), kwargs={'y': 200, 'argv': ['a', 123, 456.7]})
    # スレッドスタート
    t1.start()
    t2.start()
    logging.debug('started')
    print(CommonThread.some_are_active())
    while CommonThread.some_are_active():
        time.sleep(0.001)
        CommonThread.log_active_threads()
        # while not t0.outq.empty():
        #     x = t0.outq.get()
        #     logging.debug(x)
    # while not t0.outq.empty():
    #     x = t0.outq.get()
    #     logging.debug(x)
    CommonThread.log_active_threads()

    t0.join()
    t1.join()
    t2.join()
    print(CommonThread.some_are_active())

    # logging.debug(len(CommonThread.all_threads))