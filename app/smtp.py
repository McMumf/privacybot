import smtplib, ssl

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "my@gmail.com"
password = input("Type your password and press enter: ")

class smtp_client:
    """
    Configures SMTP client for secure
    """
    def __init__(self, api_token: str):
        context = ssl.create_default_context()
        self.server = smtplib.SMTP(smtp_server, port)
        self.server.starttls(context=context) # Secure the connection

    def send_email(self, sender: str, receiver: str, contents: str):
        self.server.sendmail(sender, receiver, contents)
