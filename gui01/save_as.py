import PySimpleGUI as sg
from psgui_util import *


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
            filename = psgui_get_file_name_to_open(
                pattern='*.txt;*.bxproj', width=60, verb='処理する', old_value=window.FindElement('-FILE-').Get())
            print('filename={}'.format(filename))
            if filename:
                window.FindElement('-FILE-').Update(filename)
            else:
                window.FindElement('-FILE-').Update('')
        if event == '-SAVE_AS_BTN-':
            filename = psgui_get_file_name_to_save(
                pattern='*.txt;*.log', old_value=window.FindElement('-FILE_TO_SAVE-').Get())
            print(filename)
            if filename:
                window.FindElement('-FILE_TO_SAVE-').Update(filename)
            else:
                window.FindElement('-FILE_TO_SAVE-').Update('')
        if event == '-FOLDER_BTN-':
            filename = psgui_get_folder_name(old_value=window.FindElement('-FOLDER-').Get())
            print(filename)
            if filename:
                window.FindElement('-FOLDER-').Update(filename)
            else:
                window.FindElement('-FOLDER-').Update('')

    window.Close()


if __name__ == '__main__':

    gui_main()

    from commonthread import *
    import datetime
    import logging
    import time

    CommonThreadLogger.setup_basic_logging(format='%(threadName)s ==> %(message)s')
    lg = CommonThreadLogger()


    def worker1(th, *args, **kwargs):
        lg.debug('start')
        lg.debug(args)
        lg.debug(kwargs)
        th.output('from worker1')
        time.sleep(2)
        lg.debug('end')

    def worker3(th, *args):
        lg.debug('start')
        lg.debug(args)
        th.add_argument('operation', choices=['install', 'uninstall', 'update'], help='type of operation')
        th.add_argument('x')
        th.add_argument('y')
        th.add_argument('-z', required=True)
        th.add_argument('-w', action='store_true')
        th.add_argument('rest', nargs='*', help='file or directory')
        th.parse_args()
        lg.debug(th.params)
        time.sleep(2)
        lg.debug('end')

    class MyThread(CommonThread):

        def __init__(self, *args, **kwargs):
            CommonThread.__init__(self, *args, **kwargs)

        def entry(self, *args, **kwargs):
            lg.debug('Starting Thread named {}, args={}, kwargs={}'.format(self.name, args, kwargs))
            self.outq.put(['this', 'is', 'array'])
            lg.debug(self.args)
            for i in self.args:
                lg.debug(i)
                self.output(i)
            time.sleep(5)
            lg.debug('end')

    class ParserThread(CommonThread):

        def __init__(self, *args, **kwargs):
            CommonThread.__init__(self, *args, **kwargs)

        def entry(self, *args, **kwargs):
            self.add_argument('x')
            self.add_argument('y')
            # self.add_argument('z')
            result = self.parse_args()
            lg.debug(result)
            while True:
                inputs = self.inputs_available()
                for i in inputs:
                    lg.debug(i)
                    if i is None:
                        return

    logging.debug('starting')

    t0 = MyThread('ONE', 'TWO', 'THREE', required=True)
    t0.name = 'MyThread'
    t0.start()

    t1 = WorkerThread(worker1, 123, 'abc', 4.56, kw1=1, kw2='abcxyz')
    t1.name = "worker1"
    t1.start()

    t2 = ParserThread(123, datetime.datetime(2017, 9, 1, 12, 12))
    t2.name = 't2@ParserThread'
    t2.start()

    t3 = WorkerThread(worker3, 'install', '-z', 78.654321, 'abc', 'XYZ', 123, 456)
    t3.name = "worker3"
    t3.start()

    for i in range(30):
        print(i)
        # t2.inq.put(i)
        t2.send(i)
    # t2.inq.put(None)
    t2.send(None)

    logging.debug('started')
    print(CommonThread.some_are_active())
    while CommonThread.some_are_active():
        time.sleep(0.001)
        CommonThread.log_threads_output(use_print=True)
    CommonThread.log_threads_output(use_print=True)

    # t0.join()
    # t1.join()

    print(CommonThread.some_are_active())
