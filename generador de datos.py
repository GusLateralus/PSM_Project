import random
import pandas as pd
import time
from datetime import datetime

# Función para generar un registro con valores aleatorios para cada columna
def generar_dato(trastorno):
    # Fecha y Hora actual
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    hora_actual = datetime.now().strftime("%H:%M:%S")

    # Valores predeterminados
    oxigenacion, pulsos, co2 = 90, 80, 400  # Valores predeterminados
    temperatura = round(random.uniform(36.5, 37.5), 1)  # Temperatura normal
    humedad = random.randint(30, 50)  # Humedad normal
    parpadeosminuto = random.randint(5, 30)  # Parpadeos entre 5 y 30
    movimientospiernashora = random.randint(0, 30)  # Movimientos de piernas entre 0 y 30

    # Dependiendo del trastorno, ajustar los valores
    if trastorno == 'Apnea':
        oxigenacion = random.randint(80, 89)
        pulsos = random.randint(60, 100)
        co2 = random.randint(800, 1000)
    elif trastorno == 'Insomnio Intermedio':
        oxigenacion = random.randint(90, 100)
        pulsos = random.randint(80, 120)
        co2 = random.randint(300, 1000)
        movimientospiernashora = random.randint(5, 15)
    elif trastorno == 'Paralisis del Sueno':
        oxigenacion = random.randint(90, 100)
        pulsos = random.randint(60, 90)
        co2 = random.randint(300, 800)
        movimientospiernashora = random.randint(0, 5)
    elif trastorno == 'Sindrome de Piernas Inquietas':
        oxigenacion = random.randint(90, 100)
        pulsos = random.randint(70, 100)
        co2 = random.randint(300, 1000)
        movimientospiernashora = random.randint(15, 30)

    return [fecha_actual, hora_actual, oxigenacion, pulsos, co2, temperatura, humedad, parpadeosminuto, movimientospiernashora, trastorno]

# Definir los trastornos
trastornos = ['Insomnio Intermedio', 'Apnea', 'Sin Trastorno', 'Paralisis del Sueno', 'Sindrome de Piernas Inquietas']
data = []

# Crear registros con pausa de 7 segundos entre ellos
for trastorno in trastornos:
    for _ in range(50):  # Puedes ajustar la cantidad de registros por trastorno
        data.append(generar_dato(trastorno))
        print(f"Generando datos para {trastorno}...")  # Mensaje informativo
        time.sleep(7)  # Esperar 7 segundos

# Convertir a DataFrame y guardar como CSV
df = pd.DataFrame(data, columns=['Fecha', 'Hora', 'oxigenacion', 'pulsos', 'co2', 'temperatura', 'humedad', 'parpadeosminuto', 'movimientospiernashora','transtorno'])
df.to_csv('base_datos_trastornos_sueño.csv', index=False)

print("Datos generados y guardados en 'base_datos_trastornos_sueño1.csv'.")
