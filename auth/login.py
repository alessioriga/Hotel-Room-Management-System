from flask import Blueprint, render_template, request, session, redirect, url_for
from db.connection import login_db_connection


login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = login_db_connection()
        user = connection.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password)).fetchone()
        connection.close()

        if user:
            session['username'] = user['username']
            session['account_name'] = user['account_name']
            return redirect (url_for('home_bp.home')) 
        else:
            return render_template('login.html', error="Incorrect username or password")
 
    # When the user first opens /login in the browser, they are doing a GET request.
    # request.method == 'POST' is False, because they haven't submitted the form yet.
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_bp.login'))