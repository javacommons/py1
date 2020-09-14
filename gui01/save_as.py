import sys
import PySimpleGUI as sg
from sg_util import *

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
            filename = sg_get_file_name_to_open(pattern='*.txt;*.bxproj', width=60, verb='処理する')
            print('filename={}'.format(filename))
            if filename:
                window.FindElement('-FILE-').Update(filename)
            else:
                window.FindElement('-FILE-').Update('')
        if event == '-SAVE_AS_BTN-':
            filename = sg_get_file_name_to_save(pattern='*.txt', )
            print(filename)
        if event == '-FOLDER_BTN-':
            filename = sg_get_folder_name()
            print(filename)

    window.Close()

    import os, time, sys, subprocess

    # o = subprocess.run([sys.executable, "longtask.py", '123'], check=False, capture_output=True)
    # print((o.stdout, o.stderr))

    subprocess.run([sys.executable, __file__, '-h'], stderr=sys.stderr, stdout=sys.stdout)
    subprocess.run([sys.executable, __file__, 'install', '11', '22'], stderr=sys.stderr, stdout=sys.stdout)


def console_main():
    import argparse
    parser = argparse.ArgumentParser(description='description of this program')
    # parser.add_argument('arg1', help='Help of arg1')
    # parser.add_argument('arg2', help='Help of arg2')
    parser.add_argument('--arg3')
    parser.add_argument('--arg4', '-a', required=True)
    parser.add_argument('operation', choices=['install', 'uninstall', 'update'], help='type of operation')
    parser.add_argument('inst_dir', help='installation directory')
    parser.add_argument('rest', nargs='*', help='file or directory')

    args = parser.parse_args()
    # print('arg1={}'.format(args.arg1))
    # print('arg2={}'.format(args.arg2))
    print('operation={}'.format(args.operation))
    print('inst_dir={}'.format(args.inst_dir))
    print('arg3={}'.format(args.arg3))
    print('arg4={}'.format(args.arg4))
    print('rest={}'.format(args.rest))


if __name__ == '__main__':
    print(len(sys.argv))

    if len(sys.argv) <= 1:
        gui_main()
    else:
        console_main()

    print('end')