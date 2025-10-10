import cv2
import numpy as np
import webbrowser
from pyzbar.pyzbar import decode

def leer_qr():
    cap = cv2.VideoCapture(0)  # Usa la cámara
    enlace_abierto = False  # Variable para asegurarse de abrir solo una vez
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Decodificar QR en la imagen
        for qr in decode(frame):
            datos = qr.data.decode('utf-8')
            print(f"QR Detectado: {datos}")

            # Si el contenido es un enlace y aún no se ha abierto, abrirlo en el navegador
            if (datos.startswith("http://") or datos.startswith("https://")) and not enlace_abierto:
                print("Abriendo enlace en el navegador...")
                webbrowser.open(datos)
                enlace_abierto = True  # Evitar múltiples aperturas

            # Dibujar un rectángulo alrededor del código QR
            puntos = qr.polygon
            if len(puntos) == 4:
                pts = np.array([(p.x, p.y) for p in puntos], dtype=np.int32)
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=3)

        cv2.imshow('Lector QR', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Presiona 'q' para salir
            break

    cap.release()
    cv2.destroyAllWindows()

leer_qr()