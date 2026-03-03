import sqlite3
import smtplib
import os
from email.message import EmailMessage
from twilio.rest import Client
from dotenv import load_dotenv
from database import get_prompt

# Load environment variables
load_dotenv()

DB_NAME = "candidates.db"

# -------------------------
# LOAD SECRETS FROM .env
# -------------------------
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

twilio = Client(TWILIO_SID, TWILIO_AUTH)


def generate_message(candidate):

    if candidate["category"] == "Qualified":
        template = get_prompt("email_qualified")
    else:
        template = get_prompt("email_rejected")

    if not template:
        raise Exception("Email prompt not found in database.")

    lines = template.strip().split("\n")
    subject_line = lines[0]

    if subject_line.startswith("Subject:"):
        subject = subject_line.replace("Subject:", "").strip()
        body_template = "\n".join(lines[1:])
    else:
        subject = "Application Update"
        body_template = template

    body = body_template.format(
        name=candidate["name"],
        location=candidate["location"],
        category=candidate["category"]
    )

    return subject, body


def send_email(candidate):

    subject, body = generate_message(candidate)

    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = candidate["email"]
    msg["Subject"] = subject
    msg.set_content(body)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()

    print("Email sent to:", candidate["email"])


def send_whatsapp(candidate):

    subject, body = generate_message(candidate)

    message = twilio.messages.create(
        body=body,
        from_=TWILIO_WHATSAPP_NUMBER,
        to="whatsapp:" + candidate["phone"]
    )

    print("WhatsApp sent to:", candidate["phone"])


def run():

    print("Notification agent running...")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidates WHERE status='processed'")
    rows = cursor.fetchall()

    for row in rows:

        candidate = {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "location": row[4],
            "category": row[7]
        }

        try:
            send_email(candidate)

            if candidate["category"] == "Qualified":
                send_whatsapp(candidate)

            cursor.execute("""
                UPDATE candidates
                SET status='notified'
                WHERE id=?
            """, (candidate["id"],))

            conn.commit()

        except Exception as e:
            print("Notification error:", e)

    conn.close()


if __name__ == "__main__":
    run()