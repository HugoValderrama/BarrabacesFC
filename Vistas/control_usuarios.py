import tkinter as tk
from tkinter import messagebox, ttk
import os
from admin import (agregar_alumno, agregar_apoderado, agregar_profesor, 
modificar_alumno, modificar_apoderado, modificar_profesor, 
eliminar_alumno, eliminar_apoderado, eliminar_profesor, 
cargar)

# Glosario:
#event.widget: Se refiere al widget que activó el evento, como el Combobox en este caso.
#combobox.master.winfo_children(): Obtiene todos los widgets dentro del mismo contenedor (frame) que el Combobox.
#grid_info(): Devuelve información sobre la posición del widget en el diseño de cuadrícula (grid)
#winfo_children(): Devuelve una lista con todos los widgets hijos dentro del frame.
#all(): Verifica que todas las condiciones en una lista sean verdaderas.

# Función para volver a la ventana principal
def volver_ventana_principal():
    messagebox.showinfo("Control de Usuarios", "Redirigiendo a Página Principal")
    ventana.quit()
    ventana.destroy()
    os.system("python Vistas/principal.py")

def rut_duplicado(rut):
    datos = cargar()  # Carga los datos del sistema

    # Revisar en todas las listas de usuarios
    for usuario in datos["profesores"] + datos["alumnos"] + datos["apoderados"]:
        if usuario["rut"] == rut:  # Cambia usuario.rut por usuario["rut"]
            return True
    return False

def validar_rut(rut):
    """
    Valida un RUT chileno. Verifica el formato y el dígito verificador.
    """
    try:
        # Limpiar el RUT
        rut = rut.replace(".", "").replace("-", "").strip().upper()
        print(f"RUT para validar: '{rut}'")

        # Separar el cuerpo y el dígito verificador
        cuerpo, dv = rut[:-1], rut[-1]
        print(f"Cuerpo: '{cuerpo}', Dígito Verificador ingresado: '{dv}'")  

        # Validar que el cuerpo sea numérico
        if not cuerpo.isdigit():
            print("El cuerpo del RUT no es numérico.") 
            return False

        # Calcular el dígito verificador esperado
        suma = 0
        factor = 2
        for c in reversed(cuerpo):
            suma += int(c) * factor
            factor = 2 if factor == 7 else factor + 1

        resto = suma % 11
        dv_calculado = "0" if resto == 0 else "K" if resto == 1 else str(11 - resto)
        print(f"Dígito Verificador calculado: '{dv_calculado}'")  # Debugging

        # Comparar el dígito verificador calculado con el ingresado
        return dv.upper() == dv_calculado.upper()
    except Exception as e:
        print(f"Error al validar RUT: {e}")  # Debugging
        return False

def actualizar_nombre_por_rut(event):
    """Actualiza el nombre correspondiente al RUT seleccionado en el Combobox."""
    tipo = tipo_usuario.get()  # Obtiene el tipo de usuario seleccionado (Profesor, Alumno o Apoderado).
    if not tipo:  # Si no se seleccionó un tipo de usuario, termina la función.
        return

    datos = cargar()  # Carga los datos desde el archivo JSON utilizando la función `cargar`.
    combobox = event.widget  # Obtiene el widget (Combobox) que disparó el evento.
    rut_seleccionado = combobox.get()  # Obtiene el valor seleccionado en el Combobox.

    nombre = ""  # Inicializa el nombre como vacío.
    if tipo == "Profesor":  # Si el usuario seleccionado es un Profesor:
        for profesor in datos["profesores"]:  # Recorre la lista de profesores.
            if profesor["rut"] == rut_seleccionado:  # Si el RUT coincide:
                nombre = profesor["nombre"]  # Obtiene el nombre del profesor.
                break
    elif tipo == "Alumno":  # Si el usuario seleccionado es un Alumno:
        for alumno in datos["alumnos"]:  # Recorre la lista de alumnos.
            if alumno["rut"] == rut_seleccionado:  # Si el RUT coincide:
                nombre = alumno["nombre"]  # Obtiene el nombre del alumno.
                break
    elif tipo == "Apoderado":  # Si el usuario seleccionado es un Apoderado:
        for apoderado in datos["apoderados"]:  # Recorre la lista de apoderados.
            if apoderado["rut"] == rut_seleccionado:  # Si el RUT coincide:
                nombre = apoderado["nombre"]  # Obtiene el nombre del apoderado.
                break

    # Actualiza el campo de nombre asociado al Combobox seleccionado.
    # Encontrar el campo de nombre asociado al Combobox y actualizarlo
    for sibling in combobox.master.winfo_children():
        if isinstance(sibling, tk.Entry) and sibling.grid_info()["row"] == combobox.grid_info()["row"] + 1:
            sibling.delete(0, tk.END)  # Limpiar el campo
            sibling.insert(0, nombre)  # Insertar el nombre correspondiente
            sibling.config(state="readonly")  # Hacerlo de solo lectura

