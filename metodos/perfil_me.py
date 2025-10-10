import tkinter as tk
from tkinter import PhotoImage
import os
from alumno.solicitar_cambio_a import Solicitar_Cambio_A

def cargar_imagenes():
    imagenes = []
    ruta_perfil = "img/perfil"

    try:
        archivos = [f for f in os.listdir(ruta_perfil) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        
        for archivo in archivos:
            try:
                img = PhotoImage(file=os.path.join(ruta_perfil, archivo))
                imagenes.append(img)
            except Exception as e:
                print(f"Error cargando {archivo}: {str(e)}")
                
        return imagenes if imagenes else None
        
    except FileNotFoundError:
        print(f"Error: No se encontró la carpeta {ruta_perfil}")
        return None
    
def ir_solicitar_cambio_alumno(splash):
    splash.withdraw()
    ventana_cambio = tk.Toplevel(splash)
    Solicitar_Cambio_A(ventana_cambio, splash)
    
