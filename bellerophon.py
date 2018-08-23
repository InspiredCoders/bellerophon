"""docstring placeholder"""
import os

path = os.path.join(os.getcwd(), 'tests','garbbage')
dirs = []
files = []
excluded_strings = ['amal', 'hurry']
for e in os.scandir(path):
    if e.is_file():
        filename = e.name
        file_info = []
        #file_info = [(f, e.name, filename.replace(f, ''), 'RENAMED') for f in excluded_strings if f in e.name]
        for unwanted in excluded_strings:
            if unwanted in filename:
                new_filename = filename.replace(unwanted, '')
                file_info.append((filename, new_filename, 'RENAMED', unwanted))
                filename = new_filename
        if file_info.__len__() > 0:
            files.append(file_info)
        else:
            files.append((filename, filename, 'NO_CHANGE', None))
    elif e.is_dir():
        dirs.append(e.name)
print(files)
#print(dirs)
