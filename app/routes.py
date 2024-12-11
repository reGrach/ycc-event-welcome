from flask import render_template, jsonify, request
from PIL import Image
from app import app, rec_ser

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpeg']

@app.route('/')
@app.route('/index')
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
