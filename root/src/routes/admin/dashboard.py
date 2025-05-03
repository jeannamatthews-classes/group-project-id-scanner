from flask import render_template, session, redirect, url_for
from . import admin_bp

@admin_bp.route("/dashboard")
def dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))
    return render_template("admin/dashboard.html")
