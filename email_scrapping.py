# To receive emails and extract their content, you can use Python's built-in imaplib library.
# Here's an example of how to connect to an IMAP email server and fetch the contents of an email:

from dotenv import load_dotenv
import os
import imaplib
import email
import base64
from generate_summary import generate_summary
from mysql_queries import MySQLDatabase


# Load the variables from the .env file
load_dotenv()


def fetch_email():
    # Connect to the email server
    # imap_server = imaplib.IMAP4_SSL('imap.transmail.com')  # For transmail emails
    imap_server = imaplib.IMAP4_SSL(os.getenv('IMAP_SERVER_HOSTNAME'))
    imap_server.login(os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD'))
    imap_server.select("Inbox")

    # Fetch the latest email
    # status, response = imap_server.search(None, 'SUBJECT "Your email subject"')
    status, data = imap_server.search(None, "ALL")
    # result, data = imap_server.search(None, 'FROM "example@domain.com" SUBJECT "important"')
    # print(len(data[0]))
    # email_ids = data[0].split()
    # email_ids = data[0].split(b' ')
    # for email_id in email_ids:
    #     print(email_id)

    # for byte in data[0]:
    #     character = chr(byte)
    #     print(character)
    latest_email_id = data[0].split()[-1]
    # print(latest_email_id)
    status, email_data = imap_server.fetch(latest_email_id, "(RFC822)")
    # print(status)

    # Parse the email content
    raw_email = email_data[0][1]
    email_message = email.message_from_bytes(raw_email)
    sender_email_address = email_message.get('From')
    email_subject = email_message.get('Subject')

    # Extract the email body and attachments
    email_body = ""
    attachments = []
    for part in email_message.walk():
        if part.get_content_type() == "text/plain":
            email_body += part.get_payload()
        elif part.get_content_type().startswith("image/"):
            attachments.append(part)
        elif part.get_content_type() == "application/pdf":
            attachments.append(part)

    return sender_email_address, email_subject, email_body, attachments


# Calling the above function and unpack the variables
sender_email_address, email_subject, email_body, attachments = fetch_email()


# Generate the summary from chatgpt
if email_body:
    summary = generate_summary(email_body)
    if summary:
        db = MySQLDatabase("localhost", "root", "", "email_scrapping")
        db.connect()
        db.insertion(sender_email_address, email_subject, email_body, summary)
        db.close()
        print(email_body)

# The below code is required if the email body will receive as encoding string
# Converting bytes to string
# Decoding the string
# decoded_string = base64.b64decode(email_body)

# Converting bytes to string
# decoded_string = decoded_string.decode("utf-8")


# print(generate_summary(decoded_string))
# message = generate_summary(decoded_string)

# print(message)
# summary = insertion(generate_summary(decoded_string))

# summary = insertion(message)
# print(summary)
