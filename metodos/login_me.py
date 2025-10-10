import tkinter as tk
from maestro.interfaz_maestro import Interfaz_Maestro
from alumno.interfaz_alumno import Interfaz_Alumno
from alumno.recuperacion_alumno import Recuperacion_Alumno
from maestro.recuperacion_maestro import Recuperacion_Maestro
from tkinter import messagebox
import base64
from db.conexionFirebase import obtener_db
db = obtener_db()

def abrir_interfaz_maestro(splash):
    splash.withdraw()
    ventana_interfaz_maestro = tk.Toplevel(splash)
    Interfaz_Maestro(ventana_interfaz_maestro, splash)

def abrir_interfaz_alumno(splash):
    splash.withdraw()
    ventana_interfaz_alumno = tk.Toplevel(splash)
    Interfaz_Alumno(ventana_interfaz_alumno, splash)

def abrir_recuperacion(splash):
    splash.withdraw()
    ventana_recuperacion = tk.Toplevel(splash)
    Recuperacion_Alumno(ventana_recuperacion, splash)

def abrir_recuperacion_maestro(splash):
    splash.withdraw()
    ventana_recuperacion = tk.Toplevel(splash)
    Recuperacion_Maestro(ventana_recuperacion, splash)

def descifrar_contraseña_base64(contraseña_cifrada):
    return base64.b64decode(contraseña_cifrada).decode()

def verificar_credenciales(correo, contraseña):
    usuarios_ref = db.collection('alumno')
    query = usuarios_ref.where('correo_tutor', '==', correo).stream()

    for usuario in query:
        usuario_data = usuario.to_dict()
        contraseña_cifrada = usuario_data['contraseña']
        contraseña_descifrada = descifrar_contraseña_base64(contraseña_cifrada)

        if contraseña_descifrada == contraseña:
            return True, usuario_data
        else:
            return False, None

    return False, None