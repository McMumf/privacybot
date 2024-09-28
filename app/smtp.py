import smtplib, ssl
from os import getenv
from dotenv import load_dotenv

port = 587  # For starttls

class smtp_client:
    """
    Configures SMTP client for secure connection to the host.
    """
    def __init__(self):
        load_dotenv()
        self.sender_email = getenv('SENDER_USER')
        self.password = getenv('SMTP_PASSWORD')
        self.smtp_host = getenv('SMTP_HOST')

        self.context = ssl.create_default_context()

        self.server = smtplib.SMTP(self.smtp_host, port)
        self.server.starttls(context=self.context) # Secure the connection
        self.server.login( self.sender_email,  self.password)

    def __exit__(self, exc_type, exc_value, traceback):
        self.server.quit()

    def send_email(self, sender: str, receiver: str, contents: str):
        try:
            self.server.sendmail(sender, receiver, contents)
        except Exception as e:
            print(e)
