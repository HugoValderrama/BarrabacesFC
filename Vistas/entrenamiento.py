import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
from tkcalendar import Calendar
from admin import cargar, guardar

def volver_ventana_principal():
    messagebox.showinfo("Entrenamiento", "Redirigiendo a Página Principal")
    ventana.quit()
    ventana.destroy()
    os.system("python Vistas/principal.py")

# Función para registrar goles
def registrar_goles():
    alumno = combo_alumnos.get()
    goles = entry_goles.get()
    fecha = calendar.get_date()

    if not alumno or not goles.isdigit():
        messagebox.showerror("Error", "Debe seleccionar un alumno y especificar un número válido de goles.")
        return

    goles = int(goles)

    datos = cargar()

    # Buscar el alumno en la lista de alumnos
    alumno_data = next((al for al in datos["alumnos"] if al["nombre"] == alumno), None)
    if not alumno_data:
        messagebox.showerror("Error", f"El alumno {alumno} no se encuentra en los registros.")
        return

    rut_alumno = alumno_data["rut"]

    # Registrar el gol en la sección de goles
    if "goles" not in datos:
        datos["goles"] = []

    # Buscar si ya existe un registro para este alumno en esta fecha
    registro_existente = next((gol for gol in datos["goles"] if gol["rut_alumno"] == rut_alumno and gol["fecha"] == fecha), None)

    if registro_existente:
        registro_existente["cantidad_goles"] += goles
    else:
        datos["goles"].append({"rut_alumno": rut_alumno, "fecha": fecha, "cantidad_goles": goles})

    guardar(datos)
    messagebox.showinfo("Éxito", f"Se registraron {goles} goles para {alumno} el {fecha}.")
    entry_goles.delete(0, tk.END)
    actualizar_tabla()

# Función para actualizar la tabla
def actualizar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)

    datos = cargar()
    fecha_seleccionada = calendar.get_date()
    goles_seleccionados = [gol for gol in datos.get("goles", []) if gol["fecha"] == fecha_seleccionada]

    resumen_goles = {}

    for gol in goles_seleccionados:
        rut_alumno = gol["rut_alumno"]
        alumno_data = next((al for al in datos["alumnos"] if al["rut"] == rut_alumno), None)
        if not alumno_data:
            continue

        nombre_alumno = alumno_data["nombre"]
        resumen_goles[nombre_alumno] = resumen_goles.get(nombre_alumno, 0) + gol["cantidad_goles"]

    for alumno, total_goles in resumen_goles.items():
        tabla.insert("", tk.END, values=(alumno, total_goles))

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Entrenamiento - Registro de Goles")
ventana.geometry("800x600")
ventana.configure(bg="#1c1f33")

# Cargar alumnos desde el JSON
datos = cargar()
alumnos = [alumno["nombre"] for alumno in datos.get("alumnos", [])]

# Frame para registrar goles
frame_registro = tk.Frame(ventana, bg="white", bd=2, relief="solid")
frame_registro.pack(padx=20, pady=20, fill=tk.X)

lbl_alumno = tk.Label(frame_registro, text="Alumno:", font=("Arial", 12, "bold"), bg="white")
lbl_alumno.grid(row=0, column=0, padx=10, pady=10, sticky="w")

combo_alumnos = ttk.Combobox(frame_registro, values=alumnos, state="readonly", font=("Arial", 10))
combo_alumnos.grid(row=0, column=1, padx=10, pady=10, sticky="w")

lbl_goles = tk.Label(frame_registro, text="Goles:", font=("Arial", 12, "bold"), bg="white")
lbl_goles.grid(row=1, column=0, padx=10, pady=10, sticky="w")

entry_goles = tk.Entry(frame_registro, font=("Arial", 10))
entry_goles.grid(row=1, column=1, padx=10, pady=10, sticky="w")

lbl_fecha = tk.Label(frame_registro, text="Fecha:", font=("Arial", 12, "bold"), bg="white")
lbl_fecha.grid(row=2, column=0, padx=10, pady=10, sticky="w")

calendar = Calendar(frame_registro, selectmode="day", date_pattern="yyyy-mm-dd")
calendar.grid(row=2, column=1, padx=10, pady=10, sticky="w")

btn_registrar = tk.Button(frame_registro, text="Registrar Goles", font=("Arial", 12, "bold"), bg="#66CCFF", fg="black", command=registrar_goles)
btn_registrar.grid(row=3, column=0, columnspan=2, pady=10)

# Tabla para mostrar datos
frame_tabla = tk.Frame(ventana, bg="white", bd=2, relief="solid")
frame_tabla.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

tabla = ttk.Treeview(frame_tabla, columns=("Alumno", "Total Goles"), show="headings", height=10)

tabla.heading("Alumno", text="Alumno")
tabla.heading("Total Goles", text="Total Goles")

tabla.pack(fill=tk.BOTH, padx=5, pady=5)

# Botones horizontales
frame_botones = tk.Frame(ventana, bg="#1c1f33")
frame_botones.pack(pady=10)

btn_actualizar = tk.Button(frame_botones, text="Actualizar Tabla", font=("Arial", 12, "bold"), bg="#66CCFF", fg="black", command=actualizar_tabla)
btn_actualizar.grid(row=0, column=0, padx=10)

btn_volver = tk.Button(frame_botones, text="Atrás", font=("Arial", 12, "bold"), bg="#66CCFF", fg="black", command=volver_ventana_principal)
btn_volver.grid(row=0, column=1, padx=10)

# Cargar datos iniciales
actualizar_tabla()

ventana.mainloop()