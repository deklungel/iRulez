import smtplib
import src.irulez.log as log
from abc import ABC, abstractmethod
import json

logger = log.get_logger('mail_processor')


class MailProcessor(ABC):
    @abstractmethod
    def send_mail(self, json_object):
        pass


class AuthenticateSMTP_Processor(MailProcessor):
    def __init__(self, user: object, pwd: object, port: object, url: object) -> object:
        self.gmail_user = user
        self.gmail_pwd = pwd
        self._from = user
        self.port = port
        self.url = url

    def send_mail(self, payload):

        json_object = json.loads(payload)
        recipient = json_object['mails']

        to = recipient if type(recipient) is list else [recipient]
        subject = json_object['subject']
        body = json_object['message']

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (self._from, ", ".join(to), subject, body)
        try:
            server = smtplib.SMTP(self.url, self.port)
            server.ehlo()
            server.starttls()
            server.login(self.gmail_user, self.gmail_pwd)
            server.sendmail(self._from, to, message)
            server.close()
            logger.info(f"successfully sent the mail")
        except:
            logger.warning(f"failed to send mail")
