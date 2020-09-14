# click a button to browse for a file
# contents of selected file is displayed
import PySimpleGUI as sg
import os


def get_file_name_to_open(parent=None,
                          message='開くファイルを選択してください',
                          title='ファイルを開く',
                          verb='開く',
                          width=50):
    keep_on_top = True
    if parent:
        keep_on_top = False
        parent.Hide()
    # print(keep_on_top)
    filename = ''
    finished = False
    while not finished:
        event, values = sg.Window(title,
                                  [[sg.Text(message)],
                                   [sg.Input(filename, size=(width, 1), key='-FILE-'), sg.FileBrowse('参照')],
                                   [sg.Open(verb, key='-OPEN-'), sg.Cancel('キャンセル', key='-CANCEL-')]],
                                  keep_on_top=keep_on_top).read(close=True)
        # print(event, values)
        filename = None
        if event == '-OPEN-':
            filename = values['-FILE-']
            filename = filename.strip()
            if os.path.isfile(filename):
                finished = True
            else:
                sg.popup('ファイル"{}"は存在しません'.format(filename))
                finished = False
        else:
            finished = True
    if parent:
        parent.UnHide()
    return filename


layout = [
    [sg.Button('読込', key='-READ_BTN-'), sg.Text(size=(80, 1), key='-FILE-')]
]

window = sg.Window('File Browser', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event is None or event == 'Exit':
        break
    if event == '-READ_BTN-':
        # filename = get_file_name_to_open(window, width=50)
        filename = get_file_name_to_open(width=60, verb='処理する')
        print('filename={}'.format(filename))
        if filename:
            window.FindElement('-FILE-').Update(filename)
        else:
            window.FindElement('-FILE-').Update('')

window.Close()