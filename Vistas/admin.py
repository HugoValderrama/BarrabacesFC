import json
import re
import hashlib

JSON = "Vistas/data.json"

def hash_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

def obtener_usuarios():
    datos = cargar()
    return datos.get("usuarios", {})

def contrasena_segura(contrasena):
    if len(contrasena) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    if not re.search(r"[A-Z]", contrasena):
        return False, "Debe contener al menos una letra mayúscula"
    if not re.search(r"[a-z]", contrasena):
        return False, "Debe contener al menos una letra minúscula"
    if not re.search(r"\d", contrasena):
        return False, "Debe contener al menos un número"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena):
        return False, "Debe contener al menos un símbolo"
    return True, ""

def registrar_usuario(usuario, contrasena):
    datos = cargar()
    if "usuarios" not in datos:
        datos["usuarios"] = {}

    if usuario in datos["usuarios"]:
        return False

    datos["usuarios"][usuario] = hash_contrasena(contrasena)
    guardar(datos)
    return True

def autenticar_usuario(usuario, contrasena):
    usuarios = obtener_usuarios()
    return usuarios.get(usuario) == hash_contrasena(contrasena)


def cargar():
    try:
        with open(JSON, "r", encoding="utf-8") as archivo:  # Especificar la codificación
            return json.load(archivo)
    except FileNotFoundError:
        return {"profesores": [], "alumnos": [], "apoderados": [], "goles": []}

# Función para guardar datos en el archivo JSON
def guardar(datos):
    with open(JSON, "w") as archivo:
        json.dump(datos, archivo, indent=4)  # Guardar los datos con formato legible

# Funciones - Profesor

def agregar_profesor(rut, nombre, anio_nacimiento, especialidad):
    datos = cargar()
    nuevo_profesor = {"rut": rut, "nombre": nombre, "anio_nacimiento": anio_nacimiento, "especialidad": especialidad}
    datos["profesores"].append(nuevo_profesor)  # Añadir al listado de profesores
    guardar(datos)

def modificar_profesor(rut, nuevos_datos):
    datos = cargar()
    for profesor in datos["profesores"]:
        if profesor["rut"] == rut:  # Buscar el profesor por RUT
            profesor.update(nuevos_datos)  # Actualizar los datos
    guardar(datos)

def eliminar_profesor(rut):
    datos = cargar()
    # Crear una nueva lista excluyendo al profesor con el RUT indicado
    datos["profesores"] = [prof for prof in datos["profesores"] if prof["rut"] != rut]
    guardar(datos)

# Funciones - Apoderado

def agregar_apoderado(rut, nombre, telefono):
    datos = cargar()
    nuevo_apoderado = {"rut": rut, "nombre": nombre, "telefono": telefono}
    datos["apoderados"].append(nuevo_apoderado)  # Añadir al listado de apoderados
    guardar(datos)

def modificar_apoderado(rut, nuevos_datos):
    datos = cargar()
    for apoderado in datos["apoderados"]:
        if apoderado["rut"] == rut:  # Buscar apoderado por RUT
            apoderado.update(nuevos_datos)  # Actualizar datos
    guardar(datos)

def eliminar_apoderado(rut):
    datos = cargar()
    # Crear una nueva lista excluyendo al apoderado con el RUT indicado
    datos["apoderados"] = [apod for apod in datos["apoderados"] if apod["rut"] != rut]
    guardar(datos)

# Funciones - Alumno

def agregar_alumno(rut, nombre, direccion, anio_nacimiento, posicion, año_incorporacion, profesor, apoderado):
    datos = cargar()
    nuevo_alumno = {
        "rut": rut, "nombre": nombre, "direccion": direccion,
        "anio_nacimiento": anio_nacimiento, "posicion": posicion,
        "año_incorporacion": año_incorporacion, "profesor": profesor, "apoderado": apoderado
    }
    datos["alumnos"].append(nuevo_alumno)  # Añadir al listado de alumnos
    guardar(datos)

def modificar_alumno(rut, nuevos_datos):
    datos = cargar()
    for alumno in datos["alumnos"]:
        if alumno["rut"] == rut:  # Buscar alumno por RUT
            alumno.update(nuevos_datos)  # Actualizar datos
    guardar(datos)

def eliminar_alumno(rut):
    datos = cargar()
    # Crear una nueva lista excluyendo al alumno con el RUT indicado
    datos["alumnos"] = [alum for alum in datos["alumnos"] if alum["rut"] != rut]
    guardar(datos)

# Generar un listado de alumnos atendidos por un profesor específico
def listado_alum(nombre_profesor):
    datos = cargar()
    # Filtrar alumnos cuyo profesor coincida con el nombre indicado
    alumnos = [alumno for alumno in datos["alumnos"] if alumno["profesor"] == nombre_profesor]
    return alumnos

# Obtener el contacto de un apoderado a partir del RUT de un alumno
def contacto_apoderado(rut_alumno):
    datos = cargar()
    alumno_encontrado = None
    for alumno in datos["alumnos"]:
        if alumno["rut"] == rut_alumno:  # Buscar alumno por RUT
            alumno_encontrado = alumno
            break
    
    if alumno_encontrado is not None:
        # Buscar el apoderado correspondiente al alumno
        for apoderado in datos["apoderados"]:
            if apoderado["rut"] == alumno_encontrado["apoderado"]:
                return {"nombre": apoderado["nombre"], "telefono": apoderado["num_telefono"]}
    
    return None  # Retorna None si no se encuentra el apoderado

# Generar un ranking de goleadores en un mes específico

def ranking_goleadores(mes, año, n):
    datos = cargar()
    
    # Filtrar los goles según el mes y el año
    goles_mes = []
    for gol in datos["goles"]:
        fecha = gol["fecha"]
        if fecha.startswith(f"{año}-{mes:02d}"):
            goles_mes.append(gol)
    
    # Contar los goles por alumno
    ranking = {}
    for gol in goles_mes:
        rut_alumno = gol["rut_alumno"]
        if rut_alumno in ranking:
            ranking[rut_alumno] += gol["cantidad_goles"]
        else:
            ranking[rut_alumno] = gol["cantidad_goles"]
    
    # Ordenar los alumnos por cantidad de goles
    ranking_ordenado = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    top_n = ranking_ordenado[:n]  # Tomar los n mejores
    
    # Crear el resultado con los nombres de los alumnos
    resultado = []
    for rut, goles in top_n:
        nombre_alumno = None
        for alumno in datos["alumnos"]:
            if alumno["rut"] == rut:
                nombre_alumno = alumno["nombre"]
                break
        
        if nombre_alumno is None:
            nombre_alumno = rut  # Mostrar el RUT si no se encuentra el nombre
        
        resultado.append((nombre_alumno, goles))
    
    return resultado