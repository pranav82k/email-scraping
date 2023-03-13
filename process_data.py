from dotenv import load_dotenv
import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

from generate_summary import generate_summary
from mysql_queries import MySQLDatabase
# from send_email import send_email

# Load the variables from the .env file
load_dotenv()


def process_data(email_data):
    # print("from_part" + email_data['from_part'])
    # if email_data['email_body'] and len(email_data['email_body']) < 4097:
    if email_data['email_body']:
        summary = generate_summary(email_data['email_body'])
        if summary:
            db = MySQLDatabase(os.getenv('DB_HOST'),
                               os.getenv('DB_USER'),
                               os.getenv('DB_PASSWORD'),
                               os.getenv('DB_DATABASE_NAME'))
            db.connect()
            db.insertion(email_data['sender_email_address'],
                         email_data['email_subject'],
                         email_data['email_body'],
                         summary)
            db.close()

            # Compose the reply message
            msg = MIMEMultipart()
            msg['To'] = email_data['from_part']
            msg['From'] = os.getenv('EMAIL_USERNAME')
            msg['Subject'] = Header("Re: " + email_data['email_subject'], 'utf-8')
            # text = os.getenv('AUTOGENERATE_EMAIL_REPLY_CONTENT')
            text = summary
            msg.attach(MIMEText(text))

            # Attach a file to the reply
            # with open('/path/to/file.pdf', 'rb') as f:
            #     attachment = MIMEApplication(f.read(), _subtype='pdf')
            #     attachment.add_header('Content-Disposition', 'attachment', filename='file.pdf')
            #     msg.attach(attachment)

            # Send the reply message
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD'))
                smtp.sendmail(os.getenv('EMAIL_USERNAME'), msg['To'], msg.as_string())

            # Send an auto generate email to the sender
            # send_email(
            #     os.getenv('EMAIL_USERNAME'),
            #     os.getenv('EMAIL_PASSWORD'),
            #     email_data['sender_email_address'],
            #     msg['Subject'],
            #     msg
            # )
