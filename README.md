# AI Resume Screening System

An AI-powered automated hiring pipeline that:

- Stores candidate data in SQLite
- Stores resumes in AWS S3
- Downloads and parses resume text
- Uses LLM (Ollama) for classification
- Sends automated email & WhatsApp notifications
- Uses database-driven configurable prompts

## Architecture

Candidate → SQLite → S3 → Processor → LLM → Notification Agent

## Features

- Dynamic HR-editable classification rules
- Dynamic email templates stored in DB
- Secure secrets using .env
- WhatsApp integration using Twilio
- Fully modular backend design

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Create .env file with:
   SENDER_EMAIL=
   SENDER_PASSWORD=
   TWILIO_SID=
   TWILIO_AUTH=
   TWILIO_WHATSAPP_NUMBER=

3. Initialize database:
   python
   import database
   database.init_db()

4. Run processor:
   python processor.py

5. Run notification agent:
   python notification_agent.py