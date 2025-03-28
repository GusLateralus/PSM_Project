import sys
from PyQt6.QtWidgets import QTableView,QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox, QDialog, QHBoxLayout
from PyQt6.QtGui import QKeyEvent, QStandardItem,QFont, QIcon, QPixmap, QStandardItemModel
from PyQt6.QtCore import QSize
from conetsion import create_connection
from register import RegistrarUsuarioView
from security import verificar_password
import os
from icon_manager import get_icon_path
#from main import MainWindow
#from security import hash_password, verificar_password

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.setModal(True) #checar esto
        self.inicializar_ui()
        self.setFixedSize(400,300)
        

    def inicializar_ui(self):
        self.setGeometry(200, 200, 400, 300)  # Tamaño de la ventana
        self.setWindowTitle('Bienvenido')
        self.setWindowIcon(QIcon(get_icon_path('sleep.png')))
        self.setStyleSheet('''QWidget {
        background: qlineargradient(
            spread:pad, 
            x1:0, y1:0, x2:1, y2:1, 
            stop:0 rgba(19, 30, 20, 0.8), 
            stop:1 rgba(66, 151, 131, 0.8)
        );
         }''')
        
        # Creamos un QLabel para la imagen de fondo
        fondo_label = QLabel(self)
        fondo_label.setPixmap(QPixmap(get_icon_path('IPN-Symbol.png')))
        fondo_label.setGeometry(0, 0, 400, 250) # Ajustamos las dimensiones para cubrir la ventana
        fondo_label.setScaledContents(True)
        #self.setStyleSheet('background-color: brown;')
        self.generar_formulario()  # Mandamos a llamar al método generar_formulario()
        fondo_label.lower() # El fondo estará detrás de los demás elementos
        self.show()  # Y lo mostramos

    

    def mostrar_contrasena(self):
        # Si la variable clicked es verdadera, entonces muestra la contraseña
        # Debido a los cambios en el checkbox, ya no utiliza clicked, ahora se usa la condición que si se presiona el botón, entonces 
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.check_view_password.setIcon(QIcon(get_icon_path("show2.png")))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.check_view_password.setIcon(QIcon(get_icon_path("hide2.png")))

    def registrar_usuario(self):
        self.new_user_form = RegistrarUsuarioView()
        self.new_user_form.show()

    def open_main_window(self, usuario):
        from main import MainWindow
        self.main_window = MainWindow(usuario=usuario)
        self.main_window.show()
        self.close()


    def generar_formulario(self):
        self.is_logged = False  # Con esta variable verificamos si el usuario está conectado
        user_label = QLabel(self)
        user_label.setText('Usuario:')
        user_label.setFont(QFont('Arial Black', 10))
        user_label.setStyleSheet('''
                                color: #5A9;
                                background-color:transparent;
                                ''')
        # El médico ingresará sus datos
        self.user_input = QLineEdit(self)
        self.create_line_edit(self.user_input)
        
        # Contraseña
        password_label = QLabel(self)
        password_label.setText('Contraseña:')
        password_label.setFont(QFont('Arial Black', 10))
        password_label.setStyleSheet('''
                                color: #5A9;
                                background-color:transparent;
                                ''')

        self.password_input = QLineEdit(self)  # Recuerda que self es una variable de instancia, esto me permite acceder a las variables desde cualquier parte de la clase
        self.create_line_edit(self.password_input)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Login
    
        login_button = self.create_button(get_icon_path("login.png"),24,10,'Login')
        login_button.clicked.connect(self.login)
        # Register
        register_button = self.create_button(get_icon_path('add-user.png'),24,10,'Regístrate')
        register_button.clicked.connect(self.registrar_usuario)
    
        # Botón enter:
        self.password_input.returnPressed.connect(self.login)

        # Cargando las imágenes
        open_eye_icon = QIcon(QPixmap(get_icon_path('show2.png')))
        closed_eye_icon = QIcon(QPixmap(get_icon_path('hide2.png')))
        
        #Checkbox del ojo (ahora botón)
        self.check_view_password = QPushButton(self) # Recuerda que QPushButton no emite un valor booleano, por lo que la función mostrar_contrasena debes manejarla diferente
        self.check_view_password.setIcon(closed_eye_icon) # El botón inicia con el ojo cerrado
        self.check_view_password.setFlat(True) #Eliminamos el borde del botón
        self.check_view_password.setStyleSheet('''border: none;
                                                  background-color:transparent;''') # Aseguramos que esté sin bordes
        #self.check_view_password.move(320, 85)
        self.check_view_password.clicked.connect(self.mostrar_contrasena)

        # Creamos layouts para esta ventana:
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QVBoxLayout()
        layout_main = QVBoxLayout()

        # Añadimos los widgets a cada layout:
        layout1.addWidget(user_label)
        layout1.addWidget(self.user_input)
        layout2.addWidget(password_label)
        layout2.addWidget(self.password_input)
        layout2.addWidget(self.check_view_password)
        layout3.addWidget(login_button)
        layout3.addWidget(register_button)
        
        # Agregamos los layouts al principal:
        layout_main.addLayout(layout1)
        layout_main.addLayout(layout2)
        layout_main.addLayout(layout3)

        # Y colocamos el layout principal para que aparezca
        self.setLayout(layout_main)
    
    def create_button(self, icon_path, icon_tamano, tamanio_fuente, text):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(icon_tamano,icon_tamano))
        button.setFont(QFont('Arial Black',tamanio_fuente))
        button.setStyleSheet( '''QPushButton {
                border: 2px solid transparent;  /* Asegura que el borde sea visible */
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
                background-color: #3d3d3d;
                color: #5A9;
                font-size: 12px;
                padding: 4px;  /* Ajusta el tamaño interno del botón */
            }
            QPushButton:hover {
                background-color: #000000;
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;    
            }''')
        return button

    def create_line_edit(self, qline):
        qline.setStyleSheet("""
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
        """)
        


    def login(self):
        usuario = self.user_input.text().strip()
        contrasenia = self.password_input.text()

        try:
            conn=create_connection()
            cursor = conn.cursor()
        
            cursor.execute("select contrasenia from usuarios where nombre_usuario = %s",(usuario,))
            resultado = cursor.fetchone()
            print(resultado)

            if resultado:
                stored_password = resultado[0] # Recuperamos el hash almacenado

                # Convertir la contraseña hasheada de str a bytes
                stored_password_bytes = stored_password.encode('utf-8')
                

                # Verificamos la contraseña
                if verificar_password(contrasenia, stored_password_bytes):
                    QMessageBox.information(self, 'Inicio sesión',
                                            'Inicio de sesión exitoso',
                                            QMessageBox.StandardButton.Ok)
                    
                    self.open_main_window(usuario)
                    self.close()
                    return usuario
                    
                else:
                    QMessageBox.warning(self, 'Error Message', 'Credenciales incorrectas',
                                        QMessageBox.StandardButton.Close)
            else:
                QMessageBox.warning(self, 'Error Message',
                                    'Usuario no encontrado',
                                    QMessageBox.StandardButton.Close)
            
        except Exception as e:
            QMessageBox.warning(self, 'Error Message',
                                f'Error en el servidor: {e}',
                                QMessageBox.StandardButton.Close)
            
# Aquí accedes a la GUI
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Toma todas las interacciones que el usuario haga con la app
    login = LoginWindow()  # Creamos una instancia de la clase LoginWindow()
    sys.exit(app.exec())

