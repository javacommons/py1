import tarfile
import os
import stat
from commonthread import *
import winshell
from win32com.client import Dispatch

lg = CommonThreadLogger()
lg.setup_basic()


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

topdir = 'C:/temp/extracted'

# tarアーカイブに含まれるファイル／フォルダ名を取得
# for tarinfo in tar:
#     print(tarinfo.name)

lg.debug('rmtree')
rmtree(topdir)

lg.debug('extractall')
tar.extractall(topdir)

lg.debug('shortcut')
# desktop = winshell.desktop()
desktop = 'C:/temp/shortcuts'
os.makedirs(desktop, exist_ok=True)
path = os.path.join(desktop, "MinGW32 Terminal.lnk")
target = topdir + "/msys32/mingw32.exe"
wDir = ""
icon = target
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.IconLocation = icon
shortcut.save()

lg.debug('end')
