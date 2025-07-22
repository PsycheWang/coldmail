import smtplib
from email.message import EmailMessage

def send_email(sender_email, sender_password, receiver_email, smtp_server, smtp_port, subject, html_content, attachment_path, context):
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

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
        print(f"✔ Email sent to {receiver_email}")