# Conectar el botón Confirmar con las funciones correspondientes
def ejecutar_operacion():
    """
    Ejecuta la operación seleccionada según el tipo de usuario y acción.
    """
    tipo = tipo_usuario.get()  # Obtiene el tipo de usuario seleccionado.
    oper = operacion.get()  # Obtiene la operación seleccionada.

    # Validar selección de tipo de usuario y operación.
    if not tipo or not oper:
        messagebox.showwarning("Advertencia", "Debe seleccionar el tipo de usuario y la operación.")
        return

    # Identificar el frame y los campos del formulario según el tipo y operación.
    frame = None
    if tipo == "Profesor":
        frame = {
            "Ingresar": frame_profesor_ingresar,
            "Modificar": frame_profesor_modificar,
            "Eliminar": frame_profesor_eliminar,
        }.get(oper)
    elif tipo == "Alumno":
        frame = {
            "Ingresar": frame_alumno_ingresar,
            "Modificar": frame_alumno_modificar,
            "Eliminar": frame_alumno_eliminar,
        }.get(oper)
    elif tipo == "Apoderado":
        frame = {
            "Ingresar": frame_apoderado_ingresar,
            "Modificar": frame_apoderado_modificar,
            "Eliminar": frame_apoderado_eliminar,
        }.get(oper)

    if not frame:
        messagebox.showerror("Error", "Operación no reconocida.")
        return

    # Validar y obtener el RUT.
    try:
        rut_entry = frame.winfo_children()[1]  # Se asume que el campo de RUT es el segundo widget.
        rut = rut_entry.get().strip()  # Eliminar espacios en blanco antes y después.
        if not validar_rut(rut):
            messagebox.showerror("Error", f"El RUT '{rut}' ingresado no es válido. Inténtelo nuevamente.")
            return  # Bloquea la operación si el RUT es inválido.
    except IndexError:
        messagebox.showerror("Error", "No se encontró un campo para ingresar el RUT.")
        return

    # Procesar según tipo y operación.
    if tipo == "Profesor":
        if oper == "Ingresar":
            nombre = frame.winfo_children()[3].get().strip()
            anio_nacimiento = frame.winfo_children()[5].get().strip()
            especialidad = frame.winfo_children()[7].get().strip()
            if not all([nombre, anio_nacimiento, especialidad]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            if rut_duplicado(rut):
                messagebox.showerror("Error", "Este RUT ya está registrado.")
                return

            agregar_profesor(rut, nombre, int(anio_nacimiento), especialidad)
        elif oper == "Modificar":
            nuevos_datos = {
                "nombre": frame.winfo_children()[4].get().strip(),
                "anio_nacimiento": frame.winfo_children()[6].get().strip(),
                "especialidad": frame.winfo_children()[8].get().strip(),
            }
            modificar_profesor(rut, nuevos_datos)
        elif oper == "Eliminar":
            eliminar_profesor(rut)

    elif tipo == "Alumno":
        if oper == "Ingresar":
            nombre = frame.winfo_children()[3].get().strip()
            direccion = frame.winfo_children()[5].get().strip()
            anio_nacimiento = frame.winfo_children()[7].get().strip()
            posicion = frame.winfo_children()[9].get().strip()
            anio_incorporacion = frame.winfo_children()[11].get().strip()
            apoderado = frame.winfo_children()[13].get().strip()
            profesor = frame.winfo_children()[15].get().strip()
            if not all([nombre, direccion, anio_nacimiento, posicion, anio_incorporacion, profesor, apoderado]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            if rut_duplicado(rut):
                messagebox.showerror("Error", "Este RUT ya está registrado.")
                return
            agregar_alumno(rut, nombre, direccion, int(anio_nacimiento), posicion, int(anio_incorporacion), profesor, apoderado)
        elif oper == "Modificar":

            print("Total widgets:", len(frame.winfo_children()))
            for i, widget in enumerate(frame.winfo_children()):
                print(f"{i}: {type(widget)} - {str(widget)}")
            nuevos_datos = {
                "nombre": frame.winfo_children()[4].get().strip(),
                "direccion": frame.winfo_children()[6].get().strip(),
                "anio_nacimiento": frame.winfo_children()[8].get().strip(),
                "posicion": frame.winfo_children()[12].get().strip(),
                "anio_incorporacion": frame.winfo_children()[14].get().strip(),
                "profesor": frame.winfo_children()[16].get().strip(),
                "apoderado": frame.winfo_children()[17].get().strip(),
            }
            modificar_alumno(rut, nuevos_datos)
        elif oper == "Eliminar":
            eliminar_alumno(rut)

    elif tipo == "Apoderado":
        if oper == "Ingresar":
            nombre = frame.winfo_children()[3].get().strip()
            telefono = frame.winfo_children()[5].get().strip()
            if not all([nombre, telefono]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            if rut_duplicado(rut):
                messagebox.showerror("Error", "Este RUT ya está registrado.")
                return
            agregar_apoderado(rut, nombre, telefono)
        elif oper == "Modificar":
            nuevos_datos = {
                "nombre": frame.winfo_children()[4].get().strip(),
                "telefono": frame.winfo_children()[6].get().strip(),
            }
            modificar_apoderado(rut, nuevos_datos)
        elif oper == "Eliminar":
            eliminar_apoderado(rut)

    # Mostrar mensaje de éxito.
    messagebox.showinfo("Éxito", f"{tipo} {oper.lower()} exitosamente.")

def cargar_ruts_para_modificar_eliminar():
    """Carga los RUTs según el tipo de usuario para los Combobox en Modificar y Eliminar."""
    tipo = tipo_usuario.get()  # Obtiene el tipo de usuario seleccionado.
    if not tipo:  # Si no se seleccionó un tipo de usuario, termina la función.
        return

    datos = cargar()  # Carga los datos desde el archivo JSON.
    ruts = []  # Inicializa una lista para almacenar los RUTs según el tipo de usuario.

    # Selecciona los RUTs según el tipo de usuario.
    if tipo == "Profesor":
        ruts = [profesor["rut"] for profesor in datos["profesores"]]
    elif tipo == "Alumno":
        ruts = [alumno["rut"] for alumno in datos["alumnos"]]
    elif tipo == "Apoderado":
        ruts = [apoderado["rut"] for apoderado in datos["apoderados"]]

    # Actualiza los Combobox en los formularios de Modificar y Eliminar.
    for widget in [frame_profesor_modificar, frame_profesor_eliminar, 
                   frame_alumno_modificar, frame_alumno_eliminar, 
                   frame_apoderado_modificar, frame_apoderado_eliminar]:
        for child in widget.winfo_children():  # Recorre todos los widgets hijos.
            if isinstance(child, ttk.Combobox):  # Si el widget es un Combobox:
                # Obtiene la etiqueta asociada al Combobox.
                label_text = child.master.grid_slaves(row=child.grid_info()['row'], column=0)[0].cget("text")
                if "RUT" in label_text:  # Si la etiqueta indica un Combobox de RUT:
                    child.config(values=ruts)  # Actualiza los valores del Combobox con los RUTs.

# Cargar datos en los combobox
def cargar_datos_combobox():
    """Carga los nombres de profesores y apoderados en los Combobox correspondientes."""
    datos = cargar()  # Carga los datos desde el archivo JSON.
    nombres_profesores = [profesor["nombre"] for profesor in datos["profesores"]]  # Obtiene nombres de profesores.
    nombres_apoderados = [apoderado["nombre"] for apoderado in datos["apoderados"]]  # Obtiene nombres de apoderados.

    # Actualiza los Combobox en el formulario de ingreso de alumnos.
    for widget in frame_alumno_ingresar.winfo_children():  # Recorre todos los widgets hijos del frame.
        if isinstance(widget, ttk.Combobox):  # Si el widget es un Combobox:
            label_text = widget.master.grid_slaves(row=widget.grid_info()['row'], column=0)[0].cget("text")
            if label_text == "Profesor:":  # Si la etiqueta asociada indica un profesor:
                widget.config(values=nombres_profesores)  # Actualiza con los nombres de profesores.
            elif label_text == "Apoderado:":  # Si la etiqueta asociada indica un apoderado:
                widget.config(values=nombres_apoderados)  # Actualiza con los nombres de apoderados.

    # Actualiza los Combobox en el formulario de modificación de alumnos.
    for widget in frame_alumno_modificar.winfo_children():  # Similar a lo anterior, pero para modificar.
        if isinstance(widget, ttk.Combobox):
            label_text = widget.master.grid_slaves(row=widget.grid_info()['row'], column=0)[0].cget("text")
            if label_text == "Profesor:":
                widget.config(values=nombres_profesores)
            elif label_text == "Apoderado:":
                widget.config(values=nombres_apoderados)

# Actualizar el estado de los botones de operación
def actualizar_estado_operaciones(*args):
    if tipo_usuario.get():  # Si hay un tipo de usuario seleccionado
        btn_ingresar.config(state="normal")
        btn_modificar.config(state="normal")
        btn_eliminar.config(state="normal")
    else:
        btn_ingresar.config(state="disabled")
        btn_modificar.config(state="disabled")
        btn_eliminar.config(state="disabled")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Control de Usuarios - Barrabases FC")
ventana.geometry("600x650")
ventana.config(bg="#1c1f33")

# Etiqueta de título
titulo = tk.Label(ventana, text="Seleccione tipo de usuario", font=("Arial", 16, "bold"), bg="#1c1f33", fg="white")
titulo.pack(pady=10)

# Frame para selección de usuario
frame_usuario = tk.Frame(ventana, bg="#1c1f33")
frame_usuario.pack(pady=10)

# Botones de usuario
tipo_usuario = tk.StringVar()
tipo_usuario.trace_add("write", actualizar_estado_operaciones)
tipo_usuario.trace_add("write", lambda *args: cargar_ruts_para_modificar_eliminar())
btn_profesor = tk.Radiobutton(frame_usuario, text="Profesor", variable=tipo_usuario, value="Profesor", indicatoron=0, width=10, font=("Arial", 12), bg="#D1B2FF")
btn_alumno = tk.Radiobutton(frame_usuario, text="Alumno", variable=tipo_usuario, value="Alumno", indicatoron=0, width=10, font=("Arial", 12), bg="#D1B2FF")
btn_apoderado = tk.Radiobutton(frame_usuario, text="Apoderado", variable=tipo_usuario, value="Apoderado", indicatoron=0, width=10, font=("Arial", 12), bg="#D1B2FF")

btn_profesor.grid(row=0, column=0, padx=5)
btn_alumno.grid(row=0, column=1, padx=5)
btn_apoderado.grid(row=0, column=2, padx=5)

# Etiqueta de operación
titulo_operacion = tk.Label(ventana, text="Seleccione operación", font=("Arial", 16, "bold"), bg="#1c1f33", fg="white")
titulo_operacion.pack(pady=10)

# Frame para selección de operación
frame_operacion = tk.Frame(ventana, bg="#1c1f33")
frame_operacion.pack(pady=10)

# Botones de operación
operacion = tk.StringVar()
btn_ingresar = tk.Radiobutton(frame_operacion, text="Ingresar", variable=operacion, value="Ingresar", indicatoron=0, width=10, font=("Arial", 12), bg="#66B2FF", state="disabled")
btn_modificar = tk.Radiobutton(frame_operacion, text="Modificar", variable=operacion, value="Modificar", indicatoron=0, width=10, font=("Arial", 12), bg="#66B2FF", state="disabled")
btn_eliminar = tk.Radiobutton(frame_operacion, text="Eliminar", variable=operacion, value="Eliminar", indicatoron=0, width=10, font=("Arial", 12), bg="#66B2FF", state="disabled")

btn_ingresar.grid(row=0, column=0, padx=5)
btn_modificar.grid(row=0, column=1, padx=5)
btn_eliminar.grid(row=0, column=2, padx=5)

# Frame para formularios
frame_formulario = tk.Frame(ventana, bd=1, relief="solid", bg="white", padx=10, pady=10)
frame_formulario.pack(pady=10, fill="x", padx=10)

# Ocultar todos los frames al inicio
def ocultar_frames():
    for widget in frame_formulario.winfo_children():
        widget.pack_forget()

# Función para actualizar el formulario dinámicamente
def actualizar_formulario(*args):
    ocultar_frames()  # Ocultar todos los frames al inicio

    # 9 combinaciones totales

    if tipo_usuario.get() == "Alumno" and operacion.get() == "Ingresar":
        frame_alumno_ingresar.pack(fill="x", pady=5)
    elif tipo_usuario.get() == "Alumno" and operacion.get() == "Modificar":
        frame_alumno_modificar.pack(fill="x", pady=5)
    elif tipo_usuario.get() == "Alumno" and operacion.get() == "Eliminar":
        frame_alumno_eliminar.pack(fill="x", pady=5)
    elif tipo_usuario.get() == "Profesor" and operacion.get() == "Ingresar":
        frame_profesor_ingresar.pack(fill="x", pady=5)
    elif tipo_usuario.get() == "Profesor" and operacion.get() == "Modificar":
        frame_profesor_modificar.pack(fill="x", pady=5)
    elif tipo_usuario.get() == "Profesor" and operacion.get() == "Eliminar":
        frame_profesor_eliminar.pack(fill="x", pady=5)
    elif tipo_usuario.get() == "Apoderado" and operacion.get() == "Ingresar":
        frame_apoderado_ingresar.pack(fill="x", pady=5)
    elif tipo_usuario.get() == "Apoderado" and operacion.get() == "Modificar":
        frame_apoderado_modificar.pack(fill="x", pady=5)
    elif tipo_usuario.get() == "Apoderado" and operacion.get() == "Eliminar":
        frame_apoderado_eliminar.pack(fill="x", pady=5)

# Frames específicos para cada combinación

# Ingresar Alumno
frame_alumno_ingresar = tk.Frame(frame_formulario, bg="white")

tk.Label(frame_alumno_ingresar, text="RUT:", bg="white").grid(row=0, column=0, pady=5)
tk.Entry(frame_alumno_ingresar, width=25).grid(row=0, column=1, pady=5)

tk.Label(frame_alumno_ingresar, text="Nombre:", bg="white").grid(row=1, column=0, pady=5)
tk.Entry(frame_alumno_ingresar, width=25).grid(row=1, column=1, pady=5)

tk.Label(frame_alumno_ingresar, text="Dirección:", bg="white").grid(row=2, column=0, pady=5)
tk.Entry(frame_alumno_ingresar, width=25).grid(row=2, column=1, pady=5)

tk.Label(frame_alumno_ingresar, text="Año de nacimiento:", bg="white").grid(row=3, column=0, pady=5)
tk.Entry(frame_alumno_ingresar, width=25).grid(row=3, column=1, pady=5)

tk.Label(frame_alumno_ingresar, text="Posición:", bg="white").grid(row=4, column=0, pady=5)
ttk.Combobox(frame_alumno_ingresar, width=25, values=["Portero", "Defensa central", "Lateral izquierdo", "Lateral derecho",
"Carrilero", "Mediocampista defensivo", "Mediocampista central", "Mediocampista ofensivo", "Mediocampista lateral", "Extremo",
"Delantero centro", "Delantero central", "Extremo lateral", "Segundo delantero", "Polivalente"]).grid(row=4, column=1, pady=5)

tk.Label(frame_alumno_ingresar, text="Año de incorporación:", bg="white").grid(row=5, column=0, pady=5)
tk.Entry(frame_alumno_ingresar, width=25).grid(row=5, column=1, pady=5)

tk.Label(frame_alumno_ingresar, text="Apoderado:", bg="white").grid(row=6, column=0, pady=5)
ttk.Combobox(frame_alumno_ingresar, width=25).grid(row=6, column=1, pady=5)

tk.Label(frame_alumno_ingresar, text="Profesor:", bg="white").grid(row=7, column=0, pady=5)
ttk.Combobox(frame_alumno_ingresar, width=25).grid(row=7, column=1, pady=5)    

# Modificar Alumno

frame_alumno_modificar = tk.Frame(frame_formulario, bg="white")

tk.Label(frame_alumno_modificar, text="RUT del alumno a modificar:", bg="white").grid(row=0, column=0, pady=5)
combo_rut_alumno_modificar = ttk.Combobox(frame_alumno_modificar, width=25)
combo_rut_alumno_modificar.grid(row=0, column=1, pady=5)

tk.Label(frame_alumno_modificar, text="Nuevos datos", bg="white").grid(row=1, column=0, pady=5)

tk.Label(frame_alumno_modificar, text="Nombre:", bg="white").grid(row=2, column=0, pady=5)
tk.Entry(frame_alumno_modificar, width=25).grid(row=2, column=1, pady=5)

tk.Label(frame_alumno_modificar, text="Dirección:", bg="white").grid(row=3, column=0, pady=5)
tk.Entry(frame_alumno_modificar, width=25).grid(row=3, column=1, pady=5)

tk.Label(frame_alumno_modificar, text="Año de nacimiento:", bg="white").grid(row=4, column=0, pady=5)
tk.Entry(frame_alumno_modificar, width=25).grid(row=4, column=1, pady=5)

tk.Label(frame_alumno_modificar, text="Posición:", bg="white").grid(row=5, column=0, pady=5)
ttk.Combobox(frame_alumno_modificar, width=25, values=["Portero", "Defensa central", "Lateral izquierdo", "Lateral derecho",
"Carrilero", "Mediocampista defensivo", "Mediocampista central", "Mediocampista ofensivo", "Mediocampista lateral", "Extremo",
"Delantero centro", "Delantero central", "Extremo lateral", "Segundo delantero", "Polivalente"]).grid(row=5, column=1, pady=5)

tk.Label(frame_alumno_modificar, text="Año de incorporación:", bg="white").grid(row=6, column=0, pady=5)
tk.Entry(frame_alumno_modificar, width=25).grid(row=6, column=1, pady=5)

tk.Label(frame_alumno_modificar, text="Profesor:", bg="white").grid(row=7, column=0, pady=5)
ttk.Combobox(frame_alumno_modificar, width=25).grid(row=7, column=1, pady=5)

# Eliminar Alumno

frame_alumno_eliminar = tk.Frame(frame_formulario, bg="white")

tk.Label(frame_alumno_eliminar, text="RUT del alumno a eliminar:", bg="white").grid(row=0, column=0, pady=5)

combo_rut_alumno_eliminar = ttk.Combobox(frame_alumno_eliminar, width=25)
combo_rut_alumno_eliminar.grid(row=0, column=1, pady=5)
combo_rut_alumno_eliminar.bind("<<ComboboxSelected>>", actualizar_nombre_por_rut)

tk.Label(frame_alumno_eliminar, text="Nombre:", bg="white").grid(row=1, column=0, pady=5)
tk.Entry(frame_alumno_eliminar, width=25).grid(row=1, column=1, pady=5)

# Ingresar Alumno

frame_profesor_ingresar = tk.Frame(frame_formulario, bg="white")

tk.Label(frame_profesor_ingresar, text="RUT:", bg="white").grid(row=0, column=0, pady=5)
tk.Entry(frame_profesor_ingresar, width=25).grid(row=0, column=1, pady=5)

tk.Label(frame_profesor_ingresar, text="Nombre:", bg="white").grid(row=1, column=0, pady=5)
tk.Entry(frame_profesor_ingresar, width=25).grid(row=1, column=1, pady=5)

tk.Label(frame_profesor_ingresar, text="Año de nacimiento:", bg="white").grid(row=2, column=0, pady=5)
tk.Entry(frame_profesor_ingresar, width=25).grid(row=2, column=1, pady=5)

tk.Label(frame_profesor_ingresar, text="Especialidad:", bg="white").grid(row=3, column=0, pady=5)
ttk.Combobox(frame_profesor_ingresar, width=25, values=["Portero", "Defensa", "Mediocampista", "Delantero", "Preparación Física",
"Estrategia y Táctica", "Entrenamiento Técnico", "Entrenamiento Mental", "Análisis de Videos y Datos", "Formación Integral"]).grid(row=3, column=1, pady=5)

# Modificar Profesor

frame_profesor_modificar = tk.Frame(frame_formulario, bg="white")

tk.Label(frame_profesor_modificar, text="RUT del profesor a modificar:", bg="white").grid(row=0, column=0, pady=5)
combo_rut_profesor_modificar = ttk.Combobox(frame_profesor_modificar, width=25)
combo_rut_profesor_modificar.grid(row=0, column=1, pady=5)

tk.Label(frame_profesor_modificar, text="Nuevos datos", bg="white").grid(row=1, column=0, pady=5)

tk.Label(frame_profesor_modificar, text="Nombre:", bg="white").grid(row=2, column=0, pady=5)
tk.Entry(frame_profesor_modificar, width=25).grid(row=2, column=1, pady=5)

tk.Label(frame_profesor_modificar, text="Año de nacimiento:", bg="white").grid(row=3, column=0, pady=5)
tk.Entry(frame_profesor_modificar, width=25).grid(row=3, column=1, pady=5)

tk.Label(frame_profesor_modificar, text="Especialidad:", bg="white").grid(row=4, column=0, pady=5)
ttk.Combobox(frame_profesor_modificar, width=25, values=["Portero", "Defensa", "Mediocampista", "Delantero", "Preparación Física",
"Estrategia y Táctica", "Entrenamiento Técnico", "Entrenamiento Mental", "Análisis de Videos y Datos", "Formación Integral"]).grid(row=4, column=1, pady=5)

# Eliminar Profesor

frame_profesor_eliminar = tk.Frame(frame_formulario, bg="white")

tk.Label(frame_profesor_eliminar, text="RUT del profesor a eliminar:", bg="white").grid(row=0, column=0, pady=5)
combo_rut_profesor_eliminar = ttk.Combobox(frame_profesor_eliminar, width=25)
combo_rut_profesor_eliminar.grid(row=0, column=1, pady=5)
combo_rut_profesor_eliminar.bind("<<ComboboxSelected>>", actualizar_nombre_por_rut)

tk.Label(frame_profesor_eliminar, text="Nombre:", bg="white").grid(row=1, column=0, pady=5)
tk.Entry(frame_profesor_eliminar, width=25).grid(row=1, column=1, pady=5)

# Apoderado Ingresar

frame_apoderado_ingresar = tk.Frame(frame_formulario, bg="white")

tk.Label(frame_apoderado_ingresar, text="RUT:", bg="white").grid(row=0, column=0, pady=5)
tk.Entry(frame_apoderado_ingresar, width=25).grid(row=0, column=1, pady=5)

tk.Label(frame_apoderado_ingresar, text="Nombre:", bg="white").grid(row=1, column=0, pady=5)
tk.Entry(frame_apoderado_ingresar, width=25).grid(row=1, column=1, pady=5)

tk.Label(frame_apoderado_ingresar, text="Contacto:", bg="white").grid(row=2, column=0, pady=5)
tk.Entry(frame_apoderado_ingresar, width=25).grid(row=2, column=1, pady=5)

# Apoderado Modificar

frame_apoderado_modificar = tk.Frame(frame_formulario, bg="white")

tk.Label(frame_apoderado_modificar, text="RUT del apoderado a modificar:", bg="white").grid(row=0, column=0, pady=5)
combo_rut_apoderado_modificar = ttk.Combobox(frame_apoderado_modificar, width=25)
combo_rut_apoderado_modificar.grid(row=0, column=1, pady=5)

tk.Label(frame_apoderado_modificar, text="Nuevos datos", bg="white").grid(row=1, column=0, pady=5)

tk.Label(frame_apoderado_modificar, text="Nombre:", bg="white").grid(row=2, column=0, pady=5)
tk.Entry(frame_apoderado_modificar, width=25).grid(row=2, column=1, pady=5)

tk.Label(frame_apoderado_modificar, text="Contacto:", bg="white").grid(row=3, column=0, pady=5)
tk.Entry(frame_apoderado_modificar, width=25).grid(row=3, column=1, pady=5)

# Apoderado Eliminar

frame_apoderado_eliminar = tk.Frame(frame_formulario, bg="white")

tk.Label(frame_apoderado_eliminar, text="RUT del apoderado a eliminar:", bg="white").grid(row=0, column=0, pady=5)
combo_rut_apoderado_eliminar = ttk.Combobox(frame_apoderado_eliminar, width=25)
combo_rut_apoderado_eliminar.grid(row=0, column=1, pady=5)
combo_rut_apoderado_eliminar.bind("<<ComboboxSelected>>", actualizar_nombre_por_rut)

tk.Label(frame_apoderado_eliminar, text="Nombre:", bg="white").grid(row=1, column=0, pady=5)
tk.Entry(frame_apoderado_eliminar, width=25).grid(row=1, column=1, pady=5)

# Asignar eventos a las variables tipo_usuario y operacion
tipo_usuario.trace_add("write", actualizar_formulario)
operacion.trace_add("write", actualizar_formulario)

# Ocultar todos los frames al inicio
ocultar_frames()

# Botones finales
btn_confirmar = tk.Button(ventana, text="Confirmar", bg="#66CCFF", font=("Arial", 12, "bold"), command=ejecutar_operacion)
btn_confirmar.pack(pady=10)

btn_volver = tk.Button(ventana, text="Volver", bg="#66CCFF", font=("Arial", 12, "bold"), command=volver_ventana_principal)
btn_volver.pack(pady=10)

# Cargar datos iniciales
cargar_datos_combobox()
ventana.mainloop()