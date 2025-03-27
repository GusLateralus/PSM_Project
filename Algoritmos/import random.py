import random
import pandas as pd

# Función para generar un registro con valores aleatorios para cada columna
def generar_dato(trastorno):
    # Asignar valores predeterminados
    oxigenacion, pulsos, co2 = 90, 80, 400  # Valores predeterminados
    temperatura = round(random.uniform(36.5, 37.5), 1)  # Temperatura normal
    humedad = random.randint(30, 50)  # Humedad normal
    parpadeosminuto = random.randint(5, 30)  # Parpadeos entre 5 y 30
    movimientospiernashora = random.randint(0, 30)  # Movimientos de piernas entre 0 y 30

    # Dependiendo del trastorno, ajustar los valores
    if trastorno == 'Apnea':
        oxigenacion = random.randint(80, 89)  # Oxigenación < 90
        pulsos = random.randint(60, 100)  # Pulsos entre 60 y 100
        co2 = random.randint(800, 1000)  # CO2 > 800
    elif trastorno == 'Insomnio Intermedio':
        oxigenacion = random.randint(90, 100)  # Oxigenación normal
        pulsos = random.randint(80, 120)  # Pulsos altos o irregulares
        co2 = random.randint(300, 1000)  # CO2 en rango normal
        movimientospiernashora = random.randint(5, 15)  # Movimientos moderados
    elif trastorno == 'Paralisis del Sueno':
        oxigenacion = random.randint(90, 100)  # Oxigenación normal
        pulsos = random.randint(60, 90)  # Pulsos estables
        co2 = random.randint(300, 800)  # CO2 en rango normal
        movimientospiernashora = random.randint(0, 5)  # Baja actividad de movimientos
    elif trastorno == 'Sindrome de Piernas Inquietas':
        oxigenacion = random.randint(90, 100)  # Oxigenación normal
        pulsos = random.randint(70, 100)  # Pulsos estables
        co2 = random.randint(300, 1000)  # CO2 en rango normal
        movimientospiernashora = random.randint(15, 30)  # Movimientos altos

    return [oxigenacion, pulsos, co2, temperatura, humedad, parpadeosminuto, movimientospiernashora, trastorno]

# Definir los trastornos
trastornos = ['Insomnio Intermedio', 'Apnea', 'Sin Trastorno', 'Paralisis del Sueno', 'Sindrome de Piernas Inquietas']
data = []

# Crear 40 registros para cada trastorno
for trastorno in trastornos:
    for _ in range(150):
        data.append(generar_dato(trastorno))

# Convertir a DataFrame y guardar como CSV
df = pd.DataFrame(data, columns=['oxigenacion', 'pulsos', 'co2', 'temperatura', 'humedad', 'parpadeosminuto', 'movimientospiernashora', 'trastorno'])
df.to_csv('base_datos_trastornos_sueño.csv', index=False)
