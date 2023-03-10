# To receive emails and extract their content, you can use Python's built-in imaplib library.
# Here's an example of how to connect to an IMAP email server and fetch the contents of an email:

import imaplib
import email
import quopri
import chardet
import urllib.parse
from bs4 import BeautifulSoup
from langdetect import detect
from email.mime.text import MIMEText

from dotenv import load_dotenv
import os

from process_data import process_data
from string_conversion import decode_base64_string

# Load the variables from the .env file
load_dotenv()


def fetch_email(max_iterations):
    emails = []
    try:
        # Connect to the email server
        # imap_server = imaplib.IMAP4_SSL('imap.transmail.com')  # For transmail emails
        imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
        imap_server.login("phppranav304@gmail.com", "nsjwobizdkxvtnum")

        # Select the mailbox to search in
        imap_server.select("Inbox")

        # Fetch the unread emails in ascending order
        # Search for unread emails
        status, data = imap_server.search(None, 'UNSEEN')
        # status, data = imap_server.search(None, "ALL")
        # result, data = imap_server.search(None, 'FROM "example@domain.com" SUBJECT "important"')
        # status, response = imap_server.search(None, 'SUBJECT "Your email subject"')

        # Set a counter for the number of emails
        counter = 0

        # Following commented code is for reverse the email IDs in descending order if required
        # emails_ids = data[0].split()
        # print(emails_ids[::-1])
        # reverse_emails_ids = emails_ids[::-1]
        # print(reverse_emails_ids)

        # Iterate through the list of email IDs returned by the search command
        for num in data[0].split():
            print(num)  # printing the unique email ID

            # Fetch the email data using the ID
            status, email_data = imap_server.fetch(num, '(RFC822)')

            # Process the email data
            # Parse the email content
            raw_email = email_data[0][1]

            # Get the email message
            email_message = email.message_from_bytes(raw_email)

            # Get the sender email address
            # sender_email_address = email_message.get('From')  # Get the name and email
            from_part = email_message.get('From')
            sender_email_address = email.utils.parseaddr(from_part)[1]

            # Get the email subject
            email_subject = email_message.get('Subject')

            # Decode the subject header
            decoded_subject = ''
            for part, charset in email.header.decode_header(email_subject):
                if charset:
                    decoded_part = part.decode(charset)
                else:
                    decoded_part = part
                decoded_subject += decoded_part
            email_subject = decoded_subject

            # If we want to get the date of an email
            # email_date = email_message.get("Date")

            # Extract the email body
            email_body = ""
            is_html = False
            is_plain_text = False
            for part in email_message.walk():
                if part.get_content_type() == "text/plain" and not is_html:
                    # print("text/plain")
                    is_plain_text = True
                    email_body += part.get_payload()
                elif part.get_content_type() == 'text/html' and not is_plain_text:
                    # print("text/html")
                    is_html = True
                    email_body += part.get_payload()

            # Get email content language
            # content_language = detect(email_body)

            if is_html:
                soup = BeautifulSoup(email_body, "html.parser")
                email_body = soup.get_text().strip()
            # print(type(email_body))

            # Pass the email body to check the string is encoded or not, if encoded then decode using base64,
            # Otherwise we will return the same string that we passed as argument
            email_body = decode_base64_string(email_body)

            # Check the encoding type of string
            # result = chardet.detect(email_body.encode())
            # encoding = result["encoding"]
            # print(f"encoding type is {encoding}")
            # print(decode_base64_string(email_body))

            # if encoding.isascii():
            #     print("it contains asciiii")
            #     email_body = email_body.encode("utf-8")
            #     email_body = email_body.decode("utf-8")

            # print(email_body)
            # return sender_email_address, email_subject, email_body
            email_data = {'sender_email_address': sender_email_address,
                          'from_part': from_part,
                          'email_subject': email_subject,
                          'email_body': email_body}
            emails.append(email_data)
            # emails.append(sender_email_address, email_subject, email_body)

            # Calling the function by passing dictionary for generating summary and save the record in the database
            # print("email msg id" + email_message['Message-ID'])
            process_data(email_data)

            # create the reply message
            # reply_msg = MIMEText(os.getenv('AUTOGENERATE_EMAIL_REPLY_CONTENT'))
            # reply_msg['To'] = sender_email_address
            # reply_msg['From'] = os.getenv('EMAIL_USERNAME')
            # reply_msg['Subject'] = email_subject
            # reply_msg['In-Reply-To'] = email_message['Message-ID']
            #
            # # upload the reply message to the mailbox
            # imap_server.append('inbox', None, None, reply_msg.as_bytes())

            # Increment the counter
            counter += 1

            # Break out of the loop if we have collected 5 emails
            if counter == max_iterations:
                break

        # Close the connection
        imap_server.close()
        imap_server.logout()

        # Return the list of email data
        return emails
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Calling the above function
response = fetch_email(max_iterations=10)
print(response)
