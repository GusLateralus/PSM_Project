import random
import pandas as pd

# Función para generar un registro con valores aleatorios para cada columna
def generar_dato(trastorno):
    oxigenacion = random.randint(85, 100)
    pulsos = random.randint(60, 100)
    co2 = random.randint(300, 1000)
    temperatura = round(random.uniform(36.5, 37.5), 1)
    humedad = random.randint(30, 50)
    parpadeosminuto = random.randint(5, 30)
    movimientospiernashora = random.randint(0, 20)

    return [oxigenacion, pulsos, co2, temperatura, humedad, parpadeosminuto, movimientospiernashora, trastorno]

# Definir los trastornos
trastornos = ['Insomnio Intermedio', 'Apnea', 'Sin Trastorno', 'Parálisis del Sueño', 'Síndrome de Piernas Inquietas']
data = []

# Crear 40 registros para cada trastorno
for trastorno in trastornos:
    for _ in range(40):
        data.append(generar_dato(trastorno))

# Convertir a DataFrame y guardar como CSV
df = pd.DataFrame(data, columns=['oxigenacion', 'pulsos', 'co2', 'temperatura', 'humedad', 'parpadeosminuto', 'movimientospiernashora', 'trastorno'])
df.to_csv('base_datos_trastornos_sueño.csv', index=False)
