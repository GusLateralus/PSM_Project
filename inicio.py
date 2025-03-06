import tkinter as tk
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import serial
import math
import time
import numpy as np
import threading

# Función que se ejecuta al presionar el botón
def ejecutar_codigo():
    print("¡El código se está ejecutando!")
     #------------------------------ Importamos las librerias ------------------------------
    from PIL import Image, ImageTk
    import cv2
    import mediapipe as mp
    import serial
    import math
    import time
    import numpy as np
    import threading

    # Variables para detección de parpadeos
    bloqueo = False
    tiempo_de_bloqueo = 0.5  # Tiempo de bloqueo en segundos
    parpadeos = 0
    tiempo_condicion_cumplida = 0
    tiempo_condicion_cumplida2 = 0
    tiempo_limite = 3
    tiempo_guardado = 1  # Tiempo para guardar datos en segundos
    ultimo_guardado = time.time()  # Marca de tiempo del último guardado
    contador_movimientos = 0
    ultima_actualizacion = 0  # Momento del último conteo
    tiempo_inicio=0
    