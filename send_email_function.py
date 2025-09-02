# send_email_function.py
from email.message import EmailMessage

def build_email_message(sender_email, receiver_email, subject, html_content, attachment_path=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content("This email requires HTML support.")
    msg.add_alternative(html_content, subtype='html')

    if attachment_path:
        with open(attachment_path, 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='pdf',
                filename=attachment_path.split('/')[-1]
            )

    return msg
