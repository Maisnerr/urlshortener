from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random
import string
from termcolor import colored
import regex as re
import qrcode
import cloudinary.uploader
import cloudinary.api
import cloudinary.uploader
import io
from PIL import Image
from waitress import serve
import logging
import requests
import datetime
import uuid
from dotenv import load_dotenv
import os
from argon2 import PasswordHasher

load_dotenv()

if(os.getenv("PRODUCTION")=="True"):
    PRODUCTION = True
else:   
    PRODUCTION = False

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME"),
    api_key=os.getenv("CLOUDINARY_KEY"),
    api_secret=os.getenv("CLOUDINARY_SECRET")
)
 
if(PRODUCTION):
    LOCALURL = "https://www.linkly.fun/"
else:
    LOCALURL = "http://192.168.1.138:5000/"

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_HEALTH = os.getenv("WEBHOOK_HEALTH")

def send_webhook(title, desc, color, type):
    data = {
    "username": "Linkly.fun",
    "avatar_url": "https://i.imgur.com/4M34hi2.png",  # Optional custom avatar
    "embeds": [{
            "title": title,
            "description": desc,
            "color": color,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }]
    }
    requests.post(type, json=data)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
SITES = [
    "https://www.linkly.fun", 
    "https://linkly.fun", 
    "https://linkly-fnbx.onrender.com",
    "http://192.168.1.138:5000"
]
CORS(app, resources={r"/*": {"origins": SITES}})
hasher = PasswordHasher(time_cost=2, memory_cost=10240, parallelism=2)

class URL(db.Model):
    __tablename__ = "Linklyfun"

    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2048), nullable=False)

    short_url = db.Column(db.String(10), unique=True, nullable=False)

    clicks = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.date.today)

    img_url = db.Column(db.String(2048), nullable=False)

class UserBase(db.Model):
    __tablename__ = "linklyfun_userbase"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    uuid = db.Column(db.String(36), unique=True, nullable=True)
    pfp_url = db.Column(db.String, default="https://res.cloudinary.com/drxgvf9hq/image/upload/v1751063741/defaultuser_hjdpwm.png", nullable=True)  # profile picture URL
    creation = db.Column(db.Date, default=datetime.date.today, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, default="user", nullable=False)  # e.g. "user", "admin"

##
##  chatgpt je frajer
##  NEROZUMIM TOMU ALE FUNGUJE TO 
##
def is_valid_url(url):
    """
    Validate the URL format using regex.
    Returns True if valid, False otherwise.
    """
    regex = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    return re.match(regex, url) is not None


##
##  PREDCHUDCE NOVEHO SHORT URL
##
def generate_short_url(url):
    if(url==""):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(random.choices(characters, k=5))
        return short_url
    else:
        short_url = url
        return url

##
##  FINALNI GENEROVANI NOVEHO SHORT URL
##
def new_short_url():
    all_urls = URL.query.all()
    short_url = generate_short_url("")
    for url in all_urls:
        if short_url == url.short_url:
            return new_short_url()
    return short_url

##
##  GENEROVANI QR KODU
##
def generate_qr_code(short_url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1
    )

    qr.add_data(LOCALURL + short_url)
    qr.make(fit=True)
    file = qr.make_image(fill='black', back_color='white')

    img_byte_arr = io.BytesIO()
    file.save(img_byte_arr, format='PNG')  # Save as PNG or another format
    img_byte_arr.seek(0)  # Reset buffer position to the beginning

    response = cloudinary.uploader.upload(img_byte_arr)

    image_url = response["secure_url"]
    print(f"Image uploaded successfully! URL: {image_url}")

    print(colored(f"QR Code generated and saved as {short_url}.png","green"))

    return image_url

##
##  CHECK ZDA JE SHORT URL OK
##
def check_after(after):
    characters = string.digits + string.ascii_letters
    all_urls = URL.query.all()

    for url in all_urls:
        if after == url.short_url:
            return "used"

    if(len(after)>2 and len(after)<11):
        pass
    else:
        return "invalid"
    for i in after:
        if(i not in characters):
            return "invalid"
    return "chill"

##
##  FORMATOVANI DAT PRO VRACENI V @/getdata
##
def format_for_return(entry):
    data = []
    data.append(entry.short_url)

    if(len(entry.long_url) > 128):
        data.append(str((entry.long_url[:-(len(entry.long_url)-128)]))+"...")
    else:
        data.append(entry.long_url)

    data.append(entry.clicks)

    data.append(entry.date)

    data.append(entry.img_url)

    return data

