import cv2
from ultralytics import YOLO

# Caminho para a imagem
image_path = '/Users/joaop/OneDrive/Área de Trabalho/Nova pasta (2)/s-l400.jpg'

# Caminho para o modelo YOLO
model_path = 'C:/Users/joaop/runs/classify/train3/weights/last.pt'

# Carrega o modelo
model = YOLO(model_path)

# Limiar de detecção
threshold = 0.5

# Lê a imagem
frame = cv2.imread(image_path)

# Detecta objetos na imagem
results = model(frame)

# Desenha caixas delimitadoras e rótulos para objetos detectados
for result in results.xyxy[0].tolist():
    x1, y1, x2, y2, score, class_id = result

    if score > threshold:
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
        cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

# Mostra a imagem com as detecções
cv2.imshow('Detecções de objetos', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
