import sys
sys.path.append('backend')

from flask import Flask
from flask import render_template
from recognizer import recognize_service as rs

app = Flask(__name__)
rec_ser = rs.recognize_service()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/recognize', methods=['GET'])
def recognize():  
  return f'Hello, {rec_ser.recognize(None)}'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080, ssl_context='adhoc')