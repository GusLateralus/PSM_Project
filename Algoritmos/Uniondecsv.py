import pandas as pd

# Cargar los archivos CSV
archivo_1 = pd.read_csv('DATOS2.CSV')  # Archivo con 6 columnas
archivo_2 = pd.read_csv('registro_camara2.txt')  # Archivo con 3 columnas

# Asegurarse de que las columnas de fecha estén tratadas como string
archivo_1[' Hora'] = archivo_1[' Hora'].astype(str)
archivo_2[' Hora'] = archivo_2[' Hora'].astype(str)

# Hacer el merge de los dos archivos por las columnas de hora
archivo_unido = pd.merge(archivo_1, archivo_2, left_on=' Hora', right_on=' Hora', how='inner')

# Renombrar las columnas para mejor claridad si es necesario (opcional)
archivo_unido.rename(columns={'Fecha_x': 'Fecha Archivo 1', 'Fecha_y': 'Fecha Archivo 2'}, inplace=True)

# Guardar el archivo combinado en un nuevo CSV
archivo_unido.to_csv('archivo_unido.csv', index=False)

# Eliminar la columna 'Fecha Archivo 2'
archivo_unido = archivo_unido.drop(columns=['Fecha Archivo 2'])

# Guardar el archivo combinado sin la columna 'Fecha Archivo 2'
archivo_unido.to_csv('archivo_unidoTT.csv', index=False)

print("Columna 'Fecha Archivo 2' eliminada y archivo guardado correctamente como 'archivo_unido_sin_fecha2.csv'")
