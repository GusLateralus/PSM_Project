import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import seaborn as sns
import pandas as pd
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QSplitter, QGridLayout, QDialog, QMessageBox, QFileDialog
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from conetsion import create_connection
from icon_manager import get_icon_path

# Clase principal de la aplicación
class SleepDataWindow(QWidget):
    def __init__(self, usuario, conexion):  # Constructor corregido
        super().__init__()
        self.init_ui()
        self.connection = conexion
        self.usuario = usuario
        self.data = None
        #print(f'Usuario: {self.usuario}') #Línea de código para depurar


    def init_ui(self):
        self.setWindowTitle('Resultados del estudio')
        self.setGeometry(300, 300, 800, 600)  # Ajustamos el tamaño para dar más espacio a las gráficas
        self.setWindowIcon(QIcon(get_icon_path('bar-graph.png')))
        self.setStyleSheet('''QWidget {
            background: qlineargradient(
                spread:pad, 
                x1:0, y1:0, x2:1, y2:1, 
                stop:0 rgba(36, 62, 101, 0.94), 
                stop:1 rgba(7, 19, 36, 0.94)
            );
        }''')
        self.generar_contenido()

    def generar_contenido(self):
        # Crear el QSplitter para dividir la ventana en dos secciones
        splitter = QSplitter(Qt.Orientation.Vertical)

        #Layout principal:
        layMain = QVBoxLayout()
        
        # Layout horizontal para los controles (campo de texto y botón)
        layouth1 = QHBoxLayout()
        layouth2 = QHBoxLayout()

        # Añadimos los widgets para introducir el número de estudio de un paciente asociado a un médico en particular
        self.read_estudio = QLineEdit()
        self.read_estudio.setPlaceholderText('Inserte el número de estudio del paciente')
        self.read_estudio.setStyleSheet(
             """
            QLineEdit {
                border: 2px solid #5A9;
                border-radius: 15px;
                padding: 5px;
                background-color: transparent;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #7AB; /* Color diferente al enfocar */
            }
            """
        )
       
        button_estudio = self.create_button('Buscar',get_icon_path('search.png'),'Arial Black',34)

        # Aquí creamos un botón para regresar a la ventana anterior y cerrar la ventana de los resultados
        back_button = self.create_button('Regresar',get_icon_path('left.png'),'Arial Black',34)


        # Campo de texto para la ruta del archivo
        self.ruta_archivo = QLineEdit()
        self.ruta_archivo.setPlaceholderText('Inserte un archivo .csv')
        self.ruta_archivo.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #5A9;
                border-radius: 15px;
                padding: 5px;
                background-color: transparent;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #7AB; /* Color diferente al enfocar */
            }
            """
        )
        self.ruta_archivo.setFixedSize(600, 40)
        self.ruta_archivo.setVisible(False)

        # Botón de lectura de archivo
        self.boton_leer_csv = self.create_button('',get_icon_path('upload.png'),'Arial Black',34)
        self.boton_leer_csv.setVisible(False)

        # Botón para realizar prediagnóstico:
        self.prediagnosis_button = self.create_button('Prediagnóstico',get_icon_path('diagnosis.png'),'Arial Black',34)
        self.prediagnosis_button.setVisible(False)


        layouth1.addWidget(self.read_estudio)
        layouth1.addWidget(button_estudio)
        layouth1.addWidget(back_button)
        layouth2.addWidget(self.ruta_archivo)
        layouth2.addWidget(self.boton_leer_csv)
        layouth2.addWidget(self.prediagnosis_button)

        layMain.addLayout(layouth1)
        layMain.addLayout(layouth2)
        

        # Panel para los gráficos (vacío por ahora, solo el espacio)
        grafico_panel = QWidget()
        self.grafico_layout = QGridLayout()  # Cambiar a QGridLayout para manejar múltiples gráficas
        
        # Ejemplo de diferentes tipos de gráficos
        #self.plot_multiple_graphs(self.grafico_layout)

        grafico_panel.setLayout(self.grafico_layout)

        # Crear un QWidget para los controles y añadirlo al QSplitter
        left_panel = QWidget()
        left_panel.setLayout(layMain)
        splitter.addWidget(left_panel)  # Panel izquierdo con los controles

        # Añadir el panel de gráficos al QSplitter
        splitter.addWidget(grafico_panel)  # Panel derecho con gráficos

        # Añadir el QSplitter al layout principal
        layout_main = QVBoxLayout()
        layout_main.addWidget(splitter)

        # Configurar el layout de la ventana principal
        self.setLayout(layout_main)

        #Aquí intentaremos arreglar el bug del caracter vacío:
        
        # Conexiones con los botones y métodos:
        self.read_estudio.returnPressed.connect(lambda: self.buscar_estudio_id(self.read_estudio.text().strip())) # Para detectar la tecla "Enter"
        button_estudio.clicked.connect(lambda: self.buscar_estudio_id(
            self.read_estudio.text().strip()
        ))
        self.boton_leer_csv.clicked.connect(self.buscar_archivo)
        back_button.clicked.connect(self.back2menu)
        self.prediagnosis_button.clicked.connect(self.open_prediagnosis_window)

    # Método para crear botones con patrones en común
    def create_button(self,title, icon_path, font, size_icon):
        button = QPushButton(title)
        button.setIcon(QIcon(icon_path))
        button.setFont(QFont(font))
        button.setIconSize(QSize(size_icon,size_icon))
        button.setStyleSheet(
            '''
            QPushButton {
                border: 2px solid transparent;  /* Asegura que el borde sea visible */
                border-radius: 15px;  /* Redondeo en todas las esquinas */
                background-color: #3d3d3d;
                color: white;
                font-size: 16px;
                padding: 5px 10px;  /* Reducido el padding para hacer el botón más corto */
            }
            QPushButton:hover {
                background-color: #000000;
                border-radius: 20px;  /* Aumentamos un poco el redondeo en hover */
            }
            '''
        )
        return button
        

    def plot_multiple_graphs(self, layout, tiempo, columnas_sensores):
        """Método para dibujar diferentes tipos de gráficos"""
        try:
            # Limpiar el layout
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)
            
            plt.style.use('dark_background')

            # Diccionario de unidades
            unidades = {
                'Temp. Ambiental (DHT11)': '°C',
                'Humedad (DHT11)': '%',
                'CO2 PPM (MQ135)': 'ppm',
                'Temp. Corporal (MLX90614)':'°C',
                'Pulso Card. (MAX30102)':'bpm',
                'Oxigenacion (MAX30102)':'SpO₂%',
                'Parpadeos por Minuto':'parpadeos/minuto',
                'Movimientos Piernas por Hora': 'movimientos/hora'
            }

            self.graph_images = []

            # Crear gráficos para cada sensor
            for idx, sensor in enumerate(columnas_sensores):
                #print(f'Sensor: {sensor}')
                canvas = FigureCanvas(Figure(figsize=(5, 4)))
                ax = canvas.figure.add_subplot(111)

                if tiempo is not None:
                    # Formatear las horas
                    ax.plot(tiempo, self.data[sensor], label=sensor, color='#BB00FF')
                    ax.set_xlabel('Tiempo')
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Formato HH:MM:SS
                    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Ajustar intervalos mayores
                    canvas.figure.autofmt_xdate()  # Ajustar etiquetas para que no se encimen
                else:
                    ax.plot(self.data[sensor], label=sensor, color='#BB00FF')
                
                # Personalizar gráficos
                ax.set_title(f'Mediciones de {sensor}', color='white')
                
                # Obtener la unidad correspondiente para el sensor, si está en el diccionario
                unidad = unidades.get(sensor, 'unidad desconocida')  # Si no hay unidad, se muestra 'unidad desconocida'
                ax.set_ylabel(f'Valor ({unidad})')  # Mostrar unidad en el eje Y
                
                ax.legend()

                # Agregar al layout en cuadrícula
                layout.addWidget(canvas, idx // 2, idx % 2)  # Filas y columnas

                # Guardamos la imagen en memoria como un objeto BytesIO
                image_stream = io.BytesIO() #Instanciamos un objeto
                canvas.figure.savefig(image_stream, format='png', dpi=300, bbox_inches='tight')
                image_stream.seek(0)
                self.graph_images.append(image_stream)



            QMessageBox.information(self, 'Operación exitosa', 'Gráficos generados correctamente')

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'No se pudo generar los gráficos: {e}')


    def buscar_estudio_id(self, estudio_id):
        if not estudio_id.isdigit():
            QMessageBox.warning(self,'Advertencia','Por favor, ingrese un número de estudio válido')
            return 

        try:
            cursor = self.connection.cursor()
            query = '''
                    select nombre1, nombre2, apellido1, apellido2 from estudio
                    inner join pacientes on estudio.paciente_id = pacientes.paciente_id
                    where estudio_id = %s  and usuario_id = (select usuario_id from usuarios where nombre_usuario = %s)
                    '''
            cursor.execute(query, (estudio_id, self.usuario))
            resultado = cursor.fetchone()

            if resultado:
                    nombre_completo = f'{resultado[0]} {resultado[1]} {resultado[2]} {resultado[3]}'
                    self.ruta_archivo.setVisible(True)
                    self.boton_leer_csv.setVisible(True)
                    QMessageBox.information(self, "Éxito", f"Número de estudio válido. Nombre del paciente: {nombre_completo}. Por favor, suba al archivo .csv del estudio correspondiente.")
            else:
                    self.ruta_archivo.setVisible(False)
                    self.boton_leer_csv.setVisible(False)
                    QMessageBox.warning(self, "Error", "Número de estudio no encontrado o no pertenece a un paciente suyo.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error al validar el estudio: {str(e)}")
            

    
    def buscar_archivo(self):      
         # Mostrar el explorador de archivos
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar Archivo CSV", 
            "", 
            "Archivos CSV (*.csv);;Todos los Archivos (*)"
        )
        
        if file_path:
            print(f"Archivo seleccionado: {file_path}")
            self.ruta_archivo.setText(file_path)
            self.cargar_datos_csv(file_path)
    
    def back2menu(self):
        from main import MainWindow
        self.main_window = MainWindow(self.usuario)
        self.main_window.show()
        self.close()
            

    def cargar_datos_csv(self, archivo):
        try:
            # Cargar los datos del archivo CSV
            self.data = pd.read_csv(archivo)
            
            # Eliminar espacios en los nombres de las columnas
            self.data.columns = self.data.columns.str.strip()

            # Renombrar columnas considerando equivalencias:
            equivalencias = {
            'oxigenacion': 'Oxigenacion (MAX30102)',
            'pulsos': 'Pulso Card. (MAX30102)',
            'co2': 'CO2 PPM (MQ135)',
            'temperatura': 'Temp. Corporal (MLX90614)',
            'humedad': 'Humedad (DHT11)',
            'parpadeosminuto': 'Parpadeos por Minuto',
            'movimientospiernashora': 'Movimientos Piernas por Hora',
            'transtorno': 'Transtorno'
            }

            self.data.rename(columns=equivalencias, inplace=True)

            # Verificamos nombres en caso de que se hayan renombrado:
            print('Nombres de las columnas: ', self.data.columns)

            # Verificar los nombres de las columnas
            print("Nombres de las columnas:", self.data.columns)

            # Verificar las primeras filas para asegurarnos de que los datos se están leyendo correctamente
            print("Primeras filas del archivo:\n", self.data.head())

            # Verificar si existe la columna 'Hora' y 'Fecha', y combinarla para crear una nueva columna 'FechaHora'
            if 'Hora' in self.data.columns and 'Fecha' in self.data.columns:
                print("Se encontró columna 'Fecha' y 'Hora'")

                # Asegurarse de que la columna 'Hora' y 'Fecha' están en formato de texto correcto
                print("Formato de la columna 'Hora':", self.data['Hora'].dtype)
                print("Formato de la columna 'Fecha':", self.data['Fecha'].dtype)
                
                # Crear una nueva columna 'FechaHora' combinando 'Fecha' y 'Hora'
                self.data['FechaHora'] = pd.to_datetime(self.data['Fecha'] + ' ' + self.data['Hora'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
                
                # Verificar si hubo valores NaT (invalidos) después de la conversión
                print("Valores NaT en la columna 'FechaHora':", self.data['FechaHora'].isna().sum())

                # Rellenar los valores NaT con el valor anterior (por ejemplo, la hora de la fila anterior)
                self.data['FechaHora'].ffill(inplace=True)
                tiempo = self.data['FechaHora']
            elif 'Tiempo' in self.data.columns:
                tiempo = self.data['Tiempo']
            else:
                raise ValueError('El archivo no contiene una columna de tiempo válida')

            # Filtramos las columnas de sensores, excluyendo 'Fecha' y 'Hora' (en caso de que existan), aquí excluyes todas las que quieras
            columnas_sensores = [col for col in self.data.columns if col.lower() not in ['fecha', 'hora', 'fechahora','transtorno']]

            if not columnas_sensores:
                raise ValueError('El archivo no contiene columnas con mediciones de sensores')

            # Aplicamos un submuestreo para mejorar el rendimiento
            factor = 20
            self.data = self.data.iloc[::factor, :]

            # Aplicamos el submuestreo también en la variable tiempo (manteniendo el formato)
            if tiempo is not None:
                tiempo = tiempo.iloc[::factor]

            # Mostramos las gráficas, usando 'tiempo' como eje X
            self.plot_multiple_graphs(self.grafico_layout, tiempo, columnas_sensores)

            # Calculamos promedios de cada columna 
            self.promedios = self.calcular_promedios(columnas_sensores)
            #self.upload_to_model(self.promedios)


            # Mensaje de éxito
            QMessageBox.information(self, 'Operación exitosa', 'Datos cargados correctamente')
            self.prediagnosis_button.setVisible(True)
        
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'No se pudo cargar el archivo CSV: {e}')


    def calcular_promedios(self, columnas):
        '''
        Calculamos el promedio para las columnas leídas del csv.
        params: columnas --> Es una lista que contiene los nombres de las columnas del archivo csv
        return: Devolvemos un diccionario con los promedios para cada columna (esto tal vez se deba modificar)
        '''
        try:
            if self.data is None:
                raise ValueError('No hay datos cargados')
            
            # Calcular promedios sólo para las columnas numéricas
            promedios = self.data[columnas].mean(numeric_only = True)
            return promedios.to_dict()
        
        except Exception as e:
            print(f'Error al calcular los promedios del csv: {e}')
            return {} # Devolvemos un diccionario vacío 
    
    def open_prediagnosis_window(self):
        from prediagnostico import PrediagnosisWindow
        self.prediagnosis_window = PrediagnosisWindow(connection=self.connection, user= self.usuario, 
                                                      promedios=self.promedios, study_id=self.read_estudio.text().strip(),
                                                      graph_images=self.graph_images)
        self.prediagnosis_window.show()



# Inicializar aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = SleepDataWindow()
    main_window.show()
    sys.exit(app.exec())
