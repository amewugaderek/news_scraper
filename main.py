# To handle http requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
# To parse HTML.
from bs4 import BeautifulSoup
# To manipulate system date and time
import datetime
# To compose email body
import email.mime
# To send email
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get current date time
now = datetime.datetime.now()
# Email content placeholder
email_content = ""


# Extracting news (daily graphic | https://www.graphic.com.gh/news.html)
def extract_news (url:str):
    news_content = ''
    subject = "HEADLINES - GRAPHIC ONLINE"
    news_content += (f"<b>{subject}</b>\n" + "<br>")
    # Extract url content
    url_extracted_contents = requests.get(url)
    # Extract contents from url extracted content
    extracted_content = url_extracted_contents.content
    # Compose soup
    soup = BeautifulSoup(extracted_content, 'html.parser')

    for index, td in enumerate(soup.find_all('td', attrs={'class': 'list-title'})):
        # Find the <a> tag inside the <td>
        a_tag = td.find('a')
        if a_tag and a_tag.get('href'):
            headline = a_tag.text.strip()
            link = a_tag.get('href')
            # Format as HTML with a clickable link
            news_content += f"{index + 1} :::: <a href='https://www.graphic.com.gh{link}'>{headline}</a><br>\n"
        else:
            # Fallback if no <a> tag is found
            news_content += f"{index + 1} :::: {td.text.strip()}<br>\n"
    return news_content

content = extract_news("https://www.graphic.com.gh/news.html")
email_content += content

email_content += ("<br>=========================<br>")
email_content += ("<br><br> End of Message")


# Get email credentials from environment variables
# Send the email - email details
# SERVER = smtplib.SMTP('smtp.gmail.com', 587)
FROM = os.getenv("EMAIL_ADDRESS")
PASS = os.getenv("EMAIL_PASSWORD")
TO = 'amewugaaws@gmail.com'

# Create message body
message = MIMEMultipart()
message['Subject'] = f"HEADLINES - GRAPHIC ONLINE {str(now.day)} - {str(now.year)}"
message ['From'] = FROM
message ['To'] = TO
# Attach the html body
message.attach(MIMEText(email_content, 'html'))

# Initialize server
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.set_debuglevel(True)
        # Gmail requires a secure connection (either STARTTLS on port 587 or SMTP_SSL on port 465)
        server.starttls()
        server.login(FROM, PASS)
        server.sendmail(FROM, TO, message.as_string())
        print("Email successfully sent")
        server.quit()


except smtplib.SMTPException as e:
    print("Error: unable to send email")
    print("Error: ", e)





