import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os



def create_connection():
    try:
        load_dotenv()
        conn = psycopg2.connect(host=os.getenv('HOST'), 
                                user=os.getenv('USER'), 
                                password = os.getenv('PASSWORD'), 
                                database = os.getenv('DATABASE'),
                                port= os.getenv('PORT'))
        cursor = conn.cursor()
        #cursor.execute('select * from pacientes')
        #pacientes = cursor.fetchall()
        print('Conexión exitosa')

        return conn
    
    except OperationalError as e:
        print('Error al conectar a la base de datos:', e)
        return None

#conn = create_connection()


        

