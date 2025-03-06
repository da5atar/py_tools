'''
email_header_checker.py
-----------------------

This script parses the headers of an email file (EML format) and extracts relevant information such as:
 sender, recipient, subject, date, message ID, and additional headers like SPF, DKIM, DMARC, etc.

To run the script, provide the path to the email file you want to analyze.
Note: You need to have the 'email' library installed to run this script.
'''
import email
import quopri
from email import policy
from email.parser import BytesParser

def parse_email(file_path):
    """Parse the email file and extract relevant header information."""
    with open(file_path, 'rb') as file:
        msg = BytesParser(policy=policy.default).parse(file)

    print("From:", msg.get("From", "N/A"))
    print("To:", msg.get("To", "N/A"))
    print("Subject:", msg.get("Subject", "N/A"))
    print("Date:", msg.get("Date", "N/A"))
    print("Message ID:", msg.get("Message-ID", "N/A"))
    print("X-Mailer:", msg.get("X-Mailer", "N/A"))
    # Additional Information
    print("\n--- Additional Information ---\n")
    print("SPF:", msg.get("Received-SPF", "N/A"))
    print("DKIM:", msg.get("DKIM-Signature", "N/A"))
    print("DMARC:", msg.get("DMARC-Filter", "N/A"))
    print("SENDERIP:", msg.get("X-Sender-IP", "N/A"))
    print("RETURN PATH:", msg.get("Return-Path", "N/A"))
    print("Reply-To:", msg.get("Reply-To", "N/A"))
    print('Authentication Results:\n', msg.get('Authentication-Results','N/A'))
    print('Message ID', msg.get('Message-Id','N/A'))

def main():
    email_file_path = "/content/Sample.eml"  ## Email File
    parse_email(email_file_path)
if __name__ == "__main__":
    main()
