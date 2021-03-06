"""
Bellerophone Class
This class methods will rename files/folders present in a given location
by using provided list of blacklisted strings(blacklisted strings will be
removed from file/folder names). The operation can be done in recursive
way as well. A class attribute named log stores all rename operation details
"""
import os
import time
import traceback
import sys


class Bellerophone():

    def __init__(self, blacklist_file_location):
        """
        Initializes Bellerophone with blacklisted strings

        :param string blacklist_file_location: blacklist_file_location
        """
        self.blacklisted_strings = []
        if blacklist_file_location:
            self.blacklisted_strings = [
                line.replace('\n', '') for line in open(blacklist_file_location, "r")
                ]
        self.log = []
        self.unnamed_counter = 0


    def find_replace(self, object_type, object_name, location, old_string, new_string):
        """
        function to replace old_string with new_string in a given file/folder name
        """
        status = "UNKNOWN"
        comments = "FIND_REPLACE, FIND = " + old_string + " REPLACE = " + new_string
        new_name = object_name.replace(old_string, new_string)
        if object_name.__contains__(old_string):
            if object_type == "directory" and new_name == "":
                new_name = "unnamed" + str(self.unnamed_counter)
                self.unnamed_counter += 1
            elif object_type == "file" and new_name.split('.')[0] == "":
                new_name = \
                    "unnamed" + str(self.unnamed_counter) + new_name
                self.unnamed_counter += 1
            try:
                os.rename(
                    os.path.join(location, object_name),
                    os.path.join(location, new_name)
                )
                status = "success"
            except KeyboardInterrupt:
                raise
            except FileExistsError:
                new_name = \
                    "RENAMED_" + str(self.unnamed_counter) + "_" + new_name
                self.unnamed_counter += 1
                os.rename(
                    os.path.join(location, object_name),
                    os.path.join(location, new_name)
                )
                status = "RENAMED_FILE_EXISTS"
            except:
                comments = ''.join(
                    traceback.format_exception(*sys.exc_info())[-2:]
                    ).strip().replace('\n', ': ')
                status = "ERROR"
            self.log.append(
                (
                    location,
                    object_type,
                    object_name,
                    new_name,
                    old_string,
                    time.time(),
                    # print(
                    # datetime.datetime.fromtimestamp(
                    # time.time()
                    # ).strftime('%Y-%m-%d %H:%M:%S')
                    # )
                    status,
                    comments
                )
            )


    def rename(self, object_type, object_name, location):
        """
        function to rename files or directory by removing blacklisted
        string if there are any and returns a list contains renaming
        operational details

        :param string object_type: "file" or "directory"
        :param string object_name: name of the "file" or "directory"
        :param string location: absolute location of the directory where
        program should look for
        """
        status = "UNKNOWN"
        comments = "N.A"
        old_name = object_name
        removed_strings = ""
        # takes every string from the list of configured string(for removal
        # purposes) and
        # check whether it is present in the object name.
        for backlisted_string in self.blacklisted_strings:
            if backlisted_string in object_name:
                # object name has a string which is to be removed, so removes
                # the string
                object_name = object_name.replace(backlisted_string, '')
                if removed_strings != "":
                    removed_strings += ", "
                removed_strings += backlisted_string
        # if object name is changed, file has been renamed
        if old_name != object_name:
            if object_type == "directory" and object_name == "":
                object_name = "unnamed" + str(self.unnamed_counter)
                self.unnamed_counter += 1
            elif object_type == "file" and object_name.split('.')[0] == "":
                object_name = \
                    "unnamed" + str(self.unnamed_counter) + object_name
                self.unnamed_counter += 1
            try:
                os.rename(
                    os.path.join(location, old_name),
                    os.path.join(location, object_name)
                )
                status = "success"
            except KeyboardInterrupt:
                raise
            except FileExistsError:
                object_name = \
                    "RENAMED_" + str(self.unnamed_counter) + "_" + object_name
                self.unnamed_counter += 1
                os.rename(
                    os.path.join(location, old_name),
                    os.path.join(location, object_name)
                )
                status = "RENAMED_FILE_EXISTS"
            except:
                comments = ''.join(
                    traceback.format_exception(*sys.exc_info())[-2:]
                    ).strip().replace('\n', ': ')
                status = "ERROR"
            self.log.append(
                (
                    location,
                    object_type,
                    old_name,
                    object_name,
                    removed_strings,
                    time.time(),
                    # print(
                    # datetime.datetime.fromtimestamp(
                    # time.time()
                    # ).strftime('%Y-%m-%d %H:%M:%S')
                    # )
                    status,
                    comments
                )
            )

    def crawl_and_rename(self, location, is_recursive):
        """
        Function to scan through the target_location for files and folders for
        renaming

        :param string target_location: absolute location of the directory where
        program should look for
        :param boolean is_recursive: it will scan all folders present in the
        location recursively if this parameter is set to True
        """
        # look for the files and directories present at given location
        for child_object in os.scandir(location):
            if child_object.is_file():
                self.rename('file', child_object.name, location)
            elif child_object.is_dir():
                if is_recursive is True:
                    self.crawl_and_rename(
                        os.path.join(
                            location, child_object.name
                            ), True
                        )
                self.rename('directory', child_object.name, location)


    def crawl_and_find_and_replace(self, location, is_recursive, old_string, new_string):
        """
        Function to scan through the target_location for files and folders for
        find and replace

        :param string target_location: absolute location of the directory where
        program should look for
        :param boolean is_recursive: it will scan all folders present in the
        location recursively if this parameter is set to True
        """
        # look for the files and directories present at given location
        for child_object in os.scandir(location):
            if child_object.is_file():
                self.find_replace('file', child_object.name, location, old_string, new_string)
            elif child_object.is_dir():
                if is_recursive is True:
                    self.crawl_and_find_and_replace(
                        os.path.join(
                            location, child_object.name
                            ), True, old_string, new_string
                        )
                self.find_replace('directory', child_object.name, location, old_string, new_string)
