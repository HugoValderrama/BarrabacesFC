import tkinter as tk  
import os  
from tkinter import messagebox  # Importa el módulo messagebox para mostrar cuadros de diálogo.

# Función para abrir la sección "Control de Usuarios"
def abrir_control_usuarios():
    messagebox.showinfo("Control de Usuarios", "Redirigiendo a Control de Usuarios")  
    ventana.quit() 
    ventana.destroy() 
    os.system("python Vistas/control_usuarios.py")  
    
# Función para abrir la sección "Lista de Alumnos"
def abrir_lista_alumnos():
    messagebox.showinfo("Lista de Alumnos", "Redirigiendo a Lista de Alumnos")  # Muestra un cuadro de información.
    ventana.quit()  # Detiene el bucle principal de la ventana actual.
    ventana.destroy()  # Cierra la ventana actual.
    os.system("python Vistas/listado_alumnos.py")  # Ejecuta el script correspondiente a "Lista de Alumnos".

# Función para abrir la sección "Contactos"
def abrir_contactos():
    messagebox.showinfo("Contactos", "Redirigiendo a Contactos") 
    ventana.quit()  
    ventana.destroy()  
    os.system("python Vistas/contactos.py")

# Función para abrir la sección "Ranking"
def abrir_ranking():
    messagebox.showinfo("Ranking", "Redirigiendo a Ranking") 
    ventana.quit()  
    ventana.destroy()  
    os.system("python Vistas/ranking.py") 

# Función para abrir la sección "Entrenamiento"
def abrir_entrenamiento():
    messagebox.showinfo("Entrenamiento", "Redirigiendo a Entrenamiento")  
    ventana.quit() 
    ventana.destroy() 
    os.system("python Vistas/entrenamiento.py") 

# Crear la ventana principal
ventana = tk.Tk()  # Crea una instancia de la ventana principal de Tkinter.
ventana.title("Barrabases FC")  # Establece el título de la ventana.
ventana.geometry("600x400")  # Define el tamaño de la ventana en píxeles.
ventana.config(bg="#1c1f33")  # Cambia el color de fondo de la ventana.

# Título principal de la ventana
titulo = tk.Label(
    ventana,  # Asocia el título con la ventana principal.
    text="BARRABASES FC",  # Texto del título.
    font=("Arial", 24, "bold"),  # Fuente, tamaño y estilo del texto.
    bg="#1c1f33",  # Color de fondo del título.
    fg="white"  # Color del texto del título.
)
titulo.pack(pady=10)  # Empaqueta el título en la ventana con un margen vertical de 10 píxeles.

# Crear un contenedor para los botones de las secciones principales
frame_secciones = tk.Frame(ventana, bg="#1c1f33")  # Crea un marco con el mismo color de fondo que la ventana.
frame_secciones.pack(pady=20)  # Empaqueta el marco con un margen vertical de 20 píxeles.

# Botón para la sección "Control de Usuarios"
boton_control_usuarios = tk.Button(
    frame_secciones,  # Asocia el botón con el marco.
    text="Control de Usuarios",  # Texto que muestra el botón.
    font=("Arial", 12, "bold"),  # Fuente, tamaño y estilo del texto.
    command=abrir_control_usuarios,  # Función que se ejecutará al hacer clic.
    bg="#3b4fe4",  # Color de fondo del botón.
    fg="white",  # Color del texto del botón.
    width=20  # Ancho del botón en caracteres.
)
boton_control_usuarios.grid(row=0, column=0, padx=10, pady=10)  # Posiciona el botón en una cuadrícula dentro del marco.

# Botón para la sección "Lista de Alumnos"
boton_lista_alumnos = tk.Button(
    frame_secciones,  # Asocia el botón con el marco.
    text="Lista de Alumnos",  # Texto que muestra el botón.
    font=("Arial", 12, "bold"),  # Fuente, tamaño y estilo del texto.
    command=abrir_lista_alumnos,  # Función que se ejecutará al hacer clic.
    bg="#324f6b",  # Color de fondo del botón.
    fg="white",  # Color del texto del botón.
    width=20  # Ancho del botón en caracteres.
)
boton_lista_alumnos.grid(row=0, column=1, padx=10, pady=10)  # Posiciona el botón en una cuadrícula dentro del marco.

# Botón para la sección "Contactos"
boton_contactos = tk.Button(
    frame_secciones,  # Asocia el botón con el marco.
    text="Contactos",  # Texto que muestra el botón.
    font=("Arial", 12, "bold"),  # Fuente, tamaño y estilo del texto.
    command=abrir_contactos,  # Función que se ejecutará al hacer clic.
    bg="#3b4fe4",  # Color de fondo del botón.
    fg="white",  # Color del texto del botón.
    width=20  # Ancho del botón en caracteres.
)
boton_contactos.grid(row=1, column=0, padx=10, pady=10)  # Posiciona el botón en una cuadrícula dentro del marco.

# Botón para la sección "Ranking"
boton_ranking = tk.Button(
    frame_secciones,  # Asocia el botón con el marco.
    text="Ranking",  # Texto que muestra el botón.
    font=("Arial", 12, "bold"),  # Fuente, tamaño y estilo del texto.
    command=abrir_ranking,  # Función que se ejecutará al hacer clic.
    bg="#324f6b",  # Color de fondo del botón.
    fg="white",  # Color del texto del botón.
    width=20  # Ancho del botón en caracteres.
)
boton_ranking.grid(row=1, column=1, padx=10, pady=10)  # Posiciona el botón en una cuadrícula dentro del marco.

# Botón para la sección "Entrenamiento"
boton_entrenamiento = tk.Button(
    ventana,  # Asocia el botón directamente con la ventana principal.
    text="Entrenamiento",  # Texto que muestra el botón.
    font=("Arial", 12, "bold"),  # Fuente, tamaño y estilo del texto.
    command=abrir_entrenamiento,  # Función que se ejecutará al hacer clic.
    bg="#2a2f49",  # Color de fondo del botón.
    fg="white",  # Color del texto del botón.
    width=20  # Ancho del botón en caracteres.
)
boton_entrenamiento.pack(pady=10)  # Empaqueta el botón con un margen vertical de 10 píxeles.

# Inicia el bucle principal de la interfaz gráfica
ventana.mainloop()  # Mantiene la ventana abierta y responde a las interacciones del usuario.