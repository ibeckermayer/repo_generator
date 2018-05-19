import re
import os


def file_handle(f):
    # split into list of individual files
    files = re.split(r'[,]', f)
    for fi in files:

        # split into list of directories follow by file
        dirs_and_file = re.split(r'[/]', fi)

        # make any necessary directories
        for directory in dirs_and_file[:-1]:
            try:
                os.mkdir(directory.strip())
                print(directory)
            except FileExistsError:
                pass

        # now make all the files
        try:
            os.mknod(fi.strip())
        except FileExistsError:
            pass
