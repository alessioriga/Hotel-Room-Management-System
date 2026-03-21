from flask import Blueprint, render_template, request, redirect, url_for
from auth.decorators import login_required
from db.repository import *


in_house_bp = Blueprint("in_house_bp", __name__)

@in_house_bp.route("/in_house")
@login_required
def in_house() -> str:
    """
    Display all bookings currently checked in ('In-House' status).

    Returns:
        str: Rendered HTML page for in-house bookings.
    """
    bookings: list[dict] = get_in_house_bookings()

    return render_template("in_house.html", bookings=bookings)

@in_house_bp.route("/checkout/<int:booking_id>", methods=["GET", "POST"])
@login_required
def checkout_booking(booking_id: int) -> str:
    """
    View booking checkout page or perform checkout.

    GET: Show checkout details and available rooms.  
    POST: Check out booking and redirect to arrivals.

    Args:
        booking_id (int): ID of the booking to check out.

    Returns:
        str: Rendered HTML page or redirect response.
    """

    if request.method == "POST":

        check_out_to_arriving(booking_id)

        return redirect(url_for("arrivals_bp.arrivals"))


    booking: dict = get_booking_by_id(booking_id)

    rooms: list[dict] = get_available_rooms_for_booking(booking["room_type"])

    return render_template(
        "checkout_details.html",
        booking=booking,
        rooms=rooms
    )