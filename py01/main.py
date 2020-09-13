import os
import sys

config_name = 'myapp.cfg'

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    print(sys.executable)
    application_path = os.path.dirname(sys.executable)
elif __file__:
    print(__file__)
    application_path = os.path.dirname(__file__)

config_path = application_path + "/" + config_name

print(config_path)