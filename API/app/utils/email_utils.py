import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .token_utils import token
import os



EMAIL_USER= os.environ.get('EMAIL_USER')
EMAIL_PASSWORD=os.environ.get('EMAIL_PASSWORD')
EMAIL_PORT=os.environ.get('EMAIL_PORT')
EMAIL_DOMAIN=os.environ.get('EMAIL_DOMAIN')

VERIFICATION_ENDPOINT  = 'http://localhost:5173/verification/'

def send_order_confirmation(email:str, order_id: str):
    _token = token(email=email, order_id=order_id)
    _url = VERIFICATION_ENDPOINT+_token+'/'
    message = format_confirmation_email(url=_url, email_to=email)
    
    with smtplib.SMTP_SSL(EMAIL_DOMAIN,EMAIL_PORT) as server:
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, EMAIL_USER,message)

    return None


def format_email(order, items_list, orders_list ,email_to):
    """Builds HTML for Order Details Email """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Order Details'
    msg['From'] = "audie.artavia19@gmail.com"
    msg['To'] = email_to

    html = f'<html><h2>Your order</h2> <b> {order}</b>  with Items:<br></br>{items_list}</html>'

    body = MIMEText(html, 'html')
    msg.attach(body)
    return msg.as_string()


def format_confirmation_email(url, email_to):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Please confirm your order'
    msg['From'] = "audie.artavia19@gmail.com"
    msg['To'] = email_to

    html = f'<html>Please click on the link to confirm your order {url} </html>'

    body = MIMEText(html, 'html')
    msg.attach(body)
    return msg.as_string()

