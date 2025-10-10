from alumno.login_alumno import Login_Alumno
from alumno.registro_alumno import Registro_Alumno
import tkinter as tk

def abrir_login(ventana_seleccion):
    ventana_seleccion.withdraw()
    ventana_login = tk.Toplevel(ventana_seleccion)
    Login_Alumno(ventana_login, ventana_seleccion)

def abrir_registro(ventana_seleccion):
    ventana_seleccion.withdraw()
    ventana_registro = tk.Toplevel(ventana_seleccion)
    Registro_Alumno(ventana_registro, ventana_seleccion)
