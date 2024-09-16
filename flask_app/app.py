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
    """
    Função que retorna o formulário de upload para a rota raiz ("/").
    """
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Função para lidar com o upload de arquivos.

    Esta função é responsável por receber uma requisição POST contendo um arquivo e realizar o upload do mesmo. 
    O arquivo é salvo em uma pasta específica e, em seguida, é feita uma análise do conteúdo do arquivo utilizando um modelo de visão computacional.
    O resultado da análise é utilizado para determinar se o arquivo contém uma imagem de uma chave ou de uma trava. Caso seja identificado como uma trava, o tipo de trava é adicionado a uma lista de travas.
    Por fim, é renderizado um template HTML que exibe a imagem, o resultado da análise e a lista de travas.

    Parâmetros:
        - Nenhum parâmetro é necessário.

    Retorno:
        - Nenhum valor é retornado explicitamente, mas a função realiza o upload do arquivo e renderiza um template HTML.
    """
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

@app.route('/image/<filename>')
def send_file(filename):
    '''
    Função que retorna um arquivo da pasta de uploads.

    Parâmetros:
    - filename (str): O nome do arquivo a ser retornado.

    Retorno:
    - O arquivo especificado pelo nome na pasta de uploads.

    Exemplo de uso:
        send_file('imagem.jpg')
    '''
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/display/<filename>')
def uploaded_file(filename):
    """
    Rota para exibir uma imagem.

    Parâmetros:
    - filename (str): O nome do arquivo da imagem a ser exibida.

    Retorno:
    - render_template: O template HTML para exibir a imagem.

    """
    return render_template('display_image.html', filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
