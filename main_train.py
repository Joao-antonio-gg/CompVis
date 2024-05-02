from ultralytics import YOLO

model = YOLO('yolov8n-cls.pt')  # load a pretrained model (recommended for training)
# Train the model
results = model.train(data='/Users/joaop/OneDrive/Área de Trabalho/Limbo EleModC/Compvis/Projeto/CompVis/scripts/dataset', epochs=100, imgsz=64, hsv_h=0.5, hsv_v=0.6, degrees = 180,translate=0.5, scale=1, shear=180, perspective=0.0005, flipud=0.5, fliplr=0.5, mosaic=1.0)  