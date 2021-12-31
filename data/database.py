import sqlite3 as sql

class Database:
    def __init__(self):
        self.connection = sql.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.row_factory = sql.Row

        self.set_up()
    

    def set_up(self):
        self.execute_statement('''
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            img_path TEXT
        )
        ''')
        self.execute_statement('''
        CREATE TABLE IF NOT EXISTS Card (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            language TEXT,
            code TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES User(id)
        )
        ''')


    def execute_statement(self, sql, parameters=None):
        if parameters == None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, parameters)
            

        self.connection.commit()


    def execute_query(self, query, parameters=None):
        if parameters == None:
            self.cursor.execute(query)
        else:    
            self.cursor.execute(query, parameters)

        return self.cursor.fetchall()
    
    def close_connection(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()