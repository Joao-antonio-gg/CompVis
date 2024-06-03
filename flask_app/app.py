from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import numpy
from ultralytics import YOLO
app = Flask(__name__)

# Configurações
model = YOLO('treinamento/best.pt')
UPLOAD_FOLDER = 'image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS # Verifica se a extensão do arquivo é permitida

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename): # Verifica se o arquivo é permitido
        filename = secure_filename(file.filename) # Garante que o nome do arquivo é seguro
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Salva o arquivo
        #pehar a imagem 
        image = 'image/' + filename
        result = model(image)
        name = result[0].names
        probs = result[0].probs.data.numpy()
        result_f = (name[numpy.argmax(probs)])
        travas = ['cadeado','etiqueta']
        if result_f != 'chave':
            travas.append(result_f)
        return render_template('display_image.html', filename=filename, result=result_f, travas=travas)
    return redirect(request.url)

@app.route('/image/<filename>') # Rota para servir arquivos da pasta de uploads
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/display/<filename>') # Rota para exibir a imagem
def uploaded_file(filename):
    return render_template('display_image.html', filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
