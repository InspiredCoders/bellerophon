from config_manager import ConfigManager
from data_access_layer import DatabaseContext
from bellerophon import Bellerophone
import os
import argparse


def parse_args():
    """
    Function wrapping the argument parse for cli
    """
    parser = argparse.ArgumentParser(description='File rename util.')
    parser.add_argument('-p', '--path', required=True,
                        help='Path containing files to be renamed')
    parser.add_argument('-f', '--findreplace', action='store_true',
                        required=False,
                        help='Find and replace option for filenames')
    parser.add_argument('-s', '--search', required=False,
                        help='The word to be replaced')
    parser.add_argument('-d', '--dest', required=False,
                        help='Destination word')
    parser.add_argument('-b', '--blacklist', required=False,
                        help='File containing blacklisted names')

    args = vars(parser.parse_args())

    # Check for optional arguments
    if(args['findreplace'] and
       args['search'] is None and
       args['dest'] is None):

        parser.error('The --findreplace argument requires --search and -dest')
        exit

    return args


def rename(path):
    """
    Main code to run
    """
    program_config = ConfigManager()
    db_location = program_config.get_config("database_location")

    blacklist_file_location = program_config.get_config("blacklist_file")
    print(os.path.realpath(__file__))
    blacklist_file_location = os.path.join(
        ConfigManager.current_dir, blacklist_file_location
        )
    blacklisted_strings = [
        line.replace('\n', '') for line in open(blacklist_file_location, "r")
        ]
    # target_location = input(
    #     "Provide target directory location(fully qualified location):"
    #     )
    target_location = path
    bellerophone = Bellerophone(blacklist_file_location)
    print("Renaming is in progress...")
    bellerophone.crawl_and_rename(target_location, True)
    if bellerophone.log == []:
        print("No objects to rename!")
    else:
        print("Renaming is completed and saving tracks...")
    with DatabaseContext(db_location) as db:
        db.create_processing_history_table()
    with DatabaseContext(db_location) as db:
        for child in bellerophone.log:
            db.insert_into_processing_history_table(
                child[0], child[1], child[2],
                child[3], child[4], child[5], child[6], child[7]
            )
    print("Execution completed.")


def find_replace(path, source, destination):
    """
    Find and Replace
    """
    program_config = ConfigManager()
    db_location = program_config.get_config("database_location")

    target_location = path
    bellerophone = Bellerophone("")
    old_string = source
    if old_string:
        new_string = destination
        if new_string:
            bellerophone.crawl_and_find_and_replace(target_location, True,
                                                    old_string, new_string)
        if bellerophone.log == []:
            print("No objects to rename!")
        else:
            print("Renaming is completed and saving tracks...")
        with DatabaseContext(db_location) as db:
            db.create_processing_history_table()
        with DatabaseContext(db_location) as db:
            for child in bellerophone.log:
                db.insert_into_processing_history_table(
                    child[0], child[1], child[2],
                    child[3], child[4], child[5], child[6], child[7]
                )
    print("Execution completed.")


def main():
    args = parse_args()
    if(args['findreplace']):
        find_replace(args['path'], args['search'], args['dest'])
    else:
        rename(args['path'])


if __name__ == '__main__':
    main()
