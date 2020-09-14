# click a button to browse for a file
# contents of selected file is displayed
import PySimpleGUI as sg


def get_file_name_to_open(parent=None, message='開くファイルを選択してください', width=50):
    keep_on_top = True
    if parent:
        keep_on_top = False
        parent.Hide()
    print(keep_on_top)
    event, values = sg.Window('ファイルを開く',
                    [[sg.Text(message)],
                    [sg.Input(size=(width, 1), key='-FILE-'), sg.FileBrowse('参照')],
                    [sg.Open('開く', key='-OPEN-'), sg.Cancel('キャンセル', key='-CANCEL-')]],
                              keep_on_top=keep_on_top).read(close=True)
    # print(event, values)
    filename = None
    if event == '-OPEN-':
        filename = values['-FILE-']
        if filename.strip() == '':
            filename = None
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
        filename = get_file_name_to_open(width=20)
        print('filename={}'.format(filename))
        if filename:
            window.FindElement('-FILE-').Update(filename)
        else:
            window.FindElement('-FILE-').Update('')

window.Close()