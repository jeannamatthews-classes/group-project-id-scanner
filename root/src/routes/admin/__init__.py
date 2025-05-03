from flask import Blueprint

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Defer importing subroutes to avoid circular imports
def register_admin_routes(app):
    from . import auth, dashboard, users, scans, machines

    app.register_blueprint(admin_bp)
