import os


def remove_file(path):
    if os.path.isfile(path):
        os.remove(path)
    else:
        raise FileNotFoundError
