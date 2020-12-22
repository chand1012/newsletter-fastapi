import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, Content

def send_notification_email(subscriber_emails, subject, content):
    message = Mail(
        from_email=From(email=os.environ.get('SENDGRID_SEND_EMAIL'), name="chand1012.dev Blog"),
        to_emails=subscriber_emails,
        subject=subject,
        html_content=Content("text/html", content)
    )

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    resp = sg.send(message)

    if resp.status_code != 200:
        print(resp.body)
        print(resp.headers)

def send_confirm_email(email, key):
    with open(os.path.join('templates', 'emails.html')) as f:
        content = f.read()

    message = Mail(
        from_email=From(email=os.environ.get('SENDGRID_SEND_EMAIL'), name="chand1012.dev Blog"),
        to_emails=email,
        subject='chand1012.dev Subscription Confirmation',
        html_content=Content("text/html", content.replace("{{key}}", key))
    )

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    resp = sg.send(message)
    print(resp.body)
    print(resp.headers)
