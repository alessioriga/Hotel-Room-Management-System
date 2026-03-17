from flask import Blueprint, render_template, request, session, redirect, url_for
from db.connection import login_db_connection


login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods = ['GET', 'POST'])
def login() -> object:
    """
    Handle user authentication.

    GET:
        Displays the login page.

    POST:
        Validates the username and password against the Users table.
        If credentials are correct, the user session is created and the
        user is redirected to the home page.

    Returns:
        object: A rendered HTML template or a redirect response.
    """
    if request.method == 'POST':
        username: str = request.form['username']
        password: str = request.form['password']

        connection: object = login_db_connection()
        user: object = connection.execute(
            'SELECT * FROM Users WHERE username = ? AND password = ?', (username, password)
        ).fetchone()

        connection.close()

        if user:
            session['username'] = user['username']
            session['account_name'] = user['account_name']
            return redirect (url_for('home_bp.home')) 
        else:
            return render_template('login.html', error="Incorrect username or password")
 
    return render_template('login.html')

@login_bp.route('/logout')
def logout() -> object:
    """
    Log the user out of the application.

    Removes the username from the session and redirects
    the user back to the login page.

    Returns:
        object: Redirect response to the login page.
    """
    session.pop('username', None)
    return redirect(url_for('login_bp.login'))
