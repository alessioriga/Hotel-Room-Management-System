import os
from db.setup_db import *

def initialise_database():
    """
    Initialise both admin.db and hotel_bookings.db if they don't exist.
    Reports the status for each database.
    """
    # Admin DB
    if not os.path.exists("admin.db"):
        print("Creating admin.db...")
        createUserTable()
        insertValueUser()
        print("admin.db created and initialised successfully.\n")
    else:
        print("admin.db already exists. Skipping creation.\n")
    
    # Hotel Bookings DB
    if not os.path.exists("hotel_bookings.db"):
        print("Creating hotel_bookings.db...")
        createHotelTable()
        insertValuesBookings()
        print("hotel_bookings.db created and initialised successfully.\n")
    else:
        print("hotel_bookings.db already exists. Skipping creation.\n")

    print("Database initialisation complete.")