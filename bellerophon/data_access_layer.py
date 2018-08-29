import sqlite3


class DatabaseContext(object):
    def __init__(self, db_location):
        self.connection = sqlite3.connect(db_location)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
            print(Exception)
        else:
            self.connection.commit()
        self.connection.close()

    def clean_variable(variable):
        """
        Function to remove non alphanumerical characters from a value of
        a variable
        :param string variable: variable which contains a value to clean
        """
        return ''.join(char for char in variable if char.isalnum())

    def create_processing_history_table(self):
        sql = (
            "CREATE TABLE IF NOT EXISTS tbl_processing_history"
            "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "location TEXT,"
            "object_type TEXT,"
            "file_name TEXT,"
            "new_name TEXT,"
            "removed_strings TEXT,"
            "timestamp REAL,"
            "status TEXT,"
            "comments TEXT);"
            )
        self.cursor.execute(sql)

    def insert_into_processing_history_table(
            self,
            location,
            object_type,
            file_name,
            new_name,
            removed_strings,
            timestamp,
            status,
            comments
            ):
        self.cursor.execute(
            'INSERT INTO tbl_processing_history'
            '(location, object_type, file_name, new_name, removed_strings'
            ', timestamp, status, comments) VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
            (
                location,
                object_type,
                file_name,
                new_name,
                removed_strings,
                timestamp,
                status,
                comments
                )
        )
        self.connection.commit()
