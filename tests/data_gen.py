"""
data_gen.py

File containing the functionality to generate test files and folders
for testing bellerophon.
"""
import os
import random
import time


def dir_gen(directory_name):
    """
    Function to create files.

    :param string directory_name: Fully qualified dierctory name which is
    to be created
    """
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def file_gen(file_name):
    """
    Function to create folders.

    :param string filename: Fully qualified file name which is to be craeted
    """
    file_hanlder = open(file_name, 'wb+')
    file_hanlder.write(b'This is a test file')
    file_hanlder.close()


def millis_time():
    return str(int(round(time.time())))


def main():
    parent_directory = os.path.join('tests', 'garbbage')
    epochs = 10000  # Increase the epochs to create more files and dirs
    f_count = 10  # Number of files per directory
    max_path_length = 200  # Number of characters allowed in the path name
    is_directory = [True, False]
    go_inside = [True, False]
    name_list = ['amal', 'hurry', 'test', 'random', 'orange', 'goat', 'normal']
    extension = ['txt', 'mp3', 'cpp', 'hpp', 'mkv', 'wav', 'mp4', 'lst', 'cap']
    dir_count = 0
    file_count = 0

    dir_gen(parent_directory)

    dir_list = [parent_directory]

    for _ in range(epochs):
        if random.choice(is_directory):
            choice = random.choice(name_list)
            dir_name = os.path.join(*dir_list, choice)
            dir_gen(dir_name)
            dir_count += 1
            if random.choice(go_inside) and len(dir_name) < max_path_length:
                dir_list.append(choice)
            elif (
                not(os.path.join(*dir_list) == parent_directory) and
                len([name for name in os.listdir(dir_name)]) >=
                (epochs/f_count)
            ):
                del dir_list[-1]
        else:
            extn = random.choice(extension)
            name_part = random.choice(name_list)
            full_name = name_part + '_' + millis_time() + '.' + extn
            file_name = os.path.join(*dir_list, full_name)
            file_gen(file_name)
            file_count += 1

    print('Created {} files and {} directories in {}'
          .format(file_count, dir_count, parent_directory))

if __name__ == '__main__':
    main()
