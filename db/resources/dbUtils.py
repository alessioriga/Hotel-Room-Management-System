from db.connection import hotel_db_connection

def get_bookings_by_status(booking_status_id: int) -> list[dict]:
    """
    Retrieve bookings filtered by booking status ID.

    Args:
        booking_status_id (int): Status ID to filter bookings.
            For example, 1 = Arriving, 2 = In-House.

    Returns:
        list[dict]: List of bookings with customer, room info, and status.
    """
    connection = hotel_db_connection()
    bookings = connection.execute("""
        SELECT 
            b.id, 
            b.booking_number, 
            b.check_in_date, 
            b.check_out_date, 
            b.number_guests,
            c.surname || ' ' || c.name AS customer_name,
            r.room_number, 
            rt.type_name AS room_type,
            bs.type AS booking_status
        FROM Booking b 
        JOIN Customer c ON b.customer_id = c.id
        LEFT JOIN Room r ON b.room_id = r.id
        LEFT JOIN RoomType rt ON r.room_type_id = rt.id
        JOIN BookingStatus bs ON b.booking_status_id = bs.id
        WHERE b.booking_status_id = ?
    """, (booking_status_id,)).fetchall()
    connection.close()
    return bookings

def get_booking_by_id(booking_id: int) -> dict | None:
    """
    Retrieve detailed information for a booking by its ID.

    Args:
        booking_id (int): The ID of the booking to retrieve.

    Returns:
        dict | None: Dict representing the booking, or None if not found.
    """
    connection = hotel_db_connection()
    
    booking = connection.execute("""
        SELECT 
            b.id,
            b.booking_number,
            b.check_in_date,
            b.check_out_date,
            b.number_guests,
            
            c.name || ' ' || c.surname AS customer_name,
            c.address,
            c.phone,
            c.email,
            
            r.id AS room_id,
            r.room_number,
            rt.type_name AS room_type,
            
            bs.type AS booking_status,
            b.billing_id,
            pm.type AS payment_method,
            bl.number_of_nights,
            bl.price_per_night,
            bl.total_amount
            

        FROM Booking b
        JOIN Customer c ON b.customer_id = c.id
        JOIN Room r ON b.room_id = r.id
        JOIN RoomType rt ON r.room_type_id = rt.id
        JOIN BookingStatus bs ON b.booking_status_id = bs.id
        JOIN Billing bl ON b.billing_id = bl.id
        JOIN PaymentMethod pm ON b.payment_method_id = pm.id
        WHERE b.id = ?
    """, (booking_id,)).fetchone()
    
    connection.close()
    return booking

def search_bookings(keyword: str) -> list[dict]:
    """
    Search bookings by customer name, surname, phone, or booking number.

    Args:
        keyword (str): The keyword to search for.

    Returns:
        list[dict]: List of bookings matching the search criteria.
    """
    connection = hotel_db_connection()

    search = f"%{keyword}%"

    results = connection.execute("""
        SELECT 
            b.id,
            b.booking_number,
            b.check_in_date,
            b.check_out_date,
            b.number_guests,

            c.surname || ' ' || c.name AS customer_name,
            c.phone,

            r.room_number,
            rt.type_name AS room_type,

            bs.type AS booking_status

        FROM Booking b

        JOIN Customer c ON b.customer_id = c.id
        LEFT JOIN Room r ON b.room_id = r.id
        LEFT JOIN RoomType rt ON r.room_type_id = rt.id
        JOIN BookingStatus bs ON b.booking_status_id = bs.id

        WHERE
            c.name LIKE ?
            OR c.surname LIKE ?
            OR c.phone LIKE ?
            OR b.booking_number LIKE ?

        ORDER BY b.check_in_date DESC
    """, (search, search, search, search)).fetchall()

    connection.close()

    return results
