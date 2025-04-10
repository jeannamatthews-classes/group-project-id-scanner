"""
app

Is the main file that creates and configures the Flask application, and starts the server
"""


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy  # Lets us interact with the database using Python classes instead of raw SQL
import os  # Used to construct the path to the SQLite file
from tables import init_db  # Import the database initialization function from models.py
from config import Config
from routes.scans import bp as scans_bp  # Import the Blueprint from scans.py
from routes.users import bp as users_bp

# Configure SQLite database
# I think some of the stuff here belongs in the config file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "../static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "../templates")

# Creates the Flask application object
app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)

# Register the Blueprint
app.register_blueprint(scans_bp)
app.register_blueprint(users_bp)

# Configure database
app.config.from_object(Config)

# Initialize the database (binds the models to the app)
init_db(app)

# Defines route for homepage (/) that returns a message to confirm the app is running
@app.route("/")
def index():
    return render_template("index.html")

# Runs Flask development server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
