"""
scans

Handles scanning events
"""

# src/routes/scans.py
from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from tables import db, User, Scans, Machine

# Create a Blueprint for scanning events
bp = Blueprint('scans', __name__, url_prefix='/scan')

@bp.route('/in/<rfid>', methods=['POST'])
def scan_in(rfid):
    """Called by the RFID listener when a user scans in.
       Creates a new scan record (with time_out left NULL) and then redirects.
    """
    user = User.query.get_or_404(rfid)
    # Create a new row in Scans with time_out = NULL
    visit = Scans(rfid=rfid, date=datetime.today().date(), time_in=datetime.now().time())
    db.session.add(visit)
    db.session.commit()
    return redirect(url_for('index'))

@bp.route('/out/<rfid>', methods=['GET', 'POST'])
def scan_out(rfid):
    """Called by the RFID listener when a user scans out.
       GET: Displays the page (returning.html) where the user selects machines.
       POST: Receives the machine selection and updates the scan record.
    """
    user = User.query.get_or_404(rfid)

    if request.method == "GET":
        machines = Machine.query.order_by(Machine.name).all()
        return render_template("returning.html", user=user, machines=machines)
    
    open_visit = Scans.query.filter_by(rfid=rfid, time_out=None).first()
    if not open_visit:
        return "No open visit found", 400

    open_visit.time_out = datetime.now().time()

    # machines come in as list of machine IDs (as strings)
    ids = request.form.getlist("machine_ids")
    open_visit.machines = Machine.query.filter(Machine.id.in_(ids)).all()

    db.session.commit()
    return redirect(url_for("index"))
