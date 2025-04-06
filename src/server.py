from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy  # Lets us interact with the database using Python classes instead of raw SQL
import os  # Used to construct the path to the SQLite file

app = Flask(__name__)  # Creates the Flask application object

# Configure SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Gets the absolute path to the folder
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"  # Configures database connection
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disables a feature we don't need

db = SQLAlchemy(app)  # Creates the database object and links it with the Flask app

# Table for users
class User(db.Model):
    rfid = db.Column(db.String(32), primary_key=True)  # RFID from ID card as primary key
    student_id = db.Column(db.String(20), unique=True, nullable=False)  # School ID (unique but not primary)
    username = db.Column(db.String(64), unique=True, nullable=False)  # School login username
    first_name = db.Column(db.String(50), nullable=False)  # First name
    last_name = db.Column(db.String(50), nullable=False)  # Last name

    # Debug helper: shows a readable string when a User object is printed
    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

# Table for machines
class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Machine {self.name}>"

# Association table for many-to-many relationship between Scans and Machine
scan_machine = db.Table('scan_machine',
    db.Column('scan_id', db.Integer, db.ForeignKey('scans.id'), primary_key=True),
    db.Column('machine_id', db.Integer, db.ForeignKey('machine.id'), primary_key=True)
)

# Table for instances of sign-ins (Scans)
class Scans(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each scan
    rfid = db.Column(db.String(32), db.ForeignKey('user.rfid'), nullable=False)  # Links to the User table
    date = db.Column(db.Date, nullable=False)  # Date of the scan
    time_in = db.Column(db.Time, nullable=False)  # Time in
    time_out = db.Column(db.Time, nullable=True)  # Time out (nullable for ongoing sessions)

    # Many-to-many relationship: each scan can have multiple machines, and each machine can be used in many scans
    machines = db.relationship('Machine', secondary=scan_machine, lazy='subquery',
                               backref=db.backref('scans', lazy=True))

    # Debug helper: shows a readable string when a Scans object is printed
    def __repr__(self):
        return f"<Scans {self.rfid} on {self.date}>"

# Create the database
# If database.db already exists, then nothing changes unless new tables are added
with app.app_context():
    db.create_all()

# Defines route for homepage (/) that returns a message to confirm the app is running
@app.route("/")
def index():
    return "Database setup complete!"

# Runs Flask development server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

