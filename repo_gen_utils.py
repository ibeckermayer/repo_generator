import re
import os
import code


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
            except FileExistsError:
                pass

        # now make all the files
        try:
            os.mknod(fi.strip())
        except FileExistsError:
            pass


def snippet_handle(s):
    l = 0
    lines = s.splitlines()
    # code.interact(local=locals())
    while l < len(lines):
        words = re.split(r'[ ]', lines[l])
        i = 0
        while i < len(words):
            if words[i] == "cat":
                i+=1
                l+=1
                if i < len(words):
                    while words[i][0] == "-":  # skip options
                        i+=1
                    filename = words[i]
                    try:            # make the file
                        os.mknod(filename.strip())
                    except FileExistsError:
                        pass
                    while l < len(lines):  # continue down line by line
                        if '@' not in lines[l] and '$' not in lines[l]:
                            with open(filename, 'a') as f:
                                f.write(lines[l] + '\n')
                            l+=1
                        else:
                            break
                    break
            else:
                i+=1
        l+=1
