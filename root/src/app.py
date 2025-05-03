"""
app

Is the main file that creates and configures the Flask application, and starts the server
"""

from scheduler_setup import setup_scheduler
from flask import Flask, render_template
import os
from config import Config
from tables import init_db

from routes.scans import bp as scans_bp
from routes.users import bp as users_bp
from routes.kiosk import kiosk_bp
from routes.admin import register_admin_routes  # updated import

# Configure paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "../static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "../templates")

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)

# Register standard blueprints
app.register_blueprint(scans_bp)
app.register_blueprint(users_bp)
app.register_blueprint(kiosk_bp)

# Register admin routes via function (fixes circular import)
register_admin_routes(app)

# Load configuration
app.config.from_object(Config)

# Initialize the database (creates tables if needed)
init_db(app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    setup_scheduler(app)
    app.run(host="0.0.0.0", port=5000, debug=True)

