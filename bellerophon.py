"""docstring placeholder"""
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
_blacklist = ['amal', 'hurry']
_path = os.path.join(os.getcwd(), 'tests', 'garbbage')


def rename(object_type, object_name):
    """
    function to rename files or directory

    :param string object_type: mention whether object is "file" or "directory"
    :param string object_name: name of the "file" or "directory"
    checked in the file/directory name to determine whether raname should
    perform or not
    """
    object_action_info = []
    # takes every string from the list of configured string(for removal
    # purposes) and
    # check whether it is present in the object name.
    for backlisted_string in _blacklist:
        if backlisted_string in object_name:
            # object name has a string which is to be removed, so removes
            # the string
            new_name = object_name.replace(backlisted_string, '')
            # add the action details to the list
            object_action_info = (
                _path,
                object_type,
                object_name,
                'RENAMED',
                new_name,
                backlisted_string
                )
            _children.append(object_action_info)
            object_name = new_name
        _children.append(
            (
                _path,
                object_type,
                object_name,
                'NO_ACTION',
                object_name,
                backlisted_string
            )
        )


def main():
    # look for the files and directories present at given location
    for child_object in os.scandir(_path):
        if child_object.is_file():
            rename('file', child_object.name)
        elif child_object.is_dir():
            rename('directory', child_object.name)
    for child in _children:
        print(
            '{}\t{}\t{}\t{}\t{}\t{}'.format(
                    child[0], child[1], child[2], child[3], child[4], child[5]
                )
            )

if __name__ == '__main__':
    main()
