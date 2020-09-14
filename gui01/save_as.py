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
            filename = sgui_get_file_name_to_open(pattern='*.txt;*.bxproj', width=60, verb='処理する')
            print('filename={}'.format(filename))
            if filename:
                window.FindElement('-FILE-').Update(filename)
            else:
                window.FindElement('-FILE-').Update('')
        if event == '-SAVE_AS_BTN-':
            filename = sgui_get_file_name_to_save(pattern='*.txt', )
            print(filename)
        if event == '-FOLDER_BTN-':
            filename = sgui_get_folder_name()
            print(filename)

    window.Close()

    import os, time, sys, subprocess

    # o = subprocess.run([sys.executable, "longtask.py", '123'], check=False, capture_output=True)
    # print((o.stdout, o.stderr))

    task_subprocess_run1(__file__, ['-h'])
    task_subprocess_run1(__file__, ['install', '-s', '{type=msys32, font_size=14}', '11', '22'])
    task_subprocess_run1(__file__, ['install', '-w', '-s={type=msys32, font_size=14}', '11', '22'])


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

    if len(sys.argv) <= 1:
        gui_main()
    else:
        console_main()

    print(['11', 22] + ['A', 'B'])

    print('end')

    import logging
    import threading
    import time

    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

    def worker1():
        # thread の名前を取得
        logging.debug('start')
        time.sleep(5)
        logging.debug('end')


    def worker2(x, y=1):
        logging.debug('start')
        logging.debug(x)
        logging.debug(y)
        time.sleep(5)
        logging.debug('end')

    # スレッドに workder1 関数を渡す
    t1 = threading.Thread(name='rename worker1', target=worker1)
    t2 = threading.Thread(target=worker2, args=([100, 200, 300],), kwargs={'y': 200})
    # スレッドスタート
    t1.start()
    t2.start()
    print('started')