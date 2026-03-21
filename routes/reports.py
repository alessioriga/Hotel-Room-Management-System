from flask import Blueprint, render_template
from auth.decorators import login_required
from db.repository import get_room_report

reports_bp = Blueprint('reports_bp', __name__)

@reports_bp.route("/reports")
@login_required
def reports() -> str:
    """
    Display a report of all rooms, including current status and guest information.

    Returns:
        str: Rendered HTML page for room reports.
    """
    rooms: list[dict] = get_room_report()
    
    rooms_list: list[dict] = []

    for room in rooms:

        display_status = "Vacant" if room["guest_name"] is None else room["room_status"]

        rooms_list.append({
            "room_number": room["room_number"],
            "type_name": room["type_name"],
            "status": display_status,
            "guest_name": room["guest_name"] or "-",
            "check_in_date": room["check_in_date"] or "-",
            "check_out_date": room["check_out_date"] or "-"
        })

    return render_template("reports.html", rooms=rooms_list)

