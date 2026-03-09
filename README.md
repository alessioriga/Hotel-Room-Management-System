# Hotel Room Management System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![Database](https://img.shields.io/badge/Database-SQLite-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A **Flask-based web application** for managing hotel room bookings, arrivals, and in-house guests through a simple web interface.

---

# Overview

Hotels often struggle to manage room availability, bookings, and customer records when using manual processes or disconnected systems. This can lead to inefficiencies, double bookings, and poor customer experience.

This project provides a **centralised Hotel Room Management System** built with **Python, Flask, and SQLite**. The application allows hotel staff to manage reservations, assign rooms during check-in, and track guests currently staying in the hotel.

The system uses a **modular architecture**, making the codebase easier to maintain and extend for future improvements.

---

## Key Features

- **User authentication**: login-protected routes.
- **Room Management**: Room assignment on check-in.
- **Customer Management**: Store customer information and link them to bookings.
- **Booking System**: Check-in/check-out bookings and prevent assigning the same room to multiple bookings.

---

## Technology Stack

* **Frontend:** HTML5, CSS 
* **Backend:** Python 3.10+, Flask  
* **Database:** SQLite (`sqlite3`)  
* **Version Control:** GitHub

---

## Project Structure

- `app.py` – application entry point
- `routes/` – Flask route blueprints (e.g. `arrivals.py`, `home.py`)
- `db/` – database connection and repository functions
- `auth/` – authentication logic and decorators
- `templates/` – Jinja2 HTML templates
- `static/` – CSS/assets

---

## Installation

1. Open terminal in the project root
2. Install required packages:

```powershell
pip install Flask
```

---

## Run the Application

In the same terminal, run:

```powershell
python app.py
```

Then open:

`http://127.0.0.1:5000`

---

## Demo Credentials

For testing purposes:

- **Username:** `admin`
- **Password:** `1234`

---

## Future Improvements

- Role-based access control (admin/staff)
- Payment tracking
- Reporting and analytics
- REST API support
- Docker deployment

---

## Project Links

* [GitHub Repository: Code](https://github.com/alessioriga/Hotel-Room-Management-System)
* [Project Kanban Board](https://github.com/users/alessioriga/projects/3)
* [Project Roadmap](https://github.com/users/alessioriga/projects/3/views/4)

---

## License

This project is licensed under the MIT License.
