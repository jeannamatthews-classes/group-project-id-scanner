"""
tables

Contrains definitions of database tables and sets up the database
"""




from flask_sqlalchemy import SQLAlchemy  # Lets us interact with the database using Python classes instead of raw SQL

# Create the SQLAlchemy db instance (not bound to an app yet)
db = SQLAlchemy()

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

# Function to initialize the database with the Flask app
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
