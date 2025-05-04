# root/src/routes/admin/export.py

from flask import Blueprint, render_template, Response
from io import StringIO
from datetime import datetime
import csv

from tables import db, User, Scans
from . import admin_bp  # Make sure this import happens AFTER admin_bp is defined in __init__.py


@admin_bp.route("/export")
def export_page():
    return render_template("admin/export.html")


@admin_bp.route("/export/download")
def download_csv():
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Student ID", "Full Name", "Username", "Date",
        "Time In", "Time Out", "Total Time", "Was Auto", "Machines"
    ])

    scans = Scans.query.order_by(Scans.date, Scans.time_in).all()

    for scan in scans:
        user = db.session.get(User, scan.rfid)
        student_id = user.student_id if user else ""
        username   = user.username if user else ""
        full_name  = f"{user.first_name} {user.last_name}" if user else ""

        date_str = scan.date.isoformat()
        time_in_str = scan.time_in.strftime("%H:%M:%S") if scan.time_in else ""
        time_out_str = scan.time_out.strftime("%H:%M:%S") if scan.time_out else ""

        if scan.time_in and scan.time_out:
            dt_in = datetime.combine(scan.date, scan.time_in)
            dt_out = datetime.combine(scan.date, scan.time_out)
            total_time = str(dt_out - dt_in)
        else:
            total_time = ""

        was_auto = "Yes" if getattr(scan, "was_auto_signed_out", False) else "No"
        machines = ";".join(m.name for m in scan.machines)

        writer.writerow([
            student_id, full_name, username,
            date_str, time_in_str, time_out_str,
            total_time, was_auto, machines
        ])

    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=scan_data.csv"}
    )
