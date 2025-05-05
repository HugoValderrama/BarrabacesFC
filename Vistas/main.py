import subprocess
import os

# Ruta al archivo login.py (ajústala si está en otra carpeta)
ruta_login = "login.py"

# Verificar que login.py exista
if os.path.exists("Vistas/login.py"):
    subprocess.run(["python", "Vistas/login.py"])
else:
    print("Error: No se encontró el archivo 'login.py'.")
