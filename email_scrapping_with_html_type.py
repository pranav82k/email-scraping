# To receive emails and extract their content, you can use Python's built-in imaplib library.
# Here's an example of how to connect to an IMAP email server and fetch the contents of an email:

from dotenv import load_dotenv
import os
import imaplib
import email
import chardet
import urllib.parse
from bs4 import BeautifulSoup
import base64
from dotenv import load_dotenv
from generate_summary import generate_summary
from mysql_queries import MySQLDatabase
from string_conversion import decode_base64_string

# Load the variables from the .env file
load_dotenv()


def fetch_email():
    emails = []
    try:
        # Connect to the email server
        # imap_server = imaplib.IMAP4_SSL('imap.transmail.com')  # For transmail emails
        imap_server = imaplib.IMAP4_SSL(os.getenv('IMAP_SERVER_HOSTNAME'))
        imap_server.login(os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD'))

        # Select the mailbox to search in
        imap_server.select("Inbox")

        # Fetch the latest email
        # status, response = imap_server.search(None, 'SUBJECT "Your email subject"')
        # Search for unread emails
        typ, data = imap_server.search(None, 'UNSEEN')
        # status, data = imap_server.search(None, "ALL")
        # print(data[0])
        # result, data = imap_server.search(None, 'FROM "example@domain.com" SUBJECT "important"')
        # Iterate through the list of email IDs returned by the search command

        # Set a counter for the number of emails
        counter = 0

        # Following commented code is for reverse the string in descending order if required
        # emails_ids = data[0].split()
        # print(emails_ids[::-1])

        for num in data[0].split():
            print(num)
            # Fetch the email data using the ID
            status, email_data = imap_server.fetch(num, '(RFC822)')
            # Process the email data
            # Parse the email content
            raw_email = email_data[0][1]
            email_message = email.message_from_bytes(raw_email)
            sender_email_address = email_message.get('From')
            email_subject = email_message.get('Subject')

            # Extract the email body and attachments
            email_body = ""
            attachments = []
            is_html = False
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    # print("text/plain")
                    email_body += part.get_payload()
                elif part.get_content_type() == 'text/html':
                    print("text/html")
                    is_html = True
                    email_body += part.get_payload()
                    # email_body += urllib.parse.unquote(part.get_payload(), encoding='utf8')
                #     # Get the raw HTML content and decode it using the appropriate character encoding
                #     email_body += base64.b64decode(part.get_payload()).decode(part.get_content_charset())
                elif part.get_content_type().startswith("image/"):
                    attachments.append(part)
                elif part.get_content_type() == "application/pdf":
                    attachments.append(part)

            if is_html:
                soup = BeautifulSoup(email_body, "html.parser")
                email_body = soup.get_text().strip()
            # print(type(email_body))

            email_body = decode_base64_string(email_body)
            result = chardet.detect(email_body.encode())
            encoding = result["encoding"]
            # print(f"encoding type is {encoding}")
            # print(decode_base64_string(email_body))

            if encoding.isascii():
                print("it contains asciiii")
                email_body = email_body.encode("utf-8")
                email_body = email_body.decode("utf-8")

            print(email_body)
            # return sender_email_address, email_subject, email_body, attachments
            email_data = {'sender_email_address': sender_email_address,
                          'email_subject': email_subject,
                          'email_body': email_body,
                          'attachments': attachments}
            emails.append(email_data)
            # emails.append(sender_email_address, email_subject, email_body, attachments)

            # Generate the summary from chatgpt
            if email_body and len(email_body) < 4097:
                summary = generate_summary(email_body)
                if summary:
                    db = MySQLDatabase("localhost", "root", "", "email_scrapping")
                    db.connect()
                    db.insertion(sender_email_address, email_subject, email_body, summary)
                    db.close()

            # Increment the counter
            counter += 1

            # Break out of the loop if we have collected 5 emails
            if counter == 10:
                break

        # Close the connection
        imap_server.close()
        imap_server.logout()

        # Return the list of email data
        return emails
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Calling the above function
print(fetch_email())
# sender_email_address, email_subject, email_body, attachments = fetch_email()


# Generate the summary from chatgpt
# summary = generate_summary(email_body)
# db = MySQLDatabase("localhost", "root", "", "email_scrapping")
# db.connect()
# db.insertion(sender_email_address, email_subject, email_body, summary)
# db.close()
# print("Process Completed successfully")