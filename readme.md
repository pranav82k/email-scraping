The purpose of the code is to scrap the email, get the content from the email, generate a summary using the extracted text, save it in the MySQL database, and auto-reply an email to the sender.

Create a file with a function to connect and fetch unseen emails from the inbox, also added the code in the form of comments for fetching all the emails, fetching emails with a specific subject, or specific mail with a specific subject. 
Also added the code as the form of comments to split all the email IDs and reverse it in descending order if required.

Added the code to handle the text/html content type emails. Check if the email is in the text/html content type use the bs4 library to import BeautifulSoup. by using this, extract the body part of the email.

Also handled the base64 encoded email by creating a function in a separate file that takes the email content as input string and added the try-except block to check if the string is encoded then performing b64decode and decoding it with utf-8 and returning, otherwise returning the same string as we did pass as argument to function.

Create a dictionary with the required email data and pass it to the process data function that takes the email body and generates the summary according to it, also added a code as a comment format to restrict the further process if the length of content is greater than 4097.

If we got the summary from the OpenAIAPI, we will pass the required database connection arguments to the MySQLDatabase class, then call the connect method, then insert the record in the table and close the connection.

If everything is going well then create a message by using MIMEMultipart class, added the required parameters like To, From, msg, etc, and attach text by using MIMEText class. I also added a  code as a comment format for Attaching a file to the reply.

Then set up smtplib pass the required arguments and use the sendmail function to send an email. Also, created a separate file that contains a function that takes required data like email, password, receiver email address, subject, body, etc.

Use the try-except block in the main file to handle at least basic exceptions.

Also, install the dotenv library, create a .env in the root, and define variables for all the secret credentials and values in it. from dotenv load, the load_dotenv, call it for including all the variables in the file. using the os library to access the environment variables.


The main files are
email_scrapping.py - Scrap the email IDs, scrap the data from the latest email, generate a summary, and save the record in the table.
unread_email_scrapping.py - Scrap the email IDs, scrap the data from the email, and pass the content of the email to string conversion, decode it if requires.
string_conversion.py - Takes the email content, if it's encoding then decode it with base64 decoding.
generate_summary.py - Communicate with OpenAIAPI to fetch the summary.
mysql_query.py - A class that has different functions for connecting, inserting, and closing the connection with the database.
process_data.py - Central file that takes the data from email, generates summary using the function of generate_summary file, communicates with mysql_query's MySQLDatabase classes, generates the reply, and sends the auto-reply using the smtplib


I have also added a file that uses PyPDF3 to read the PDF files and extract text from them. File name - pdf_text_extraction.py


There are other files including some backup files that have similar code with different approaches.