import smtplib


def send_email(sender_email, sender_password, receiver_email, subject, body):
    # print("receiver_email" + receiver_email)
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Set up the email message
    message = f"Subject: {subject}\n\n{body}"

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        if isinstance(receiver_email, str):
            receiver_email = [receiver_email]
        server.sendmail(sender_email, receiver_email, message)

    # print("Email sent successfully!")


# sender_email = "example@gmail.com"
# sender_password = "password"
# receiver_email = "pranav@1touch-dev.com"
# subject = "Automatic reply"
# body = "Hello, this is a automatic email sent using Python!"
#
# send_email(sender_email, sender_password, receiver_email, subject, body)

