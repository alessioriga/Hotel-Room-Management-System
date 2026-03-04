from flask import Blueprint, session, render_template
from auth.decorators import login_required
from db.connection import hotel_db_connection


home_bp = Blueprint("home_bp", __name__)

@home_bp.route('/home')
@login_required
def home():
    conn = hotel_db_connection()
    
    # Sum people and count bookings where status is 'Arriving'
    arrivals = conn.execute("""
        SELECT SUM(b.number_guests) AS total_people_arriving,
               COUNT(b.id) AS total_bookings
        FROM Booking b
        WHERE b.booking_status_id = '1'
    """).fetchone()

    in_house = conn.execute("""
        SELECT COUNT(DISTINCT b.room_id) AS rooms_occupied,
               SUM(b.number_guests) AS total_people_in_house
        FROM Booking b
        WHERE b.booking_status_id = '2'
    """).fetchone()


    sold_rooms = conn.execute("""
        SELECT COUNT(DISTINCT b.room_id) AS sold
        FROM Booking b
        JOIN BookingStatus bs ON b.booking_status_id = bs.id
        WHERE bs.type IN ('Checked-in', 'Arriving')
    """).fetchone()["sold"] or 0

    total_rooms = conn.execute("""
        SELECT COUNT(*) AS total 
        FROM Room
    """).fetchone()["total"] or 0

    available_rooms = total_rooms - sold_rooms
    
    conn.close()
    return render_template(
        "home.html",
        username=session["username"],
        arrivals_people=arrivals["total_people_arriving"] or 0,
        arrivals_bookings=arrivals["total_bookings"] or 0,
        in_house_rooms=in_house["rooms_occupied"] or 0,
        in_house_people=in_house["total_people_in_house"] or 0,
        room_summary_available=available_rooms,
        room_summary_sold=sold_rooms,
        room_summary_total=total_rooms
    )
