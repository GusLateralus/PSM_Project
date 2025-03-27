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
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
# "Leer" el conjunto de datos mediante pandas
datos_referencia = pd.read_csv(r"C:\Users\Rober\PycharmProjects\TT\base_datos_trastornos_sueño.csv", encoding='latin-1', sep=',')
# If the above doesn't work, try 'ISO-8859-1'
# horny = pd.read_csv(r"/content/datos_sensores2 (1).csv", encoding='ISO-8859-1')
dref=pd.get_dummies(datos_referencia['trastorno'],prefix='trastorno')
dref = dref.astype(int)
print(dref)
#Remove the column from datos_referencia2 instead of datos_referencia
datos_referencia8=datos_referencia.drop(['trastorno'],axis=1)
datos_referencia2=pd.concat([datos_referencia8,dref],axis=1)
# Supongamos que las columnas son: oxigenacion, pulsos, temperatura, humedad, co2 y trastorno
X_referencia = datos_referencia[['oxigenacion', 'pulsos', 'co2', 'temperatura', 'humedad','parpadeosminuto','movimientospiernashora']].values
# Seleccionar variables independientes y objetivo
# y = f(x)
# peeeeero después puede ser de la forma
# y = f(w, u, v, w2, x, r, s, t, ...)
x_train = datos_referencia8[['oxigenacion', 'pulsos', 'co2', 'temperatura', 'humedad','parpadeosminuto','movimientospiernashora']]
# Verify the correct column name from the dataframe 'dref' and add the 'trastorno_' prefix

y_train = dref[['trastorno_Sin Trastorno','trastorno_Apnea','trastorno_Insomnio Intermedio','trastorno_Paralisis del Sueno','trastorno_Sindrome de Piernas Inquietas']]
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split

# Dividir los datos en entrenamiento (80%) y prueba (20%)
X_train, X_test, Y_train, Y_test = train_test_split(
    x_train, y_train, test_size=0.3, random_state=42
)
modelo = tf.keras.models.Sequential()
modelo.add(tf.keras.layers.Dense(128, input_dim=7, activation='relu'))  # 4 características de entrada
modelo.add(tf.keras.layers.Dense(64, activation='relu'))
modelo.add(tf.keras.layers.Dense(32, activation='relu'))
modelo.add(tf.keras.layers.Dense(16, activation='relu'))
modelo.add(tf.keras.layers.Dense(5, activation='softmax'))  # 4 clases en la salida

modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Entrenar el modelo
epocas  = modelo.fit(X_train, Y_train, epochs=70, batch_size=32)
#modelo.fit(x_train, y_train, epochs=50)

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
oxigenacion = 81
pulsos = 87
co2=902
temperatura = 36.9
humedad = 33
parpadeosminuto=30
movimientospiernashora=23
# Crear un array con los datos de entrada88,80,728,37.1,34,13,14,
datos_entrada = np.array([[oxigenacion, pulsos,co2, temperatura, humedad,parpadeosminuto,movimientospiernashora]])

# Realizar la predicción
transtornos = modelo.predict(datos_entrada)

# Mostrar el valor predicho
print(f"Valor predicho: {transtornos}")
import numpy as np

# Convertir probabilidades a etiquetas (para clasificación multiclase)
etiqueta_predicha = np.argmax(transtornos, axis=1)

print(f"Probabilidades predichas: {transtornos}")
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

# Predicciones para el conjunto de prueba
predicciones_test = modelo.predict(X_test)
etiquetas_predichas_test = np.argmax(predicciones_test, axis=1)

# Convertir las etiquetas reales en formato entero
etiquetas_reales_test = np.argmax(Y_test.values, axis=1)

# Calcular la matriz de confusión
matriz_confusion_test = confusion_matrix(etiquetas_reales_test, etiquetas_predichas_test)

# Visualizar la matriz de confusión
disp_test = ConfusionMatrixDisplay(
    confusion_matrix=matriz_confusion_test,
    display_labels=['Sin Trastorno', 'Apnea', 'Insomnio Intermedio', 'Parálisis', 'Piernas Inquietas']
)
disp_test.plot(cmap=plt.cm.Blues)
plt.title("Matriz de Confusión - Conjunto de Prueba")
plt.show()
# Guardar el modelo entrenado
modelo.save("modelo_trastornos_sueno1.h5")
