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



def main():
    parent_directory = os.path.join('tests','garbbage')
    epochs           = 10  # Increase the epochs to create more files and dirs
    is_directory     = [True, False]
    name_list = ['amal', 'hurry', 'test', 'random', 'orange', 'goat', 'normal']
    extension = ['txt', 'mp3', 'cpp', 'hpp', 'mkv', 'wav', 'mp4', 'lst', 'cap']
    millis_time = lambda: str(int(round(time.time())))
    dir_count  = 0
    file_count = 0
    
    dir_gen(parent_directory)

    for _ in range(epochs):
        if random.choice(is_directory):
            dir_name = os.path.join(parent_directory, random.choice(name_list))
            dir_gen(dir_name)
            dir_count += 1
        else:
            extn     = random.choice(extension)
            name_part = random.choice(name_list)
            full_name = name_part + '_' + millis_time() + '.' + extn
            file_name = os.path.join(parent_directory, full_name)
            file_gen(file_name)
            file_count += 1

    print('Created {} files and {} directories in {}'
        .format(file_count, dir_count, parent_directory))

if __name__ == '__main__':
    main()
