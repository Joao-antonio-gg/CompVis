import os
path = '/Users/joaop/OneDrive/Área de Trabalho/Limbo EleModC/Compvis/Projeto/CompVis/scripts/labeled1/registro2'

files = os.listdir(path)
for index, file in enumerate(files):
    os.rename(os.path.join(path, file), os.path.join(path, f'reg{index+61}.png'))

