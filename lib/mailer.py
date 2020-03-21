import smtplib, ssl

from lib.config import config

port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = config["mail"]["address"]
password = config["mail"]["password"]

message = """\
Subject: Hi there

This message is sent from Python."""

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()  # Can be omitted
    server.starttls(context=context)  # Secure the connection
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    # TODO: Send email here
    server.sendmail(sender_email, "piotrgredowski@gmail.com", message)
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit()
