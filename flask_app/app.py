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
    """
    Verifica se a extensão do arquivo é permitida.

    Args:
        filename (str): O nome do arquivo a ser verificado.

    Returns:
        bool: True se a extensão do arquivo estiver na lista de extensões permitidas, False caso contrário.
    """
    return ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

def save_file(file):
    """
    Salva o arquivo enviado pelo usuário no diretório de upload.

    Args:
        file (FileStorage): O arquivo a ser salvo.

    Returns:
        tuple: O caminho completo do arquivo e o nome do arquivo.
    """
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath, filename

def process_image(filepath):
    """
    Processa a imagem usando o modelo YOLO e retorna a classe prevista.

    A imagem é processada pelo modelo YOLO, que retorna uma lista de probabilidades para cada classe. 
    A função então retorna a classe com a maior probabilidade.

    Args:
        filepath (str): O caminho para o arquivo de imagem a ser processado.

    Returns:
        str: A classe prevista para a imagem.
    """
    result = model(filepath)
    names = result[0].names
    probs = result[0].probs.data.numpy()
    predicted_class = names[numpy.argmax(probs)]
    return predicted_class


@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if not file or file.filename == '':
        return redirect(request.url)  
    if allowed_file(file.filename):
        filepath, filename = save_file(file)
        predicted_class = process_image(filepath)
        travas = ['cadeado','etiqueta']
        if predicted_class != 'chave':
            travas.append(predicted_class)

        return render_template('display_image.html', filename=filename, result=predicted_class, travas=travas)
    return redirect(request.url)

@app.route('/image/<filename>') # Rota para servir arquivos da pasta de uploads
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/display/<filename>') # Rota para exibir a imagem
def uploaded_file(filename):
    return render_template('display_image.html', filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
