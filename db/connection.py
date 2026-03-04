import sqlite3 as db


def login_db_connection():
    connection = db.connect('admin.db')
    connection.row_factory = db.Row
    return connection

def hotel_db_connection():
    connection = db.connect('hotel_bookings.db')   
    connection.row_factory = db.Row
    return connection

