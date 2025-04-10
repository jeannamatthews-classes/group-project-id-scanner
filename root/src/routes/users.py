"""
users

Handles new user registration events

NOTE: will not be working until changes are made to newmember.html to reflect the database tables
"""

# src/routes/users.py
from flask import Blueprint, render_template, request, redirect, url_for
from tables import db, User, Scans  # Import the database and User mode
from datetime import datetime

# Create a Blueprint for user-related routes
bp = Blueprint('users', __name__, url_prefix='/users')

# Route to display the new user registration form and handle form submissions
@bp.route('/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        # Retrieve data from the form
        rfid = request.form.get('rfid')
        student_id = request.form.get('student-id')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        # Create a new User instance with the submitted data
        new_user = User(
            rfid=rfid,
            student_id=student_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        # Add the new user to the database session and commit
        db.session.add(new_user)
        db.session.commit()

        user = User.query.get_or_404(rfid)
    
        # Create a new row in scans table with time_out = none
        visit = Scans(rfid=rfid, date=datetime.today().date(), time_in=datetime.now().time())
        db.session.add(visit)
        db.session.commit()
    
        # After registration, redirect to the same page or another page as desired
        return redirect(url_for('users.new_user'))

    # For GET requests, render the registration form
    return render_template('newmember.html')
