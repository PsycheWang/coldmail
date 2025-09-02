# main.py
import csv
import ssl
import smtplib
from send_email_function import build_email_message
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

# 👉 一次性登录
with smtplib.SMTP_SSL(config["smtp_server"], config["smtp_port"], context=context) as smtp:
    smtp.login(config["email"], config["password"])

    for row in rows:
        to_email = row['Email']
        name = row['Contact Name']
        subject = f"Self-Ligating Brackets - Zhejiang Protect"
        html_body = html_template.replace('{name}', name)

        # 这里用一个 helper 函数，只负责构建 msg
        msg = build_email_message(
            sender_email=config["email"],
            receiver_email=to_email,
            subject=subject,
            html_content=html_body,
            attachment_path=config["attachment_path"]
        )

        smtp.send_message(msg)
        print(f"✔ Email sent to {to_email}")

        if not row.get('Second'):
            row['Second'] = date.today().isoformat()

# 写回 CSV
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
