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

    # args = parser.parse_args()
    # # print('arg1={}'.format(args.arg1))
    # # print('arg2={}'.format(args.arg2))
    # print('operation={}'.format(args.operation))
    # print('spec={}'.format(args.spec))
    # print('inst_dir={}'.format(args.inst_dir))
    # print('argX={}'.format(args.argX))
    # print('w={}'.format(args.w))
    # print('rest={}'.format(args.rest))

    args2 = parser.parse_args(['uninstall', '-w', '-s={type=msys32, font_size=14}', '123', '456'])
    print('operation={}'.format(args2.operation))
    print('spec={}'.format(args2.spec))
    print('inst_dir={}'.format(args2.inst_dir))
    print('argX={}'.format(args2.argX))
    print('w={}'.format(args2.w))
    print('rest={}'.format(args2.rest))


if __name__ == '__main__':
    print(len(sys.argv))

    gui_main()

    import commonthread
    import logging
    import time

    commonthread.CommonThread.set_basic_logging(format='%(threadName)s:: %(message)s')

    def worker1(thread, *args):
        # thread の名前を取得
        logging.debug('start')
        logging.debug(args)
        thread.outq.put('from worker1')
        time.sleep(2)
        logging.debug('end')

    class MyThread(commonthread.CommonThread):

        def __init__(self, *args):
            commonthread.CommonThread.__init__(self, *args)

        def run(self):
            logging.debug('Starting Thread named {}, args={} inq={}, outq={}'.format(
                self.name, self.params, self.inq, self.outq))
            self.outq.put(['this', 'is', 'array'])
            logging.debug(self.params)
            for i in self.params:
                logging.debug(i)
                self.outq.put(i)
            time.sleep(5)
            logging.debug('end')

    class ParserThread(commonthread.ArgumentParserThread):

        def __init__(self, *args):
            commonthread.ArgumentParserThread.__init__(self, *args)

        def run(self):
            self.parser.add_argument('x')
            self.parser.add_argument('y')
            # self.parser.add_argument('z')
            self.parse()
            logging.debug(self.args)

    logging.debug('starting')

    t0 = MyThread('ONE', 'TWO', 'THREE')
    t0.name = 'MyThread'
    t0.start()

    t1 = commonthread.WorkerThread(worker1, 123, 'abc', 4.56)
    t1.name = "worker1"
    t1.start()

    t2 = ParserThread('123', '456')
    t2.start()

    logging.debug('started')
    print(commonthread.CommonThread.some_are_active())
    while commonthread.CommonThread.some_are_active():
        time.sleep(0.001)
        commonthread.CommonThread.log_threads_output(use_print=True)
    commonthread.CommonThread.log_threads_output(use_print=True)

    # t0.join()
    # t1.join()

    print(commonthread.CommonThread.some_are_active())
    console_main()
