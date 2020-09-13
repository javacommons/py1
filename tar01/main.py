import tarfile
import os
import stat


def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    if os.path.exists(top):
        os.rmdir(top)


tar = tarfile.open('C:/root/data/msys2-base-i686-20200517.tar.xz', 'r:xz')

# tarアーカイブに含まれるファイル／フォルダ名を取得
# for tarinfo in tar:
#     print(tarinfo.name)

rmtree('./extracted')

# tar.extractall('./extracted')
# pip install pywin32

import os, winshell
from win32com.client import Dispatch
desktop = winshell.desktop()
path = os.path.join(desktop, "Media Player Classic.lnk")
target = r"P:\Media\Media Player Classic\mplayerc.exe"
wDir = r"P:\Media\Media Player Classic"
icon = r"P:\Media\Media Player Classic\mplayerc.exe"
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.IconLocation = icon
shortcut.save()