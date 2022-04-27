from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin
from StudentAssist.config import sa_cfg
from StudentAssist.__init__ import app
import logging
import os
import bcrypt

log = logging.getLogger()

db_path = sa_cfg["database"]["path"]

db = None

try:
    # Initialize the database connector
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + db_path
    db = SQLAlchemy(app)
except:
    log.error("Failed to find database file at: " + db_path)

# DB Models
# Godly user password management concepts from:
# https://stackoverflow.com/questions/52190989/how-to-encrypt-password-using-python-flask-security-using-bcrypt#52191670
class User(db.Model, UserMixin):
    __tablename__ = "Users"
    userID = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), unique=False, nullable=False)
    lastName = db.Column(db.String(20), unique=False, nullable=False)
    emailAddress = db.Column(db.String(20), unique=False, nullable=False)
    phoneNumber = db.Column(db.String(20), unique=False, nullable=False)
    passwordHash = db.Column(db.String(128), unique=False, nullable=False)
    emailNotifs = db.Column(db.String(20), unique=False, nullable=False)
    phoneNotifs = db.Column(db.String(20), unique=False, nullable=False)

    @property
    def password(self):
        raise AttributeError('password not readable')
    
    @password.setter
    def password(self, password):
        self.passwordHash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        
class Tasks(db.Model):
    __tablename__ = "Tasks"
    userID = db.Column(db.Integer, db.ForeignKey(User.userID), unique=False, primary_key=True)
    taskName = db.Column(db.String(20), unique=False, primary_key=True)
    taskStartDate = db.Column(db.String(20), unique=False, nullable=False)
    taskDueDate = db.Column(db.String(20), unique=False, nullable=False)
    taskProgress = db.Column(db.String(20), unique=False, nullable=False)

# Task and user creation
def createTask(userID, taskName, taskStartDate, taskDueDate, taskProgress):
    if db:
        newTask = Tasks(userID=userID, 
                        taskName=taskName, 
                        taskStartDate=taskStartDate, 
                        taskDueDate=taskDueDate, 
                        taskProgress=taskProgress)

        db.session.add(newTask)
        db.session.commit()
        return {"success" : "task created"}
    else:
        log.error("couldn't load database for task creation!")
        return {"error" : "couldn't load database!"}

def createUser(firstName, lastName, emailAddress, phoneNumber, password, emailNotifs, phoneNotifs):
    if db:
        newUser = User(firstName=firstName, 
                        lastName=lastName, 
                        emailAddress=emailAddress,
                        phoneNumber=phoneNumber,
                        password=password, 
                        emailNotifs=emailNotifs, 
                        phoneNotifs=phoneNotifs)
        
        db.session.add(newUser)
        db.session.commit()

        return {"success" : "Account created! Please login."}
    else:
        log.error("couldn't load database for user creation!")
        return {"error" : "couldn't load database!"}

# Update a specific task
def changeTask(userID, taskName, newState):
    if db:
        if newState == "delete":
            db.session.query(Tasks).filter(Tasks.userID == userID, Tasks.taskName == taskName).delete()
            db.session.commit()
        else:
            db.session.query(Tasks).filter(Tasks.userID == userID, Tasks.taskName == taskName).update({"taskProgress" : newState})
            db.session.commit()
        log.debug("Updated task: \"" + taskName + "\" for user ID: " + str(userID) + " to have a status of \"" + newState + "\"")
        return {"success" : "task updated"}
    else:
        log.error("couldn't load database!")
        return {"error" : "couldn't load database!"}

# Update a specific task
def changeUser(userID, toChange, newValue):
    if db:
        db.session.query(User).filter(User.userID == userID).update({toChange : newValue})
        db.session.commit()
        log.debug("Updated field \"" + toChange + "\" on account with user ID: " + str(userID))
        return {"success" : "Account updated!"}
    else:
        log.error("couldn't load database!")
        return {"error" : "couldn't load database!"}

# Functions to pull info from tables, all outputs are in JSON
def getTasks(userID):
    if db:
        tasks = []
        result = db.session.query(Tasks).filter(Tasks.userID == userID)
        for row in result:
            tasks.append({"userID" : row.userID, 
                        "taskName" : row.taskName, 
                        "taskStartDate" : row.taskStartDate,
                        "taskDueDate" : row.taskDueDate,
                        "taskProgress" : row.taskProgress})
        return {"tasks" : tasks}
    else:
        log.error("couldn't load database to pull tasks!")
        return {"error" : "couldn't load database!"}

def getAllTasks():
    if db:
        tasks = []
        result = db.session.query(Tasks)
        for row in result:
            tasks.append({"userID" : row.userID, 
                        "taskName" : row.taskName, 
                        "taskStartDate" : row.taskStartDate,
                        "taskDueDate" : row.taskDueDate,
                        "taskProgress" : row.taskProgress})
        return {"tasks" : tasks}
    else:
        log.error("couldn't load database to pull tasks!")
        return {"error" : "couldn't load database!"}

def getUser(userID):
    if db:
        result = db.session.query(User).filter(User.userID == userID)[0]
        user_info = {"userID" : result.userID,
                    "firstName" : result.firstName,
                    "lastName" : result.lastName,
                    "emailAddress" : result.emailAddress,
                    "phoneNumber" : result.phoneNumber,
                    "emailNotifs" : result.emailNotifs,
                    "phoneNotifs" : result.phoneNotifs}
        
        return {"user" : user_info}
    else:
        log.error("couldn't load database to pull user!")
        return {"error" : "couldn't load database!"}

def getAllUsers():
    if db:
        users = []
        result = db.session.query(User)
        for row in result:
            users.append({"userID" : row.userID, 
                        "passwordHash" : row.passwordHash, 
                        "emailAddress" : row.emailAddress})

        return {"users" : users}
    else:
        log.error("couldn't load database to pull tasks!")
        return {"error" : "couldn't load database!"}

def verifyPassword(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


# Brief informal testing
if __name__ == "__main__":
    p = User(firstName="Wesley", lastName="Appler", emailAddress="wesleyaou@protonmail.com", phoneNumber="3153352552@vtext.com", password="testPass", emailNotifs="true", phoneNotifs="true")
    db.session.add(p)
    db.session.commit()
    # t = Tasks(userID=2, taskName="CSC433 Final Project #5", taskStartDate="02/14/2022", taskDueDate="04/27/2022", taskProgress="inprog")
    # db.session.add(t)
    # db.session.commit()
    # query = db.select([Tasks])
    # engine = db.create_engine("sqlite:///" + db_path, {})
    # result = engine.execute(query).fetchall()
    # print(result)
    # tasks = getTasks(2)["tasks"]
    # for task in tasks:
    #     print(task)
    #     print("*" * 16)

    # print(getUser(2))

    # changeTask(2, "CSC433 Final Project #3", "inprog")