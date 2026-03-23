import sqlite3 as db


def createUserTable() -> None:
    """
    Create the 'Users' table in the admin.db database if it does not exist.

    The table contains:
        - id (primary key, autoincrement)
        - account_name (text, not null)
        - username (text, unique, not null)
        - password (text, not null)
    """
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


def createHotelTable() -> None:
    """
    Create all necessary hotel-related tables in the hotel_bookings.db database.

    Tables created:
        - RoomType
        - Room
        - RoomStatus
        - Customer
        - PaymentMethod
        - BookingStatus
        - Billing
        - Booking
    """
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


def insertValueUser() -> None:
    """
    Insert default users into the Users table in admin.db.

    Users added:
        - Admin (username: admin, password: 1234)
        - John (username: john, password: 5678)

    Duplicate usernames are ignored.
    """
    connection = db.connect("admin.db")
    cursor = connection.cursor()

    users = [
        ("Admin", "admin", "1234"),
        ("John", "john", "5678")
    ]

    #Adds a user to the Users only if does not already exist (so there are not duplicate entries)
    cursor.executemany(
        "INSERT OR IGNORE INTO Users (account_name, username, password) VALUES (?, ?, ?)",
        users
    )

    connection.commit()
    connection.close()


def insertValuesBookings() -> None:
    """
    Insert initial data into hotel_bookings.db for hotel operations.

    This function populates the following tables:
        1. RoomType       - different room types with price and max occupancy
        2. RoomStatus     - status of rooms (Available, Occupied)
        3. Room           - individual rooms with type and status
        4. Customer       - guest details
        5. PaymentMethod  - payment types
        6. BookingStatus  - booking statuses (Arrival, Checked-in)
        7. Billing        - billing info for each booking
        8. Booking        - actual bookings linking rooms, customers, billing, and status

    Duplicate entries are ignored to prevent conflicts.
    """
    connection = db.connect("hotel_bookings.db")
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys= ON")

    # 1. Room Types
    roomTypeValues = [
        ("Single", 50.00, 1),
        ("Double", 80.00, 2),
        ("Twin", 90.00, 2),
        ("Small Family", 110.00, 3),
        ("Family", 140.00, 4),
        ("Suite", 160.00, 2)
    ]

    # 2. Rooms
    roomValues = [
        (101, 2, 1),(102, 2, 1),(103, 2, 1),(104, 2, 1),(105, 2, 1),(106, 2, 1),(107, 2, 1),(108, 1, 1),(109, 1, 1),(110, 1, 1),
        (201, 2, 2),(202, 2, 2),(203, 2, 2),(204, 2, 2),(205, 2, 2),(206, 2, 2),(207, 2, 2),(208, 1, 2),(209, 1, 2),(210, 1, 2),
        (301, 2, 3),(302, 2, 3),(303, 2, 3),(304, 2, 3),(305, 2, 3),(306, 2, 3),(307, 2, 3),(308, 1, 3),(309, 1, 3),(310, 1, 3),
        (401, 2, 4),(402, 2, 4),(403, 2, 4),(404, 2, 4),(405, 2, 4),(406, 2, 4),(407, 2, 4),(408, 1, 4),(409, 1, 4),(410, 1, 4),
        (501, 2, 5),(502, 2, 5),(503, 2, 5),(504, 2, 5),(505, 2, 5),(506, 2, 5),(507, 1, 5),(508, 1, 5),(509, 1, 5),(510, 1, 5),
        (601, 2, 6),(602, 2, 6),(603, 2, 6),(604, 2, 6),(605, 2, 6),(606, 2, 6),(607, 1, 6),(608, 1, 6),(609, 1, 6),(610, 1, 6)
    ]

    # 3. Customers
    customerValues = [
        ("Alex", "Stone","50 Bury Street, London, UK", "07700900001", "alex.stone01@example.com"),
        ("Maya", "Green", "12 Glenview Road, Cardiff, UK", "07700900002", "maya.green02@example.com"),
        ("Leo", "Carter", "88 Rosehill Avenue, Belfast, UK", "07700900003", "leo.carter03@example.com"),
        ("Nina", "Woods", "34 Thistle Lane, Edinburgh, UK", "07700900004", "nina.woods04@example.com"),
        ("Ethan", "Price", "17 Oakmere Drive, Manchester, UK", "07700900005", "ethan.price05@example.com"),
        ("Sara", "Miles", "29 Seaview Crescent, Swansea, UK", "07700900006", "sara.miles06@example.com"),
        ("Tom", "Baker", "73 Castlehill Road, Stirling, UK", "07700900007", "tom.baker07@example.com"),
        ("Lily", "Frost", "21 Elmwood Close, Birmingham, UK", "07700900008", "lily.frost08@example.com"),
        ("Ryan", "Cole", "46 Heatherbank Way, Dundee, UK", "07700900009", "ryan.cole09@example.com"),
        ("Zoe", "Hart", "5 Larkspur Grove, Liverpool, UK", "07700900010", "zoe.hart10@example.com"),

        ("Oscar", "Lane", "62 Windmill Street, Glasgow, UK", "07700900011", "oscar.lane11@example.com"),
        ("Eva", "Knight", "14 Primrose Court, Newcastle, UK", "07700900012", "eva.knight12@example.com"),
        ("Noah", "Blake", "38 Ashfield Road, Aberdeen, UK", "07700900013", "noah.blake13@example.com"),
        ("Ivy", "Rowe", "90 Willowbank Drive, Leeds, UK", "07700900014", "ivy.rowe14@example.com"),
        ("Max", "Turner", "27 Foxglove Rise, Inverness, UK", "07700900015", "max.turner15@example.com"),
        ("Clara", "Hughes", "11 Maplewood Avenue, Sheffield, UK", "07700900016", "clara.hughes16@example.com"),
        ("Ben", "Scott", "65 Bramble Lane, Derry", "07700900017", "ben.scott17@example.com"),
        ("Ella", "Young", "19 Fernhill Road, Nottingham, UK", "07700900018", "ella.young18@example.com"),
        ("Jack", "Reed", "82 Bluebell Way, Bangor, UK", "07700900019", "jack.reed19@example.com"),
        ("Ruby", "Hall", "6 Chestnut Grove, Leicester, UK", "07700900020", "ruby.hall20@example.com"),

        ("Theo", "West", "33 Rowan Street, York, UK", "07700900021", "theo.west21@example.com"),
        ("Mila", "Fox", "58 Hollybank Crescent, Limerick, UK", "07700900022", "mila.fox22@example.com"),
        ("Owen", "King", "24 Sycamore Drive, Coventry, UK", "07700900023", "owen.king23@example.com"),
        ("Isla", "Moon", "77 Pinehill Road, Bath, UK", "07700900024", "isla.moon24@example.com"),
        ("Luke", "Page", "9 Cloverfield Close, Oxford, UK", "07700900025", "luke.page25@example.com"),
        ("Nora", "Lake", "41 Hazelwood Lane, Cambridge, UK", "07700900026", "nora.lake26@example.com"),
        ("Adam", "Snow", "15 Birchfield Avenue, Reading, UK", "07700900027", "adam.snow27@example.com"),
        ("Tara", "Bloom", "70 Meadowbank Road, Bristol, UK", "07700900028", "tara.bloom28@example.com"),
        ("Finn", "Ray", "3 Honeysuckle Way, Cheltenham, UK", "07700900029", "finn.ray29@example.com"),
        ("Vera", "Cloud", "86 Lavender Rise, Brighton, UK", "07700900030", "vera.cloud30@example.com"),

        ("Archie", "Stone", "28 Moorfield Crescent, Exeter, UK", "07700900031", "archie.stone31@example.com"),
        ("Maya-Lynn", "Green", "13 Rosewood Drive, Plymouth, UK", "07700900032", "mayalynn.green32@example.com"),
        ("Leona", "Carter", "55 Ashgrove Lane, Southampton, UK", "07700900033", "leona.carter33@example.com"),
        ("Nico", "Woods", "36 Beechwood Road, Norwich, UK", "07700900034", "nico.woods34@example.com"),
        ("Ethaniel", "Price", "20 Daffodil Court, Wrexham, UK", "07700900035", "ethaniel.price35@example.com"),
        ("Sarah", "Miles", "74 Highland View, Perth, UK", "07700900036", "sarah.miles36@example.com"),
        ("Thomas", "Baker", "8 Glenwood Drive, Armagh, UK", "07700900037", "thomas.baker37@example.com"),
        ("Lilian", "Frost", "47 Oakridge Avenue, Derby, UK", "07700900038", "lilian.frost38@example.com"),
        ("Ryland", "Cole", "31 Sunflower Way, Lincoln, UK", "07700900039", "ryland.cole39@example.com"),
        ("Zoey", "Hart", "22 Hawthorn Crescent, Durham, UK", "07700900040", "zoey.hart40@example.com")
    ]

    # 4. Payment Methods
    paymentMethodValues = [
        ("Credit Card",),
        ("Debit Card",),
    ]

    # 5. Booking Statuses
    bookingStatusValues = [
        ("Arrival",),
        ("Checked-in",)
    ]

    # 6. Billing
    billingValues = [
        (2, 50.0, 100.0),
        (3, 80.0, 240.0),
        (3, 90.0, 270.0),
        (4, 50.0, 200.0),
        (4, 140.0, 560.0),
        (4, 80.0, 320.0),
        (4, 160.0, 640.0),
        (5, 110.0, 550.0),
        (5, 90.0, 450.0),
        (6, 140.0, 840.0),
        
        (3, 50.0, 150.0),
        (4, 80.0, 320.0),
        (4, 90.0, 360.0),
        (5, 110.0, 550.0),
        (5, 140.0, 700.0),
        (4, 80.0, 320.0),
        (2, 50.0, 100.0),
        (6, 160.0, 960.0),
        (5, 90.0, 450.0),
        (6, 110.0, 660.0),

        (5, 140.0, 700.0),
        (6, 160.0, 960.0),
        (6, 50.0, 300.0),
        (7, 80.0, 560.0),
        (6, 90.0, 540.0),
        (7, 110.0, 770.0),
        (6, 140.0, 840.0),
        (7, 160.0, 1120.0),
        (6, 110.0, 660.0),
        (7, 90.0, 630.0),

        (6, 80.0, 480.0),
        (7, 50.0, 350.0),
        (6, 160.0, 960.0),
        (7, 110.0, 770.0),
        (6, 90.0, 540.0),
        (7, 140.0, 980.0),
        (6, 160.0, 960.0),
        (7, 110.0, 770.0),
        (6, 80.0, 480.0),
        (7, 50.0, 350.0)
    ]

    # 7. Bookings
    bookingValues = [
        # Checked-in (status=2)
        (1, 1, 1, 1, 2, 600001, "06-04-2029", "08-04-2029", 1),  # Single, 2 nights, 1 guest
        (2, 11, 2, 2, 2, 600002, "06-04-2029", "09-04-2029", 2),  # Double, 3 nights, 2 guests
        (3, 21, 3, 1, 2, 600003, "06-04-2029", "09-04-2029", 2),  # Twin, 3 nights, 2 guests
        (4, 2, 4, 1, 2, 600004, "06-04-2029", "10-04-2029", 1),  # Single, 4 nights, 1 guest
        (5, 41, 5, 2, 2, 600005, "06-04-2029", "10-04-2029", 4),  # Family, 4 nights, 4 guests
        (6, 12, 6, 2, 2, 600006, "06-04-2029", "10-04-2029", 2),  # Double, 4 nights, 2 guests
        (7, 51, 7, 1, 2, 600007, "06-04-2029", "10-04-2029", 2),  # Suite, 4 nights, 2 guests
        (8, 31, 8, 2, 2, 600008, "06-04-2029", "11-04-2029", 3),  # Small Family, 5 nights, 3 guests
        (9, 22, 9, 1, 2, 600009, "06-04-2029", "11-04-2029", 2),  # Twin, 5 nights, 2 guests
        (10, 42, 10, 2, 2, 600010, "06-04-2029", "12-04-2029", 4), # Family, 6 nights, 4 guests

        # Arriving (status=1)
        (11, 3, 11, 1, 1, 600011, "06-04-2029", "09-04-2029", 1),   # Single, 3 nights
        (12, 13, 12, 2, 1, 600012, "06-04-2029", "10-04-2029", 2),   # Double, 4 nights
        (13, 23, 13, 2, 1, 600013, "06-04-2029", "10-04-2029", 2),   # Twin, 4 nights
        (14, 32, 14, 1, 1, 600014, "06-04-2029", "11-04-2029", 3),   # Small Family, 5 nights
        (15, 43, 15, 1, 1, 600015, "06-04-2029", "11-04-2029", 4),   # Family, 5 nights
        (16, 14, 16, 2, 1, 600016, "06-04-2029", "10-04-2029", 2),   # Double, 4 nights
        (17, 4, 17, 1, 1, 600017, "06-04-2029", "08-04-2029", 1),   # Single, 2 nights
        (18, 52, 18, 2, 1, 600018, "06-04-2029", "12-04-2029", 2),   # Suite, 6 nights
        (19, 24, 19, 2, 1, 600019, "06-04-2029", "11-04-2029", 2),   # Twin, 5 nights
        (20, 33, 20, 2, 1, 600020, "06-04-2029", "12-04-2029", 3),   # Small Family, 6 nights

        (21, 44, 21, 1, 1, 600021, "06-04-2029", "11-04-2029", 4),   # Family, 5 nights
        (22, 53, 22, 2, 1, 600022, "06-04-2029", "12-04-2029", 2),   # Suite, 6 nights
        (23, 5, 23, 1, 1, 600023, "06-04-2029", "12-04-2029", 1),   # Single, 6 nights
        (24, 15, 24, 2, 1, 600024, "06-04-2029", "13-04-2029", 2),   # Double, 7 nights
        (25, 25, 25, 1, 1, 600025, "06-04-2029", "12-04-2029", 2),   # Twin, 6 nights
        (26, 34, 26, 1, 1, 600026, "06-04-2029", "13-04-2029", 3),   # Small Family, 7 nights
        (27, 45, 27, 2, 1, 600027, "06-04-2029", "12-04-2029", 4),   # Family, 6 nights
        (28, 54, 28, 2, 1, 600028, "06-04-2029", "13-04-2029", 2),   # Suite, 7 nights
        (29, 35, 29, 1, 1, 600029, "06-04-2029", "12-04-2029", 3),   # Small Family, 6 nights
        (30, 26, 30, 1, 1, 600030, "06-04-2029", "13-04-2029", 2),   # Twin, 7 nights

        (31, 16, 31, 2, 1, 600031, "06-04-2029", "12-04-2029", 2),   # Double, 6 nights
        (32, 6, 32, 1, 1, 600032, "06-04-2029", "13-04-2029", 1),   # Single, 7 nights
        (33, 55, 33, 2, 1, 600033, "06-04-2029", "12-04-2029", 2),   # Suite, 6 nights
        (34, 36, 34, 1, 1, 600034, "06-04-2029", "13-04-2029", 3),   # Small Family, 7 nights
        (35, 27, 35, 2, 1, 600035, "06-04-2029", "12-04-2029", 2),   # Twin, 6 nights
        (36, 46, 36, 2, 1, 600036, "06-04-2029", "13-04-2029", 4),   # Family, 7 nights
        (37, 56, 37, 1, 1, 600037, "06-04-2029", "12-04-2029", 2),   # Suite, 6 nights
        (38, 37, 38, 2, 1, 600038, "06-04-2029", "13-04-2029", 3),   # Small Family, 7 nights
        (39, 17, 39, 2, 1, 600039, "06-04-2029", "12-04-2029", 2),   # Double, 6 nights
        (40, 7, 40, 1, 1, 600040, "06-04-2029", "13-04-2029", 1)    # Single, 7 nights
    ]

    # 8. Room Statuses
    # Insert Room Statuses
    cursor.executemany(
        "INSERT OR IGNORE INTO RoomStatus (room_status) VALUES (?)",
        [("Available",),("Occupied",)] 
    )

    # Insert Room Types
    cursor.executemany(
        "INSERT OR IGNORE INTO RoomType (type_name, price_per_night, max_occupancy) VALUES (?, ?, ?)",
        roomTypeValues
    )

    # Insert Rooms
    cursor.executemany(
        "INSERT OR IGNORE INTO Room (room_number, room_status_id, room_type_id) VALUES (?, ?, ?)",
        roomValues
    )

    # Insert Customers
    cursor.executemany(
        "INSERT OR IGNORE INTO Customer (name, surname, address, phone, email) VALUES (?, ?, ?, ?, ?)",
        customerValues
    )

    # Insert Payment Methods
    cursor.executemany(
        "INSERT OR IGNORE INTO PaymentMethod (type) VALUES (?)",
        paymentMethodValues
    )

    # Insert Booking Statuses
    cursor.executemany(
        "INSERT OR IGNORE INTO BookingStatus (type) VALUES (?)",
        bookingStatusValues
    )

    # Insert Billing
    cursor.executemany(
        "INSERT OR IGNORE INTO Billing (number_of_nights, price_per_night, total_amount) VALUES (?, ?, ?)",
        billingValues
    )

    # Insert Bookings
    cursor.executemany(
        """INSERT OR IGNORE INTO Booking 
        (customer_id, room_id, billing_id, payment_method_id, booking_status_id, booking_number, 
            check_in_date, check_out_date, number_guests)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        bookingValues
    )

    connection.commit()
    connection.close()
    