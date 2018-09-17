from config_manager import ConfigManager
from data_access_layer import DatabaseContext
from bellerophon import Bellerophone
import os


def greet():
    print('--------------------')
    print('    BELLEROPHON')
    print('--------------------')
    print()


def rename():
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
    target_location = input(
        "Provide target directory location(fully qualified location):"
        )
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


def find_replace():
    """
    Find and Replace
    """
    program_config = ConfigManager()
    db_location = program_config.get_config("database_location")

    target_location = input(
        "Provide target directory location(fully qualified location):"
        )
    bellerophone = Bellerophone("")
    old_string = input("FIND:")
    if old_string:
        new_string = input("REPLACE:")
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
    greet()
    while True:
        print('Choose [B]ulk rename, [R]ename or [Q]uit')
        option = input('Your option: ')
        if str(option).upper() == 'B':
            rename()
        elif str(option).upper() == 'R':
            find_replace()
        elif str(option).upper() == 'Q':
            print('Goodbye')
            break
        else:
            print("Invalid input")
            print()


if __name__ == '__main__':
    main()
