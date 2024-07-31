import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Configuration de l'email
EMAIL_ADDRESS = "lebotdeleo75@gmail.com"
EMAIL_PASSWORD = "zlno qawq rxms gvou"
EMAIL_RECIPIENT = ["lhs75@icloud.com.com", "lh5218@ic.ac.uk"]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# URL de la page à surveiller
URL = 'https://lavasque.paris2024.org/'

def check_availability():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    page_text = str(soup)
    print(page_text) 
    search_text = "Nous sommes victimes de notre succès, tous les créneaux ont été réservés"
    
    if search_text not in page_text:
        return True
    return False


def send_email():
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(EMAIL_RECIPIENT)
    msg['Subject'] = "Billets disponibles !"
    body = "Les billets ppour la vasque des jo sont maintenant disponibles ! Visitez : " + URL
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, EMAIL_RECIPIENT, text)

while True:
    if check_availability():
        send_email()
        break
    time.sleep(60)  
