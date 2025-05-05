import tkinter as tk 
from tkinter import messagebox, ttk  
import os  
from admin import cargar 

# Función para volver a la ventana principal
def volver_ventana_principal():
    messagebox.showinfo("Contactos", "Redirigiendo a Página Principal")
    ventana.quit()
    ventana.destroy()
    os.system("python Vistas/principal.py")

# Función para actualizar el nombre del alumno según el RUT seleccionado
def actualizar_nombre_alumno(event=None):  # `event` es necesario para manejar eventos de selección en Combobox.
    """Actualizar el nombre del alumno según el RUT seleccionado."""
    rut_seleccionado = combo_alumno.get()  # Obtiene el RUT seleccionado en el Combobox.
    # Si no se selecciona ningún RUT válido, restablece el nombre del alumno.
    if rut_seleccionado == "Seleccionar alumno" or not rut_seleccionado:
        texto_nombre_alumno.set("Nombre del alumno")  # Restablece el marcador de posición.
        return

    # Busca el nombre del alumno en los datos cargados.
    for alumno in datos["alumnos"]:  # Recorre la lista de alumnos del archivo JSON.
        if alumno["rut"] == rut_seleccionado:  # Compara el RUT seleccionado con los RUTs disponibles.
            texto_nombre_alumno.set(alumno["nombre"])  # Actualiza el nombre del alumno si coincide.
            return

    # Si no se encuentra el RUT, restablece el marcador de posición.
    texto_nombre_alumno.set("Nombre del alumno")

# Función para confirmar la selección del RUT
def confirmar_rut():
    """Confirmar el RUT seleccionado y mostrar datos asociados."""
    rut_seleccionado = combo_alumno.get()  # Obtiene el RUT seleccionado en el Combobox.
    # Si no se selecciona un RUT válido, muestra una advertencia.
    if rut_seleccionado == "Seleccionar alumno" or not rut_seleccionado:
        messagebox.showwarning("Advertencia", "Debe seleccionar un RUT válido.")
        return

    # Actualiza los campos relacionados con el RUT seleccionado.
    actualizar_contactos(None)  # Llama a la función para actualizar contactos asociados al RUT.
    messagebox.showinfo("Confirmación", f"RUT {rut_seleccionado} confirmado.")  # Muestra un mensaje de confirmación.

# Función para actualizar los datos del apoderado según el RUT seleccionado
def actualizar_contactos(event=None):  # `event` maneja la selección en el Combobox.
    """Actualizar los campos de apoderado y contacto según el RUT seleccionado."""
    rut_seleccionado = combo_alumno.get()  # Obtiene el RUT seleccionado en el Combobox.
    # Si no se selecciona un RUT válido, restablece los valores de apoderado y contacto.
    if rut_seleccionado == "Seleccionar alumno" or not rut_seleccionado:
        texto_fijo_nombre.set("Nombre del apoderado")  # Restablece el marcador de posición para el apoderado.
        texto_fijo_contacto.set("Teléfono del apoderado")  # Restablece el marcador de posición para el teléfono.
        return

    # Busca el apoderado y su contacto en los datos cargados.
    for alumno in datos["alumnos"]:  # Recorre la lista de alumnos.
        if alumno["rut"] == rut_seleccionado:  # Compara el RUT seleccionado con los RUTs disponibles.
            texto_fijo_nombre.set(alumno["apoderado"])  # Actualiza el nombre del apoderado.
            for apoderado in datos["apoderados"]:  # Busca el contacto del apoderado en la lista de apoderados.
                if apoderado["nombre"] == alumno["apoderado"]:  # Coincide el nombre del apoderado.
                    texto_fijo_contacto.set(apoderado["telefono"])  # Actualiza el número de contacto.
                    break
            return

    # Si no se encuentra información para el RUT seleccionado, restablece los valores.
    texto_fijo_nombre.set("Nombre del apoderado")
    texto_fijo_contacto.set("Teléfono del apoderado")
    messagebox.showwarning("Advertencia", f"No se encontró información para el RUT: {rut_seleccionado}")

# Crear la ventana principal
ventana = tk.Tk()  # Crea la ventana principal.
ventana.title("Contactos - Barrabases FC")  # Establece el título de la ventana.
ventana.geometry("800x400")  # Define el tamaño de la ventana en píxeles (ancho x alto).
ventana.configure(bg="#1c1f33")  # Cambia el color de fondo de la ventana.