@app.route("/stats")
def statssite():
    return render_template("stats.html")

@app.route("/register")
def registerpage():
    return render_template("register.html")

@app.route("/")
def index():
    return render_template("index.html")

##
##  ZKRACENI URL
##
@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.json
    long_url = data.get("long_url")

    after = data.get("after")
    normal_url = True

    if after != "":
        if check_after(after) == "invalid":
            return jsonify({"error": "Invalid character in after. Please use 3-10 characters and 0-9;a-Z" }), 400
        elif check_after(after) == "used":
            return jsonify({"error": "This short url is already used, please try another one"}), 400
        else:
            normal_url = False
            short_url = after
    else:
        short_url = new_short_url()

    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    # Validate if the input is a valid URL
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL format"}), 400

    # Check if URL is already shortened
    existing_url = URL.query.filter_by(long_url=long_url).first()
    if normal_url:
        if existing_url:
            return jsonify({"short_url": LOCALURL + existing_url.short_url, "file_url": f"{LOCALURL}static/qrs/{existing_url.short_url}.png", "img_url": existing_url.img_url})

    img_url = generate_qr_code(short_url)

    new_entry = URL(long_url=long_url, short_url=short_url, clicks=0, date=datetime.date.today(), img_url=img_url)

    db.session.add(new_entry)
    db.session.commit()

    send_webhook("New URL Created!", f"URL: {LOCALURL+short_url}", int("5fe3a8", 16), WEBHOOK_URL)
    return jsonify({"short_url": LOCALURL + short_url, "file_url": f"{LOCALURL}static/qrs/{short_url}.png", "img_url": img_url})   

##
##  ZMENA KRATKEHO URL NA STRANKU
##
@app.route("/<short_url>")
def redirect_to_long(short_url):
    url_entry = URL.query.filter_by(short_url=short_url).first()
    if url_entry:
        url_entry.clicks += 1
        db.session.commit()
        print(colored("adding +1 to "+str(url_entry.clicks), "blue"))
        send_webhook("URL Redirected!", f"URL: {LOCALURL+short_url}", int("5951e8", 16), WEBHOOK_URL)
        return redirect(url_entry.long_url)
    return jsonify({"error": "URL not found"}), 404

##
##  VRACI STATISTIKY O LINKU
##
@app.route("/stats/<short_url>")
def actual_get_stats(short_url):

    if(len(short_url)<11):
        url_entry = URL.query.filter_by(short_url=short_url).first()
    
    if not url_entry:
        return jsonify({"error": "URL not found"}), 69

    return jsonify({"short_url": short_url, "long_url":url_entry.long_url, "clicks":url_entry.clicks, "date":url_entry.date, "img_url":url_entry.img_url})

##
##  VUBEC NEVIM CO TOTO DELA ALE JE TO DULEZITE
##
@app.route("/getlength", methods=["POST"])
def getlength():
    length = []

    for i in range(URL.query.count()):
        length.append(1)

    return jsonify({"len": length})

##
##  REGISTRACE UZIVATELE
##
@app.route("/registering", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    password = data.get("pass")

    hashed_password = hasher.hash(password)

    try:
        new_entry = UserBase(username=name, password=hashed_password, uuid=str(uuid.uuid4()))
        db.session.add(new_entry)
        db.session.commit()
    except Exception as e:
        print(colored(f"Error while registering user: {e}", "red"))
        return jsonify({"error": "Unexpected error happened on the server, please try again later"}), 400

    return jsonify({"redirect": "http://192.168.1.138:5000/"})

##
##  TAKY NEVIM CO TOTO DELA
##
@app.route("/getdata", methods=["POST"])
def return_data():
    data = request.json

    amount = data.get("amount")

    url_entry = URL.query.get(int(URL.query.count())-int(amount))

    mezi = format_for_return(url_entry)

    return jsonify({"short_url": mezi[0], "long_url": mezi[1], "clicks": mezi[2], "date": mezi[3], "img_url": mezi[4]})

##
##  CHECK ZDA SERVER BEZI
##
@app.route("/serverhealth", methods=["GET"])
def server_health():
    send_webhook("Server Check!", f"Server is running just fine", int("34d958", 16), WEBHOOK_HEALTH)
    return "OK", 200

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    if(PRODUCTION):
        send_webhook("Server Running!", f"All good g", int("41ba4f", 16), WEBHOOK_URL)
        serve(app, host="0.0.0.0", port=5000)
    else:
        app.run(debug=True, host="0.0.0.0", port=5000)

