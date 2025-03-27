import pandas as pd

# Cargar los archivos CSV
archivo_1 = pd.read_csv('DATOS2.CSV')  # Archivo con 6 columnas
archivo_2 = pd.read_csv('registro_camara.txt')  # Archivo con 3 columnas

# Asegurarse de que las columnas de fecha estén tratadas como string
archivo_1[' Hora'] = archivo_1[' Hora'].astype(str)
archivo_2[' Hora'] = archivo_2[' Hora'].astype(str)

# Hacer el merge de los dos archivos por las columnas de fecha
# Usamos 'Timestamp' del archivo_1 y 'Fecha' del archivo_2
archivo_unido = pd.merge(archivo_1, archivo_2, left_on=' Hora', right_on=' Hora', how='inner')

# Eliminar la columna de fecha del segundo archivo (archivo_2)
#archivo_unido = archivo_unido.drop(columns=[' Hora'])

# Guardar el archivo combinado en un nuevo CSV
archivo_unido.to_csv('archivo_unido.csv', index=False)

print("Archivos unidos y guardados correctamente como 'archivo_unido.csv'")

