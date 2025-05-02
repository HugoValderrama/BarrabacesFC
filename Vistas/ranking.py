import tkinter as tk
from tkinter import ttk
from admin import cargar
from datetime import datetime
import os  
from tkinter import messagebox

# Función para volver a la ventana principal
def volver_ventana_principal():
    messagebox.showinfo("Ranking", "Redirigiendo a Página Principal")
    ventana.quit()
    ventana.destroy()
    os.system("python Vistas/principal.py")

# Función para actualizar el ranking
def actualizar_ranking():
    mes_seleccionado = combo_mes.get()
    if not mes_seleccionado:
        return

    # Obtener el mes y año actual
    año_actual = datetime.now().year
    mes_num = meses.index(mes_seleccionado) + 1

    # Cargar datos y filtrar goles del mes seleccionado
    datos = cargar()
    goles_mes = [gol for gol in datos.get("goles", []) if gol["fecha"].startswith(f"{año_actual}-{mes_num:02d}")]

    # Contar los goles por alumno
    ranking = {}
    for gol in goles_mes:
        rut_alumno = gol["rut_alumno"]
        cantidad_goles = gol["cantidad_goles"]
        if rut_alumno in ranking:
            ranking[rut_alumno] += cantidad_goles
        else:
            ranking[rut_alumno] = cantidad_goles

    # Ordenar el ranking por cantidad de goles
    ranking_ordenado = sorted(ranking.items(), key=lambda item: item[1], reverse=True)[:5]

    # Actualizar la tabla
    for row in tabla.get_children():
        tabla.delete(row)

    for rut, goles in ranking_ordenado:
        # Buscar el nombre del alumno
        alumno = next((al for al in datos["alumnos"] if al["rut"] == rut), None)
        nombre = alumno["nombre"] if alumno else "Desconocido"
        tabla.insert("", tk.END, values=(nombre, goles))

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Ranking de Goleadores")
ventana.geometry("700x500")
ventana.configure(bg="#1c1f33")

# Lista de meses
datos = cargar()
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# Frame para la selección del mes
frame_seleccion = tk.Frame(ventana, bg="white", bd=2, relief="solid")
frame_seleccion.pack(padx=20, pady=20, fill=tk.X)

lbl_mes = tk.Label(frame_seleccion, text="Seleccione un mes:", font=("Arial", 12, "bold"), bg="white")
lbl_mes.grid(row=0, column=0, padx=10, pady=10, sticky="w")

combo_mes = ttk.Combobox(frame_seleccion, values=meses, state="readonly", font=("Arial", 10))
combo_mes.grid(row=0, column=1, padx=10, pady=10)
combo_mes.bind("<<ComboboxSelected>>", lambda e: actualizar_ranking())

# Tabla para mostrar el ranking
frame_tabla = tk.Frame(ventana, bg="white", bd=2, relief="solid")
frame_tabla.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

tabla = ttk.Treeview(frame_tabla, columns=("Alumno", "Goles"), show="headings", height=10)

tabla.heading("Alumno", text="Alumno")
tabla.heading("Goles", text="Goles")

tabla.pack(fill=tk.BOTH, padx=5, pady=5)

# Personalizar estilos de la tabla
tabla.tag_configure("evenrow", background="#f2f2f2")
tabla.tag_configure("oddrow", background="#ffffff")

# Botones para actualizar y volver
frame_botones = tk.Frame(ventana, bg="#1c1f33")
frame_botones.pack(pady=10)

btn_actualizar = tk.Button(frame_botones, text="Actualizar Ranking", font=("Arial", 12, "bold"), bg="#66CCFF", fg="black", command=actualizar_ranking)
btn_actualizar.grid(row=0, column=0, padx=10)

btn_volver = tk.Button(frame_botones, text="Atrás", font=("Arial", 12, "bold"), bg="#66CCFF", fg="black", command=volver_ventana_principal)
btn_volver.grid(row=0, column=1, padx=10)

# Iniciar con diseño ajustado
ventana.mainloop()