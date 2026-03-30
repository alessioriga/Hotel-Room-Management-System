from flask import Flask, redirect
from auth.login import login_bp
from routes.home import home_bp
from routes.arrivals import arrivals_bp
from routes.in_house import in_house_bp
from routes.reports import reports_bp
from routes.search import search_bp
from db.initialise_db import initialise_database

# Initialise databases before creating the app
initialise_database()

app = Flask(__name__)
app.secret_key = "ucenmanchester2026"

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(home_bp)
app.register_blueprint(arrivals_bp)
app.register_blueprint(in_house_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(search_bp)

@app.route("/")
def start() -> str:
    """
    Redirect the root URL to the login page.

    Returns:
        str: Redirect response to /login
    """
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=False)

