from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import sa_cfg
from __init__ import app
import logging
import os

log = logging.getLogger()

db_path = sa_cfg["database"]["path"]

db = None

def dbExists(db_path):
    return os.path.isfile(db_path)

if dbExists(db_path=db_path):
    # Initialize the database connector
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + db_path
    db = SQLAlchemy(app)
else:
    log.error("Failed to find database file at: " + db_path)

# DB Models
class User(db.Model):
    __tablename__ = "Users"
    userID = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), unique=False, nullable=False)
    lastName = db.Column(db.String(20), unique=False, nullable=False)
    emailAddress = db.Column(db.String(20), unique=False, nullable=False)
    phoneNumber = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    emailNotifs = db.Column(db.String(20), unique=False, nullable=False)
    phoneNotifs = db.Column(db.String(20), unique=False, nullable=False)
 
    # def __repr__(self):
    #     return f"Name : {self.first_name}, Age: {self.age}"

class Tasks(db.Model):
    __tablename__ = "Tasks"
    userID = db.Column(db.Integer, db.ForeignKey(User.userID), unique=False, primary_key=True)
    taskName = db.Column(db.String(20), unique=False, primary_key=True)
    taskStartDate = db.Column(db.String(20), unique=False, nullable=False)
    taskDueDate = db.Column(db.String(20), unique=False, nullable=False)
    taskProgress = db.Column(db.String(20), unique=False, nullable=False)


# Update a specific task
def changeTask(userID, taskName, newState):
    if db:
        db.session.query(Tasks).filter(Tasks.userID == userID, Tasks.taskName == taskName).update({"taskProgress" : newState})
        db.session.commit()
        return {"success" : "task updated"}
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
        log.error("couldn't load database!")
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



# Brief informal testing
if __name__ == "__main__":
    # p = User(firstName="test", lastName="user", emailAddress="test@gmail.com", password="testPass", emailNotifs="true", phoneNotifs="false")
    # db.session.add(p)
    # db.session.commit()
    # t = Tasks(userID=2, taskName="CSC433 Final Project #5", taskStartDate="02/14/2022", taskDueDate="04/27/2022", taskProgress="inprog")
    # db.session.add(t)
    # db.session.commit()
    # query = db.select([Tasks])
    # engine = db.create_engine("sqlite:///" + db_path, {})
    # result = engine.execute(query).fetchall()
    # print(result)
    tasks = getTasks(2)["tasks"]
    for task in tasks:
        print(task)
        print("*" * 16)

    print(getUser(2))

    changeTask(2, "CSC433 Final Project #3", "inprog")