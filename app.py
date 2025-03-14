from flask import Flask, request, render_template, jsonify
import threading
import time
import requests
import sqlite3

app = Flask(__name__)

DB_FILE = "urls.db"

def init_db():
    # """Initialize the database and create table if it doesn't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL
            )
        ""
        )
        conn.commit()

def get_saved_urls():
    # """Retrieve all stored URLs from the database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM urls")
        return [row[0] for row in cursor.fetchall()]

def save_url(url):
    """Save a new URL to the database if it's not already stored."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO urls (url) VALUES (?)", (url,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # URL already exists

def send_requests():
    """Function to send requests to all saved URLs and itself every 14 minutes."""
    while True:
        saved_urls = get_saved_urls()
        for url in saved_urls:
            try:
                requests.get(url, timeout=5)
                print(f"Requested: {url}")
            except Exception as e:
                print(f"Error requesting {url}: {e}")

        # Self-request using Render's public URL
        self_url = "https://render-bot-ewv3.onrender.com"
        try:
            requests.get(self_url, timeout=5)
            print(f"Requested: {self_url} (self-request)")
        except Exception as e:
            print(f"Error requesting itself: {e}")

        time.sleep(14 * 60)  # Wait for 14 minutes

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            save_url(url)
        return jsonify({"message": "URL saved!", "urls": get_saved_urls()})
    return render_template("index.html", urls=get_saved_urls())

if __name__ == "__main__":
    init_db()
    thread = threading.Thread(target=send_requests, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=5000)
