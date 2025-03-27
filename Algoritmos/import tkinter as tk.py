import tkinter as tk
from PIL import Image, ImageTk
from camaraIntento2 import  calcular_distancia_real,medir_distancia_ojos_camara

# Función que se ejecuta al presionar el botón
def ejecutar_codigo():
    print("¡El código se está ejecutando!")
    
    # Aquí puedes agregar más código para lo que desees ejecutar cuando presionas el botón

# Crear ventana principal
ventana = tk.Tk()
ventana.geometry("1440x900")
ventana.title("Ventana con fondo")

# Cargar la imagen JPG con Pillow
ruta_imagen = r"C:\Users\Rober\PycharmProjects\TT\sueno.jpg"
imagen = Image.open(ruta_imagen)
imagen = imagen.resize((1440, 900))  # Ajustar el tamaño de la imagen al de la ventana
fondo = ImageTk.PhotoImage(imagen)

# Crear un Label con la imagen de fondo
label_fondo = tk.Label(ventana, image=fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Agregar widgets sobre el fondo
etiqueta = tk.Label(ventana, text="Bienvenido\n Haga clic para iniciar la grabación\n Indique la distancia en la que estarán sus ojos de la cámara", font=("Helvetica", 17, "bold"), fg="black", bg="white", padx=400, pady=20)
etiqueta.pack(pady=20)
# Crear un Label para describir el campo de entrada (etiqueta)
#label_distancia = tk.Label(ventana, text="Ingresa la distancia de referencia:", font=("Helvetica", 17,"bold"), bg="white", fg="purple", width=20, height=2, padx=100, pady=20)
#label_distancia.place(x=500, y=270) 

# Crear un Entry para ingresar el valor de la distancia con tamaño ajustado
entry_distancia = tk.Entry(ventana, font=("Helvetica", 17), bg="white", fg="purple", width=20)  # Ajusta el ancho con 'width'
entry_distancia.place(x=520, y=350)


# Crear el botón y asignarle la función
boton = tk.Button(ventana, text="iniciar grabacion", command=ejecutar_codigo, font=("Helvetica", 17, "bold"), bg="white", fg="purple", width=20, height=2)
# Ubicación exacta con place
boton.place(x=500, y=550) 
# Iniciar la interfaz gráfica
ventana.mainloop()
