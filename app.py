from flask import Flask, request, render_template, jsonify
import threading
import time
import requests

app = Flask(__name__)

saved_urls = []  # Store multiple URLs

def send_requests():
    """Function to send requests to all saved URLs and itself every 14 minutes."""
    while True:
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
    global saved_urls
    if request.method == "POST":
        url = request.form.get("url")
        if url and url not in saved_urls:
            saved_urls.append(url)
        return jsonify({"message": "URL saved!", "urls": saved_urls})
    return render_template("index.html", urls=saved_urls)

if __name__ == "__main__":
    thread = threading.Thread(target=send_requests, daemon=True)
    thread.start()

    app.run(host="0.0.0.0", port=5000)
