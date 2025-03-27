#------------------------------ Importamos las librerias ------------------------------
import cv2
import mediapipe as mp
import serial
import math
import time
import numpy as np

# Variables para detección de parpadeos
bloqueo = False
tiempo_de_bloqueo = 0.5  # Tiempo de bloqueo en segundos
parpadeos = 0
tiempo_condicion_cumplida = 0
tiempo_condicion_cumplida2 = 0
tiempo_limite = 3
tiempo_guardado = 15  # Tiempo para guardar datos en segundos
ultimo_guardado = time.time()  # Marca de tiempo del último guardado
contador_movimientos = 0
ultima_actualizacion = 0  # Momento del último conteo
tiempo_inicio=0
###################################################################################################################
cerrados = False  # Indica si los ojos están cerrados
parpadeos_con_ojos_cerrados = 0  # Contador de parpadeos con ojos cerrados
umbral_base_cierre = 19  # Umbral para considerar que los ojos están cerrados


  # Umbral para considerar micromovimientos
ultimo_valor_EARI = None  # Último valor de EARI para detectar cambios
distancia_base=65
###################################################################################################################
# Constantes
DISTANCIA_REAL_OJOS_CM = 6.3  # Distancia promedio entre ojos en cm
DISTANCIA_CONOCIDA_CM = 50    # Distancia conocida entre cámara y rostro para calibrar (en cm)
PIXELS_OJOS_CONOCIDA = 100    # Distancia entre ojos en píxeles a la distancia conocida
##################################################################################################################
# Variables iniciales
rodilla_izq_fuera = False
rodilla_der_fuera = False
contador_movimientos = 0
umbral_movimiento = 1.5  # Define el umbral de movimiento en metros o unidades relevantes
ultima_actualizacion = time.time()  # Tiempo inicial
espera_actualizacion = 1  # Tiempo en segundos para verificar movimientos
###################################################################################################################
# Calcular la focal de la cámara
FOCAL = (PIXELS_OJOS_CONOCIDA * DISTANCIA_CONOCIDA_CM) / DISTANCIA_REAL_OJOS_CM

def calcular_distancia_real(distancia_pixeles):
    
    if distancia_pixeles == 0:
        return float('inf')  # Evitar división por cero
    return (DISTANCIA_REAL_OJOS_CM * FOCAL) / distancia_pixeles
# Inicializar herramientas de MediaPipe
def medir_distancia_ojos_camara():
    # Inicializar MediaPipe y la cámara
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

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


#------------------------------Capturar el video--------------------------------
# Configurar el códec y el archivo de salida
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Códec para archivos .mp4
out = cv2.VideoWriter('output_video.mp4', fourcc, 20.0, (width, height))

