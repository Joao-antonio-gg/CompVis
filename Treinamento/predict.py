from ultralytics import YOLO
import numpy

model = YOLO('Backend/treinamento/best.pt')  # load a custom model


results = model('/Users/joaop/OneDrive/Área de Trabalho/Limbo EleModC/Compvis/Projeto/CompVis/scripts/dataset_new2/val/Valvula/655cf1d8def4eb00120335e2.png')  # predict on an image  caminho da imagem a ser testada

names = results[0].names

probs = results[0].probs.data.numpy()  # or .top5per() for top 5 class percentages

# for i in probs:
#     print(i)

# print(names)
# print(probs)
# print(results)

print(names[numpy.argmax(probs)]) # most confident class
