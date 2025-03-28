from PyQt6.QtWidgets import (QDialog, QLabel, QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QVBoxLayout)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QSize
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from conetsion import create_connection
from security import hash_password
from icon_manager import get_icon_path

class RegistrarUsuarioView(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.setFixedSize(350, 400)
        self.generar_formulario()

    def generar_formulario(self):
        # Primero creamos los componentes de la ventana y después los layouts
        #self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Registro')
        self.setWindowIcon(QIcon(get_icon_path('IPN-logo.png')))

        # Etiquetas y QLineEdit
        user_label = QLabel(self)
        user_label.setText('Usuario:')
        user_label.setFont(QFont('Arial Black', 10))
        user_label.setStyleSheet('color: #5A9')

        self.user_input = QLineEdit(self)
        self.create_style(self.user_input)
        self.user_input.setPlaceholderText('Nombre de usuario')

        password_1_label = QLabel(self)
        password_1_label.setText('Password: ')
        password_1_label.setFont(QFont('Arial Black', 10))
        password_1_label.setStyleSheet('color: #5A9')
       

        self.password_1_input = QLineEdit(self)
        self.create_style(self.password_1_input)
        self.password_1_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_1_input.setPlaceholderText('Contraseña')

        password_2_label = QLabel(self)
        password_2_label.setText('Password: ')
        password_2_label.setFont(QFont('Arial Black', 10))
        password_2_label.setStyleSheet('color: #5A9')

        self.password_2_input = QLineEdit(self)
        self.create_style(self.password_2_input)
        self.password_2_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_2_input.setPlaceholderText('Confirme contraseña...')

        email_label = QLabel(self)
        email_label.setText('Email:')
        email_label.setFont(QFont('Arial Black', 10))
        email_label.setStyleSheet('color: #5A9')

        self.email_input = QLineEdit(self)
        self.create_style(self.email_input)
        self.email_input.setPlaceholderText('Correo Gmail...')

        # Botones
        create_button = QPushButton(self)
        create_button.setIcon(QIcon(get_icon_path('ok.png')))
        create_button.setIconSize(QSize(34,34))
        create_button.setText('Crear')
        create_button.setFont(QFont('Arial Black', 10))
        create_button.setStyleSheet("""
            QPushButton {
                border: 2px solid transparent;  /* Asegura que el borde sea visible */
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                background-color: #3d3d3d;
                color: #5A9;
                font-size: 16px;
                padding: 10px 20px;  /* Ajusta el tamaño interno del botón */
            }
            QPushButton:hover {
                background-color: #000000;
                border-top-left-radius: 20px;
                border-bottom-left-radius: 20px;    
            }
        """)
        create_button.clicked.connect(self.crear_usuario)

        cancel_button = QPushButton(self)
        cancel_button.setIcon(QIcon(get_icon_path('cancel.png')))
        cancel_button.setIconSize(QSize(34,34))
        cancel_button.setText('Cancelar')
        cancel_button.setFont(QFont('Arial Black', 10))
        cancel_button.setStyleSheet("""
            QPushButton {
                border: 2px solid transparent;  /* Asegura que el borde sea visible */
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
                background-color: #3d3d3d;
                color: #5A9;
                font-size: 16px;
                padding: 10px 20px;  /* Ajusta el tamaño interno del botón */
            }
            QPushButton:hover {
                background-color: #000000;
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;    
            }
        """)
        cancel_button.clicked.connect(self.cancelar_creacion)

         # Layouts
        layout1_h = QHBoxLayout()
        layout2_h = QHBoxLayout()
        layout3_h = QHBoxLayout()
        layout4_h = QHBoxLayout()
        layout5_h = QHBoxLayout()
        layout_main = QVBoxLayout()

        # Añadiendo los Widgets a los layouts
        layout1_h.addWidget(user_label)
        layout1_h.addWidget(self.user_input)
        layout2_h.addWidget(password_1_label)
        layout2_h.addWidget(self.password_1_input)
        layout3_h.addWidget(password_2_label)
        layout3_h.addWidget(self.password_2_input)
        layout4_h.addWidget(email_label)
        layout4_h.addWidget(self.email_input)
        layout5_h.addWidget(create_button)
        layout5_h.addWidget(cancel_button)

        layout_main.addLayout(layout1_h)
        layout_main.addLayout(layout2_h)
        layout_main.addLayout(layout3_h)
        layout_main.addLayout(layout4_h)
        layout_main.addLayout(layout5_h)

        self.setLayout(layout_main)


    def cancelar_creacion(self):
        self.close()
    
    def create_style(self, line_edit):
        line_edit.setStyleSheet("""
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
        line_edit.setFixedSize(200, 40)

    def enviar_email(self, email, usuario, password):

        load_dotenv()
        
        msg = EmailMessage()
        msg.set_content(f'''Estimado usuario, estas son las credenciales para acceder a nuestro sistema 
                         Usuario: {usuario} 
                         Clave: {password}. 
                         
                         No compartas estos datos con nadie. Bienvenido a la familia Somnus AI,
                         
                         Equipo de soporte.''')
        msg['Subject'] = 'Credenciales para login'
        msg['From'] = os.getenv('USUARIO_EMAIL')
        msg['To'] = email

        try:
            with smtplib.SMTP_SSL(os.getenv('SMTP_SSL'), 465) as smtp:
                smtp.login(os.getenv('USUARIO_EMAIL'), os.getenv('PASSWORD_EMAIL'))
                smtp.send_message(msg)
            QMessageBox.information(self, 'Correo enviado', 'Credenciales enviadas con éxito')
        except smtplib.SMTPException as e:
            QMessageBox.warning(self, 'Error', f'Error al enviar el correo: {e}')
        
    
    def crear_usuario(self):
        #user_path = 'ProyectoPSM/usuarios.txt'
        usuario = self.user_input.text().strip()
        password1 = self.password_1_input.text()
        password2 = self.password_2_input.text()
        email = self.email_input.text().strip()

    

        # Validación de campos vacíos
        if usuario == '' or password1 == '' or password2 == '' or email == '':
            QMessageBox.warning(self, 'Error', 'Por favor, ingrese datos válidos',
                                QMessageBox.StandardButton.Close)

        # Validación de contraseñas diferentes
        elif password1 != password2:
            QMessageBox.warning(self, 'Error', 'Las contraseñas no coinciden',
                                QMessageBox.StandardButton.Close)

        elif '@gmail' not in email or '.' not in email:
            QMessageBox.warning(self, 'Error', 'Por favor, ingrese un correo electrónico de gmail válido',
                                QMessageBox.StandardButton.Close)

        # Si los datos son correctos
        else:
            try:
                # Llamamos a la función para crear la conexión
                conn = create_connection()
                cursor = conn.cursor()
            
                # Hasheado y salteado de la contraseña:
                hashed_password=hash_password(password1)

            
                #Insertamos en la base de datos:
                cursor.execute(
                    "INSERT INTO usuarios (nombre_usuario, email, contrasenia) VALUES (%s, %s, %s)", 
                    (usuario, email, hashed_password )
                ) # Recuerda que el orden en como colocas los valores es EXTREMADAMENTE IMPORTANTE

                conn.commit()
                cursor.close()
                conn.close()

                QMessageBox.information(self,'Creación exitosa',
                                        'Usuario creado correctamente, revise su correo electrónico',
                                        QMessageBox.StandardButton.Ok)

                self.enviar_email(email, usuario, password1)
                #print(type(hashed_password)) Recuerda que el tipo de dato debe ser string, no bytes, para eso usas decode('utf-8')
                self.close()
            except Exception as e:
                QMessageBox.warning(self, 'Error',
                                    f'Error al crear el usuario: {e}',
                                    QMessageBox.StandardButton.Close)