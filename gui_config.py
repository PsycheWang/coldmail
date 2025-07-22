import json
import os
import tkinter as tk
from tkinter import filedialog, simpledialog

CONFIG_FILE = 'config.json'


def get_email_config_gui():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)

    # 如果没有配置文件，就弹出界面让用户输入
    root = tk.Tk()
    root.withdraw()

    email = simpledialog.askstring("Email Config", "Enter your email:")
    password = simpledialog.askstring("Email Config", "Enter your password:", show="*")
    smtp_server = simpledialog.askstring("Email Config", "Enter SMTP server:")
    smtp_port = simpledialog.askinteger("Email Config", "Enter SMTP port:", initialvalue=465)

    csv_file = filedialog.askopenfilename(title="Select CSV File")
    template_path = filedialog.askopenfilename(title="Select HTML Template")
    attachment_path = filedialog.askopenfilename(title="Select Attachment File (optional)")

    config = {
        "email": email,
        "password": password,
        "smtp_server": smtp_server,
        "smtp_port": smtp_port,
        "csv_file": csv_file,
        "template_path": template_path,
        "attachment_path": attachment_path
    }

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

    return config