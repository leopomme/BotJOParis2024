import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from datetime import datetime, timedelta

# Configuration de l'email
EMAIL_ADDRESS = "lebotdeleo75@gmail.com"
EMAIL_PASSWORD = "zlno qawq rxms gvou"
EMAIL_RECIPIENT = ["lhs75@icloud.com", "lh5218@ic.ac.uk"]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# URL de la page à surveiller
URL = 'https://lavasque.paris2024.org/'

# Time management
last_status_email_time = datetime.now()
status_email_interval = timedelta(hours=24)  # 24 hours interval

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(EMAIL_RECIPIENT)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, EMAIL_RECIPIENT, text)

def check_availability():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Convert soup to string and search for the text
    page_text = str(soup)
    search_text = "Nous sommes victimes de notre succès, tous les créneaux ont été réservés"
    
    if search_text not in page_text:
        return True
    return False

# Send initial email
send_email("Bot Started", "You have been added to the bot. We will notify you if tickets become available.")

while True:
    if check_availability():
        send_email("Billets disponibles !", "Les billets pour la vasque des JO sont maintenant disponibles ! Visitez : " + URL)
        break
    else:
        print('No tickets available.')
    
    # Check if it's time to send the daily status email
    if datetime.now() - last_status_email_time >= status_email_interval:
        send_email("Status Update", "No tickets have been released yet.")
        last_status_email_time = datetime.now()
    
    time.sleep(60)  # Check every 60 seconds
