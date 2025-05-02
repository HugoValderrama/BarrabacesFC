import tkinter as tk
from tkinter import messagebox
import os
from admin import autenticar_usuario, registrar_usuario  # Importa funciones desde admin.py

# Función de autenticación
def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if autenticar_usuario(usuario, contrasena):
        messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso")
        ventana.quit()
        ventana.destroy()
        os.system("python Vistas/principal.py")
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Abrir ventana de registro
def abrir_registro():
    registro = tk.Toplevel(ventana)
    registro.title("Registro de Usuario")
    registro.geometry("400x300")
    registro.config(bg="#1c1f33")

    tk.Label(registro, text="Usuario:", bg="#1c1f33", fg="white").pack(pady=5)
    entry_nuevo_usuario = tk.Entry(registro, font=("Arial", 12), justify="center")
    entry_nuevo_usuario.pack(pady=5)

    tk.Label(registro, text="Contraseña:", bg="#1c1f33", fg="white").pack(pady=5)
    entry_nueva_contrasena = tk.Entry(registro, show="*", font=("Arial", 12), justify="center")
    entry_nueva_contrasena.pack(pady=5)

    def registrar():
        usuario = entry_nuevo_usuario.get()
        contrasena = entry_nueva_contrasena.get()

        if registrar_usuario(usuario, contrasena):
            messagebox.showinfo("Registro", "Usuario registrado exitosamente")
            registro.destroy()
        else:
            messagebox.showerror("Error", "El usuario ya existe")

    tk.Button(registro, text="Registrar", command=registrar, font=("Arial", 12), bg="white", fg="#1c1f33").pack(pady=20)

# Función para manejar marcador de posición
def on_entry_click(entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg="white")

def on_focusout(entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg="grey")

# Interfaz de inicio de sesión
ventana = tk.Tk()
ventana.title("Inicio de Sesión - Barrabases FC")
ventana.geometry("500x600")
ventana.config(bg="#1c1f33")

# Título
titulo = tk.Label(ventana, text="BARRABASES FC", font=("Arial", 24, "bold"), bg="#1c1f33", fg="white")
titulo.pack(pady=30)

# Campo usuario
entry_usuario = tk.Entry(ventana, font=("Arial", 14), width=25, justify="center")
entry_usuario.insert(0, "NOMBRE DE USUARIO")
entry_usuario.config(fg="grey", bg="#3b4fe4", relief="flat")
entry_usuario.bind("<FocusIn>", lambda event: on_entry_click(entry_usuario, "NOMBRE DE USUARIO"))
entry_usuario.bind("<FocusOut>", lambda event: on_focusout(entry_usuario, "NOMBRE DE USUARIO"))
entry_usuario.pack(pady=15)

# Campo contraseña
entry_contrasena = tk.Entry(ventana, font=("Arial", 14), width=25, justify="center")
entry_contrasena.insert(0, "CONTRASEÑA")
entry_contrasena.config(fg="grey", bg="#324f6b", relief="flat")
entry_contrasena.bind("<FocusIn>", lambda event: on_entry_click(entry_contrasena, "CONTRASEÑA"))
entry_contrasena.bind("<FocusOut>", lambda event: on_focusout(entry_contrasena, "CONTRASEÑA"))
entry_contrasena.pack(pady=15)

# Botón ingresar
boton_ingresar = tk.Button(
    ventana, text="INGRESAR", font=("Arial", 14, "bold"), command=iniciar_sesion,
    width=15, bg="white", fg="#1c1f33"
)
boton_ingresar.pack(pady=30)

# Botón registrarse
boton_registrar = tk.Button(
    ventana, text="REGISTRARSE", font=("Arial", 12), command=abrir_registro,
    width=15, bg="#3b4fe4", fg="white"
)
boton_registrar.pack()

# Ejecutar ventana
ventana.mainloop()