from ultralytics import YOLO
import numpy as np

model = YOLO('C:/Users/joaop/runs/classify/train3/weights/last.pt')  # load a custom model


results = model('scripts/dataset/val/disjuntor/456.png')  # predict on an image  caminho da imagem a ser testada

names = results[0].names

probs = results[0].probs


print(probs)