#-------------------------------Empezamos el while True --------------------------------
with detector.FaceDetection(min_detection_confidence=0.5, model_selection=1) as rostros:
    with mp_holistic.Holistic(static_image_mode=False, model_complexity=1) as holistic:
            # Abrir archivo de texto para guardar datos
        with open("registro_camara2.txt", "w") as archivo_txt:
            archivo_txt.write("Fecha, Hora, Parpadeos, MovimientoPiernas\n")
        with open('registro_camara2.txt', mode='a') as archivo_txt:
                    while cap.isOpened():
                        #time.sleep(1)
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
                           
                         

                            punto_nariz = results.face_landmarks.landmark[1]  # Nariz (por ejemplo)
                            punto_menton = results.face_landmarks.landmark[152]  # Mentón
                            punto_frente = results.face_landmarks.landmark[10]  # Frente (parte superior)
                             
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
                            # Convertir coordenadas a píxeles en naris
                            x_nariz, y_nariz = int(punto_nariz.x * anchura), int(punto_nariz.y * altura)
                            x_menton, y_menton = int(punto_menton.x * anchura), int(punto_menton.y * altura)
                            x_frente, y_frente = int(punto_frente.x * anchura), int(punto_frente.y * altura)
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
                            #ojos principales
                            ojo_prind = results.face_landmarks.landmark[33]  # Punto medio del párpado inferior del ojo izquierdo
                            ojo_prinI = results.face_landmarks.landmark[263] 
                            x_ojo_prind, y_ojo_prind = int(ojo_prind.x * anchura), int(ojo_prind.y * altura)
                            x_ojo_prinI, y_ojo_prinI = int(ojo_prinI.x * anchura), int(ojo_prinI.y * altura)
                             
                            

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

                            EARI = round(((long1 + long2) / (2 * long3)) * 100,2)
                            EARD = round(((long4 + long5) / (2 * long6)) * 100,2)
                            import numpy as np

                            # Inicialización del Filtro de Kalman
                            EARI_est = 30.88  # Estado inicial estimado
                            EARI_cov = 1      # Covarianza inicial (incertidumbre)

                            EARD_est = 30.1   # Estado inicial estimado
                            EARD_cov = 1      # Covarianza inicial (incertidumbre)

                            process_variance = 0.1  # Variabilidad del sistema (ajustar según sea necesario)
                            measurement_variance = 0.5  # Ruido de medición (ajustar según sea necesario)

                            def filtro_kalman(estimado, covarianza, medicion):
                                # Predicción
                                estimado_pred = estimado
                                covarianza_pred = covarianza + process_variance

                                # Actualización
                                kalman_gain = covarianza_pred / (covarianza_pred + measurement_variance)
                                estimado = estimado_pred + kalman_gain * (medicion - estimado_pred)
                                covarianza = (1 - kalman_gain) * covarianza_pred

                                return estimado, covarianza

                            

                            # Aplicar el filtro de Kalman
                            EARI_est, EARI_cov = filtro_kalman(EARI_est, EARI_cov, EARI)
                            EARD_est, EARD_cov = filtro_kalman(EARD_est, EARD_cov, EARD)

                            print(f"EARI suavizado (Kalman): {EARI_est}")
                            print(f"EARD suavizado (Kalman): {EARD_est}")

                                                        


                            #print(EARI, EARD)

                            cv2.putText(frame, 'EARD: ' + str(EARD_est), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 255, 255), 3)
                            cv2.putText(frame, 'EARI: ' + str(EARI_est), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 255, 255), 3)
