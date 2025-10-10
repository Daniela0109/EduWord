import tkinter as tk
import os
import subprocess
from maestro.certificado_maestro import generar_pdf_certificado
from herramientas.lectorTexto import Lector_Texto
from db.conexionFirebase import obtener_db
db = obtener_db()

def ir_generar_certificado(splash):
    splash.withdraw()
    ventana_perfil = tk.Toplevel(splash)
    Perfil_Alumno(ventana_perfil, splash)