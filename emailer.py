import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
from datetime import datetime



load_dotenv()
sender = os.getenv("sender")
receiver = os.getenv("receiver")
password = os.getenv("password")
context = ssl.create_default_context()
host = "smtp.gmail.com"
port = 465


def send_email(file_path="motion.png", sender=sender, to=receiver, subject="Motion Detected"):
    # 1. Create the container (MIMEMultipart)
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = to
    message['Subject'] = subject

    # 2. Attach the email body
    message.attach(MIMEText(f"{datetime.now()}", 'plain'))

    # 3. Attach the file
    try:
        with open(file_path, "rb") as attachment:
            # Add file as application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(file_path)}",
        )

        # Add attachment to message
        message.attach(part)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return

    # 4. Log in and send
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender, password)
        # message.as_string() converts the whole multipart object to text
        server.sendmail(sender, to, message.as_string())

    print("Email with attachment sent!")
