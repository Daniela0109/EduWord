from maestro.login_maestro import Login_Maestro
from maestro.registro_maestro import Registro_Maestro
import tkinter as tk

def abrir_login(ventana_seleccion):
    ventana_seleccion.withdraw()
    ventana_login = tk.Toplevel(ventana_seleccion)
    Login_Maestro(ventana_login, ventana_seleccion)

def abrir_registro(ventana_seleccion):
    ventana_seleccion.withdraw()
    ventana_registro = tk.Toplevel(ventana_seleccion)
    Registro_Maestro(ventana_registro, ventana_seleccion)