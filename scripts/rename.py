import os
path = '/Users/joaop/OneDrive/Área de Trabalho/Limbo EleModC/Compvis/Projeto/CompVis/scripts/crawled6'
files = os.listdir(path)
for index, file in enumerate(files):
    os.rename(os.path.join(path, file), os.path.join(path, f'{index+391}.png'))

    