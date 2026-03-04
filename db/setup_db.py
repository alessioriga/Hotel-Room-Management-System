import sqlite3 as db


def createUserTable():
    connection = db.connect('admin.db')
    cursor = connection.cursor()
    
    usersTable = """
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )
    """
    
    cursor.execute(usersTable)
    connection.commit()
    connection.close()
    print("User table created successfully.")