from flask import Blueprint, session, render_template
from auth.decorators import login_required
from db.connection import hotel_db_connection


home_bp = Blueprint("home_bp", __name__)

