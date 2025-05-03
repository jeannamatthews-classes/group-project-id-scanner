from flask import render_template
from tables import db, User, Scans, Machine
from . import admin_bp  # Use the existing admin blueprint

@admin_bp.route("/scans")
def view_scans():
    """View all scans in the system."""
    scans = Scans.query.order_by(Scans.date.desc(), Scans.time_in.desc()).all()
    return render_template("admin/scans.html", scans=scans)