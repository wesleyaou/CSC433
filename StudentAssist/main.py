# RESTful naming conventions https://restfulapi.net/resource-naming/

from flask import Flask, jsonify, render_template
import logging

# TODO: Make logging level dynamic and cleaner
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()
log.info("Starting StudentAssist!") 

# Initialize the app object and set the static/templates folders
# TODO: Make this class based
app = Flask(__name__, static_folder="web/static", template_folder="web/templates")


""" 
==================
UI HTML Pages
================== 
"""

# Returns the main landing page of PILOT
@app.route("/home", methods=["GET"])
def serve_home():
    return render_template("home.html")

@app.route("/calendar", methods=["GET"])
def serve_calendar():
    return render_template("calendar.html")

@app.route("/settings", methods=["GET"])
def serve_settings():
    return render_template("settings.html")


"""
==================
Main application runner
================== 
"""

# Main method used to start the flask server
def main():
    log.info("Starting Flask Application...")
    app.run(host="0.0.0.0", port=5000)

# Run the Application
if __name__ == "__main__":
    main()