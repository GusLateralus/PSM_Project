import cv2
import mediapipe as mp
import math
import time
import serial

# Configuración del puerto serial para mover el servo
com = serial.Serial("COM5", 9600, write_timeout=10)
d = 'd'
i = 'i'
p = 'p'

# Variables para detección de parpadeos
bloqueo = False
tiempo_de_bloqueo = 0.5  # Tiempo de bloqueo en segundos
parpadeos = 0
tiempo_condicion_cumplida = 0
tiempo_limite = 3
tiempo_guardado = 5  # Tiempo para guardar datos en segundos
ultimo_guardado = time.time()  # Marca de tiempo del último guardado

# Inicializar herramientas de MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_face_detection = mp.solutions.face_detection

# Capturar el video desde la cámara
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Inicializar los modelos de MediaPipe FaceMesh, Holistic y FaceDetection
with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh, \
     mp_holistic.Holistic(
        static_image_mode=False,
        model_complexity=2) as holistic, \
     mp_face_detection.FaceDetection(min_detection_confidence=0.5) as rostros:

    parpadeo_contado = False  # Bandera para realizar un seguimiento de parpadeos
    centro = int(cap.get(3) / 2)  # Centro de la imagen en la cámara

    # Abrir archivo de texto para guardar datos
    with open("registro_camara.txt", "w") as archivo_txt:
        archivo_txt.write("Fecha,Parpadeos,Dis CI - PI,Dis CD - PD\n")
    with open('registro_camara.txt', mode='a') as archivo_txt:
        distancia_cadera_pie_izq_metros = 0
        distancia_cadera_pie_der_metros = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Procesar el frame con los modelos de FaceMesh, Holistic y FaceDetection
            face_results = face_mesh.process(frame_rgb)
            holistic_results = holistic.process(frame_rgb)
            resultado_rostros = rostros.process(frame_rgb)

            # --- Detección de parpadeos (FaceMesh) ---
            if face_results.multi_face_landmarks is not None:
                for face_landmarks in face_results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, face_landmarks,
                        mp_face_mesh.FACEMESH_TESSELATION,
                        mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                        mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))

                    lista = []
                    for i, puntos in enumerate(face_landmarks.landmark):
                        alto, ancho, c = frame.shape
                        x, y = int(puntos.x * ancho), int(puntos.y * alto)
                        lista.append([i, x, y])

                    if len(lista) == 468:
                        x1, y1 = lista[160][1:]; x2, y2 = lista[144][1:]; long1 = math.hypot(x2 - x1, y2 - y1)
                        x3, y3 = lista[158][1:]; x4, y4 = lista[153][1:]; long2 = math.hypot(x4 - x3, y4 - y3)
                        x5, y5 = lista[33][1:]; x6, y6 = lista[133][1:]; long3 = math.hypot(x6 - x5, y6 - y5)
                        x7, y7 = lista[387][1:]; x8, y8 = lista[373][1:]; long4 = math.hypot(x8 - x7, y8 - y7)
                        x9, y9 = lista[385][1:]; x10, y10 = lista[380][1:]; long5 = math.hypot(x10 - x9, y10 - y9)
                        x11, y11 = lista[362][1:]; x12, y12 = lista[263][1:]; long6 = math.hypot(x12 - x11, y12 - y11)

                        EARI = ((long1 + long2) / (2 * long3)) * 100
                        EARD = ((long4 + long5) / (2 * long6)) * 100

                        if EARI < 15 and EARD < 15:
                            if tiempo_condicion_cumplida == 0:
                                tiempo_condicion_cumplida = time.time()

                            tiempo_transcurrido = time.time() - tiempo_condicion_cumplida
                            if tiempo_transcurrido >= tiempo_limite:
                                cv2.putText(frame, 'Somnolencia', (85, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        else:
                            tiempo_condicion_cumplida = 0

                        if EARI < 15 and not bloqueo:
                            parpadeos += 1
                            bloqueo = True
                            tiempo_inicio = time.time()

                        if bloqueo and time.time() - tiempo_inicio >= tiempo_de_bloqueo:
                            bloqueo = False

                    cv2.putText(frame, 'Parpadeos: ' + str(parpadeos), (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

            # --- Detección de rostro más cercano y seguimiento (FaceDetection) ---
            if resultado_rostros.detections is not None:
                min_distancia = float('inf')
                rostro_cercano = None
                al, an, _ = frame.shape

                for id, rostro in enumerate(resultado_rostros.detections):
                    x = rostro.location_data.relative_bounding_box.xmin
                    y = rostro.location_data.relative_bounding_box.ymin
                    ancho = rostro.location_data.relative_bounding_box.width
                    alto = rostro.location_data.relative_bounding_box.height

                    x, y = int(x * an), int(y * al)
                    x1, y1 = int(ancho * an), int(alto * al)
                    xf, yf = x + x1, y + y1
                    cx = (x + xf) // 2
                    cy = (y + yf) // 2

                    distancia_centro = abs(cx - centro)

                    if distancia_centro < min_distancia:
                        min_distancia = distancia_centro
                        rostro_cercano = (cx, cy, x, y, xf, yf, id)

                if rostro_cercano:
                    cx, cy, x, y, xf, yf, id = rostro_cercano
                    cv2.circle(frame, (cx, cy), 3, (0, 0, 255), cv2.FILLED)
                    cv2.line(frame, (cx, 0), (cx, al), (0, 0, 255), 2)
                    cv2.rectangle(frame, (x, y), (xf, yf), (255, 255, 0), 3)
                    cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

                    if cx < centro - 50:
                        com.write('i'.encode('ascii'))
                    elif cx > centro + 50:
                        com.write('d'.encode('ascii'))
                    else:
                        com.write('p'.encode('ascii'))
            out.write(frame)
            cv2.imshow("Detección de parpadeos y seguimiento de rostro", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()