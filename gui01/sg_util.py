def sg_get_file_name_to_open(parent=None,
                             pattern='*.*',
                             width=50,
                             message='開くファイルを指定してください',
                             title='ファイルを開く',
                             verb='開く'):
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
                                   [sg.Input(filename, size=(width, 1), key='-PATH-'),
                                    sg.FileBrowse('参照', file_types=((pattern, pattern),))],
                                   [sg.Open(verb, key='-DOIT-'), sg.Cancel('キャンセル', key='-CANCEL-')]],
                                  keep_on_top=keep_on_top).read(close=True)
        # print(event, values)
        filename = None
        if event == '-DOIT-':
            filename = values['-PATH-']
            filename = filename.strip()
            if filename == '':
                sg.popup('ファイル名が入力されていません')
                continue
            else:
                abspath = os.path.abspath(filename).replace('\\', '/')
                if filename != abspath:
                    filename = abspath
                    finished = False
                    continue
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


def sg_get_file_name_to_save(parent=None,
                             pattern='*.*',
                             width=50,
                             message='保存先のファイルを指定してください',
                             title='名前を付けて保存',
                             verb='保存'):
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
                                   [sg.Input(filename, size=(width, 1), key='-PATH-'), sg.FileSaveAs('参照', file_types=((pattern, pattern),))],
                                   [sg.Open(verb, key='-DOIT-'), sg.Cancel('キャンセル', key='-CANCEL-')]],
                                  keep_on_top=keep_on_top).read(close=True)
        # print(event, values)
        filename = None
        if event == '-DOIT-':
            filename = values['-PATH-']
            filename = filename.strip()
            # if os.path.isfile(filename):
            #     break
            # el
            if filename == '':
                sg.popup('ファイル名が入力されていません')
                continue
            else:
                abspath = os.path.abspath(filename).replace('\\', '/')
                if filename != abspath:
                    filename = abspath
                    finished = False
                    continue
                dirname = os.path.dirname(filename)
                # print(dirname)
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


def sg_get_folder_name(parent=None,
                       width=50,
                       message='フォルダを指定してください',
                       title='フォルダ選択',
                       verb='選択'):
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
                                   [sg.Input(filename, size=(width, 1), key='-PATH-'), sg.FolderBrowse('参照')],
                                   [sg.Open(verb, key='-DOIT-'), sg.Cancel('キャンセル', key='-CANCEL-')]],
                                  keep_on_top=keep_on_top).read(close=True)
        # print(event, values)
        filename = None
        if event == '-DOIT-':
            filename = values['-PATH-']
            filename = filename.strip()
            if filename == '':
                sg.popup('フォルダ名が入力されていません')
                continue
            else:
                abspath = os.path.abspath(filename).replace('\\', '/')
                if filename != abspath:
                    filename = abspath
                    finished = False
                    continue
                dirname = filename
                # print(dirname)
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
