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

def createHotelTable():
    connection = db.connect('hotel_bookings.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys= ON")

    roomTypeTable = """
        CREATE TABLE IF NOT EXISTS RoomType (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_name TEXT NOT NULL,
        price_per_night REAL NOT NULL,
        max_occupancy INTEGER NOT NULL
        )
    """

    roomTable = """
        CREATE TABLE IF NOT EXISTS Room (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_number INTEGER NOT NULL UNIQUE,
        room_status_id INTEGER NOT NULL, -- 1 = Available, 2 = Occupied
        room_type_id INTEGER NOT NULL,
        FOREIGN KEY (room_type_id) REFERENCES RoomType(id) ON DELETE RESTRICT,
        FOREIGN KEY (room_status_id) REFERENCES RoomStatus(id) ON UPDATE CASCADE
        )
    """

    roomStatusTable = """
        CREATE TABLE IF NOT EXISTS RoomStatus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_status TEXT NOT NULL
        )
    """

    customerTable = """
        CREATE TABLE IF NOT EXISTS Customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        address TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL
        )
    """

    paymentMethodTable = """
        CREATE TABLE IF NOT EXISTS PaymentMethod (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL
        )
    """

    bookingStatusTable = """
        CREATE TABLE IF NOT EXISTS BookingStatus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL
        )
    """

    billingTable = """
        CREATE TABLE IF NOT EXISTS Billing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number_of_nights INTEGER NOT NULL,
        price_per_night REAL NOT NULL,
        total_amount REAL NOT NULL
        )
    """

    bookingTable = """
        CREATE TABLE IF NOT EXISTS Booking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        room_id INTEGER NOT NULL,
        billing_id INTEGER NOT NULL,
        payment_method_id INTEGER NOT NULL,
        booking_status_id INTEGER NOT NULL,
        booking_number INTEGER UNIQUE NOT NULL,
        check_in_date TEXT NOT NULL,
        check_out_date TEXT NOT NULL,
        number_guests INTEGER NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE RESTRICT,
        FOREIGN KEY (room_id) REFERENCES Room(id) ON DELETE RESTRICT,
        FOREIGN KEY (billing_id) REFERENCES Billing(id) ON DELETE RESTRICT,
        FOREIGN KEY (payment_method_id) REFERENCES PaymentMethod(id) ON DELETE RESTRICT,
        FOREIGN KEY (booking_status_id) REFERENCES BookingStatus(id) ON DELETE RESTRICT
        )
    """

    cursor.execute(roomTypeTable)
    cursor.execute(roomTable)
    cursor.execute(roomStatusTable)
    cursor.execute(bookingTable)
    cursor.execute(customerTable)
    cursor.execute(paymentMethodTable)
    cursor.execute(billingTable)
    cursor.execute(bookingStatusTable)
    
    connection.commit()
    connection.close()
    print("Hotel bookings tables created successfully.")