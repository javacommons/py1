import sys
import PySimpleGUI as sg
from sgui_util import *


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


if __name__ == '__main__':

    gui_main()

    import commonthread
    import datetime
    import logging
    import time

    commonthread.CommonThread.set_basic_logging(format='%(threadName)s ==> %(message)s')

    def worker1(th, *args, **kwargs):
        th.log_debug('start')
        th.log_debug(args)
        th.log_debug(kwargs)
        th.output('from worker1')
        time.sleep(2)
        th.log_debug('end')

    def worker3(th, *args):
        th.log_debug('start')
        th.log_debug(args)
        th.add_argument('operation', choices=['install', 'uninstall', 'update'], help='type of operation')
        th.add_argument('x')
        th.add_argument('y')
        th.add_argument('-z', required=True)
        th.add_argument('-w', action='store_true')
        th.add_argument('rest', nargs='*', help='file or directory')
        th.parse_args()
        th.log_debug(th.params)
        time.sleep(2)
        th.log_debug('end')

    class MyThread(commonthread.CommonThread):

        def __init__(self, *args):
            commonthread.CommonThread.__init__(self, *args)

        def run(self):
            self.log_debug('Starting Thread named {}, args={}'.format(self.name, self.args))
            self.outq.put(['this', 'is', 'array'])
            self.log_debug(self.args)
            for i in self.args:
                self.log_debug(i)
                self.output(i)
            time.sleep(5)
            self.log_debug('end')

    class ParserThread(commonthread.CommonThread):

        def __init__(self, *args):
            commonthread.CommonThread.__init__(self, *args)

        def run(self):
            self.add_argument('x')
            self.add_argument('y')
            # self.add_argument('z')
            self.parse_args()
            self.log_debug(self.params)

    logging.debug('starting')

    t0 = MyThread('ONE', 'TWO', 'THREE')
    t0.name = 'MyThread'
    t0.start()

    t1 = commonthread.WorkerThread(worker1, 123, 'abc', 4.56, kw1=1, kw2='abcxyz')
    t1.name = "worker1"
    t1.start()

    t2 = ParserThread(123, datetime.datetime(2017, 9, 1, 12, 12))
    t2.name = 't2@ParserThread'
    t2.start()

    t3 = commonthread.WorkerThread(worker3, 'install', '-z', 78.654321, 'abc', 'XYZ', 123, 456)
    t3.name = "worker3"
    t3.start()

    logging.debug('started')
    print(commonthread.CommonThread.some_are_active())
    while commonthread.CommonThread.some_are_active():
        time.sleep(0.001)
        commonthread.CommonThread.log_threads_output(use_print=True)
    commonthread.CommonThread.log_threads_output(use_print=True)

    # t0.join()
    # t1.join()

    print(commonthread.CommonThread.some_are_active())
