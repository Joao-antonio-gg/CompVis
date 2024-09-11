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
        bool: True se a extensão do arquivo é permitida, False caso contrário.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
