import PySimpleGUI as sg
from sg_util import *

if __name__ == '__main__':

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

    subprocess.run([sys.executable, "longtask.py", '-h'], stderr=sys.stderr, stdout=sys.stdout)
    subprocess.run([sys.executable, "longtask.py", '11', '22'], stderr=sys.stderr, stdout=sys.stdout)

    print('end')