# Marco central para los contenidos principales
frame_central = tk.Frame(ventana, bg="white", bd=2, relief="solid")  # Crea un marco con borde.
frame_central.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")  # Posiciona el marco.

# Combobox para seleccionar el RUT
lbl_rut = tk.Label(
    frame_central, text="Seleccione RUT del alumno:",  # Etiqueta de ayuda.
    font=("Arial", 12, "bold"), bg="white"
)
lbl_rut.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Posiciona la etiqueta.

texto_fijo_rut = tk.StringVar()  # Variable para manejar el texto seleccionado en el Combobox.
combo_alumno = ttk.Combobox(
    frame_central, font=("Arial", 10), textvariable=texto_fijo_rut,  # Crea el Combobox.
    state="readonly", width=40  # Solo lectura y ancho definido.
)
combo_alumno.grid(row=0, column=1, padx=10, pady=10, sticky="w")  # Posiciona el Combobox.
combo_alumno.set("Seleccionar alumno")  # Establece el texto inicial.

# Botón para confirmar el RUT
btn_confirmar_rut = tk.Button(
    frame_central, text="Confirmar RUT", bg="#66CCFF", fg="black",  # Botón con texto y colores.
    font=("Arial", 10, "bold"), command=confirmar_rut  # Llama a la función `confirmar_rut`.
)
btn_confirmar_rut.grid(row=0, column=2, padx=10, pady=10, sticky="w")  # Posiciona el botón.

# Entrada para mostrar el nombre del alumno
lbl_nombre_alumno = tk.Label(
    frame_central, text="Nombre del alumno:", 
    font=("Arial", 12, "bold"), bg="white"
)
lbl_nombre_alumno.grid(row=1, column=0, padx=10, pady=10, sticky="w")

texto_nombre_alumno = tk.StringVar()
texto_nombre_alumno.set("Nombre del alumno")
entry_nombre_alumno = tk.Entry(
    frame_central, textvariable=texto_nombre_alumno, state="readonly", 
    font=("Arial", 10), width=50
)
entry_nombre_alumno.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="w")

# Etiqueta y entrada para apoderado
lbl_apoderado = tk.Label(
    frame_central, text="Apoderado:", 
    font=("Arial", 12, "bold"), bg="white"
)
lbl_apoderado.grid(row=2, column=0, padx=10, pady=10, sticky="w")

texto_fijo_nombre = tk.StringVar()
texto_fijo_nombre.set("Nombre del apoderado")
entry_apoderado = tk.Entry(
    frame_central, textvariable=texto_fijo_nombre, state="readonly", 
    font=("Arial", 10), width=50
)
entry_apoderado.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="w")

# Etiqueta y entrada para contacto
lbl_contacto = tk.Label(
    frame_central, text="Contacto:", 
    font=("Arial", 12, "bold"), bg="white"
)
lbl_contacto.grid(row=3, column=0, padx=10, pady=10, sticky="w")

texto_fijo_contacto = tk.StringVar()
texto_fijo_contacto.set("Teléfono del apoderado")
entry_contacto = tk.Entry(
    frame_central, textvariable=texto_fijo_contacto, state="readonly", 
    font=("Arial", 10), width=50
)
entry_contacto.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="w")

# Botón de volver
btn_volver = tk.Button(
    ventana, text="Volver", bg="#66CCFF", fg="black", 
    font=("Arial", 12, "bold"), command=volver_ventana_principal
)
btn_volver.grid(row=2, column=0, columnspan=3, pady=10)

# Cargar RUTs desde JSON
datos = cargar()
ruts_alumnos = [alumno["rut"] for alumno in datos["alumnos"]]
combo_alumno["values"] = ruts_alumnos

# Asociar evento para actualizar el nombre del alumno en tiempo real
combo_alumno.bind("<<ComboboxSelected>>", actualizar_nombre_alumno)

# Ajusta el diseño de las filas y columnas de la ventana principal.
ventana.grid_rowconfigure(1, weight=1)  # Permite que el marco central crezca con la ventana.
ventana.grid_columnconfigure(0, weight=1)  # Permite que las columnas se ajusten.

# Inicia el bucle principal de la ventana.
ventana.mainloop()  