import os
import openai
import sqlite3
import logging
from flask import Flask, request, jsonify
from datetime import datetime

# Initialize Flask App
app = Flask(__name__)

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Database File Name
DB_NAME = "emails.db"

# OpenAI API Key (use environment variables for security)
openai.api_key = "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"

# Database Setup
def setup_database():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_email TEXT,
                ai_reply TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
    except Exception as e:
        logging.error(f"Error setting up database: {e}")
    finally:
        conn.close()

# Generate AI Email Reply
def generate_email_reply(email_content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful email assistant."},
                {"role": "user", "content": f"Write a professional reply to the following email: {email_content}"}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        logging.error(f"Error generating reply: {e}")
        return f"Error generating reply: {e}"

# Save Email Reply to Database
def save_email_reply(original_email, ai_reply):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO email_replies (original_email, ai_reply, timestamp)
            VALUES (?, ?, ?)
        ''', (original_email, ai_reply, timestamp))
        conn.commit()
    except Exception as e:
        logging.error(f"Database error: {e}")
    finally:
        conn.close()

# Route: Generate Email Reply
@app.route('/generate-reply', methods=['POST'])
def generate_reply():
    try:
        data = request.json
        email_content = data.get("email_content")
        if not email_content:
            logging.warning("Email content missing in request")
            return jsonify({"error": "Email content is required"}), 400

        ai_reply = generate_email_reply(email_content)
        save_email_reply(email_content, ai_reply)
        logging.info("Reply generated successfully")
        return jsonify({"original_email": email_content, "ai_reply": ai_reply})
    except Exception as e:
        logging.error(f"Error in /generate-reply: {e}")
        return jsonify({"error": str(e)}), 500

# Route: Get Saved Replies with Pagination
@app.route('/get-replies', methods=['GET'])
def get_replies():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM email_replies ORDER BY timestamp DESC LIMIT ? OFFSET ?', (limit, offset))
        rows = cursor.fetchall()
        conn.close()

        return jsonify([
            {"id": row[0], "original_email": row[1], "ai_reply": row[2], "timestamp": row[3]}
            for row in rows
        ])
    except Exception as e:
        logging.error(f"Error in /get-replies: {e}")
        return jsonify({"error": str(e)}), 500

# Route: Health Check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Server is running"}), 200

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
