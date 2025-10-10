import tkinter as tk
from functools import partial
from pantallas.seleccion_usuario import Seleccion_Usuario

def cargar_proceso(barra_progreso, progreso_label, splash):
    if barra_progreso['value'] < 100:
        barra_progreso['value'] += 1
        progreso_label.config(text=f"Cargando... {int(barra_progreso['value'])}%")
        splash.after(30, partial(cargar_proceso, barra_progreso, progreso_label, splash))
    else:
        splash.after(500, partial(mostrar_seleccion_usuario, splash))

def mostrar_seleccion_usuario(splash):
    splash.withdraw()
    ventana_seleccion_usuario = tk.Toplevel(splash)
    Seleccion_Usuario(ventana_seleccion_usuario)