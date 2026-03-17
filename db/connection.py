import sqlite3 as db

def login_db_connection() -> db.Connection:
    """
    Create a connection to the admin database.

    The connection is used for authentication queries
    such as validating login credentials.

    Returns:
        db.Connection: SQLite connection object with Row factory enabled.
    """
    connection: db.Connection = db.connect('admin.db')
    connection.row_factory = db.Row
    return connection

def hotel_db_connection() -> db.Connection:
    """
    Create a connection to the hotel bookings database.

    The connection is used for all operational data such as
    bookings, rooms, customers, and billing.

    Returns:
        db.Connection: SQLite connection object with Row factory enabled.
    """
    connection: db.Connection = db.connect('hotel_bookings.db')   
    connection.row_factory = db.Row
    return connection

