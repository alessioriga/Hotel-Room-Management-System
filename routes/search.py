from flask import Blueprint, render_template, request
from auth.decorators import login_required
from db.repository import search_bookings

search_bp = Blueprint("search_bp", __name__)

@search_bp.route("/search", methods=["GET", "POST"])
@login_required
def search() -> str:
    """
    Handle booking search requests by keyword.
    
    GET: Show empty search page.
    POST: Perform search and display results.
    
    Returns:
        str: Rendered HTML page with search results.
    """

    results: list[dict] = []
    keyword: str = ""

    if request.method == "POST":
        keyword = request.form["keyword"]
        results = search_bookings(keyword)

    return render_template(
        "search.html",
        results=results,
        keyword=keyword
    )
