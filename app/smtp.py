import smtplib, ssl
from os import getenv

smtp_server = "smtp.gmail.com"
port = 587  # For starttls


class smtp_client:
    """
    Configures SMTP client for secure
    """
    def __init__(self):
        self.sender_email = getenv('SENDER_EMAIL_ADDR')
        self.password = getenv('SMTP_API_KEY')

        self.context = ssl.create_default_context()

        self.server = smtplib.SMTP(smtp_server, port)
        self.server.starttls(context=self.context) # Secure the connection
        self.server.login( self.sender_email,  self.password)

    def __exit__(self, exc_type, exc_value, traceback):
        self.server.quit()

    def send_email(self, sender: str, receiver: str, contents: str):
        try:
            self.server.sendmail(sender, receiver, contents)
        except Exception as e:
            print(e)
