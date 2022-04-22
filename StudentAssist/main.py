from flask import jsonify, render_template, request
from notify import NotificationManager
from time_keeper import TimeKeeper
from config import sa_cfg
from __init__ import app
import db_connector
import logging


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()
log.info("Starting StudentAssist!") 

# Initialize the Notification Manager to communicate events to the users
notif_man = NotificationManager()

# Initialize the task time manager to keep track of task due dates
# (actually run call is called in main())
timeKeeper = TimeKeeper(notif_man)
timeKeeper.run()

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
@app.route("/user/tasks/edit", methods=["POST"])
def changeTaskState():
    # Pull the query params
    params = request.args
    uid = params.get("uid")
    taskName = params.get("taskName")
    newState = params.get("newState")
    return jsonify(db_connector.changeTask(uid, taskName, newState))


""" 
==================
REST Endpoints for entity creation
================== 
"""
# Creates a new task
@app.route("/create/task", methods=["POST"])
def createTask():
    # Pull the query params
    params = request.args
    userID=params.get("uid")
    taskName=params.get("taskName")
    taskStartDate=params.get("taskStartDate")
    taskDueDate=params.get("taskDueDate")
    taskProgress=params.get("taskProgress")
    return jsonify(db_connector.createTask(userID, taskName, taskStartDate, taskDueDate, taskProgress))

# Creates a new user
@app.route("/create/user", methods=["POST"])
def createUser():
    # Pull the query params
    params = request.args
    firstName=params.get("firstName")
    lastName=params.get("lastName")
    emailAddress=params.get("emailAddress")
    password=params.get("password")
    emailNotifs=params.get("emailNotifs")
    phoneNotifs=params.get("phoneNotifs")
    return jsonify(db_connector.createUser(firstName, lastName, emailAddress, password, emailNotifs, phoneNotifs))

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