from flask import Flask, redirect
from auth.login import login_bp
from routes.home import home_bp


app = Flask(__name__)
app.secret_key = "ucenmanchester2026"

app.register_blueprint(login_bp)
app.register_blueprint(home_bp)

@app.route("/")
def start():
    return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)