def get_file_name_to_open(parent=None,
                          message='開くファイルを指定してください',
                          title='ファイルを開く',
                          verb='開く',
                          width=50):
    import PySimpleGUI as sg
    import os
    keep_on_top = True
    if parent:
        keep_on_top = False
        parent.Hide()
    # print(keep_on_top)
    filename = ''
    while True:
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
                break
            else:
                sg.popup('ファイル"{}"は存在しません'.format(filename))
                continue
        else:
            break
    if parent:
        parent.UnHide()
    return None if not filename else filename.replace('\\', '/')


def get_file_name_to_save(parent=None,
                          message='保存先のファイルを指定してください',
                          title='名前を付けて保存',
                          verb='保存',
                          width=50):
    import PySimpleGUI as sg
    import os
    keep_on_top = True
    if parent:
        keep_on_top = False
        parent.Hide()
    # print(keep_on_top)
    filename = ''
    while True:
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
                break
            elif filename == '':
                sg.popup('ファイル名が入力されていません')
                continue
            else:
                abspath = os.path.abspath(filename).replace('\\', '/')
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
                            break
                        except Exception:
                            sg.popup('フォルダ"{}"を作成できませんでした'.format(dirname))
                            continue
                    else:
                        break
                else:
                    break
        else:
            break
    if parent:
        parent.UnHide()
    return None if not filename else filename.replace('\\', '/')


if __name__ == '__main__':
    import PySimpleGUI as sg

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