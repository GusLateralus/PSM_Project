import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from PyQt6.QtWidgets import QMessageBox

def enviar_nuevas_credenciales(email, usuario, password):

        load_dotenv()
        
        msg = EmailMessage()
        msg.set_content(f'''Hola, estas son tus nuevas credenciales
                          
                        Usuario: {usuario}
                        Clave: {password} 
                        No compartas estos datos con nadie. Saludos,

                        Equipo de soporte. 
                        ''')
        msg['Subject'] = 'Nuevas credenciales'
        msg['From'] = os.getenv('USUARIO_EMAIL')
        msg['To'] = email

        try:
            with smtplib.SMTP_SSL(os.getenv('SMTP_SSL'), 465) as smtp:
                smtp.login(os.getenv('USUARIO_EMAIL'), os.getenv('PASSWORD_EMAIL'))
                smtp.send_message(msg)
            return 'Correo enviado exitosamente'
            
        except smtplib.SMTPException as e:
            return f'Error al enviar el correo electrónico: {e}'


def enviar_registro_paciente(email, curp, estudio_id, fecha, hora, nombre_medico):
    load_dotenv()
        
    msg = EmailMessage()
    msg.set_content(f'''Estimado paciente,

    Le confirmamos su registro en nuestro sistema con la siguiente información:
    - CURP: {curp}
    - ID del Estudio: {estudio_id}
    - Fecha: {fecha}
    - Hora: {hora}
    - Médico: {nombre_medico}

    Por favor, revise el archivo adjunto con la hoja de consentimiento. 
    Recuerde firmarla y enviarla por este medio antes de realizarse el estudio. En caso
    de no aceptar, su registro será eliminado de nuestro sistema.

    Atentamente,
    El equipo médico.''')

    msg['Subject'] = 'Registro de Estudio Médico y Hoja de consentimiento'
    msg['From'] = os.getenv('USUARIO_EMAIL')
    msg['To'] = email

    ruta_archivo = 'pythonProject/ProyectoPSM/CARTA PODER DE CONSENTIMIENTO INFORMADO (1).docx'

    try:
        with open(ruta_archivo, "rb") as archivo:
             msg.add_attachment(
                  archivo.read(),
                  maintype = "application",
                  subtype = 'vnd.openxmlformats-officedocument.wordprocessingml.document',
                  filename = 'Hoja_de_consentimiento.docx'
             )
        with smtplib.SMTP_SSL(os.getenv('SMTP_SSL'), 465) as smtp:
                smtp.login(os.getenv('USUARIO_EMAIL'), os.getenv('PASSWORD_EMAIL'))
                smtp.send_message(msg)
        return 'Correo enviado exitosamente'
    
    except FileNotFoundError:
         return f'Error: El archivo Word en la ruta {ruta_archivo} no existe'
            
    except smtplib.SMTPException as e:
        return f'Error al enviar el correo electrónico: {e}'


def enviar_resultados(email, paciente, estudio_id, fecha, ruta_pdf):
    load_dotenv()
    msg = EmailMessage()
    msg.set_content(f''' Estimado {paciente},
                     
    Le enviamos los resultados de su estudio con la siguiente información:
    - Número de estudio: {estudio_id}
    - Fecha: {fecha}

    Adjuntamos el archivo PDF con los resultados. Por favor, no dude en contactarnos.
    Recuerde que en caso de ser necesario, usted puede repetir su estudio.

    Atentamente,
    El equipo médico.''')
     
    msg['Subject'] = f'Resultados del Estudio {estudio_id}'
    msg['From'] = os.getenv('USUARIO_EMAIL')
    msg['To'] = email

    try:
        with open(ruta_pdf, 'rb') as archivo_pdf:
            msg.add_attachment(
                 archivo_pdf.read(),
                 maintype='application',
                 subtype='pdf',
                 filename=os.path.basename(ruta_pdf)
            )

        with smtplib.SMTP_SSL(os.getenv('SMTP_SSL'), 465) as smtp:
             smtp.login(os.getenv('USUARIO_EMAIL'), os.getenv('PASSWORD_EMAIL'))
             smtp.send_message(msg)
        
        return 'Correo enviado exitosamente'
    
    except FileNotFoundError:
        return f'Error: El archivo PDF en la ruta {ruta_pdf} no existe'
    
    except smtplib.SMTPException as e:
         return f'Error al enviar el correo electrónico: {e}'
                
    