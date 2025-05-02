import tkinter as tk
from tkinter import messagebox, ttk
import os
from admin import cargar, listado_alum  # Importar las funciones necesarias

# Glosario: 

# combobox.get(): Obtiene el valor seleccionado en el Combobox.
# tabla.get_children(): Devuelve una lista con todas las filas (nodos) actuales de la tabla.
# tabla.insert(): Inserta una nueva fila en la tabla con los valores especificados.
# relief="solid": Define un borde sólido alrededor del marco.
# fill="both", expand=True: Permite que el marco ocupe todo el espacio disponible.
# ttk.Treeview: Widget avanzado que permite mostrar datos tabulares.
# show="headings": Muestra solo los encabezados (sin una columna raíz).
# tabla.heading(): Define el texto de los encabezados.
# tabla.column(): Configura el ancho y la alineación de cada columna.

def mostrar_alumnos():
    """Muestra la lista de alumnos asignados al profesor seleccionado."""
    profesor_seleccionado = combobox.get()  # Obtiene el nombre del profesor seleccionado en el Combobox.
    if profesor_seleccionado == "Seleccione un profesor":  # Verifica si no se seleccionó un profesor válido.
        messagebox.showwarning("Advertencia", "Debe seleccionar un profesor.")  # Muestra una advertencia.
        return

    # Obtiene el listado de alumnos asignados al profesor seleccionado.
    alumnos = listado_alum(profesor_seleccionado)

    # Limpia la tabla antes de mostrar nuevos datos.
    for item in tabla.get_children():  # Recorre todas las filas de la tabla.
        tabla.delete(item)  # Elimina cada fila existente.

    # Si no hay alumnos asignados al profesor, muestra un mensaje.
    if not alumnos:
        messagebox.showinfo("Sin alumnos", f"No hay alumnos asignados a {profesor_seleccionado}.")
    else:
        # Inserta los datos de los alumnos en la tabla.
        for alumno in alumnos:
            tabla.insert("", "end", values=(alumno["rut"], alumno["nombre"], alumno["apoderado"], alumno["direccion"]))


def volver_ventana_principal():
    messagebox.showinfo("Listado de Alumnos", "Redirigiendo a Página Principal")
    ventana.quit()
    ventana.destroy()
    os.system("python Vistas/principal.py")

ventana = tk.Tk()
ventana.title("Lista de Alumnos")
ventana.geometry("800x400")
ventana.config(bg="#1c1f33")  # Fondo azul oscuro

# Frame principal con fondo blanco para todo el contenido
main_frame = tk.Frame(ventana, bg="white", bd=2, relief="solid")
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

etiqueta = ttk.Label(main_frame, text="Seleccionar el profesor:", font=("Arial", 12, "bold"), background="white", foreground="black")
etiqueta.grid(row=0, column=0, pady=10, padx=10, sticky="w")  # Posiciona la etiqueta.

# Cargar datos desde el JSON para llenar el Combobox.
datos = cargar()  # Llama a la función `cargar` para obtener los datos del archivo JSON.
nombres_profesores = [profesor["nombre"] for profesor in datos["profesores"]]  # Obtiene una lista con los nombres de los profesores.

combobox = ttk.Combobox(main_frame, values=nombres_profesores, state="readonly", width=30)  # Crea un Combobox de solo lectura.
combobox.grid(row=0, column=1, padx=10, pady=10)  # Posiciona el Combobox.
combobox.set("Seleccione un profesor")  # Establece el texto inicial del Combobox.

# Botón para mostrar alumnos
boton = ttk.Button(main_frame, text="Mostrar Alumnos", command=mostrar_alumnos)
boton.grid(row=0, column=2, padx=10, pady=10)

columnas = ("Rut", "Nombre", "Apoderado", "Dirección")  # Define las columnas de la tabla.
tabla = ttk.Treeview(main_frame, columns=columnas, show="headings", height=10)  # Crea una tabla con encabezados visibles.
tabla.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")  # Posiciona la tabla en el marco.

# Configura las columnas y encabezados de la tabla.
tabla.heading("Rut", text="Rut")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Apoderado", text="Apoderado")
tabla.heading("Dirección", text="Dirección")
tabla.column("Rut", width=100, anchor="center")  # Ancho fijo y centrado.
tabla.column("Nombre", width=200, anchor="w")  # Ancho fijo, alineado a la izquierda.
tabla.column("Apoderado", width=200, anchor="w")
tabla.column("Dirección", width=200, anchor="w")


# Ajustar filas y columnas del main_frame
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Botón Volver fuera del frame principal
btn_volver = tk.Button(ventana, text="Volver", bg="#66CCFF", font=("Arial", 12, "bold"), command=volver_ventana_principal)
btn_volver.pack(pady=10)

ventana.mainloop()