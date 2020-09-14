def task_subprocess_run1(file, args_array):
    import sys, subprocess
    # o = subprocess.run([sys.executable, "longtask.py", '123'], check=False, capture_output=True)
    # print((o.stdout, o.stderr))

    if getattr(sys, 'frozen', False):
        subprocess.run([sys.executable] + args_array, stderr=sys.stderr, stdout=sys.stdout)
    elif __file__:
        subprocess.run([sys.executable, file] + args_array, stderr=sys.stderr, stdout=sys.stdout)
    return None


def task_subprocess_run2(file, args_array):
    import sys, subprocess
    o = None
    if getattr(sys, 'frozen', False):
        o = subprocess.run([sys.executable] + args_array, check=False, capture_output=True)
    elif __file__:
        o = subprocess.run([sys.executable, file] + args_array, check=False, capture_output=True)
    return o.stdout, o.stderr
