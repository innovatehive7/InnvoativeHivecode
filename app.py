from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime
import requests
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

mail = Mail(app)

# Google Sheets integration
def get_google_sheet():
    """Connects to Google Sheets and returns the sheet object."""
    try:
        creds_json = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
        required_keys = ['type', 'project_id', 'private_key', 'client_email']
        if not all(k in creds_json for k in required_keys):
            raise ValueError("Missing required credential fields")
        
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        client = gspread.authorize(creds)
        sheet_name = os.getenv('GOOGLE_SHEET_NAME')

        try:
            sheet = client.open(sheet_name).sheet1
            return sheet
        except gspread.SpreadsheetNotFound:
            sheet = client.create(sheet_name)
            sheet.sheet1.append_row([
                'Timestamp', 'Name', 'Email', 'Phone',
                'Service', 'Goal', 'Budget', 'Message',
                'IP Address', 'User Agent'
            ])
            sheet.share(creds_json['client_email'], perm_type='user', role='writer')
            return sheet.sheet1
    except Exception as e:
        logging.error(f"Google Sheets Error: {str(e)}")
        return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    """Handles contact form submissions."""
    try:
        data = request.get_json()
        if not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({'status': 'error', 'message': 'Name, email, and message are required'}), 400

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        service = data.get('service', '').strip()
        goal = data.get('goal', '').strip()
        budget = data.get('budget', '').strip()
        message = data.get('message', '').strip()

        # Save to Google Sheets
        sheet = get_google_sheet()
        if not sheet:
            raise Exception("Could not access Google Sheets")
        sheet.append_row([
            timestamp, name, email, phone, service, goal,
            budget, message, request.remote_addr,
            request.headers.get('User-Agent', 'Unknown')
        ])
        logging.info("Data written to Google Sheets successfully.")

        # Send email notification
        try:
            msg = Message(
                "New Contact Form Submission - InnovateHive",
                recipients=[os.getenv('EMAIL_RECEIVER')]
            )
            msg.body = f"""
            Name: {name}
            Email: {email}
            Phone: {phone}
            Service: {service}
            Goal: {goal}
            Budget: {budget}
            Message: {message}
            Timestamp: {timestamp}
            IP Address: {request.remote_addr}
            """
            mail.send(msg)
            logging.info("Email sent successfully.")
        except Exception as e:
            logging.error(f"Email sending failed: {e}")

        return jsonify({'status': 'success', 'message': 'Your message has been sent successfully!'})

    except Exception as e:
        logging.error(f"Contact form error: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred. Please try again later.'}), 500

# Google Form Submission Route
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/1rRrzQbLud9FfPKTgzCXSM-9SOPFuE4isHWkqTZ7SaHg/formResponse"

@app.route('/submit-form', methods=['POST'])
def submit_to_google_form():
    """Submits data to Google Forms."""
    try:
        data = request.get_json()
        form_data = {
            "entry.2005620554": data.get("name"),
            "entry.1045781291": data.get("email"),
            "entry.1166974658": data.get("phone"),
            "entry.839337160": data.get("service"),
            "entry.671065043": data.get("goal"),
            "entry.1223232703": data.get("budget"),
            "entry.83890540": data.get("message")
        }

        response = requests.post(GOOGLE_FORM_URL, data=form_data)
        if response.status_code in [200, 302]:
            logging.info("Form submitted successfully.")
            return jsonify({"status": "success", "message": "Form submitted!"})
        else:
            logging.error(f"Form submission failed with status code {response.status_code}")
            return jsonify({"status": "error", "message": "Submission failed"}), 500

    except Exception as e:
        logging.error(f"Error submitting form: {e}")
        return jsonify({"status": "error", "message": "An error occurred"}), 500

# Additional Routes
@app.route('/website')
def website(): return render_template('website.html')

@app.route('/graphic')
def graphic(): return render_template('graphic.html')

@app.route('/video_editing')
def video_editing(): return render_template('video_editing.html')

@app.route('/content')
def content(): return render_template('content.html')

@app.route('/seo')
def seo(): return render_template('seo.html')

@app.route('/business_analysis')
def business_analysis(): return render_template('business_analysis.html')

@app.route('/app')
def app_design(): return render_template('app.html')

@app.route('/cloud')
def cloud(): return render_template('cloud.html')

@app.route('/ai_assistant_development')
def ai_assistant(): return render_template('ai_assistant_development.html')

@app.route('/all_blogs')
def all_blogs(): return render_template('all_blogs.html')

@app.route('/anurag')
def anurag(): return render_template('anurag.html')

@app.route('/dhanashri')
def dhanashri(): return render_template('dhanashri.html')

@app.route('/gurbani')
def gurbani(): return render_template('gurbani.html')

@app.route('/om_gws')
def om_gws(): return render_template('om_gws.html')

@app.route('/siddhi')
def siddhi(): return render_template('siddhi.html')

@app.route('/anuja')
def anuja(): return render_template('anuja.html')

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
