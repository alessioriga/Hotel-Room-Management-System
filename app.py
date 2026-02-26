from flask import Flask, redirect

app = Flask(__name__)
app.secret_key = "ucenmanchester2026"

@app.route("/")
def start():
    return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)