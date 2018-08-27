import sqlite3


class Database(object):
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

    def create_table(self, table_name, columns_with_attributes):
        """
        Function to create a table
        :param string table_name: name of the table
        :param list columns_with_attributes: list of tuples which contains
        columns and attributes. Each tuple should represent one column and
        its properties.
        For Example:
            Below list indicates two columns, First entry of the tuple should
            be column name and second entry should be its properties
            [
                ('col1', 'INTEGER PRIMARY KEY'),
                ('col2', 'TEXT')
            ]
        """
        cols = ""
        for column_details in columns_with_attributes:
            if cols != "":
                cols += ","
            cols += ' '.join(column_details)
        self.cursor.execute('CREATE TABLE {}({})'.format(table_name, cols))

    def insert(self, table_name, col_list, values_list):  
        self.cursor.execute(
            'INSERT INTO {table}{cols} VALUES{values}'
            .format(table=table_name, cols=col_list, values=values_list)
        )

c = [('col1', 'INTEGER PRIMARY KEY'), ('col2', 'TEXT')]
print(c)
with Database("a.db") as db:
    db.insert('db_1', "('col1', 'col2')", "(1, 'ONE')")
