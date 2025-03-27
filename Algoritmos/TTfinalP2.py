#------------------------------ Importamos las librerias ------------------------------
import cv2
import mediapipe as mp
import serial
import math
import time
# Variables para detección de parpadeos
bloqueo = False
tiempo_de_bloqueo = 0.5  # Tiempo de bloqueo en segundos
parpadeos = 0
tiempo_condicion_cumplida = 0
tiempo_limite = 3
tiempo_guardado = 5  # Tiempo para guardar datos en segundos
ultimo_guardado = time.time()  # Marca de tiempo del último guardado
# Inicializar herramientas de MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
#----------------------------- Puerto Serial Configuracion ----------------------------
com = serial.Serial("COM5", 9600, write_timeout=10)
d = 'd'
i = 'i'
p = 'p'

#------------------------------ Declaramos el detector --------------------------------
detector = mp.solutions.face_detection
dibujo = mp.solutions.drawing_utils

#------------------------------ Realizamos VideoCaptura --------------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(3, 720)
cap.set(4, 480)
#-------------------------------Empezamos el while True --------------------------------
with detector.FaceDetection(min_detection_confidence=0.5, model_selection=1) as rostros:
    with mp_holistic.Holistic(static_image_mode=False, model_complexity=1) as holistic:

                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break
                        # Convertir la imagen a RGB
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        results = holistic.process(frame_rgb)

                        # Convertir de nuevo a BGR para mostrar en pantalla con OpenCV
                        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

                        # Obtener dimensiones de la imagen para el cálculo de coordenadas
                        altura, anchura, _ = frame.shape

                        # Verificar si hay detección de puntos de referencia faciales y del cuerpo
                        if results.face_landmarks:
                            ###############################################################################################################
                            # Extraer puntos de los ojos (aproximadamente) usando índices de los landmarks de Face Mesh
                            ojo_izq = results.face_landmarks.landmark[33]  # Punto medio del parpado inferio del ojo izquierdo
                            ojo_izq2 = results.face_landmarks.landmark[160]  # Punto medio del parpado inferior del ojo derecho
                            ojo_izq3 = results.face_landmarks.landmark[158]  # Punto medio del parpado superior del ojo izquiero
                            ojo_der4 = results.face_landmarks.landmark[133]  # Punto medio del parpado superior del ojo derecho
                            ojo_izq5 = results.face_landmarks.landmark[153]  # Punto medio del parpado superior del ojo izquiero
                            ojo_der6 = results.face_landmarks.landmark[144]  # Punto medio del parpado superior del ojo derecho
                            # Convertir coordenadas normalizadas a píxeles y dibujar círculos
                            x_ojo_izq, y_ojo_izq = int(ojo_izq.x * anchura), int(ojo_izq.y * altura)
                            x_ojo_izq2, y_ojo_izq2 = int(ojo_izq2.x * anchura), int(ojo_izq2.y * altura)
                            x_ojo_izq3, y_ojo_izq3 = int(ojo_izq3.x * anchura), int(ojo_izq3.y * altura)
                            x_ojo_izq4, y_ojo_izq4 = int(ojo_der4.x * anchura), int(ojo_der4.y * altura)
                            x_ojo_izq5, y_ojo_izq5 = int(ojo_izq5.x * anchura), int(ojo_izq5.y * altura)
                            x_ojo_izq6, y_ojo_izq6 = int(ojo_der6.x * anchura), int(ojo_der6.y * altura)

                            cv2.circle(frame, (x_ojo_izq, y_ojo_izq), 5, (255, 100, 0),-1)  # Verde para ojo izquierdo
                            cv2.circle(frame, (x_ojo_izq2, y_ojo_izq2), 5, (255, 0, 100),-1)  # Verde para ojo derecho
                            cv2.circle(frame, (x_ojo_izq3, y_ojo_izq3), 5, (100, 255, 0),-1)  # Verde para ojo izquierdo
                            cv2.circle(frame, (x_ojo_izq4, y_ojo_izq4), 5, (0, 100, 255),-1)  # Verde para ojo derecho
                            cv2.circle(frame, (x_ojo_izq5, y_ojo_izq5), 5, (100, 255, 0),-1)  # Verde para ojo izquierdo
                            cv2.circle(frame, (x_ojo_izq6, y_ojo_izq6), 5, (0, 100, 255), -1)  # Verde para ojo derecho

                            ##########################################################################################################################
                            # Extraer puntos de los ojos (aproximadamente) usando índices de los landmarks de Face Mesh
                            ojo_der = results.face_landmarks.landmark[362]  # Punto medio del párpado inferior del ojo izquierdo
                            ojo_der2 = results.face_landmarks.landmark[385]  # Punto medio del párpado inferior del ojo derecho
                            ojo_der3 = results.face_landmarks.landmark[387]  # Punto medio del párpado superior del ojo izquierdo
                            ojo_izq4 = results.face_landmarks.landmark[263]  # Punto medio del párpado superior del ojo derecho
                            ojo_der5 = results.face_landmarks.landmark[373]  # Punto medio del párpado superior del ojo izquierdo
                            ojo_izq6 = results.face_landmarks.landmark[380]  # Punto medio del párpado superior del ojo derecho

                            # Convertir coordenadas normalizadas a píxeles y dibujar círculos
                            x_ojo_der, y_ojo_der = int(ojo_der.x * anchura), int(ojo_der.y * altura)
                            x_ojo_der2, y_ojo_der2 = int(ojo_der2.x * anchura), int(ojo_der2.y * altura)
                            x_ojo_der3, y_ojo_der3 = int(ojo_der3.x * anchura), int(ojo_der3.y * altura)
                            x_ojo_der4, y_ojo_der4 = int(ojo_izq4.x * anchura), int(ojo_izq4.y * altura)
                            x_ojo_der5, y_ojo_der5 = int(ojo_der5.x * anchura), int(ojo_der5.y * altura)
                            x_ojo_der6, y_ojo_der6 = int(ojo_izq6.x * anchura), int(ojo_izq6.y * altura)

                            cv2.circle(frame, (x_ojo_der, y_ojo_der), 5, (255, 100, 0),-1)  # Verde para ojo izquierdo
                            cv2.circle(frame, (x_ojo_der2, y_ojo_der2), 5, (255, 0, 100),-1)  # Verde para ojo derecho
                            cv2.circle(frame, (x_ojo_der3, y_ojo_der3), 5, (100, 255, 0),-1)  # Verde para ojo izquierdo
                            cv2.circle(frame, (x_ojo_der4, y_ojo_der4), 5, (0, 100, 255), -1)  # Verde para ojo derecho
                            cv2.circle(frame, (x_ojo_der5, y_ojo_der5), 5, (100, 255, 0),-1)  # Verde para ojo izquierdo
                            cv2.circle(frame, (x_ojo_der6, y_ojo_der6), 5, (0, 100, 255),-1)  # Verde para ojo derecho

                            x1, y1 = results.face_landmarks.landmark[160].x, results.face_landmarks.landmark[160].y
                            x2, y2 = results.face_landmarks.landmark[144].x, results.face_landmarks.landmark[144].y
                            long1 = math.hypot(x2 - x1, y2 - y1)
                            x3, y3 = results.face_landmarks.landmark[158].x, results.face_landmarks.landmark[158].y
                            x4, y4 = results.face_landmarks.landmark[153].x, results.face_landmarks.landmark[153].y
                            long2 = math.hypot(x4 - x3, y4 - y3)

                            x5, y5 = results.face_landmarks.landmark[33].x, results.face_landmarks.landmark[33].y
                            x6, y6 = results.face_landmarks.landmark[133].x, results.face_landmarks.landmark[133].y
                            long3 = math.hypot(x6 - x5, y6 - y5)

                            x7, y7 = results.face_landmarks.landmark[387].x, results.face_landmarks.landmark[387].y
                            x8, y8 = results.face_landmarks.landmark[373].x, results.face_landmarks.landmark[373].y
                            long4 = math.hypot(x8 - x7, y8 - y7)

                            x9, y9 = results.face_landmarks.landmark[385].x, results.face_landmarks.landmark[385].y
                            x10, y10 = results.face_landmarks.landmark[380].x, results.face_landmarks.landmark[
                                380].y
                            long5 = math.hypot(x10 - x9, y10 - y9)

                            x11, y11 = results.face_landmarks.landmark[362].x, results.face_landmarks.landmark[
                                362].y
                            x12, y12 = results.face_landmarks.landmark[263].x, results.face_landmarks.landmark[
                                263].y
                            long6 = math.hypot(x12 - x11, y12 - y11)

                            EARI = ((long1 + long2) / (2 * long3)) * 100
                            EARD = ((long4 + long5) / (2 * long6)) * 100
                            print(EARI, EARD);

                            cv2.putText(frame, 'EARD: ' + str(EARD), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (255, 0, 0), 3)
                            cv2.putText(frame, 'EARI: ' + str(EARI), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (255, 0, 0), 3)

                            if EARI < 20 and EARD < 20:
                                if tiempo_condicion_cumplida == 0:
                                    tiempo_condicion_cumplida = time.time()

                                tiempo_transcurrido = time.time() - tiempo_condicion_cumplida

                                if tiempo_transcurrido >= tiempo_limite:
                                    cv2.putText(frame, 'Somnolencia', (85, 150), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                (0, 0, 255), 3)
                                else:
                                    cv2.rectangle(frame, (120, 50), (200, 120), (0, 0, 255), 2)
                            else:
                                tiempo_condicion_cumplida = 0

                            if EARI < 20 and not bloqueo:
                                parpadeos += 1
                                bloqueo = True
                                tiempo_inicio = time.time()

                            if bloqueo and time.time() - tiempo_inicio >= tiempo_de_bloqueo:
                                bloqueo = False

                        cv2.putText(frame, 'Parpadeos: ' + str(parpadeos), (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 0), 3)
                        print(parpadeos)
                        if results.pose_landmarks:
                            # Extraer puntos de las caderas y rodillas (izquierda y derecha)
                            cadera_izq = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
                            cadera_der = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
                            rodilla_izq = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
                            rodilla_der = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]

                            # Convertir coordenadas a píxeles y dibujar círculos
                            x_cadera_izq, y_cadera_izq = int(cadera_izq.x * anchura), int(cadera_izq.y * altura)
                            x_cadera_der, y_cadera_der = int(cadera_der.x * anchura), int(cadera_der.y * altura)
                            x_rodilla_izq, y_rodilla_izq = int(rodilla_izq.x * anchura), int(rodilla_izq.y * altura)
                            x_rodilla_der, y_rodilla_der = int(rodilla_der.x * anchura), int(rodilla_der.y * altura)

                            # Dibujar círculos en los puntos
                            cv2.circle(frame, (x_cadera_izq, y_cadera_izq), 5, (255, 0, 0),-1)  # Azul para cadera izquierda
                            cv2.circle(frame, (x_cadera_der, y_cadera_der), 5, (255, 0, 0),-1)  # Azul para cadera derecha
                            cv2.circle(frame, (x_rodilla_izq, y_rodilla_izq), 5, (0, 0, 255),-1)  # Rojo para rodilla izquierda
                            cv2.circle(frame, (x_rodilla_der, y_rodilla_der), 5, (0, 0, 255),-1)  # Rojo para rodilla derecha
                        # Mostrar el video con puntos de referencia
                        cv2.imshow("Puntos de referencia de ojos, caderas y rodillas", frame)
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
                                    com.write(i.encode('ascii'))
                                elif cx > centro + 50:
                                    # Movemos hacia la derecha
                                    print("Moviendo a la derecha")
                                    com.write(d.encode('ascii'))
                                else:
                                    # Paramos el servo
                                    print("Parando servo")
                                    com.write(p.encode('ascii'))

                        # Mostrar el frame con los dibujos
                        cv2.imshow('Camara', frame)

                        # Salir con la tecla 'ESC'
                        t = cv2.waitKey(1)
                        if t == 27:
                            break

cap.release()
cv2.destroyAllWindows()
