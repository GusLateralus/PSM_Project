import cv2
import mediapipe as mp
import math
import time

bloqueo = False
tiempo_de_bloqueo = 0.5  # Tiempo de bloqueo en segundos
parpadeos = 0
tiempo_condicion_cumplida = 0
tiempo_limite = 3
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)


with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5) as face_mesh:
    parpadeo_contado = False  # Nueva bandera para realizar un seguimiento de si ya se ha contado un parpadeo

    while True:
        ret, frame = cap.read()
        if ret==False:
            break
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        ptosX = []
        ptosY = []
        lista = []
        r = 2

        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame, face_landmarks,
                                          mp_face_mesh.FACEMESH_TESSELATION,
                                          mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                                          mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))

                # Extraer los puntos de interés del rostro
                for i, puntos in enumerate(face_landmarks.landmark):
                    alto, ancho, c = frame.shape
                    x, y = int(puntos.x*ancho), int(puntos.y*alto)
                    ptosX.append(x)
                    ptosY.append(y)
                    lista.append([i, x, y])
                    if len(lista) == 468:
                        # Ojo izquierdo
                        x1, y1 = lista[160][1:]
                        x2, y2 = lista[144][1:]
                        cx, cy = (x1 + x2)//2, (y1 + y2)//2
                        cv2.circle(frame, (x1, y1), r, (0, 0, 0), cv2.FILLED)
                        long1 = math.hypot(x2-x1, y2-y1)

                        x3, y3 = lista[158][1:]
                        x4, y4 = lista[153][1:]
                        cx2, cy2 = (x3 + x4)//2, (y3 + y4)//2
                        cv2.circle(frame, (x3, y3), r, (0, 0, 0), cv2.FILLED)
                        long2 = math.hypot(x4-x3, y4-y3)

                        x5, y5 = lista[33][1:]
                        x6, y6 = lista[133][1:]
                        cx3, cy3 = (x5 + x6)//2, (y5 + y6)//2
                        cv2.circle(frame, (x5, y5), r, (0, 0, 0), cv2.FILLED)
                        long3 = math.hypot(x6-x5, y6-y5)

                        # Ojo derecho
                        x7, y7 = lista[387][1:]
                        x8, y8 = lista[373][1:]
                        cx4, cy4 = (x7 + x8)//2, (y7 + y8)//2
                        cv2.circle(frame, (x7, y7), r, (0, 0, 0), cv2.FILLED)
                        long4 = math.hypot(x8-x7, y8-y7)

                        x9, y9 = lista[385][1:]
                        x10, y10 = lista[380][1:]
                        cx5, cy5 = (x9 + x10)//2, (y9 + y10)//2
                        cv2.circle(frame, (x9, y9), r, (0, 0, 0), cv2.FILLED)
                        long5 = math.hypot(x10-x9, y10-y9)

                        x11, y11 = lista[362][1:]
                        x12, y12 = lista[263][1:]
                        cx6, cy6 = (x11 + x12)//2, (y11 + y12)//2
                        cv2.circle(frame, (x11, y11), r, (0, 0, 0), cv2.FILLED)
                        long6 = math.hypot(x12-x11, y12-y11)

                        EARI = ((long1 + long2)/(2*long3))*100
                        print(EARI)
                        #print(EARI * 100)
                        EARD = (long4 + long5)/(2*long6)*100
                        print(EARD)
                        #print(EARD * 100)
                        #cadena = "paradeos: ", parapadeos
                        parpadeos_cadena = str(parpadeos)
                        prp=0
                        cv2.putText(frame, 'parapadeos: ' + parpadeos_cadena, (480, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,9,255), 3)

                        if EARI < 25 and EARD < 25:
                            if tiempo_condicion_cumplida == 0:
                                tiempo_condicion_cumplida = time.time()  # Inicia el temporizador


                            tiempo_transcurrido = time.time() - tiempo_condicion_cumplida


                            if tiempo_transcurrido >= tiempo_limite:
                                cv2.putText(frame, 'somnolencia ', (85, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
                                cv2.rectangle(frame, (120, 50), (200, 120), (0, 0, 255), cv2.FILLED)
                                parpadeo_contado = True
                            else:
                                cv2.rectangle(frame, (120, 50), (200, 120), (0, 0, 255), 2)



                        else:
                            tiempo_condicion_cumplida = 0
                            cv2.rectangle(frame, (120, 50), (200, 120), (0, 0, 255), 2)
                            parpadeo_contado = False


                        if EARI < 25 and not bloqueo:
                            tiempo_transcurrido = time.time() - tiempo_condicion_cumplida
                            if tiempo_transcurrido<0.5:
                                    parpadeos += 1
                                    bloqueo = True
                                    tiempo_inicio = time.time()  # Iniciar el temporizador
                        if bloqueo and time.time() - tiempo_inicio >= tiempo_de_bloqueo:
                            bloqueo = False



        #print(parpadeos)
        cv2.imshow("Frame", frame)
        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            break

cap.release()
cv2.destroyAllWindows()