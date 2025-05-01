from flask import Flask
from threading import Thread
import os

app = Flask(__name__)
@app.route('/')
def home():
    return "The bot is running!"

def run():
    app.run(host='0.0.0.0', port= os.getenv("PORT", 8080))

def keep_alive():
    t = Thread(target=run)
    t.start()