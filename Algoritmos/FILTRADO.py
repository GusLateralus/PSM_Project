import pandas as pd

# Cargar el archivo CSV

data = pd.read_csv(r"C:\Users\Rober\PycharmProjects\TT\DATOS2.CSV", encoding='latin-1', sep=',')

# Combinar las columnas de Fecha y Hora en un único timestamp
data['Timestamp'] = pd.to_datetime(data['Fecha'] + ' ' + data[' Hora'])

# Establecer el Timestamp como índice para facilitar la agrupación
data.set_index('Timestamp', inplace=True)

# Seleccionar las columnas de los sensores
sensores = [
    ' Temperatura ambiental (DHT11)',
    ' Humedad (DHT11)',
    ' PPM (MQ135)',
    ' Temp. Objeto (MLX90614)',
    ' Pulso Card. (MAX30102)',
    ' Oxigenacion (MAX30102)'
]

# Promediar los datos cada 30 minutos
promedios = data[sensores].resample('30T').mean().round(2)

# Guardar los promedios en un nuevo archivo CSV
output_path = 'promedios_30min.csv'
promedios.to_csv(output_path)

print(f"Archivo de promedios generado: {output_path}")
