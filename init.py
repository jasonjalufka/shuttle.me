from flask import Flask
from flask_ask import Ask

app = Flask(__name__)
ask = Ask(app, "/")

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
