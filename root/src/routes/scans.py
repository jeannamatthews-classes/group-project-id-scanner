"""
scans

Handles scanning events
"""

# src/routes/users.py
from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from tables import db, User, Scans, Machine

# Create a Blueprint for user-related routes
bp = Blueprint('scans', __name__, url_prefix='/scan')

@bp.route('/new/<rfid>', methods=['POST'])
def scan_in(rfid):
    """ Called by rfid_listener.py when an ID is scanned in """
    user = User.query.get_or_404(rfid)
    
    # Create a new row in scans table with time_out = none
    visit = Scans(rfid=rfid, date=datetime.today().date(), time_in=datetime.now())
    db.session.add(visit)
    db.session.commit()
    return redirect(url_for('index'))

@bp.route('/new/<rfid>', methods=['GET', 'POST'])
def scan_out(rfid):
    """ Called by rfid_listener at the end of a visit
            - prompt for machines used, then update the row in the scans table """
            
    user = User.query.get_or_404(rfid)

    
    if request.method == "GET":
        machines = Machine.query.order_by(Machine.name).all()
        return render_template("returning.html", user=user, machines=machines)
    
    open_visit = Scans.query.filter_by(rfid=rfid, time_out=None).first()
    if not open_visit:
        return "No open visit found", 400

    open_visit.time_out = datetime.now().time()

    # machines come back as list of IDs
    ids = request.form.getlist("machine_ids")
    open_visit.machines = Machine.query.filter(Machine.id.in_(ids)).all()

    db.session.commit()
    return redirect(url_for("index"))