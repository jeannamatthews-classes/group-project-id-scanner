"""
csv_export

Exports all rows from the Scans table, printing:
  student_id, date, time_in, time_out, total_time, machines
to stdout in CSV format.
"""

import csv
import sys
from datetime import datetime

from app import app
from tables import Scans, User, db

def export_scans():
    writer = csv.writer(sys.stdout, lineterminator="\n")

    # Header row (no id, no rfid)
    writer.writerow([
        "student_id",
        "date",
        "time_in",
        "time_out",
        "total_time",
        "machines"
    ])

    with app.app_context():
        scans = Scans.query.order_by(Scans.date, Scans.time_in).all()
        for scan in scans:
            # Lookup the user to get student_id
            user = db.session.get(User, scan.rfid)
            student_id = user.student_id if user else ""

            # Format date/time
            date_str     = scan.date.isoformat()
            time_in_str  = scan.time_in.isoformat()
            time_out_str = scan.time_out.isoformat() if scan.time_out else ""

            # Compute total_time as timedelta string
            if scan.time_out:
                dt_in  = datetime.combine(scan.date, scan.time_in)
                dt_out = datetime.combine(scan.date, scan.time_out)
                total_td = dt_out - dt_in
                total_str = str(total_td)
            else:
                total_str = ""

            # Join machine names
            machine_list = ";".join(m.name for m in scan.machines)

            writer.writerow([
                student_id,
                date_str,
                time_in_str,
                time_out_str,
                total_str,
                machine_list
            ])

if __name__ == "__main__":
    export_scans()
