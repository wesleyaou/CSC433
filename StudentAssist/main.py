# RESTful naming conventions https://restfulapi.net/resource-naming/

from flask import Flask, jsonify, render_template
from config import sa_cfg
from __init__ import app
import db_connector
import logging


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()
log.info("Starting StudentAssist!") 

# Initialize the app object and set the static/templates folders
# app = Flask(__name__, static_folder="web/static", template_folder="web/templates")


""" 
==================
UI HTML Pages
================== 
"""

# Returns the main landing page of StudentAssist
@app.route("/home", methods=["GET"])
def serve_home():
    return render_template("home.html")


""" 
==================
REST Endpoints for data retrieval
================== 
"""

# Returns user account info
# TODO: Probably not the most secure method of retrival... but time crunch?
@app.route("/user/info/uid=<uid>", methods=["POST"])
def get_user_info(uid):
    return jsonify(db_connector.getUser(uid))

# Returns user's tasks
@app.route("/user/tasks/uid=<uid>", methods=["POST"])
def get_user_tasks(uid):
    return jsonify(db_connector.getTasks(uid))


""" 
==================
REST Endpoints for data editing
================== 
"""
@app.route("/user/tasks/edit/uid=<uid>&taskName=<taskName>&newState=<newState>", methods=["POST"])
def changeTaskState(uid, taskName, newState):
    return jsonify(db_connector.changeTask(uid, taskName, newState))

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