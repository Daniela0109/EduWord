import tkinter as tk
import os
import subprocess
from alumno.perfil_alumno import Perfil_Alumno
from herramientas.lectorTexto import Lector_Texto
from db.conexionFirebase import obtener_db
db = obtener_db()
 
def ir_perfil_alumno(splash):
    splash.withdraw()
    ventana_perfil = tk.Toplevel(splash)
    Perfil_Alumno(ventana_perfil, splash)

def abrir_rima():
    """Abre el archivo lectorQR.py desde la carpeta herramientas."""
    lector_qr_path = os.path.join(os.path.dirname(__file__), '..', 'alumno', 'español', 'espaDos.py')
    
    if os.path.exists(lector_qr_path):
        subprocess.Popen(["python", lector_qr_path])
    else:
        print("Error: El archivo espaUno.py no se encuentra en la carpeta español.")

def abrir_adivinar_qr():
    """Abre el archivo lectorQR.py desde la carpeta herramientas."""
    lector_qr_path = os.path.join(os.path.dirname(__file__), '..', 'alumno', 'español', 'espaUno.py')
    
    if os.path.exists(lector_qr_path):
        subprocess.Popen(["python", lector_qr_path])
    else:
        print("Error: El archivo espaUno.py no se encuentra en la carpeta español.")

def abrir_memorama():
    """Abre el archivo lectorQR.py desde la carpeta herramientas."""
    lector_qr_path = os.path.join(os.path.dirname(__file__), '..', 'alumno', 'español', 'espaTres.py')
    
    if os.path.exists(lector_qr_path):
        subprocess.Popen(["python", lector_qr_path])
    else:
        print("Error: El archivo espaUno.py no se encuentra en la carpeta español.")

def abrir_lector_qr():
    """Abre el archivo lectorQR.py desde la carpeta herramientas."""
    lector_qr_path = os.path.join(os.path.dirname(__file__), '..', 'herramientas', 'lectorQR.py')
    
    if os.path.exists(lector_qr_path):
        subprocess.Popen(["python", lector_qr_path])
    else:
        print("Error: El archivo lectorQR.py no se encuentra en la carpeta herramientas.")

def abrir_lector_texto(splash):
    splash.withdraw()
    ventana_lector = tk.Toplevel(splash)
    Lector_Texto(ventana_lector, splash)
