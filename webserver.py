from flask import Flask
import logging
from threading import Thread

app = Flask('')
logging.getLogger('werkzeug').setLevel(logging.ERROR)

@app.route('/')
def home():
    return "Alive.. Until now."

def run():
    app.run(host='0.0.0.0', port=8080)

def thread_run():
    Thread(target=run).start()