######################################################################################################################################33
#ojos      
                            # Calcular el ángulo de inclinación vertical entre mentón y nariz
                            dx_menton_nariz = x_nariz - x_menton
                            dy_menton_nariz = y_nariz - y_menton
                            angulo_inclinacion_vertical = math.degrees(math.atan2(dy_menton_nariz, dx_menton_nariz))

                            # Calcular el ángulo de inclinación respecto al frente
                            dx_frente_nariz = x_frente - x_nariz
                            dy_frente_nariz = y_frente - y_nariz
                            angulo_frente = math.degrees(math.atan2(dy_frente_nariz, dx_frente_nariz))

                            # Cálculo del ángulo de inclinación para el ojo izquierdo
                            dx_izq = x_ojo_izq2 - x_ojo_izq  # Diferencia en X entre dos puntos clave
                            dy_izq = y_ojo_izq2 - y_ojo_izq  # Diferencia en Y entre dos puntos clave
                            angulo_izq = math.degrees(math.atan2(dy_izq, dx_izq))  # Ángulo en grados

                            # Cálculo del ángulo de inclinación para el ojo derecho
                            dx_der = x_ojo_der2 - x_ojo_der  # Diferencia en X entre dos puntos clave
                            dy_der = y_ojo_der2 - y_ojo_der  # Diferencia en Y entre dos puntos clave
                            angulo_der = math.degrees(math.atan2(dy_der, dx_der))  # Ángulo en grados 
                            # Mostrar la distancia física en la ventana
                            #cv2.putText(frame, f'AnguloDER: {angulo_der:.2f} cm', (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)                        
                            #cv2.putText(frame, f'AnguloIZQ: {angulo_izq:.2f} cm', (0, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)      
                            cv2.putText(frame, f'Anguloder: { dy_der:.2f} cm', (0, 125), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)      
                              
                            # Crear arrays con las coordenadas en píxeles
                            punto_derecho = np.array([x_ojo_prind, y_ojo_prind])
                            punto_izquierdo = np.array([x_ojo_prinI, y_ojo_prinI])

                            # Calcular la distancia euclidiana en píxeles
                            distancia_pixeles = np.linalg.norm(punto_derecho - punto_izquierdo)
                            
                            # Calcular la distancia física
                            distancia_real_cm = calcular_distancia_real(distancia_pixeles)

                            # Mostrar la distancia física en la ventana
                            cv2.putText(frame, f'Distancia: {distancia_real_cm:.2f} cm', (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)                                       
#####################################################################################################################################
########################### Supongamos que `EARI` es el indicador del estado de los ojos, actualizado en cada iteración.
                            # Ajustar el umbral de cierre dinámicamente
                            # Ajustar umbrales dinámicamente
                        distancia_referencia=60
                        promedio_ojos_abiertos = (37.62 + 35.68 + 37.28 + 32.11 + 35.11) / 5  # = 0.354
                        promedio_ojos_cerrados = (25.82 + 23.35 + 24.89 + 26.69 + 28.93) / 5  # = 0.124
                        umbral_base = (promedio_ojos_abiertos+  promedio_ojos_cerrados ) / 2    
                        umbral_cierre_ajustado =( umbral_base * (distancia_real_cm / distancia_referencia))
                        # Ajustar el umbral basado en la distancia real
                        umbral_cierre_ajustado = umbral_base * (distancia_real_cm / distancia_referencia)

                        #distancia_referencia=147
                        #promedio_ojos_abiertos = (25.15 + 29.59 + 28.44 + 26.93 + 24.48) / 5  # = 0.354
                        #promedio_ojos_cerrados = (19.23 + 20.37 + 16.44 + 15.42 + 19.23) / 5  # = 0.124
                        #umbral_base = (promedio_ojos_abiertos+  promedio_ojos_cerrados ) / 2    
                        #umbral_cierre_ajustado = umbral_base * (distancia_real_cm / distancia_referencia)
                        #print(umbral_base)
                        print("u",umbral_cierre_ajustado)
                        duracion_maxima_parpadeo=50000
                        # Normalizar EARI
                        EARI_normalizado = EARI 
                        print(EARI_normalizado)
                        # Detección de parpadeos
                        if EARI_normalizado < umbral_cierre_ajustado:
                            if not cerrados:
                                cerrados = True
                                tiempo_cierre = time.time()
                            elif time.time() - tiempo_cierre > duracion_maxima_parpadeo:
                                parpadeos += 1
                                cerrados = False  # Finalizar el evento de parpadeo
                        else:
                            if cerrados:
                                cerrados = False
                                parpadeos += 1
                        #print(EARI_normalizado)
                        #print(umbral_cierre_ajustado)    

                        cv2.putText(frame, 'Parpadeos: ' + str(parpadeos), (400, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0,0,0), 3)
                        #print(parpadeos)
                        # Función para calcular la distancia de rodillas
                        def calcular_distancia(x1, y1, x2, y2):
                            return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                        # Coloca estas variables fuera del ciclo principal para evitar que se reinicien cada vez
                        tiempo_de_bloqueo2 = 0.5
                        contador = 0
                        bloqueo2 = False
                        ultimo_guardado2 = time.time()  # Marca de tiempo del último guardado
                                        
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


                            import math
                            import time

                           
                            # En cada fotograma, calculamos las distancias
                            distancia_rodilla_izq = calcular_distancia(x_cadera_izq, y_cadera_izq, x_rodilla_izq, y_rodilla_izq)
                            distancia_rodilla_der = calcular_distancia(x_cadera_der, y_cadera_der, x_rodilla_der, y_rodilla_der)
                            factor_conversion = 0.01  # Ejemplo: 1 píxel = 0.01 metros

                            import time
# Convertir las distancias de píxeles a metros
                            distancia_rodilla_izq = round(distancia_rodilla_izq * factor_conversion, 1)
                            distancia_rodilla_der = round(distancia_rodilla_der * factor_conversion, 1)
                            
##################################################################################################################################
                            umbral_movimiento2 = 590
                            
                            # Verifica el estado actual en cada iteración
                            
                            espera_actualizacion=50000
                            
                            # Verificar rodilla izquierda
                            if y_rodilla_izq > umbral_movimiento2:
                                if not rodilla_izq_fuera:  # Detectar transición
                                    rodilla_izq_fuera = True
                                    tiempo_cierre2 = time.time()
                                                                                                                              
                                elif time.time() - tiempo_cierre2 > espera_actualizacion:  # Verificar cada 7 segundos
                                    contador_movimientos += 1
                                    rodilla_izq_fuera = False
                                   
                                    #print("Movimiento detectado en la rodilla izquierda")
                            else:
                                if  rodilla_izq_fuera: 
                                 rodilla_izq_fuera = False  # Volvió a posición normal
                                 contador_movimientos += 1
                            

                            
                            
                            # Actualizar el tiempo de la última verificación
                            #ultima_actualizacion = time.time()

                        # Imprimir el número total de movimientos acumulados
                        #print(f"Movimientos de piernas detectados: {contador_movimientos}")

                   
####################################################################################################################################


                       
                        cv2.putText(frame, 'RI ' + str(y_rodilla_der), (0, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
                        cv2.putText(frame, 'RD ' + str(y_rodilla_izq), (0, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
                        cv2.putText(frame, 'MP ' + str(contador_movimientos), (400, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

                        # Dibujar círculos en los puntos
                        cv2.circle(frame, (x_cadera_izq, y_cadera_izq), 5, (255, 0, 0),-1)  # Azul para cadera izquierda
                        cv2.circle(frame, (x_cadera_der, y_cadera_der), 5, (255, 0, 0),-1)  # Azul para cadera derecha
                        cv2.circle(frame, (x_rodilla_izq, y_rodilla_izq), 5, (0, 0, 255),-1)  # Rojo para rodilla izquierda
                        cv2.circle(frame, (x_rodilla_der, y_rodilla_der), 5, (0, 0, 255),-1)  # Rojo para rodilla derecha
                         # Guardar datos en el archivo de texto cada 5 segundos
                        if time.time() - ultimo_guardado >= tiempo_guardado:
                            # Guardar datos
                            archivo_txt.write(
                                f"{time.strftime('%Y-%m-%d %H:%M:%S')},{parpadeos_con_ojos_cerrados},{contador_movimientos}\n")
                                
                            archivo_txt.flush()  # Asegurarse de que los datos se escriben inmediatamente
                            ultimo_guardado = time.time()  # Actualizar la marca de tiempo del último guardado
                        # Mostrar el video con puntos de referencia
                       # Guardar el frame en el archivo de video
                        out.write(frame)
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
                                    #print("Moviendo a la izquierda")
                                    com.write(i.encode('ascii'))
                                elif cx > centro + 50:
                                    # Movemos hacia la derecha
                                    #print("Moviendo a la derecha")
                                    com.write(d.encode('ascii'))
                                else:
                                    # Paramos el servo
                                    #print("Parando servo")
                                    com.write(p.encode('ascii'))

                        
                        # Mostrar el frame con los dibujos
                        cv2.imshow('Camara', frame)

                        # Salir con la tecla 'ESC'
                        t = cv2.waitKey(1)
                        if t == 27:
                            break
cap.release()
out.release()
cv2.destroyAllWindows()
