# click a button to browse for a file
# contents of selected file is displayed
import PySimpleGUI as sg


def get_browse_file_name(parent, msg='開くファイルを選択してください', width=50):
    parent.Hide()
    event, values = sg.Window('ファイルを開く',
                    [[sg.Text(msg)],
                    [sg.Input(size=(width, 1), key='-FILE-'), sg.FileBrowse('参照')],
                    [sg.Open('開く', key='-OPEN-'), sg.Cancel('キャンセル')]],
                              keep_on_top=False, no_titlebar=False).read(close=True)
    # print(event, values)
    filename = None
    if event == '-OPEN-':
        filename = values['-FILE-']
        if filename.strip() == '':
            filename = None
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
        filename = get_browse_file_name(window, width=20)
        print('filename={}'.format(filename))
        if filename:
            window.FindElement('-FILE-').Update(filename)
        else:
            window.FindElement('-FILE-').Update('')

window.Close()