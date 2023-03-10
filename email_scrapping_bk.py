# To receive emails and extract their content, you can use Python's built-in imaplib library. Here's an example of
# how to connect to an IMAP email server and fetch the contents of an email:

import imaplib
import email
import base64
# import quopri
from dotenv import load_dotenv
import os

# import MailBox as MailBox

# Load the variables from the .env file
load_dotenv()


def fetch_email():
    # Connect to the email server
    imap_server = imaplib.IMAP4_SSL(os.getenv('IMAP_SERVER_HOSTNAME'))
    imap_server.login(os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD'))
    imap_server.select("Inbox")

    # Fetch the latest email
    status, data = imap_server.search(None, "ALL")
    # print(data)
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
decoded_string = base64.b64decode(email_body)

# Converting bytes to string
decoded_string = decoded_string.decode("utf-8")

print(decoded_string)
# print(decode_email_body(email_body))


# from imap_tools import MailBox, A
# with MailBox('imap.mail.com').login(os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD'), 'INBOX') as mailbox:
#     for msg in mailbox.fetch(A(all=True)):
#         sender = msg.from_
#         body = msg.text or msg.html
#
#         print(body)


# def decode_email_body(msg):
#     if msg.is_multipart():
#         # If the message is multipart, loop through its parts and decode the body of each part
#         parts = []
#         for part in msg.walk():
#             charset = part.get_content_charset()
#             if part.get_content_type() == 'text/plain':
#                 parts.append(part.get_payload(decode=True).decode(charset))
#             elif part.get_content_type() == 'text/html':
#                 parts.append(part.get_payload(decode=True).decode(charset))
#         return '\n'.join(parts)
#     else:
#         # If the message is not multipart, decode the body using the message's encoding
#         charset = msg.get_content_charset()
#         body = msg.get_payload(decode=True)
#         if msg.get_content_type() == 'text/plain':
#             body = quopri.decodestring(body).decode(charset)
#         elif msg.get_content_type() == 'text/html':
#             body = quopri.decodestring(body).decode(charset)
#         elif msg.get_content_type() == 'application/octet-stream':
#             body = base64.b64decode(body).decode(charset)
#         return body
