'''
bulk_emails_sender.py
---------------------
This script sends personalized emails to multiple recipients using an HTML template.
The script reads recipient data from a CSV file and sends an email to each recipient.
The email content is personalized with the recipient's name using an HTML template.

To run the script, provide the sender's email credentials, HTML template, and recipients CSV file.
The script will send an email to each recipient with the personalized content.

Note: You need to enable 'Less Secure Apps' in your Gmail settings to send emails using this script.
'''

import smtplib, ssl, email
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import pandas as pd

# Sender email credentials
SENDER_EMAIL = "YOUR_EMAIL"
PASSWORD = "YOUR_EMAIL_PASSWORD"

# Load HTML template
with open("template.html", "r") as file:
    html_template = file.read()

# Load recipient data from CSV file
recipients_df = pd.read_csv("recipients.csv")  # CSV should have 'name' and 'email' columns

# Function to send an email to a single recipient
def send_email(recipient_name, recipient_email):
    ''' Send an email to a single recipient with personalized content. '''
    # Create MIMEMultipart email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Welcome Pythoneer!!!"
    msg["From"] = formataddr(("The Pythoneers", "Publication"))
    msg["To"] = recipient_email

    # Customize the HTML content
    personalized_html = html_template.replace("[User Name]", recipient_name)

    # Attach personalized HTML content to the email
    part = MIMEText(personalized_html, "html")
    msg.attach(part)

    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail("The Pythoneers", recipient_email, msg.as_string())
        print(f"Email sent to {recipient_name} at {recipient_email}")

# Loop through each recipient and send an email
for _, row in recipients_df.iterrows():
    send_email(row["name"], row["email"])

print("All emails have been sent!")
