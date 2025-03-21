import os
from datetime import datetime

def log_action(email, zip_name, sender_email):
    log_entry = f"{datetime.now()}: {sender_email} -> {email} - {zip_name}\n"
    log_file = f"logs/log_{datetime.now().strftime('%Y-%m-%d')}.log"

    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open(log_file, 'a') as f:
        f.write(log_entry)