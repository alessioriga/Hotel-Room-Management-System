from db.connection import hotel_db_connection
from db.resources.dbUtils import *


def get_arriving_bookings() -> list[dict]:
    """Retrieve all bookings with status 'Arriving'."""
    return get_bookings_by_status(1)


def get_in_house_bookings() -> list[dict]:
    """Retrieve all bookings with status 'In-House'."""
    return get_bookings_by_status(2)


def get_room_report() -> list[dict]:
    """
    Retrieve the current status of all rooms along with guest info if occupied.

    Returns:
        list[dict]: Each dict represents a room with its type, status, and guest info.
    """
    connection = hotel_db_connection()

    rooms = connection.execute("""
        SELECT 
            r.room_number,
            rt.type_name,
            rs.room_status,

            c.surname || ' ' || c.name AS guest_name,
            b.check_in_date,
            b.check_out_date

        FROM Room r

        JOIN RoomType rt ON r.room_type_id = rt.id
        JOIN RoomStatus rs ON r.room_status_id = rs.id

        LEFT JOIN Booking b 
            ON r.id = b.room_id 
            AND b.booking_status_id = 2

        LEFT JOIN Customer c 
            ON b.customer_id = c.id

        ORDER BY r.room_number
    """).fetchall()

    connection.close()

    return rooms

def get_available_rooms_for_booking(type_name : str) -> list[dict]:
    """
    Retrieve all available rooms of a given type.

    Args:
        type_name (str): The room type to filter by.

    Returns:
        list[dict]: List of available rooms matching the type.
    """
    connection = hotel_db_connection()
    rooms = connection.execute("""
        SELECT r.id, r.room_number, rt.type_name AS room_type
        FROM Room r
        JOIN RoomType rt ON r.room_type_id = rt.id
        JOIN RoomStatus rs ON r.room_status_id = rs.id
        WHERE rs.room_status = 'Available' AND rt.type_name = ?
        ORDER BY r.room_number
    """, (type_name,)).fetchall()
    connection.close()
    return rooms

def check_in_booking(booking_id : int, new_room_id: int) -> None:
    """
    Check a booking into a room, updating booking and room statuses.

    Args:
        booking_id (int): Booking ID to check in.
        new_room_id (int): Room ID to assign to the booking.

    Raises:
        ValueError: If the room is not available or does not exist.
    """
    connection = hotel_db_connection()

    # Check if the new room is actually available
    room = connection.execute("""
        SELECT room_status_id
        FROM Room
        WHERE id = ?
    """, (new_room_id,)).fetchone()

    if not room or room["room_status_id"] != 1:  # 1 = Available
        connection.close()
        raise ValueError(f"Room {new_room_id} is already occupied or does not exist.")

    # Get current room assigned to this booking
    current_booking = connection.execute("""
        SELECT room_id 
        FROM Booking 
        WHERE id = ?
    """, (booking_id,)).fetchone()

    current_room_id = current_booking["room_id"] if current_booking else None

    # 1. Update the booking with new room and status
    connection.execute("""
        UPDATE Booking
        SET booking_status_id = 2,
            room_id = ?
        WHERE id = ?
    """, (new_room_id, booking_id))

    # 2. Mark the new room as Occupied
    connection.execute("""
        UPDATE Room
        SET room_status_id = 2
        WHERE id = ?
    """, (new_room_id,))

    # 3. If there was a previous room and it’s different, mark it as Available
    if current_room_id and current_room_id != new_room_id:
        connection.execute("""
            UPDATE Room
            SET room_status_id = 1
            WHERE id = ?
        """, (current_room_id,))

    connection.commit()
    connection.close()


def check_out_to_arriving(booking_id: int) -> None:
    """
    Check a booking out and revert it to 'Arriving' status, freeing the room.

    Args:
        booking_id (int): The booking ID to check out.
    """
    connection = hotel_db_connection()

    # Get current room
    booking = connection.execute("""
        SELECT room_id
        FROM Booking
        WHERE id = ?
    """, (booking_id,)).fetchone()

    room_id = booking["room_id"] if booking else None

    # 1. Set booking back to Arriving
    connection.execute("""
        UPDATE Booking
        SET booking_status_id = 1
        WHERE id = ?
    """, (booking_id,))

    # 2. Free the room
    if room_id:
        connection.execute("""
            UPDATE Room
            SET room_status_id = 1
            WHERE id = ?
        """, (room_id,))

    connection.commit()
    connection.close()

