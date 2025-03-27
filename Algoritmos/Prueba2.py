import sys
import tensorflow as tf
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Cargar los datos
datos_referencia = pd.read_csv(r"C:\Users\Rober\PycharmProjects\TT\base_datos_polisomnografia_200.csv", encoding='latin-1', sep=',')
dref = pd.get_dummies(datos_referencia['trastorno'], prefix='trastorno').astype(int)
datos_referencia8 = datos_referencia.drop(['trastorno'], axis=1)
datos_referencia2 = pd.concat([datos_referencia8, dref], axis=1)

x_train = datos_referencia8[['oxigenacion', 'pulsos', 'co2', 'temperatura', 'humedad', 'parpadeosminuto', 'movimientospiernashora']]
y_train = dref[['trastorno_Sin Trastorno', 'trastorno_Apnea', 'trastorno_Insomnio Intermedio', 'trastorno_Paralisis del Sueno', 'trastorno_Piernas Inquietas']]

# Modelo de IA
modelo = tf.keras.models.Sequential([
    tf.keras.layers.Dense(256, input_dim=7, activation='relu'),
    tf.keras.layers.Dense(5, activation='softmax')
])
modelo.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss='categorical_crossentropy')

# Clase principal de la aplicación
class SleepApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Diseño
        self.setWindowTitle("Clasificación de Trastornos del Sueño")
        self.layout = QVBoxLayout()

        # Botón para entrenar y predecir
        self.train_button = QPushButton("Entrenar y Predecir")
        self.train_button.clicked.connect(self.train_and_predict)

        # Etiqueta para resultados
        self.result_label = QLabel("Resultados aparecerán aquí.")
        self.layout.addWidget(self.result_label)

        # Canvas para gráficos
        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        self.layout.addWidget(self.train_button)
        self.layout.addWidget(self.canvas)

        # Configuración de layout
        self.setLayout(self.layout)

    def train_and_predict(self):
        # Entrenar el modelo
        epocas = modelo.fit(x_train, y_train, epochs=100, verbose=0)  # Reducir número de épocas para pruebas
        loss = epocas.history["loss"]

        # Datos de entrada para predicción
        datos_entrada = np.array([[94, 89, 384, 36.2, 51,22, 1]])
        transtornos = modelo.predict(datos_entrada)
        transtornos_percent = (transtornos * 100).flatten()  # Convertir a porcentaje

        etiqueta_predicha = np.argmax(transtornos, axis=1)

        # Mostrar resultados
        trastorno_dict = {
            0: "Sin Trastorno",
            1: "Apnea",
            2: "Insomnio Intermedio",
            3: "Parálisis del Sueño",
            4: "Síndrome de Piernas Inquietas"
        }
        resultado = trastorno_dict.get(etiqueta_predicha[0], "Error en la predicción")
        self.result_label.setText(f"Predicción: {resultado}")

        # Graficar resultados
        self.update_plot(loss, transtornos_percent, list(trastorno_dict.values()))

    def update_plot(self, loss, transtornos_percent, labels):
        # Graficar en el canvas
        self.canvas.figure.clear()
        ax1 = self.canvas.figure.add_subplot(211)  # Gráfica de pérdida
        ax2 = self.canvas.figure.add_subplot(212)  # Gráfica de probabilidades

        # Gráfico de pérdida
        ax1.plot(loss)
        ax1.set_title("Pérdida durante el entrenamiento")
        ax1.set_xlabel("Épocas")
        ax1.set_ylabel("Pérdida")
        ax1.grid()

        # Gráfico de barras para las probabilidades
        ax2.bar(labels, transtornos_percent, color=['blue', 'green', 'red', 'orange', 'purple'])
        ax2.set_title("Probabilidades Predichas (%)")
        ax2.set_xlabel("Trastornos")
        ax2.set_ylabel("Probabilidad (%)")
        ax2.set_ylim(0, 100)
        for i, v in enumerate(transtornos_percent):
            ax2.text(i, v + 2, f"{v:.2f}%", ha='center', fontsize=9)

        # Dibujar el canvas
        self.canvas.draw()

# Inicializar aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = SleepApp()
    main_window.show()
    sys.exit(app.exec())
