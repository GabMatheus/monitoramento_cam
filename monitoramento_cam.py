import cv2
import numpy as np
from ultralytics import YOLO
import datetime
import os

# Configurações
rtsp_url = "rtsp://user:password@endereco:porta/cam/realmonitor?channel=1&subtype=0" #Conectar na camera
area_monitorada = (10, 450, 840, 600)  # x1, y1, x2, y2
intervalo_minimo = datetime.timedelta(seconds=15)  # intervalo entre capturas

# Carrega modelo YOLOv8 
model = YOLO("yolov8n.pt")  

# Inicializa câmera
cap = cv2.VideoCapture(rtsp_url)
if not cap.isOpened():
    print("❌ Não foi possível abrir o stream da câmera.")
    exit()

# Caminho do log
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, "caminhoes_detectados.txt")

# Função para verificar se está na área monitorada
def dentro_da_area(bbox, area):
    x1, y1, x2, y2 = area
    bx1, by1, bx2, by2 = bbox
    cx = (bx1 + bx2) / 2
    cy = (by1 + by2) / 2
    return x1 <= cx <= x2 and y1 <= cy <= y2

# Variável para controle de tempo
ultimo_registro = None

print("🎥 Monitorando caminhões-tanque...")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    agora = datetime.datetime.now()
    resultados = model(frame, classes=[7], verbose=False)  # Filtra apenas a classe 'truck' (ID 7 no YOLOv8)

    for r in resultados:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])  # Confiança da detecção
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Debug: mostra tudo que está sendo detectado
            print(f"Detectado: {model.names[cls]} - Confiança: {conf:.2f} - Coordenadas: {x1}, {y1}, {x2}, {y2}")

            # Filtro adicional para evitar falsos positivos (ex.: vans/ônibus)
            if conf < 0.7:  # Ignora detecções com confiança baixa
                continue

            # Verifica proporção da bounding box (caminhões são mais longos)
            width = x2 - x1
            height = y2 - y1
            aspect_ratio = width / height
            if aspect_ratio < 1.5:  # Ajuste conforme necessário (caminhões típicos: > 1.5)
                continue

            # Desenha a bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{model.names[cls]} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Verifica se está na área monitorada
            if dentro_da_area((x1, y1, x2, y2), area_monitorada):
                if not ultimo_registro or (agora - ultimo_registro > intervalo_minimo):
                    timestamp = agora.strftime("%Y-%m-%d_%H-%M-%S")
                    imagem_nome = f"caminhao_{timestamp}.jpg"
                    imagem_path = os.path.join(script_dir, imagem_nome)

                    # Salva imagem
                    cv2.imwrite(imagem_path, frame)
                    print(f"📸 Caminhão detectado - imagem salva: {imagem_nome}")

                    # Salva log
                    with open(log_path, "a") as f:
                        f.write(f"{timestamp} - Caminhão detectado na área (Confiança: {conf:.2f})\n")

                    # Atualiza o último registro
                    ultimo_registro = agora

    # Desenha a área monitorada
    cv2.rectangle(frame, (area_monitorada[0], area_monitorada[1]),
                  (area_monitorada[2], area_monitorada[3]), (255, 0, 0), 2)

    # Exibe a imagem
    cv2.imshow("Detecção de Caminhão (YOLOv8)", frame)

    # Tecla ESC para sair
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()