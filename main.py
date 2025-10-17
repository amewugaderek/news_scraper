# To handle http requests
import requests
# To parse HTML.
from bs4 import BeautifulSoup
# To manipulate system date and time
import datetime
# To compose email body
import email.mime
# To send email
import smtplib

# Get current date time
now = datetime.datetime.now()
# Email content placeholder
email_content = ""


# Extracting news (daily graphic | https://www.graphic.com.gh/news.html)
def extract_news (url:str):
    news_content = ''
    news_content += ("<b>HEADLINES - GRAPHIC ONLINE</b>\n" + "<br>")
    # Extract url content
    url_extracted_contents = requests.get(url)
    # Extract contents from url extracted content
    extracted_content = url_extracted_contents.content
    # Compose soup
    soup = BeautifulSoup(extracted_content.content, 'html.parser')

    for index, tag in enumerate(soup.find_all('td', attrs={'class': 'list-title, list-date small'})):
        news_content += ((str(index + 1) + " :: " + tag.text) + "\n" + '<br>')
    return news_content

content = extract_news("https://www.graphic.com.gh/news.html")
email_content += content

email_content += ("<br>=========================<br>")
email_content += ("<br><br> End of Message")




