import os
import re

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, From, Mail

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def check(email):    
    if(re.search(regex,email)):  
        return True            
    else:  
        return False

def send_notification_email(subscribers, subject, content):
    if len(subscribers) == 0:
        print('No recipients for the message, discarding.')
        return
    
    subscriber_emails = []
    for sub in subscribers:
        subscriber_emails += [sub.get('key')]

    message = Mail(
        from_email=From(email=os.environ.get('SENDGRID_SEND_EMAIL'), name="chand1012.dev Blog"),
        to_emails=subscriber_emails,
        subject=subject,
        html_content=Content("text/html", content)
    )

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    resp = sg.send(message)

    if resp.status_code >= 300 or resp.status_code < 200:
        print(resp.body)
        print(resp.headers)

def send_confirm_email(email, key):
    with open(os.path.join('templates', 'emails.html')) as f:
        content = f.read()

    message = Mail(
        from_email=From(email=os.environ.get('SENDGRID_SEND_EMAIL'), name="chand1012.dev Blog"),
        to_emails=email,
        subject='chand1012.dev Subscription Confirmation',
        html_content=Content("text/html", content.replace("{{key}}", key).replace("{{url}}", os.environ.get('BASE_URL')))
    )

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    resp = sg.send(message)
    
    if resp.status_code >= 300 or resp.status_code < 200:
        print(resp.body)
        print(resp.headers)
