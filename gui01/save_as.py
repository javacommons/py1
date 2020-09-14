# click a button to browse for a file
# contents of selected file is displayed
import PySimpleGUI as sg
import os


def get_file_name_to_open(parent=None,
                          message='開くファイルを指定してください',
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

def get_file_name_to_save(parent=None,
                          message='保存先のファイルを指定してください',
                          title='名前を付けて保存',
                          verb='保存',
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
                                   [sg.Input(filename, size=(width, 1), key='-FILE-'), sg.FileSaveAs('参照')],
                                   [sg.Open(verb, key='-SAVE-'), sg.Cancel('キャンセル', key='-CANCEL-')]],
                                  keep_on_top=keep_on_top).read(close=True)
        # print(event, values)
        filename = None
        if event == '-SAVE-':
            filename = values['-FILE-']
            filename = filename.strip()
            if os.path.isfile(filename):
                finished = True
            elif filename == '':
                sg.popup('ファイル名が入力されていません')
                finished = False
            elif os.access(filename, os.W_OK):
                sg.popup('ファイル"{}"は書き込み可能です'.format(filename))
                finished = True
            else:
                abspath = os.path.abspath(filename)
                if filename != abspath:
                    filename = abspath
                    finished = False
                    continue
                dirname = os.path.dirname(filename)
                print(dirname)
                if not os.path.exists(dirname):
                    if sg.popup_yes_no('フォルダ"{}"は存在しません。作成しますか？'.format(dirname)):
                        try:
                            os.makedirs(dirname)
                            finished = True
                        except Exception:
                            sg.popup('フォルダ"{}"を作成できませんでした'.format(dirname))
                            finished = False
                    else:
                        finished = False
                else:
                    finished = True
        else:
            finished = True
    if parent:
        parent.UnHide()
    return filename


layout = [
    [sg.Button('読込', key='-READ_BTN-'), sg.Text(size=(80, 1), key='-FILE-')],
    [sg.Button('名前を付けて保存', key='-SAVE_AS_BTN-'), sg.Text(size=(80, 1), key='-FILE_TO_SAVE-')]
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
    if event == '-SAVE_AS_BTN-':
        filename = get_file_name_to_save()
        print(filename)

window.Close()