import sys
from PyQt6.QtWidgets import (QWidget, QMessageBox, QVBoxLayout, QTableView, QApplication, 
                             QSplitter, QPushButton, QDialog, QLineEdit, QFormLayout, QLabel, 
                             QHBoxLayout, QStackedWidget, QStackedLayout, QMenu)
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont, QCursor
from conetsion import create_connection  # Asegúrate que tu archivo conetsion.py tiene la función create_connection
from PyQt6.QtCore import Qt, QSize, QPoint
from log import LoginWindow 
from security import hash_password
from send_emails import enviar_nuevas_credenciales, enviar_registro_paciente
from datetime import datetime
from icon_manager import get_icon_path


class MainWindow(QWidget):

    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.connection = create_connection()
        self.table_view = QTableView()
        self.table_view.setStyleSheet('''
                            QTableView{
                                     background-color: #000000;
                                     }
                            
                            QHeaderView{
                                     alternate-background-color: #ccecf0;
                                     gridline-color: #b2d8db;
                                     }

                            QHeaderView::section{
                                     background-color: #3aafa9;
                                     color: white;
                                     padding: 6px;
                                     font-size: 10px;
                                     border: 1px solid #6c6c6c
                                     }
                                     
                            QTableView::item{
                                     border: none;
                                     padding: 4px;
                                     }
                            QTableView::item:selected{
                                     background-color: #2b7a78;
                                     color: white;
                                     }

        ''')
        self.inicializarUI()
        

    def inicializarUI(self):
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('Pacientes')
        self.setWindowIcon(QIcon(get_icon_path('IPN-logo.png')))
        self.generar_contenido()

    def generar_contenido(self):
        # Creamos un splitter:
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Creamos un QStackedWidget
        #self.stacked_widget = QStackedWidget(self)

        # Creamos una página para el Widget (o widgets)
        #self.actualizar_pagina = QWidget()

        # Agregamos las páginas al QStackedWidget
        #self.stacked_widget.addWidget(self.actualizar_pagina)

        # Creamos botones con funciones CRUD/ def crear_boton(self, icon_path, icon_tamano, tamanio_fuente, text):
        self.patient_button = self.crear_boton(get_icon_path('patient.png'), 44, 10, 'Pacientes')
        add_button = self.crear_boton(get_icon_path('add.png'), 44, 10, 'Agregar')
        delete_button = self.crear_boton(get_icon_path('delete.png'), 44, 10, 'Eliminar')
        update_button = self.crear_boton(get_icon_path('sync.png'), 44, 10, 'Actualizar')
        self.settings_button = self.crear_boton(get_icon_path('user-gear.png'), 44, 10, 'Ajustes')

        # Conectar botones a los métodos de esta clase:
        self.patient_button.clicked.connect(self.show_menu_pacientes)
        add_button.clicked.connect(self.add_patient)
        delete_button.clicked.connect(self.delete_patient)
        update_button.clicked.connect(self.actualizar_pagina)
        self.settings_button.clicked.connect(self.show_menu)

         # Layout para botones:
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.patient_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(self.settings_button)

        # Panel para los botones
        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        #Añadimos un color verde turquesa al panel de botones
        button_widget.setStyleSheet('''QWidget {
        background: qlineargradient(
            spread:pad, 
            x1:0, y1:0, x2:1, y2:1, 
            stop:0 rgba(93, 193, 185, 255), 
            stop:1 rgba(0, 58, 225, 255)
        );
         }''')

        splitter.addWidget(button_widget) # Lo añadimos al panel
        #splitter.addWidget(self.stacked_widget)


        # Si se devuelve un objeto para la conexión y además, el usuario también existe, entonces se crea la tabla
        if self.connection and self.usuario:
            self.mostrar_tabla_pacientes()  # Si la variable arroja un True, entonces llamamos el método para mostrar la tabla de los pacientes
            splitter.addWidget(self.table_view)
        else:
            # En caso contrario, mandar un error
            QMessageBox.warning(self, 'Error', 'No se pudo conectar a la base de datos o inicio de sesión incorrecto.', QMessageBox.StandardButton.Close)

        layout = QVBoxLayout(self)
        layout.addWidget(splitter)


    def mostrar_tabla_pacientes(self):
        try:
            # Crear un cursor para ejecutar la consulta
            cursor = self.connection.cursor()
            query = '''
                    SELECT pacientes.paciente_id, estudio_id, nombre1, nombre2, apellido1, apellido2, contacto, direccion, entidad_federativa
                    from pacientes 
                    inner join usuarios on pacientes.usuario_id = usuarios.usuario_id 
                    inner join estudio on pacientes.paciente_id = estudio.paciente_id
                    where nombre_usuario= %s
                    '''
            cursor.execute(query,(self.usuario,)) # Creamos la consulta
            pacientes = cursor.fetchall()

            if not pacientes:
                QMessageBox.information(self, 'Información', 'No hay datos de pacientes para mostrar. Puede agregar pacientes dando clic en el botón "Agregar" ', QMessageBox.StandardButton.Close)
                #return

            # Crear un modelo para la tabla
            model = QStandardItemModel(len(pacientes), 9)  # Número de columnas
            model.setHorizontalHeaderLabels(['CURP', 'No. Estudio', 'Primer Nombre', 'Segundo Nombre', 'Apellido Paterno', 'Apellido Materno', 'Contacto', 'Dirección', 'Entidad'])

            # Llenar el modelo con los datos de pacientes
            for row_idx, row_data in enumerate(pacientes):
                for col_idx, col_data in enumerate(row_data):
                    item = QStandardItem(str(col_data))
                    model.setItem(row_idx, col_idx, item)

            # Crear y mostrar la vista de tabla
            #table_view = QTableView(self)
            self.table_view.setModel(model)
            

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error al ejecutar la consulta: {str(e)}', QMessageBox.StandardButton.Close)
        finally:
            cursor.close()  # Cerrar el cursor
            #self.connection.close()  # Cerrar la conexión
    
    # Creamos una función para instanciar cada botón y así reducir un montón de líneas de código
    def crear_boton(self, icon_path, icon_tamano, tamanio_fuente, text):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(icon_tamano,icon_tamano))
        button.setFont(QFont('Arial Black',tamanio_fuente))
        button.setStyleSheet( '''QPushButton {
                border: 2px solid transparent;  /* Asegura que el borde sea visible */
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                background-color: #3d3d3d;
                color: white;
                font-size: 16px;
                padding: 10px 20px;  /* Ajusta el tamaño interno del botón */
            }
            QPushButton:hover {
                background-color: #000000;
                border-top-left-radius: 20px;
                border-bottom-left-radius: 20px;    
            }''')
        return button

    def add_patient(self):
        # Generamos una ventana de diálogo 
        dialog = QDialog(self)
        dialog.setWindowTitle('Añadir paciente')
        dialog.setModal(True)
        
        # Creamos el QLabel con el texto y el hipervínculo
        link_label = QLabel(dialog)
        link_label.setText('<a href="https://www.gob.mx/curp/">CURP:</a>')  # Hipervínculo de ejemplo
        link_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)  # Habilita la interacción con el enlace
        link_label.setOpenExternalLinks(True)  # Permite abrir enlaces en el navegador

        # Creamos el widget contenedor para el layout horizontal
        

        # Resto de campos del formulario
        paciente_id_input = QLineEdit(dialog)
        paciente_id_input.setPlaceholderText('Inserte CURP...')
        nombre1_input = QLineEdit(dialog)
        nombre1_input.setPlaceholderText('Primer nombre...')
        nombre2_input = QLineEdit(dialog)
        nombre2_input.setPlaceholderText('Segundo nombre')
        apellido1_input = QLineEdit(dialog)
        apellido1_input.setPlaceholderText('Apellido paterno...')
        apellido2_input = QLineEdit(dialog)
        apellido2_input.setPlaceholderText('Apellido materno...')
        direccion = QLineEdit(dialog)
        direccion.setPlaceholderText('Dirección actual...')
        entidad_federativa = QLineEdit(dialog)
        entidad_federativa.setPlaceholderText('Estado...')
        contacto = QLineEdit(dialog)
        contacto.setPlaceholderText('Correo de gmail...')

        # Layout del formulario
        layout = QFormLayout()
        layout.addRow(link_label, paciente_id_input)  # Añadimos el widget con la CURP y el enlace
        layout.addRow('Nombre:', nombre1_input)
        layout.addRow('Segundo nombre:', nombre2_input)
        layout.addRow('Apellido paterno:', apellido1_input)
        layout.addRow('Apellido materno:', apellido2_input)
        layout.addRow('Dirección:', direccion)
        layout.addRow('Estado:', entidad_federativa)
        layout.addRow('Contacto:', contacto)

        # Botones de añadir y cancelar
        add_button = QPushButton('Añadir', dialog)
        cancel_button = QPushButton('Cancelar', dialog)
        layout.addWidget(add_button)
        layout.addWidget(cancel_button)
        dialog.setLayout(layout)

        # Conexiones para los botones
        add_button.clicked.connect(lambda: self.save_patient(
            paciente_id_input.text().strip(),  # Obtenemos el valor del QLineEdit de CURP
            nombre1_input.text().strip(),
            nombre2_input.text().strip(),
            apellido1_input.text().strip(),
            apellido2_input.text().strip(),
            direccion.text().strip(),
            entidad_federativa.text().strip(),
            contacto.text().strip(),
            dialog)
        )
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec()

    def save_patient(self, curp, nombre1, nombre2, apellido1, apellido2, direccion, estado, contacto, dialog):
        # Verificar que los campos obligatorios no estén vacíos
        if not curp or not nombre1 or not apellido1 or not direccion or not estado or not contacto:
            QMessageBox.warning(self, "Datos incompletos", "Por favor, complete los campos obligatorios.")
            return
        
        # Aquí añades el código para guardar en la base de datos
        try:
            now = datetime.now()
            fecha = now.date()
            hora = now.time()
            # Creamos un cursor
            cursor = self.connection.cursor()
            # Realiza la inserción en la base de datos
            query = '''INSERT INTO pacientes (usuario_id, paciente_id, nombre1, nombre2, apellido1, apellido2, direccion, entidad_federativa, contacto) 
                    VALUES ((SELECT usuario_id from usuarios where nombre_usuario= %s LIMIT 1), %s, %s, %s, %s, %s, %s, %s, %s)'''
            data = (self.usuario,curp, nombre1, nombre2, apellido1, apellido2, direccion, estado, contacto)
            cursor.execute(query, data)
            self.connection.commit()
            QMessageBox.information(self, "Excelente", "Paciente añadido exitosamente.")
            dialog.accept()  # Cerrar el diálogo

            cursor.execute('''
                    insert into estudio (fecha, hora, estado, paciente_id)
                    values (%s, %s, 'Pendiente', %s)
                    returning estudio_id, fecha, hora
            ''', (fecha,hora,curp))

            estudio = cursor.fetchone()

            if not estudio:
                raise Exception('No se pudo generar el nuevo estudio')
            
            estudio_id, fecha, hora = estudio
            cursor.execute('select contacto from pacientes where paciente_id = %s', (curp,))
            contacto = cursor.fetchone()[0]

            if not contacto:
                raise Exception('No se encontró el correo electrónico del paciente')
            
            registro = enviar_registro_paciente(contacto, curp, estudio_id, fecha, hora, self.usuario)

            self.connection.commit()
            self.mostrar_tabla_pacientes()  # Actualizar la tabla de pacientes si es necesario

            if 'exitosamente' in registro:
                QMessageBox.information(self, 'Paciente registrado', 'El paciente deberá revisar su correo electrónico y firmar la hoja de consentimiento')
            else:
                QMessageBox.warning(self, 'Advertencia', f'El correo no se pudo enviar: {registro}')

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo añadir el paciente: {str(e)}")

    def delete_patient(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Eliminar paciente')
        dialog.setModal(True)

        patient_id = QLineEdit(dialog)

        layout = QFormLayout()
        layout.addRow('CURP:',patient_id)

        # Añadimos botones para eliminar o cancelar la operación
        delete = QPushButton('Eliminar', dialog)
        layout.addWidget(delete)
        
        cancel_button = QPushButton('Cancelar', dialog)
        layout.addWidget(cancel_button)

        # Colocamos todo en el layout
        dialog.setLayout(layout)

        # Activamos las funciones para los botones creados
        delete.clicked.connect(lambda: self.confirm_delete(patient_id.text().strip(), dialog))
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()


    def confirm_delete(self, patient, dialog):
        if patient:
            try:
                cursor = self.connection.cursor()

                # Consultamos si el paciente pertenece al usuario actual
                cursor.execute('select paciente_id from pacientes inner join usuarios on pacientes.usuario_id = usuarios.usuario_id where paciente_id = %s and nombre_usuario = %s',(patient, self.usuario))
                paciente = cursor.fetchone()

                if paciente:
                    confirm = QMessageBox.question(self, 'Confirmar', f'¿Estás seguro de que deseas eliminar este paciente con CURP {patient}?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                    if confirm == QMessageBox.StandardButton.Yes:
                        # Eliminamos el paciente
                        cursor.execute('delete from pacientes where paciente_id = %s and usuario_id = (select usuario_id from usuarios where nombre_usuario = %s)', (patient, self.usuario))
                        self.connection.commit()
                        QMessageBox.information(self, 'Eliminación exitosa', f'Paciente con CURP {patient} eliminado con éxito')
                        dialog.accept()
                        self.mostrar_tabla_pacientes()

                    else:
                        QMessageBox.information(self, 'Operación cancelada', 'La eliminación ha sido cancelada')
                
                else:
                    QMessageBox.warning(self, 'Error', 'El paciente no pertenece al usuario actual')

            except Exception as e:
                QMessageBox.warning(self, 'Error', f'No se pudo eliminar el paciente: {e}')
        else:
            QMessageBox.warning(self, 'Advertencia', 'Por favor, ingresa un CURP válido')

        
    def setup_table(self):
        # Configurar la tabla para permitir la edición 
        self.table_view.setEditTriggers(QTableView.doubleClicked)      
        
    def actualizar_pagina(self):

        # Creamos el formulario
        #self.pagina_actualizacion_widget = QWidget()
        dialog = QDialog(self)
        dialog.setWindowTitle('Actualizar campos')
        dialog.setModal(True)

        # Creamos los campos de entrada para la actualización
        search_input = QLineEdit(dialog)
        search_button = QPushButton('Buscar')
        search_input.setPlaceholderText('Inserta CURP del paciente...')
        nombre1_input = QLineEdit(dialog)
        nombre2_input = QLineEdit(dialog)
        apellido1_input = QLineEdit(dialog)
        apellido2_input = QLineEdit(dialog)
        direccion = QLineEdit(dialog)
        entidad_federativa = QLineEdit(dialog)
        contacto = QLineEdit(dialog)

        layout = QFormLayout()
        layout.addRow(search_input,search_button)
        layout.addRow('Nombre:', nombre1_input)
        layout.addRow('Segundo nombre:', nombre2_input)
        layout.addRow('Apellido paterno:', apellido1_input)
        layout.addRow('Apellido materno:', apellido2_input)
        layout.addRow('Dirección:', direccion)
        layout.addRow('Estado:', entidad_federativa)
        layout.addRow('Contacto:', contacto)

            # Botones de añadir y cancelar
        cancel_button = QPushButton('Cancelar')
        update_button = QPushButton('Actualizar')
        layout.addRow(update_button, cancel_button)
        layout.addWidget(update_button)
        layout.addWidget(cancel_button)
        dialog.setLayout(layout)


        # Conexiones para los botones
        search_button.clicked.connect(lambda: self.search_patient(
            search_input.text().strip(),
            nombre1_input,
            nombre2_input,
            apellido1_input,
            apellido2_input,
            direccion,
            entidad_federativa,
            contacto
        ))

        update_button.clicked.connect(lambda: self.update_patient(
            # Obtenemos el valor del QLineEdit de CURP
            search_input.text().strip(),
            nombre1_input.text().strip(),
            nombre2_input.text().strip(),
            apellido1_input.text().strip(),
            apellido2_input.text().strip(),
            direccion.text().strip(),
            entidad_federativa.text().strip(),
            contacto.text().strip(),
            dialog)
        )
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec()

            # Se configura el layout en la página de actualización:
        #self.pagina_actualizacion_widget.setLayout(layout)  # Usé el nombre actualizado aquí

            # Guardamos el formulario creado para no volver a crearlo
            #self.stacked_widget.addWidget(self.pagina_actualizacion_widget)

        # Mostrar la página de actualización
        #self.stacked_widget.setCurrentWidget(self.pagina_actualizacion_widget)


    def update_patient(self,curp, nombre1, nombre2, apellido1, apellido2, direccion, entidad_federativa, contacto, dialog):
        try:
            cursor = self.connection.cursor()
            query = '''
            update pacientes
            set nombre1 = %s, nombre2= %s, apellido1= %s, apellido2 = %s, direccion = %s, entidad_federativa= %s, contacto = %s
            where paciente_id = %s and usuario_id = (select usuario_id from usuarios where nombre_usuario = %s)
                    '''
            cursor.execute(query, (nombre1, nombre2, apellido1, apellido2, direccion, entidad_federativa, contacto, curp, self.usuario))
            self.connection.commit()
            self.mostrar_tabla_pacientes()
            QMessageBox.information(self, 'Actualización exitosa', 'Los campos del paciente han sido actualizados')
            dialog.accept()

        except Exception as e:
            QMessageBox.warning(self,'Error', f'No se completó la transacción: {e}')


    def show_menu(self):
        # Esta función es posible que se modifique para que el proyecto sea más escalable
        menu = QMenu()

        menu.setStyleSheet("""
            QMenu {
                background-color: #000000; /* Fondo oscuro */
                color: white;              /* Texto blanco */
                border-radius: 8px;        /* Bordes redondeados */
                border: 1px solid #555555; /* Borde sutil */
                padding: 5px;
            }
            QMenu::item {
                font-family: 'Arial Black', sans-serif; /* Fuente Arial Black */
                font-size: 12px; /* Tamaño de fuente */
                padding: 10px 20px; /* Espaciado */
                background-color: transparent;
                border-radius: 4px; /* Bordes redondeados en las opciones */
            }
            QMenu::item:selected {
                background-color: #5A9; /* Fondo verde claro al seleccionar */
                color: white; /* Texto blanco cuando se selecciona */
                border-radius: 6px; /* Bordes redondeados al seleccionar */
            }
        """)
        

        menu.addAction('Cambiar credenciales', lambda: self.menu_action('Cambiar credenciales'))
        menu.addAction('Cerrar sesión', lambda: self.menu_action('Cerrar sesión'))

        # Mostrar menú en la posición del botón
        menu.exec(self.settings_button.mapToGlobal(QPoint(0, self.settings_button.height())))
    

    def menu_action(self, option):
        
        if option == 'Cambiar credenciales':
            self.change_access()
        elif option == 'Cerrar sesión':
            self.close_all()

    def show_menu_pacientes(self):
        # Esta función es posible que se modifique para que el proyecto sea más escalable
        menu = QMenu()

        menu.setStyleSheet("""
            QMenu {
                background-color: #000000; /* Fondo oscuro */
                color: white;              /* Texto blanco */
                border-radius: 8px;        /* Bordes redondeados */
                border: 1px solid #555555; /* Borde sutil */
                padding: 5px;
            }
            QMenu::item {
                font-family: 'Arial Black', sans-serif; /* Fuente Arial Black */
                font-size: 12px; /* Tamaño de fuente */
                padding: 10px 20px; /* Espaciado */
                background-color: transparent;
                border-radius: 4px; /* Bordes redondeados en las opciones */
            }
            QMenu::item:selected {
                background-color: #5A9; /* Fondo verde claro al seleccionar */
                color: white; /* Texto blanco cuando se selecciona */
                border-radius: 6px; /* Bordes redondeados al seleccionar */
            }
        """)
        

        menu.addAction('Mostrar resultados', lambda: self.menu_action_pacientes('Mostrar resultados'))
        
        # Mostrar menú en la posición del botón
        menu.exec(self.patient_button.mapToGlobal(QPoint(0, self.patient_button.height())))

    def menu_action_pacientes(self, option):
        
        if option == 'Mostrar resultados':
            self.show_results()
            
    
    def show_results(self):
        from resultados import SleepDataWindow
        self.results_window = SleepDataWindow(usuario=self.usuario, conexion = self.connection)
        self.results_window.show()
        self.close() 


    def change_access(self):
        dialog = QDialog()
        dialog.setWindowTitle('Actualizar credenciales')
        dialog.setWindowIcon(QIcon(get_icon_path('IPN-logo.png')))
        dialog.setModal(True)
        dialog.setFixedSize(350,400)

        # Creamos los campos de entrada para la actualización
        user_input = QLineEdit(dialog)
        user_input.setPlaceholderText('Ingrese su nuevo nombre...')
        password_input = QLineEdit(dialog)
        password_input.setPlaceholderText('Ingrese su nueva contraseña...')
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password2_input = QLineEdit(dialog)
        password2_input.setPlaceholderText('Confirme su nueva contraseña...')
        password2_input.setEchoMode(QLineEdit.EchoMode.Password)
    

        layout = QFormLayout()
        layout.addRow('Usuario:', user_input)
        layout.addRow('Password:', password_input)
        layout.addRow('Password:', password2_input)
        

            # Botones de añadir y cancelar
        cancel_button = QPushButton('Cancelar')
        update_button = QPushButton('Actualizar')

        
        layout.addRow(update_button, cancel_button)
        layout.addWidget(update_button)
        dialog.setLayout(layout)
        
        # Conexiones para los botones
        update_button.clicked.connect(lambda: self.update_user(
            user_input.text().strip(), 
            password_input.text(), 
            password2_input.text(),
            dialog))

        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()

    def update_user(self, user, password, password2, dialog):
        if user == '' or password == '' or password2 == '':
            QMessageBox.warning(self, 'Error', 'Debe llenar todos los campos', QMessageBox.StandardButton.Close)
        
        elif password != password2:
            QMessageBox.warning(self, 'Contraseñas diferentes', 'Las contraseñas no coinciden', QMessageBox.StandardButton.Close)

        else:
            try:
                cursor = self.connection.cursor()
                hashed_password = hash_password(password)
                query = '''
                update usuarios
                set nombre_usuario = %s, contrasenia = %s
                where usuario_id = (select usuario_id from usuarios where nombre_usuario = %s)
                        '''
                cursor.execute(query, (user,hashed_password, self.usuario))
                self.connection.commit()
                query_email = '''select email from usuarios where usuario_id = (select usuario_id from usuarios where nombre_usuario = %s)'''
                cursor.execute(query_email, (user,))
                save_email = cursor.fetchone()[0]

                envio_correo = enviar_nuevas_credenciales(save_email, user, password)

                if 'exitosamente' in envio_correo:
                    QMessageBox.information(self, 'Actualización exitosa', 'Se han actualizado las credenciales del usuario, revise su correo electrónico y vuelva a iniciar sesión')
                else:
                    QMessageBox.warning(self, 'Error en el correo electrónico', envio_correo)
                
                dialog.accept()
                
                self.login_window = LoginWindow()
                self.login_window.show()
                self.close()

            except Exception as e:
                QMessageBox.warning(self,'Error', f'No se completó la transacción: {e}')


    def close_all(self):
        # Creamos un cuadro de diálogo para confirmar que el usuario quiera cerrar sesión
        confirm = QMessageBox.question(self, 'Confirmar', f'¿Estás seguro de que desea cerrar sesión?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:

            self.login_window = LoginWindow() # En PyQT, debes tener una referencia persistente de este objeto
            self.login_window.show()
            self.close()
            

    def search_patient(self, curp, nombre1_input, nombre2_input, apellido1_input, apellido2_input, direccion, entidad_federativa, contacto):
        try:
            query = '''select nombre1, nombre2, apellido1, apellido2, direccion, entidad_federativa, contacto 
                        from pacientes
                        where paciente_id = %s and usuario_id = (select usuario_id from usuarios where nombre_usuario = %s )'''
            cursor = self.connection.cursor()
            cursor.execute(query, (curp, self.usuario))
            paciente = cursor.fetchone()

            if paciente:
                nombre1_input.setText(paciente[0])
                nombre2_input.setText(paciente[1] or '')
                apellido1_input.setText(paciente[2])
                apellido2_input.setText(paciente[3] or '')
                direccion.setText(paciente[4])
                entidad_federativa.setText(paciente[5])
                contacto.setText(paciente[6])
            else:
                QMessageBox.information(self, 'Paciente no encontrado', 'No se encontró al paciente con esa CURP')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'No se encontró al paciente: {str(e)}')
        
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    
    # Cuando se cierra la ventana, exec() devuelve el botón que el usuario presionó, en este caso, el botón Ok
    if login_window.exec() == QMessageBox.StandardButton.Ok:
        usuario = login_window.usuario
        main_window = MainWindow(usuario)
        main_window.show()

    sys.exit(app.exec())
