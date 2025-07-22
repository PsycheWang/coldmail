import csv
import ssl
from send_email_function import send_email
from datetime import date
from gui_config import get_email_config_gui

context = ssl.create_default_context()
config = get_email_config_gui()

csv_file = config["csv_file"]
mail_templates = config["template_path"]

with open(mail_templates, 'r', encoding='utf-8') as f:
    html_template = f.read()

with open(csv_file, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    rows = list(reader)
    fieldnames = reader.fieldnames
    if 'first_cold_mail_date' not in fieldnames:
        fieldnames.append('first_cold_mail_date')

for row in rows:
    to_email = row['Email']
    name = row['Contact Name']
    subject = f"Hello {name}, Introducing Our Self-Ligating Brackets"
    html_body = html_template.replace('{name}', name)

    send_email(
        sender_email=config["email"],
        sender_password=config["password"],
        receiver_email=to_email,
        smtp_server=config["smtp_server"],
        smtp_port=config["smtp_port"],
        subject=subject,
        html_content=html_body,
        attachment_path=config["attachment_path"],
        context=context
    )

    if not row.get('first_cold_mail_date'):
        row['first_cold_mail_date'] = date.today().isoformat()

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
