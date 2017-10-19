import smtplib
import src.irulez.log as log
from abc import ABC, abstractmethod
import json


logger = log.get_logger('mail_processor')

class mailProcessor(ABC):

    @abstractmethod
    def send_mail(self, json_object):
        pass

class gmailProcessor:
    def __init__(self, user: str, pwd: str, port: int):
        self.gmail_user = user
        self.gmail_pwd = pwd
        self.FROM = user
        self.port = port

    def send_mail(self, payload):

        json_object = json.loads(payload)
        recipient = json_object['mails']

        TO = recipient if type(recipient) is list else [recipient]
        SUBJECT = json_object['subject']
        TEXT = json_object['message']

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (self.FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", json_object['port'])
            server.ehlo()
            server.starttls()
            server.login(self.gmail_user, self.gmail_pwd)
            server.sendmail(self.FROM, TO, message)
            server.close()
            logger.info(f"successfully sent the mail")
        except:
            logger.warning(f"failed to send mail")