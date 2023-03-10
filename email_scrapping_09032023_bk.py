# To receive emails and extract their content, you can use Python's built-in imaplib library. Here's an example of
# how to connect to an IMAP email server and fetch the contents of an email:

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
    imap_server = imaplib.IMAP4_SSL(os.getenv('IMAP_SERVER_HOSTNAME'))
    imap_server.login(os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD'))
    imap_server.select("Inbox")

    # Fetch the latest email
    status, data = imap_server.search(None, "ALL")
    latest_email_id = data[0].split()[-1]
    status, email_data = imap_server.fetch(latest_email_id, "(RFC822)")
    # print(status)

    # Parse the email content
    raw_email = email_data[0][1]
    email_message = email.message_from_bytes(raw_email)

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

    return email_body, attachments


# Calling the above function
email_body, attachments = fetch_email()
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

# Generate the summary from chatgpt
message = generate_summary(email_body)
db = MySQLDatabase("localhost", "root", "", "email_scrapping")
db.connect()
db.insertion(message)
db.close()
print("Process Completed successfully")