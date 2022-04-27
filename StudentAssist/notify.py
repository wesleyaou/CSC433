from datetime import datetime
from StudentAssist.config import sa_cfg
from email.message import EmailMessage
import StudentAssist.db_connector as db_connector
import logging
import smtplib

log = logging.getLogger()

class NotificationManager:
    def __init__(self):
        self.email_address = sa_cfg["notifications"]["email"]
        self.email_password = sa_cfg["notifications"]["password"]

    # Send the notification based off the user's preferences
    def send_notification(self, uid, notif_text):
        user_info = db_connector.getUser(uid)
        if "error" in user_info.keys():
            log.error("Failed to query for user notification preferences, error: " + user_info.get("error"))
        else:
            notif_text = self.format_notification(notif_text)
            text_notifs = user_info.get("user").get("phoneNotifs")
            email_notifs = user_info.get("user").get("emailNotifs")

            if text_notifs == "true":
                phone_number = user_info.get("user").get("phoneNumber")
                log.debug("Sending SMS to User ID #" + str(uid) + " with text: \"" + notif_text)
                self.send_sms(phone_number, notif_text)
            
            if email_notifs == "true":
                email_address = user_info.get("user").get("emailAddress")
                log.debug("Sending e-mail to User ID #" + str(uid) + " with text: \"" + notif_text)
                self.send_email(email_address, notif_text)

    def send_email(self, address, message):
        email_message = EmailMessage()
        email_message.set_content(message)

        email_message["Subject"] = "StudentAssist Notification"
        email_message["From"] = self.email_address
        email_message["To"] = address

        email_server = smtplib.SMTP('smtp.gmail.com', 587)
        email_server.starttls()
        email_server.login(self.email_address, self.email_password)

        email_server.send_message(email_message)
        email_server.quit()
    
    def send_sms(self, formatted_number, message):

        # Formatting for email content
        message = "\n" + message

        email_server = smtplib.SMTP('smtp.gmail.com', 587)
        email_server.starttls()
        email_server.login(self.email_address, self.email_password)

        email_server.sendmail(self.email_address, formatted_number, message)

    def format_notification(self, notif_text):
        today = datetime.today()
        today_date = today.strftime("%m_%d_%Y %H:%M")
        formatted_notif = today_date.replace("_", "/") + ": " + "[StudentAssist Notification]: " + notif_text
        return formatted_notif

if __name__ == "__main__":
    test_notif = NotificationManager()
    test_notif.send_notification(2, "Test Notif!!")