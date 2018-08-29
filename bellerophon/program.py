from config_manager import ConfigManager
from data_access_layer import DatabaseContext
from bellerophon import Bellerophone
import os


def main():
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
    target_location = input(
        "Provide target directory location(fully qualified location):"
        )
    bellerophone = Bellerophone(blacklisted_strings)
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

if __name__ == '__main__':
    main()
