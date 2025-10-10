import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from metodos.carga_me import cargar_proceso
from functools import partial
import os

class Carga:
    def __init__(self, carga):
        self.carga = carga
        self.carga.title("EduWord")
        self.carga.geometry("1000x700")
        self.carga.resizable(False, False)

        try:
            imagen = Image.open("img/logo.png")
            imagen = imagen.resize((1000,700))
            imagen_fondo = ImageTk.PhotoImage(imagen)

            label_fondo = tk.Label(self.carga, image=imagen_fondo)
            label_fondo.place(relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")

        barra_progreso = ttk.Progressbar(self.carga, orient="horizontal", length=500, mode="determinate")
        barra_progreso.place(relx=0.5, rely=0.75, anchor="center")

        progreso_label = tk.Label(self.carga, text="Cargando... 0%", font=("Arial", 12))
        progreso_label.place(relx=0.5, rely=0.85, anchor="center")

        self.carga.after(100, partial(cargar_proceso, barra_progreso, progreso_label, self.carga))

        





