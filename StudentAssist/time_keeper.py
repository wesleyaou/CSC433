import StudentAssist.db_connector as db_connector
import logging
import threading
import time



class TimeKeeper:
    def __init__(self, notificationManager):
        # NotificationManager object from notify.py
        self.notification_man = notificationManager

        # Time vars
        self.ONE_HOUR = {"seconds": 3600, "phrase": "1 hour"}
        self.SIX_HOURS = {"seconds": 21600, "phrase": "6 hours"}
        self.ONE_DAY = {"seconds": 86400, "phrase": "1 day"}
        self.TWO_DAYS = {"seconds" : 172800, "phrase" : "2 days"}
        self.ONE_WEEK = {"seconds": 604800, "phrase": "1 week"}

        # Interval to check for tasks that could be within a threshold
        self.INTERVAL = 118

        self.log = logging.getLogger()

        self.log.debug("Task time manager started!")

    # Method to check times, returns "1 hour", "6 hours", "1 day" or None depending on criteria met
    # Allows about a 120 second (2 min) window. Update interval is 1.25 mins, but this gives room for error
    # in Python's timekeeping.
    def compare_time_ranges(self, timeDiff):
        for threshold in [self.ONE_HOUR, self.SIX_HOURS, self.ONE_DAY, self.TWO_DAYS, self.ONE_WEEK]:
            threshold_floor = threshold["seconds"] - 60
            threshold_ceil = threshold["seconds"] + 60
            if threshold_ceil > timeDiff > threshold_floor:
                return threshold["phrase"]

    # Will iterate through all tasks, comparing times to see if they're in the 1h, 6h, and 24h range 
    def check_times(self):
        pull_tasks = db_connector.getAllTasks()
        if pull_tasks.get("error"):
            self.log.error("Failed to query for user notification preferences, error: " + pull_tasks.get("error"))
        else:
            tasks = pull_tasks.get("tasks")
            # Get current epoch time
            currentTime = time.time()
            for task in tasks:
                taskEndTime = task.get("taskDueDate")
                if taskEndTime:
                    taskEndTime = float(taskEndTime)
                    time_result = self.compare_time_ranges(taskEndTime - currentTime)
                    if time_result:
                        task_notif_msg = "There is approximately " + time_result + " until your task: \"" + task.get("taskName") + "\" is due!"
                        self.notification_man.send_notification(task["userID"], task_notif_msg)
            
        time.sleep(self.INTERVAL)
    
    def main(self):
        while True:
            self.check_times()

    def run(self):
        timeThr = threading.Thread(target=self.main, name = 'time_manager')
        timeThr.start()


if __name__ == "__main__":
    import notify

    # Create tasks at different intervals ahead of time to test each notification ability
    db_connector.createTask(userID=2, taskName="Task One Hour", taskStartDate=int(time.time()), taskDueDate=int(time.time()) + 3660, taskProgress="inprog")
    db_connector.createTask(userID=2, taskName="Task Six Hours", taskStartDate=int(time.time()), taskDueDate=int(time.time()) + 21720, taskProgress="inprog")
    db_connector.createTask(userID=2, taskName="Task 24 Hours", taskStartDate=int(time.time()), taskDueDate=int(time.time()) + 86460, taskProgress="inprog")

    notifMan = notify.NotificationManager()

    timeKeeper = TimeKeeper(notifMan)

    timeKeeper.run()
