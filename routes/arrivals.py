from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth.decorators import login_required
from db.repository import *
from db.resources.dbUtils import *
from sqlite3 import Connection

arrivals_bp = Blueprint("arrivals_bp", __name__)

@arrivals_bp.route("/arrivals")
@login_required
def arrivals() -> str:
    """
    Display all bookings with 'Arriving' status.

    Returns:
        str: Rendered HTML page for arrivals.
    """
    bookings: list[dict] = get_arriving_bookings()

    return render_template("arrivals.html", bookings=bookings)

@arrivals_bp.route("/arrivals/<int:booking_id>", methods=["GET", "POST"])
@login_required
def view_booking(booking_id: int) -> str:
    """
    View and manage a single booking.
    
    GET: Show booking details and available rooms.  
    POST: Check in booking to selected room.
    
    Args:
        booking_id (int): ID of the booking to view.
    
    Returns:
        str: Rendered HTML page or redirect.
    """
    booking: dict | None = get_booking_by_id(booking_id)
    if not booking:
        return redirect(url_for("arrivals_bp.arrivals"))

    # Only show rooms of the same type as the booking and are available
    rooms: list[dict] = get_available_rooms_for_booking(booking["room_type"])

    # Include current room if the booking already has it assigned
    # Only if it is still marked as Available (status_id = 1)
    if booking["room_id"] is not None:
        connection: Connection = hotel_db_connection()
        room_status: dict | None = connection.execute("""
            SELECT room_status_id
            FROM Room
            WHERE id = ?
        """, (booking["room_id"],)).fetchone()
        connection.close()

        if room_status and room_status["room_status_id"] == 1:
            rooms.append({
                "id": booking["room_id"],
                "room_number": booking["room_number"],
                "room_type": booking["room_type"]
            })

    if request.method == "POST":
        room_id: int = int(request.form["room_id"])
        try:
            check_in_booking(booking_id, room_id)
            return redirect(url_for("in_house_bp.in_house"))
        except ValueError as e:
            # Room already occupied
            flash(str(e), "error")
            return redirect(request.url)

    return render_template(
        "booking_details.html",
        booking=booking,
        rooms=rooms
    )
