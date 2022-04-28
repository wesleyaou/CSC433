import StudentAssist.db_connector as db_connector
from flask import render_template


def validate_login(email_in, password_in):
    all_users = db_connector.getAllUsers().get("users")

    for user in all_users:
        email = user.get("emailAddress")
        passwordHash = user.get("passwordHash")
        uid = user.get("userID")

        if email_in == email:
            if db_connector.verifyPassword(password_in, passwordHash):
                return {"uid": uid}
            else:
                return {"error": "Invalid password!"}
    
    return {"error": "Email address does not belong to a valid user!"}

# Check if an email exists in users
def validate_email(email_in):
    all_users = db_connector.getAllUsers().get("users")

    for user in all_users:
        email = user.get("emailAddress")

        if email_in == email:
            return {"email" : True}

    return {"email" : False}

# The flask-security module can do this more safer but timecrunch
def check_auth(session, intended_return):
    if session.get("logged_in"):
        return intended_return
    else:
        return render_template("login.html")
