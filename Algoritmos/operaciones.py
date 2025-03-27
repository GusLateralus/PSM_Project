import cv2
import mediapipe as mp
import math
import time

# Variables para detección de parpadeos
bloqueo = False
tiempo_de_bloqueo = 0.5  # Tiempo de bloqueo en segundos
parpadeos = 0
tiempo_condicion_cumplida = 0
tiempo_limite = 3

# Inicializar herramientas de MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# Capturar el video desde la cámara
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Inicializar los modelos de MediaPipe FaceMesh y Holistic
with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh, \
     mp_holistic.Holistic(
        static_image_mode=False,
        model_complexity=2) as holistic:

    parpadeo_contado = False  # Bandera para realizar un seguimiento de parpadeos

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesar el frame con los dos modelos
        face_results = face_mesh.process(frame_rgb)
        holistic_results = holistic.process(frame_rgb)

        # --- Detección de parpadeos (FaceMesh) ---
        if face_results.multi_face_landmarks is not None:
            for face_landmarks in face_results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame, face_landmarks,
                    mp_face_mesh.FACEMESH_TESSELATION,
                    mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))

                # Extracción de puntos clave de los ojos para el cálculo de EARI y EARD
                lista = []
                for i, puntos in enumerate(face_landmarks.landmark):
                    alto, ancho, c = frame.shape
                    x, y = int(puntos.x * ancho), int(puntos.y * alto)
                    lista.append([i, x, y])

                if len(lista) == 468:
                    # Cálculo de distancias para los ojos izquierdo y derecho
                    x1, y1 = lista[160][1:]
                    x2, y2 = lista[144][1:]
                    long1 = math.hypot(x2 - x1, y2 - y1)

                    x3, y3 = lista[158][1:]
                    x4, y4 = lista[153][1:]
                    long2 = math.hypot(x4 - x3, y4 - y3)

                    x5, y5 = lista[33][1:]
                    x6, y6 = lista[133][1:]
                    long3 = math.hypot(x6 - x5, y6 - y5)

                    # Ojo derecho
                    x7, y7 = lista[387][1:]
                    x8, y8 = lista[373][1:]
                    long4 = math.hypot(x8 - x7, y8 - y7)

                    x9, y9 = lista[385][1:]
                    x10, y10 = lista[380][1:]
                    long5 = math.hypot(x10 - x9, y10 - y9)

                    x11, y11 = lista[362][1:]
                    x12, y12 = lista[263][1:]
                    long6 = math.hypot(x12 - x11, y12 - y11)

                    EARI = ((long1 + long2) / (2 * long3)) * 100
                    EARD = ((long4 + long5) / (2 * long6)) * 100

                    if EARI < 15 and EARD < 15:
                        if tiempo_condicion_cumplida == 0:
                            tiempo_condicion_cumplida = time.time()

                        tiempo_transcurrido = time.time() - tiempo_condicion_cumplida

                        if tiempo_transcurrido >= tiempo_limite:
                            cv2.putText(frame, 'Somnolencia', (85, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        else:
                            cv2.rectangle(frame, (120, 50), (200, 120), (0, 0, 255), 2)
                    else:
                        tiempo_condicion_cumplida = 0

                    if EARI < 15 and not bloqueo:
                        parpadeos += 1
                        bloqueo = True
                        tiempo_inicio = time.time()

                    if bloqueo and time.time() - tiempo_inicio >= tiempo_de_bloqueo:
                        bloqueo = False

                cv2.putText(frame, 'Parpadeos: ' + str(parpadeos), (480, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 9, 255), 3)
                print(parpadeos)
        # --- Detección de gestos y posturas (Holistic) ---
        # Detección de manos
        if holistic_results.left_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, holistic_results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=1),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2))

        if holistic_results.right_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, holistic_results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1),
                mp_drawing.DrawingSpec(color=(57, 143, 0), thickness=2))
        if holistic_results.pose_landmarks:
            # Obtener las dimensiones del frame
            altura, anchura, _ = frame.shape

            # Obtener los landmarks de las caderas
            cadera_izquierda = holistic_results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
            cadera_derecha = holistic_results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]

            # Obtener los landmarks de los índices de los pies
            pie_izquierdo = holistic_results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]
            pie_derecho = holistic_results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]

            # Convertir las coordenadas normalizadas (0 a 1) a píxeles para caderas
            x_cadera_izq, y_cadera_izq = int(cadera_izquierda.x * anchura), int(cadera_izquierda.y * altura)
            x_cadera_der, y_cadera_der = int(cadera_derecha.x * anchura), int(cadera_derecha.y * altura)

            # Convertir las coordenadas normalizadas (0 a 1) a píxeles para los índices de los pies
            x_pie_izq, y_pie_izq = int(pie_izquierdo.x * anchura), int(pie_izquierdo.y * altura)
            x_pie_der, y_pie_der = int(pie_derecho.x * anchura), int(pie_derecho.y * altura)

            # Calcular la distancia entre la cadera izquierda y el índice del pie izquierdo
            distancia_cadera_pie_izq = math.hypot(x_pie_izq - x_cadera_izq, y_pie_izq - y_cadera_izq)

            # Calcular la distancia entre la cadera derecha y el índice del pie derecho
            distancia_cadera_pie_der = math.hypot(x_pie_der - x_cadera_der, y_pie_der - y_cadera_der)

            # Mostrar la distancia en el frame para las caderas y los índices de los pies
            cv2.putText(frame, f'Distancia cadera izq - pie izq: {int(distancia_cadera_pie_izq)} px', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Distancia cadera der - pie der: {int(distancia_cadera_pie_der)} px', (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Dibujar círculos en las caderas e índices de los pies
            cv2.circle(frame, (x_cadera_izq, y_cadera_izq), 10, (0, 255, 0), -1)  # Círculo cadera izquierda
            cv2.circle(frame, (x_cadera_der, y_cadera_der), 10, (0, 0, 255), -1)  # Círculo cadera derecha
            cv2.circle(frame, (x_pie_izq, y_pie_izq), 10, (255, 255, 0), -1)  # Círculo pie izquierdo
            cv2.circle(frame, (x_pie_der, y_pie_der), 10, (255, 0, 0), -1)  # Círculo pie derecho

        # Mostrar el frame procesado
        cv2.imshow('Video', frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
