from flask import Flask, request, render_template, jsonify
import threading
import time
import requests

app = Flask(__name__)

saved_url = None  # Store the entered URL

def send_requests():
    """Function to send requests to the saved URL and itself every 14 minutes."""
    global saved_url
    while True:
        if saved_url:
            try:
                requests.get(saved_url, timeout=5)
                print(f"Requested: {saved_url}")
            except Exception as e:
                print(f"Error requesting {saved_url}: {e}")

            try:
                requests.get("http://127.0.0.1:5000", timeout=5)
                print("Requested: Flask server itself")
            except Exception as e:
                print(f"Error requesting itself: {e}")

        time.sleep(14 * 60)  # Wait for 14 minutes

@app.route("/", methods=["GET", "POST"])
def home():
    global saved_url
    if request.method == "POST":
        saved_url = request.form.get("url")
        return jsonify({"message": "URL saved!", "url": saved_url})
    return render_template("index.html", url=saved_url)

if __name__ == "__main__":
    # Start the background thread for sending requests
    thread = threading.Thread(target=send_requests, daemon=True)
    thread.start()

    app.run(host="0.0.0.0", port=5000)
