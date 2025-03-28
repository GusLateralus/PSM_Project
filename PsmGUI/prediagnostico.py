# Aquí irá la ventana del prediagnóstico
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QMessageBox, QHBoxLayout, QLabel, QTextEdit, QFormLayout, QPushButton
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon , QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from send_emails import enviar_resultados
import numpy as np
from fpdf import FPDF
import os
import io
from PIL import Image
from icon_manager import get_icon_path


class PrediagnosisWindow(QWidget):
    def __init__(self, connection, user, promedios, study_id, graph_images):
        super().__init__()
        self.connection = connection
        self.user = user
        self.promedios = promedios
        self.study_id = study_id
        self.graph_images = graph_images
        # Crear el PDF
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.init_ui()
        #print(f'{self.study_id}')
        #print(f'{self.graph_images}')
        print(f'{self.promedios}')

    
    def init_ui(self):
        self.setWindowTitle('Prediagnóstico')
        self.setGeometry(300, 300, 800, 600)
        self.setWindowIcon(QIcon(get_icon_path('diagnostico.png')))
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
        # Creamos un splitter para dividir en paneles
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Panel superior: gráficas
        panel_graficas = QWidget()
        self.layout_graficas = QHBoxLayout(panel_graficas)

        # Agregamos las gráficas al layout del panel superior
        self.plot_mean()
        porcentajes_prediccion = self.upload_to_model()
        grafica_pastel = self.crear_grafica_pastel(porcentajes_prediccion)
        #layout_graficas.addWidget(grafica_barras)
        self.layout_graficas.addWidget(grafica_pastel)

        # Panel inferior: observaciones y botón
        panel_diagnostico = QWidget()
        layout_diagnostico = QVBoxLayout(panel_diagnostico)

        title = QLabel('Observaciones')
        title.setFont(QFont('Arial', 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.observations = QTextEdit()
        self.observations.setPlaceholderText('Hola, este es un texto de prueba')

        form_layout = QFormLayout()
        form_layout.addRow(title)
        form_layout.addRow('Observaciones:', self.observations)

        self.send_button = QPushButton('Enviar')
        self.send_button.setIcon(QIcon(get_icon_path('email.png')))
        self.send_button.setIconSize(QSize(34,34))
        self.send_button.setFont(QFont('Arial Black'))
        self.send_button.setStyleSheet(
            '''
            QPushButton {
                border: 2px solid transparent;
                border-radius: 15px;
                background-color: #3d3d3d;
                color: white;
                font-size: 16px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #000000;
                border-radius: 20px;
            }
            '''
        )
        self.send_button.clicked.connect(lambda:self.obtener_observaciones())

        layout_diagnostico.addLayout(form_layout)
        layout_diagnostico.addWidget(self.send_button)

        # Agregamos los paneles al splitter
        splitter.addWidget(panel_graficas)
        splitter.addWidget(panel_diagnostico)

        # Configuramos el layout principal
        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(splitter)


    # En este método se grafican los promedios obtenidos del csv
    def plot_mean(self):
        try:
            fig = Figure(figsize=(6, 4))
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)

            #labels = list(self.promedios.keys())

            # Determinamos qué columnas usar dependiendo del formato de los datos:
            if 'Temp. Ambiental (DHT11)' in self.promedios:
                labels = ['Temperatura(°C)', 'Humedad(%)','CO2(ppm)','T. Corporal(°C)','P. Card. (bpm)','Oxigen. (SpO₂%)']
                values = [
                self.promedios.get('Temp. Ambiental (DHT11)', 0),
                self.promedios.get('Humedad (DHT11)', 0),
                self.promedios.get('CO2 PPM (MQ135)', 0),
                self.promedios.get('Temp. Corporal (MLX90614)', 0),
                self.promedios.get('Pulso Card. (MAX30102)', 0),
                self.promedios.get('Oxigenacion (MAX30102)', 0)
                ]   #Usamos get para obtener la clave, si la encuentra, entonces devuelve su valor, en caso de que no lo encuentre, mandamos 0
            

            else:
                # Si es el segundo formato
                labels = ['Oxigen(SpO₂%)','P.Card. (bpm)','CO2(ppm)','T. Corporal (°C)', 'Humedad(%)','Parps/min','Movs/Hora']
                values = [
                self.promedios.get('Oxigenacion (MAX30102)', 0),
                self.promedios.get('Pulso Card. (MAX30102)', 0),
                self.promedios.get('CO2 PPM (MQ135)', 0),
                self.promedios.get('Temp. Corporal (MLX90614)', 0),
                self.promedios.get('Humedad (DHT11)', 0),
                self.promedios.get('Parpadeos por Minuto', 0),
                self.promedios.get('Movimientos Piernas por Hora', 0)
                ]


            colors = ['#9b59b6', '#8e44ad', '#af7ac5', '#d2b4de', '#c39bd3']
            colors = colors[:len(labels)]

            ax.bar(labels, values, color=colors)
            ax.set_title('Promedio de variables biométricas', fontsize=15, color='white')
            ax.set_ylabel('Valores', color='white')
            ax.set_xlabel('Variables', color='white')
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=0, ha='center', color='white', fontsize = 8)
            ax.tick_params(axis='y', colors='white')
            ax.tick_params(axis='x', colors='white')
            ax.set_facecolor('#2c3e50')

            fig.patch.set_facecolor('#34495e')

            self.layout_graficas.addWidget(canvas)

            # Guardamos el gráfico como imagen en BytesIO
            img_buffer = io.BytesIO()
            fig.savefig(img_buffer, format='png', bbox_inches='tight')
            img_buffer.seek(0)

            #Agregamos la imagen al atributo de instancia graph_images
            if not hasattr(self,'graph_images'):
                self.graph_images = []
            
            self.graph_images.append(img_buffer)


        except Exception as e:
            QMessageBox.warning(self, 'Error', f'No se pudo generar el gráfico de barras: {e}')

    # Este método se removerá a la otra clase
    def upload_to_model(self):
        from keras.models import load_model # type: ignore
        path = get_icon_path('modelo_trastornos_sueno.h5')
        modelo = load_model(path)

        oxigenacion = self.promedios['Oxigenacion (MAX30102)']
        pulsos = self.promedios['Pulso Card. (MAX30102)']
        co2 = self.promedios['CO2 PPM (MQ135)']
        temperatura = self.promedios['Temp. Corporal (MLX90614)']
        humedad = self.promedios['Humedad (DHT11)']
        parpadeosminuto = self.promedios['Parpadeos por Minuto']
        movimientospiernashora = self.promedios['Movimientos Piernas por Hora']

        # Creamos un array de numpy con los nuevos datos
        datos_entrada = np.array([[oxigenacion, pulsos, co2, temperatura, humedad, parpadeosminuto, movimientospiernashora]])

        # Y realizamos la predicción:
        trastornos = modelo.predict(datos_entrada)

        # Convertir las probabilidades a porcentajes 
        porcentajes = (trastornos[0]*100).round(2)

        # Convertir probabilidades a etiquetas (para clasificación multiclase)
        #etiqueta_predicha = np.argmax(trastornos, axis=1)

        # Mapeo de etiquetas a los nombres de los trastornos
        trastornos_dict = {
                0: "Sin trastorno",
                1: "Apnea",
                2: "Insomnio intermedio",
                3: "Parálisis del sueño",
                4: "Síndrome de piernas inquietas"
            }
        
        # Asociamos los porcentajes con los nombres de cada trastorno
        resultados_porcentajes = {
                trastornos_dict[i]: porcentaje for i, porcentaje in enumerate(porcentajes)}
            
        # Mostrar los resultados en consola (para depurar)
        print('Probabilidades predichas: ')
        for trastorno, porcentaje in resultados_porcentajes.items():
            print(f'{trastorno}: {porcentaje}%')
        
        return resultados_porcentajes
        

    # Vamos a crear unos métodos temporales aquí sólo para la creación de gráficas:
    def crear_grafica_pastel(self, resultados_porcentajes):
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot()

        # Datos para la gráfica
        labels = list(resultados_porcentajes.keys())
        sizes = list(resultados_porcentajes.values())
        colors = ['#9b59b6', '#8e44ad', '#af7ac5', '#d2b4de', '#c39bd3']

        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',textprops={'fontsize': 8}, labeldistance=1.2)
        ax.set_title("Predicción del asistente")

        # Guardamos el gráfico como imagen en BytesIO
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight')
        img_buffer.seek(0)

        #Agregamos la imagen al atributo de instancia graph_images
        if not hasattr(self,'graph_images'):
            self.graph_images = []
            
        self.graph_images.append(img_buffer)

        return canvas
    

    def generar_reporte(self, observations=""):
        archivo_pdf = None

        try:
            #self.pdf.add_page()
            #pdf.set_y(-15)  # Posición desde el final de la página
            #pdf.cell(0, 10, f"Página {pdf.page_no()}", 0, 0, "C")

            # Configuramos la página del reporte
            self.configurar_pagina()

            # Encabezado del reporte
            self.pdf.set_font('Arial', style='B', size=16)
            self.pdf.cell(200, 10, txt='Reporte de Estudio de Polisomnografía', ln=True, align='C')
            self.pdf.ln(10)


            # Información del paciente
            info_paciente = self.obtener_informacion()
            if info_paciente:
                nombre_completo = f"{info_paciente[0]} {info_paciente[1]} {info_paciente[2]} {info_paciente[3]}"
                curp, contacto, usuario, fecha = info_paciente[4:8]  # Esta es una manera más compacta de obtener los ítems de este arreglo

                ancho_disponible = self.pdf.w-30
                self.pdf.set_font('Arial', size=8)
                self.pdf.set_x(self.margin_left)  #Se retorna el cursor al margen izquierdo, que está en la posición 15
                self.pdf.cell(ancho_disponible, 10, txt=f'Nombre: {nombre_completo}', ln=True)   # Cuando quieras colocarle bordes, sólo pon en los argumentos: border=1
                self.pdf.cell(ancho_disponible, 10, txt=f'CURP: {curp}', ln=True)
                self.pdf.cell(ancho_disponible, 10, txt=f'Número de Estudio: {self.study_id}', ln=True)
                self.pdf.cell(ancho_disponible, 10, txt=f'Médico Tratante: {usuario}', ln=True)
                self.pdf.cell(ancho_disponible, 10, txt=f'Fecha del Estudio: {fecha}', ln=True)
                self.pdf.ln(10)

                # Verificar y agregar imágenes de gráficos
            if hasattr(self, 'graph_images') and isinstance(self.graph_images, list):
                self.pdf.set_font('Arial', style='B', size=12)
                self.pdf.cell(200, 10, txt='Gráficos de Mediciones:', ln=True, align='C')
                self.pdf.ln(5)

                # Parámetros para disposición de imágenes:
                margen_izquierdo = 15
                margen_superior = self.pdf.get_y()
                espacio_horizontal = 5
                espacio_vertical = 10
                ancho_imagen = (self.pdf.w-2*margen_izquierdo-espacio_horizontal*2)/3    # Máximo 3 imágenes por fila
                altura_imagen = ancho_imagen*0.75   #Ajustar proporción de la imagen
                x_actual = margen_izquierdo
                y_actual = margen_superior

                for idx, image in enumerate(self.graph_images):
                    # Convertir de BytesIO a una imagen PIL
                    try:
                        image = Image.open(io.BytesIO(image.read()))  # Asegurarse de leer los datos correctamente
                    except Exception as e:
                        raise Exception(f"Error al convertir la imagen desde BytesIO: {e}")

                    # Guardar la imagen temporalmente en formato PNG
                    image_path = f"temp_graph_{idx}.png"
                    image.save(image_path, format="PNG")
                    
                    # Insertar la imagen en el PDF
                    self.pdf.image(image_path, x=x_actual, y=y_actual, w=ancho_imagen, h= altura_imagen)
                    x_actual += ancho_imagen+espacio_horizontal # Mover posición horizontal
                    
                    # Salto a nueva fila si se excede el ancho de la página:
                    if x_actual+ancho_imagen>self.pdf.w-margen_izquierdo:
                        x_actual=margen_izquierdo
                        y_actual+=altura_imagen+espacio_vertical
                    
                    
                    
                    # Eliminar la imagen temporal
                    os.remove(image_path)

            #Agregar observaciones:
            if observations:
                #print(f'Observaciones: {observations}')
                #self.pdf.add_page()
                self.configurar_pagina()
                self.pdf.set_font('Arial', style='B', size=12)
                self.pdf.cell(200,10, txt='Observaciones:', ln=True, align='L')
                self.pdf.ln(5)
                self.pdf.set_font('Arial', size=10)
                self.pdf.multi_cell(0, 10, txt=observations)


            # Generar y guardar el archivo PDF
            archivo_pdf = os.path.abspath(f"Reporte_{self.study_id}.pdf")
            self.pdf.output(archivo_pdf)


            if os.path.exists(archivo_pdf):
                print(f'{archivo_pdf}')
                QMessageBox.information(self, 'Operación exitosa', 'Reporte de resultados generado correctamente')
                self.insertar_resultados(observations)
            else:
                QMessageBox.warning(self, 'Error', 'El archivo PDF no se generó correctamente')
                archivo_pdf = None

        except Exception as e:
            print(f"Error al generar reporte: {e}")  # Para depurar más fácilmente
            QMessageBox.warning(self, 'Error', f'No se pudo generar el reporte: {e}')
            archivo_pdf = None

        if archivo_pdf:
            envio_correo=enviar_resultados(contacto,nombre_completo,self.study_id,fecha,archivo_pdf)

            if 'exitosamente' in envio_correo:
                QMessageBox.information(self, 'Operación exitosa', 'Envío de resultados exitoso. Recuerde que la IA puede fallar en el prediagnóstico, por lo que es recomendable repetir el estudio en caso de anomalías.')
            else:
                    QMessageBox.warning(self, 'Error en el correo electrónico', envio_correo)
            
        else:
            QMessageBox.warning(self, 'Error','No se puede enviar el reporte porque no se generó correctamente')



    def configurar_pagina(self):
        self.pdf.add_page()

        # Agregamos logotipo
        ruta_imagen = get_icon_path("IPN-logo.png")  
        ancho_imagen, alto_imagen = 10, 10
        self.pdf.image(ruta_imagen, x=5, y=10, w=ancho_imagen, h=alto_imagen)

        # Margen visible
        self.pdf.set_margins(15, 20, 15)
        page_width, page_height = self.pdf.w, self.pdf.h
        self.margin_left, margin_top, margin_right, margin_bottom = 15, 20, 15, 15
        self.pdf.set_draw_color(128, 0, 64)
        self.pdf.rect(self.margin_left, margin_top, 
                    page_width - self.margin_left - margin_right, 
                    page_height - margin_top - margin_bottom)


    
    def obtener_informacion(self):
        try:
            query = '''select nombre1, nombre2, apellido1, apellido2, pacientes.paciente_id, contacto, nombre_usuario, fecha
                        from pacientes
                        inner join estudio on pacientes.paciente_id = estudio.paciente_id
                        inner join usuarios on pacientes.usuario_id = usuarios.usuario_id
                        where nombre_usuario = %s and estudio_id = %s'''
            cursor = self.connection.cursor()
            cursor.execute(query, (self.user, self.study_id))
            info_paciente = cursor.fetchone()
            if info_paciente:
                return info_paciente
            else:
                QMessageBox.information(self, 'Paciente no encontrado', 'No se encontró al paciente asociado.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'No se encontró al paciente: {str(e)}')
    
    
    def obtener_observaciones(self):
        # Dale formato al texto para que puedas vaciar la info en la base de datos
        texto_observaciones = self.observations.toPlainText()
        print(f'{texto_observaciones}')
        self.generar_reporte(observations=texto_observaciones)
    
    def insertar_resultados(self, observaciones):
        try:
            query = '''
                    insert into resultados(estudio_id, observaciones)
                    values(%s,%s)'''
            cursor = self.connection.cursor()
            data = (self.study_id,observaciones)
            cursor.execute(query, data)
            self.connection.commit()
            print('Inserción exitosa')
        except Exception as e:
            print(f'Error al insertar resultados: {e}')
            self.connection.rollback()


