from flask import Flask
from config import Config
from app.recognize_service import recognize_service

app = Flask(__name__)
app.config.from_object(Config)

rec_ser = recognize_service(Config)
rec_ser.start()

from app import routes, errors