from flask import Flask
from flask import render_template
from services import recognize_service

app = Flask(__name__)
ser = recognize_service.recognize_service()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/recognize', methods=['GET'])
def recognize():  
  return f'Hello, {ser.recognize(None)}'


if __name__ == '__main__':
    app.run(debug=True)