"""
Implemented Features
1. Renaming files and folders in bulk in such a way that if blacklisted
    strings are present in file/folder names by removing blacklisted strings from the names.
2. Blacklisted strings are stored in a text file in the program directory
3. Program asks for target location.
4. Program generates a log file at target location once completed
    renaming with the details of rename operation
"""
import os

# list to store names and status of files/directories present in the given
# location
_children = [
    (
        'Location',
        'Type',
        'Old Name',
        'Action',
        'New Name',
        'Removed String'
    )
]

# list to store the strings to be removed from file/directory names
# NOTE: This has to be changed to be later when we load this data from
# external file
_blacklist_path = os.path.join(os.getcwd(), 'blacklist.txt')
_blacklist = [line.rstrip() for line in open(_blacklist_path, "r")]
#_path = os.path.join(os.getcwd(), 'tests', 'garbbage')
_path = input("Provide target directory location(fully qualified location):")

def rename(object_type, object_name):
    """
    function to rename files or directory

    :param string object_type: mention whether object is "file" or "directory"
    :param string object_name: name of the "file" or "directory"
    checked in the file/directory name to determine whether raname should
    perform or not
    """
    action = "No Action"
    old_name = object_name
    removed_strings = ""
    # takes every string from the list of configured string(for removal
    # purposes) and
    # check whether it is present in the object name.
    for backlisted_string in _blacklist:
        if backlisted_string in object_name:
            # object name has a string which is to be removed, so removes
            # the string
            object_name = object_name.replace(backlisted_string, '')
            if removed_strings != "":
                removed_strings += ", "
            removed_strings += backlisted_string
    # if object name is changed, file has been renamed
    if old_name != object_name:
        os.rename(os.path.join(_path, old_name), os.path.join(_path, object_name))
        action = "Renamed"
        _children.append(
            (_path, object_type, old_name, action, object_name, removed_strings)
        )


def main():
    """
    Main code to run
    """
    # look for the files and directories present at given location
    for child_object in os.scandir(_path):
        if child_object.is_file():
            rename('file', child_object.name)
        elif child_object.is_dir():
            rename('directory', child_object.name)
    log_file = open(os.path.join(_path, "log.txt"), "w")
    for child in _children:
        log_file.write(
            '{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}\n'.format(
                child[1], child[2], child[3], child[4], child[5], child[0]
            )
        )
    log_file.close()

if __name__ == '__main__':
    main()
