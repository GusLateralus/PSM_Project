#------------------------------ Importamos las librerias ------------------------------
import cv2
import mediapipe as mp
import serial

#----------------------------- Puerto Serial Configuracion ----------------------------
#com = serial.Serial("COM5", 9600, write_timeout=10)
d = 'd'
i = 'i'
p = 'p'

#------------------------------ Declaramos el detector --------------------------------
detector = mp.solutions.face_detection
dibujo = mp.solutions.drawing_utils

#------------------------------ Realizamos VideoCaptura --------------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#-------------------------------Empezamos el while True --------------------------------
with detector.FaceDetection(min_detection_confidence=0.5, model_selection=1) as rostros:

    while True:

        # Lectura de fotogramas
        ret, frame = cap.read()

        # Espejo a los frames
        frame = cv2.flip(frame, 1)

        # Convertimos el frame a RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectamos los rostros
        resultado = rostros.process(rgb)

        # Obtenemos las dimensiones del frame
        al, an, c = frame.shape
        centro = int(an / 2)

        # Inicializamos variables para el rostro más cercano al centro
        min_distancia = float('inf')
        rostro_cercano = None

        # Si hay detecciones de rostros
        if resultado.detections is not None:
            for id, rostro in enumerate(resultado.detections):
                # Extraemos las coordenadas X e Y min
                x = rostro.location_data.relative_bounding_box.xmin
                y = rostro.location_data.relative_bounding_box.ymin

                # Extraemos el ancho y el alto
                ancho = rostro.location_data.relative_bounding_box.width
                alto = rostro.location_data.relative_bounding_box.height

                # Pasamos X e Y a coordenadas en pixeles
                x, y = int(x * an), int(y * al)

                # Pasamos el ancho y el alto a pixeles
                x1, y1 = int(ancho * an), int(alto * al)
                xf, yf = x + x1, y + y1

                # Extraemos el punto central del rostro
                cx = (x + xf) // 2
                cy = (y + yf) // 2

                # Calculamos la distancia del centro del rostro al centro de la pantalla
                distancia_centro = abs(cx - centro)

                # Encontramos el rostro más cercano al centro
                if distancia_centro < min_distancia:
                    min_distancia = distancia_centro
                    rostro_cercano = (cx, cy, x, y, xf, yf, id)

            # Si encontramos un rostro cercano, seguimos su posición
            if rostro_cercano:
                cx, cy, x, y, xf, yf, id = rostro_cercano

                # Mostrar un punto en el centro del rostro
                cv2.circle(frame, (cx, cy), 3, (0, 0, 255), cv2.FILLED)
                cv2.line(frame, (cx, 0), (cx, al), (0, 0, 255), 2)

                # Dibujar el rectángulo alrededor del rostro
                cv2.rectangle(frame, (x, y), (xf, yf), (255, 255, 0), 3)
                cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

                # Condiciones para mover el servo
                if cx < centro - 50:
                    # Movemos hacia la izquierda
                    print("Moviendo a la izquierda")
                    #com.write(i.encode('ascii'))
                elif cx > centro + 50:
                    # Movemos hacia la derecha
                    print("Moviendo a la derecha")
                    #com.write(d.encode('ascii'))
                else:
                    # Paramos el servo
                    print("Parando servo")
                    #com.write(p.encode('ascii'))

        # Mostrar el frame con los dibujos
        cv2.imshow('Camara', frame)

        # Salir con la tecla 'ESC'
        t = cv2.waitKey(1)
        if t == 27:
            break

cap.release()
cv2.destroyAllWindows()
