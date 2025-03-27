import cv2
import numpy as np
import mediapipe as mp

# Constantes
DISTANCIA_REAL_OJOS_CM = 6.3  # Distancia promedio entre ojos en cm
DISTANCIA_CONOCIDA_CM = 50    # Distancia conocida entre cámara y rostro para calibrar (en cm)
PIXELS_OJOS_CONOCIDA = 100    # Distancia entre ojos en píxeles a la distancia conocida
# Definir la variable como global
distancia_real_cm = None
# Calcular la focal de la cámara
FOCAL = (PIXELS_OJOS_CONOCIDA * DISTANCIA_CONOCIDA_CM) / DISTANCIA_REAL_OJOS_CM

def calcular_distancia_real(distancia_pixeles):
    
    if distancia_pixeles == 0:
        return float('inf')  # Evitar división por cero
    return (DISTANCIA_REAL_OJOS_CM * FOCAL) / distancia_pixeles

def medir_distancia_ojos_camara():
    # Inicializar MediaPipe y la cámara
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("No se puede acceder a la cámara.")
            break

        # Convertir el frame a RGB (MediaPipe usa RGB en lugar de BGR)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesar el frame para obtener landmarks
        results = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Extraer los puntos clave faciales
                h, w, _ = frame.shape
                landmarks = [(int(pt.x * w), int(pt.y * h)) for pt in face_landmarks.landmark]

                # Calcular la distancia entre los ojos en píxeles
                distancia_pixeles = np.linalg.norm(np.array(landmarks[33]) - np.array(landmarks[263]))


                print(distancia_pixeles)
                # Calcular la distancia física
                distancia_real_cm = calcular_distancia_real(distancia_pixeles)

                # Mostrar la distancia física en la ventana
                cv2.putText(frame, f'Distancia: {distancia_real_cm:.2f} cm', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Dibujar los ojos
                cv2.circle(frame, landmarks[33], 5, (255, 0, 0), -1)  # Ojo izquierdo
                cv2.circle(frame, landmarks[263], 5, (255, 0, 0), -1)  # Ojo derecho

        # Mostrar el frame con la distancia
        cv2.imshow('Distancia entre ojos', frame)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

# Ejecutar la medición
medir_distancia_ojos_camara()

