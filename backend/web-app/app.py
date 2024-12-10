import sys
sys.path.append('backend')

from PIL import Image
from flask import Flask, render_template, jsonify, request
from recognizer import recognize_service as rs

app = Flask(__name__)
rec_ser = rs.recognize_service()
rec_ser.start()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpeg']

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
  json_data = {
     'success': False,
     'result': 'Не распознано'
  }

  # проверяем наличие файла в запросе
  if 'file' not in request.files:
     json_data['result'] = 'Файл не обнаружен'
  else:
    file = request.files['file']
    # проверяем формат файла
    if file and allowed_file(file.filename):
      img = Image.open(file)
      result = rec_ser.recognize(img)
      if(result is not None):
        json_data['success'] = True
        json_data['result'] = result
    else:
       json_data['result'] = 'Файл должен быть в формате JPG'

  return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080, ssl_context='adhoc')