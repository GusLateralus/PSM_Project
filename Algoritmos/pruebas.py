from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
datos_referencia = pd.read_csv(r"C:\Users\Rober\PycharmProjects\TT\base_datos_polisomnografia_200.csv", encoding='latin-1', sep=',')
# Cargar el modelo previamente entrenad

# Calcular los promedios solo para las columnas numéricas
promedios = datos_referencia.mean(numeric_only=True)
print(promedios)

modelo_cargado = load_model(r"C:\Users\Rober\PycharmProjects\TT\modelo_trastornos_sueno.h5")
# Nuevos datos de entrada
oxigenacion = promedios['oxigenacion']
pulsos = promedios['pulsos']
co2 = promedios['co2']
temperatura = promedios['temperatura']
humedad = promedios['humedad']
parpadeosminuto = promedios['parpadeosminuto']
movimientospiernashora = promedios['movimientospiernashora']

# Crear un array con los nuevos datos
datos_entrada = np.array([[oxigenacion, pulsos, co2, temperatura, humedad, parpadeosminuto, movimientospiernashora]])

# Realizar la predicción con el modelo cargado
transtornos = modelo_cargado.predict(datos_entrada)

# Mostrar el valor predicho
print(f"Valor predicho: {transtornos}")

# Convertir probabilidades a etiquetas (para clasificación multiclase)
etiqueta_predicha = np.argmax(transtornos, axis=1)
print(etiqueta_predicha)

print(f"Probabilidades predichas: {transtornos}")
if etiqueta_predicha == 0:
    print("El trastorno diagnosticado es Sin trastorno")
elif etiqueta_predicha == 1:
    print("El trastorno diagnosticado es Apnea")
elif etiqueta_predicha == 2:
    print("El trastorno diagnosticado es Insomnio intermedio")
elif etiqueta_predicha == 3:
    print("El trastorno diagnosticado es Parálisis")
elif etiqueta_predicha == 4:
    print("El trastorno diagnosticado es Síndrome de piernas inquietas")
else:
    print("Error en la predicción")