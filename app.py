from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random
import string
from termcolor import colored
import regex as re
import qrcode

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
CORS(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2048), nullable=False)

    short_url = db.Column(db.String(10), unique=True, nullable=False)

def is_valid_url(url):
    """
    Validate the URL format using regex.
    Returns True if valid, False otherwise.
    """
    regex = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'  # Simple regex for http/https URLs
    return re.match(regex, url) is not None

def generate_short_url():
    characters = string.digits + string.ascii_letters
    short_url = ''.join(random.choices(characters, k=5))
    return short_url

def new_short_url():
    all_urls = URL.query.all()
    short_url = generate_short_url()
    for url in all_urls:
        if short_url == url.short_url:
            return new_short_url()
    return short_url

def generate_qr_code(short_url):
    qr = qrcode.make("http://192.168.1.138:5000/"+short_url)
    qr.save(f"static/qrs/{short_url}.png")  # Save the QR code as a PNG file
    print(f"QR Code generated and saved as {short_url}.png")

@app.route("/")
def index():
    all_urls = URL.query.all()
    # You can either render these URLs on a webpage or print them in the terminal
    for url in all_urls:
        print(colored(f"{url.short_url} - {url.long_url}", "red"))

    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.json
    long_url = data.get("long_url")
    
    if not long_url:
        return jsonify({"error": "URL is required"}), 400
    
    # Validate if the input is a valid URL
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL format"}), 400

    # Check if URL is already shortened
    existing_url = URL.query.filter_by(long_url=long_url).first()
    if existing_url:
        return jsonify({"short_url": "http://192.168.1.138:5000/" + existing_url.short_url, "file_url": f"http://192.168.1.138:5000/static/qrs/{existing_url.short_url}.png"})
    
    short_url = new_short_url()
    new_entry = URL(long_url=long_url, short_url=short_url)
    
    generate_qr_code(short_url)

    db.session.add(new_entry)
    db.session.commit()
    
    print(colored(short_url, "green"))
    return jsonify({"short_url": "http://192.168.1.138:5000/" + short_url, "file_url": f"http://192.168.1.138:5000/static/qrs/{short_url}.png"})

@app.route("/<short_url>")
def redirect_to_long(short_url):
    url_entry = URL.query.filter_by(short_url=short_url).first()
    if url_entry:
        return redirect(url_entry.long_url)
    return jsonify({"error": "URL not found"}), 404

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)
