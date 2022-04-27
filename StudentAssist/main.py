from flask import jsonify, render_template, request, redirect, url_for, session
from StudentAssist.notify import NotificationManager
from StudentAssist.time_keeper import TimeKeeper
from StudentAssist.config import sa_cfg
from StudentAssist.__init__ import app
import StudentAssist.db_connector as db_connector
import StudentAssist.login as login_utils
import logging
import urllib.parse


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
Authentication endpoints
================== 
"""

# Main login REST endpoint
@app.route("/user/login", methods=["POST"])
def login():
    login_result = login_utils.validate_login(request.json["emailAddress"], request.json["password"])
    log.info("A login was attempted using email: \"" + request.json["emailAddress"] + "\"...")
    if login_result.get("uid"):
        log.info("Login attempt for \"" + request.json["emailAddress"] + "\" was successful, resulting in " + str(login_result.get("uid")))
        session["logged_in"] = True
    else:
        log.info("Login attempt for \"" + request.json["emailAddress"] + "\" failed!")

    return login_result

# Validate the user's email
@app.route("/user/validate-email", methods=["POST"])
def validate_email():
    return jsonify(login_utils.validate_email(request.json["emailAddress"]))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session["logged_in"] = False
    return redirect(url_for("serve_login"))

""" 
==================
UI HTML Pages
================== 
"""

# If just the url is typed, redirect to the home page
@app.route("/", methods=["GET"])
def redirect_home():
    return login_utils.check_auth(session, redirect(url_for("serve_home")))

# Returns the main landing page of StudentAssist
@app.route("/home", methods=["GET"])
def serve_home():
    return login_utils.check_auth(session, render_template("home.html"))

# Main login page
@app.route("/login", methods=["GET"])
def serve_login():
    return render_template("login.html")

""" 
==================
REST Endpoints for data retrieval
================== 
"""

# Returns user account info
# TODO: Probably not the most secure method of retrival... but time crunch?
@app.route("/user/info", methods=["POST"])
def get_user_info():
    params = request.args
    uid = params.get("uid")

    if uid == "undefined":
        session["logged_in"] = False
        return jsonify({"user" : None})

    return login_utils.check_auth(session, jsonify(db_connector.getUser(uid)))

# Returns user's tasks
@app.route("/user/tasks", methods=["POST"])
def get_user_tasks():
    params = request.args
    uid = params.get("uid")

    if uid == "undefined":
        session["logged_in"] = False
    
    return login_utils.check_auth(session, jsonify(db_connector.getTasks(uid)))


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
    taskName = urllib.parse.unquote(params.get("taskName"))
    newState = urllib.parse.unquote(params.get("newState"))
    
    return login_utils.check_auth(session, jsonify(db_connector.changeTask(uid, taskName, newState)))

@app.route("/user/edit", methods=["POST"])
def changeUser():
    # Pull the query params
    params = request.args
    uid = params.get("uid")
    toChange = urllib.parse.unquote(params.get("toChange"))
    newValue = urllib.parse.unquote(params.get("newValue"))
    if toChange == "name":
        if not session["logged_in"]:
            return redirect(url_for(serve_login))
        
        db_connector.changeUser(uid, "firstName", newValue.split("-")[0])
        return(db_connector.changeUser(uid, "lastName", newValue.split("-")[1]))

    elif toChange == "notifPrefs":
        if not session["logged_in"]:
            return redirect(url_for(serve_login))
        
        db_connector.changeUser(uid, "phoneNotifs", newValue.split("-")[0])
        return(db_connector.changeUser(uid, "emailNotifs", newValue.split("-")[1]))
    
    else:
        return login_utils.check_auth(session, jsonify(db_connector.changeUser(uid, toChange, newValue)))

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
    return login_utils.check_auth(session, jsonify(db_connector.createTask(userID, taskName, taskStartDate, taskDueDate, taskProgress)))

# Creates a new user
@app.route("/create/user", methods=["POST"])
def createUser():
    # Pull the query params
    params = request.json
    firstName=params.get("firstName")
    lastName=params.get("lastName")
    emailAddress=params.get("emailAddress")
    phoneNumber=params.get("phoneNumber")
    password=params.get("password")
    emailNotifs=params.get("emailNotifs")
    phoneNotifs=params.get("phoneNotifs")
    return jsonify(db_connector.createUser(firstName, lastName, emailAddress, phoneNumber, password, emailNotifs, phoneNotifs))

"""
==================
Main application runner
================== 
"""

# Main method used to start the flask server
def main():
    try:
        log.info("Starting Flask Application...")
        app.run(host="0.0.0.0", port=5000)
    except:
        session["logged_in"]

# Run the Application
if __name__ == "__main__":
    main()
