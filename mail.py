import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_notification_email(subscriber_emails, subject, content):
    message = Mail(
        from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
        to_emails=subscriber_emails,
        subject=subject,
        html_content=content
    )

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    resp = sg.send(message)

    if resp.status_code != 200:
        print(resp.body)
        print(resp.headers)

# def send_confirm_email(email, key):
#     content = 