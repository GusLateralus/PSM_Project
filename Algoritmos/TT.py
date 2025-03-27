import tensorflow as tf
import numpy as np
import numpy as np
import pandas as pd
import seaborn
import matplotlib.pyplot as mp
import cv2
import mediapipe as mp
import math
import time
# "Ler" el conjunto de datos mediante pandas
# Asegúrate de que el nombre del archivo es correcto
datos_referencia = pd.read_csv(r"C:\Users\Rober\PycharmProjects\TT\datosTT2Completos.csv", encoding='latin-1', sep=',')
# If the above doesn't work, try 'ISO-8859-1'
# horny = pd.read_csv(r"/content/datos_sensores2 (1).csv", encoding='ISO-8859-1')
dref=pd.get_dummies(datos_referencia['trastorno'],prefix='trastorno')
dref = dref.astype(int)

#Remove the column from datos_referencia2 instead of datos_referencia
datos_referencia8=datos_referencia.drop(['trastorno'],axis=1)
datos_referencia2=pd.concat([datos_referencia8,dref],axis=1)
# Supongamos que las columnas son: oxigenacion, pulsos, temperatura, humedad, co2 y trastorno
X_referencia = datos_referencia[['oxigenacion', 'pulsos', 'temperatura', 'humedad','co2']].values
# Seleccionar variables independientes y objetivo
# y = f(x)
# peeeeero después puede ser de la forma
# y = f(w, u, v, w2, x, r, s, t, ...)
x_train = datos_referencia8[['oxigenacion', 'pulsos', 'temperatura', 'humedad', 'co2']]
# Verify the correct column name from the dataframe 'dref' and add the 'trastorno_' prefix
y_train = dref[['trastorno_Sin_trastorno','trastorno_apnea','trastorno_insomnio_intermedio','trastorno_paralisis','trastorno_sindrome_piernas_inquietas']]
from keras.models import Sequential
from keras.layers import Dense

modelo = tf.keras.models.Sequential()
modelo.add(tf.keras.layers.Dense(128, input_dim=5, activation='relu'))  # 4 características de entrada
modelo.add(tf.keras.layers.Dense(5, activation='softmax'))  # 4 clases en la salida

modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss='categorical_crossentropy'
)

# Entrenar el modelo
epocas = modelo.fit(x_train, y_train, epochs=100)

# Octenemos los valores de las perdídas
print(epocas.history["loss"])
import matplotlib.pyplot as plt

# Entonces graficamos
plt.plot(epocas.history["loss"])
plt.xlabel("Época")
plt.ylabel("Función de pérdida")
plt.grid()
plt.show()
import numpy as np

# Datos de entrada
oxigenacion = 95
pulsos = 75
temperatura = 36.8
humedad = 49
co2=404
# Crear un array con los datos de entrada
datos_entrada = np.array([[oxigenacion, pulsos, temperatura, humedad,co2]])

# Realizar la predicción
transtornos = modelo.predict(datos_entrada)

# Mostrar el valor predicho
print(f"Valor predicho: {transtornos}")
import numpy as np

# Datos de entrada
oxigenacion = 95
pulsos = 75
temperatura = 36.8
humedad = 49
co2=404
# Crear un array con los datos de entrada
datos_entrada = np.array([[oxigenacion, pulsos, temperatura, humedad,co2]])

# Realizar la predicción
probabilidades = modelo.predict(datos_entrada)

# Convertir probabilidades a etiquetas (para clasificación multiclase)
etiqueta_predicha = np.argmax(probabilidades, axis=1)

print(f"Probabilidades predichas: {probabilidades}")
if etiqueta_predicha == 0:
    print("El transtorno diagnosticado es Sin transtorno")
elif etiqueta_predicha == 1:
    print("El transtorno diagnosticado es Apnea")
elif etiqueta_predicha == 2:
    print("El transtorno diagnosticado es Insomnio intermedio")
elif etiqueta_predicha == 3:
    print("El transtorno diagnosticado es Paralisis")
elif etiqueta_predicha == 4:
    print("El transtorno diagnosticado es Sindrome de piernas inquietas")
else:
    print("Error en la predicción")


