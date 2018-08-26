"""
Change History
1. Renaming files and folders in bulk in such a way that if blacklisted
    strings are present in file/folder names by removing blacklisted strings
    from the names.
2. Blacklisted strings are stored in a text file in the program directory
3. Program asks for target location.
4. Program generates a log file at target location once completed
    renaming with the details of rename operation
5. Support recursive scanning of files/folders = on 8/26/2018 11:59 AM IST
"""
import os


def rename(object_type, object_name, target_location, log_list, black_list):
    """
    function to rename files or directory

    :param string object_type: mention whether object is "file" or "directory"
    :param string object_name: name of the "file" or "directory"
    checked in the file/directory name to determine whether raname should
    perform or not
    :param string target_location: absolute location of the directory where
    program should look for
    :param list log_list: list to which the operational details has to be
    stored, children of this list would be a tuple with 6 strings(location,
    old name, action, new name, removed string(s))
    :param list black_list: list which contains strings which will be checked
    in the names of files or directories for removal
    """
    action = "No Action"
    old_name = object_name
    removed_strings = ""
    # takes every string from the list of configured string(for removal
    # purposes) and
    # check whether it is present in the object name.
    for backlisted_string in black_list:
        if backlisted_string in object_name:
            # object name has a string which is to be removed, so removes
            # the string
            object_name = object_name.replace(backlisted_string, '')
            if removed_strings != "":
                removed_strings += ", "
            removed_strings += backlisted_string
    # if object name is changed, file has been renamed
    if old_name != object_name:
        os.rename(
            os.path.join(target_location, old_name),
            os.path.join(target_location, object_name)
            )
        action = "Renamed"
        log_list.append(
            (
                target_location,
                object_type,
                old_name,
                action,
                object_name,
                removed_strings
            )
        )


def crawl_and_rename(target_location, log_list, black_list):
    """
    Function to scan through the target_location for files and folders for
    renaming

    :param string target_location: absolute location of the directory where
    program should look for
    :param list log_list: list to which the operational details has to be
    stored, children of this list would be a tuple with 6 strings(location,
    old name, action, new name, removed string(s))
    :param list black_list: list which contains strings which will be checked
    in the names of files     or directories for removal
    """
    # look for the files and directories present at given location
    for child_object in os.scandir(target_location):
        if child_object.is_file():
            rename(
                'file',
                child_object.name,
                target_location,
                log_list,
                black_list
                )
        elif child_object.is_dir():
            # if the child is a directory, instead of renaming it, going
            # inside of the directory to perform scanning first, once whole
            # children are analyed it will come back and rename the directory
            crawl_and_rename(
                os.path.join(
                    target_location, child_object.name
                    ),
                log_list,
                black_list
                )
            rename(
                'directory',
                child_object.name,
                target_location,
                log_list,
                black_list
                )


def main():
    """
    Main code to run
    """
    # list to store names and status of files/directories present in the given
    # location
    log = [
        (
            'Location',
            'Type',
            'Old Name',
            'Action',
            'New Name',
            'Removed String(s)'
        )
    ]

    # list to store the strings to be removed from file/directory names
    # NOTE: This has to be changed to be later when we load this data from
    # external file
    blacklist_file_location = os.path.join(os.getcwd(), 'blacklist.txt')
    black_list = [
        line.replace('\n', '') for line in open(blacklist_file_location, "r")
        ]
    print(black_list)
    target_location = input(
        "Provide target directory location(fully qualified location):"
        )
    crawl_and_rename(target_location, log, black_list)
    log_file = open(os.path.join(target_location, "log.txt"), "w")
    for child in log:
        log_file.write(
            '{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}\n'.format(
                child[1], child[2], child[3], child[4], child[5], child[0]
            )
        )
    log_file.close()

if __name__ == '__main__':
    main()
