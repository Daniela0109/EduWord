import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk

from metodos.select_user_me import mostrar_ayuda, acerca_de, crear_mision

from alumno.seleccion_alumno import Seleccion_Alumno
from maestro.seleccion_maestro import Seleccion_Maestro

class Seleccion_Usuario:
    def __init__(self, select):
        self.seleccionar = select
        self.seleccionar.title("Seleccionar Usuario")
        self.seleccionar.geometry("1000x700")

        banner_frame = tk.Frame(self.seleccionar, bg="#3498db", height=100)
        banner_frame.pack(fill=tk.X)

        try:
            imagen_banner = Image.open("img/logo.png")
            imagen_banner = imagen_banner.resize((80,80))
            logo = ImageTk.PhotoImage(imagen_banner)
        except FileNotFoundError:
            print("Error: El archivo de la imagen no fue encontrado")
            logo = None

        if logo:
            logo_label = tk.Label(banner_frame, image=logo, bg="#3498db")
            logo_label.image = logo
            logo_label.grid(row=0, column=0, padx=10, pady=10)

        titulo_label = tk.Label(banner_frame, text="EduWord", font=("Helvetica", 30, "bold"), fg="white", bg="#3498db")
        titulo_label.grid(row=0, column=1, padx=20, pady=10)

        navbar_frame = tk.Frame(self.seleccionar)
        navbar_frame.pack(pady=10, fill="x")

        boton_inicio = ttk.Button(navbar_frame, text="Inicio", command=self.mostrar_inicio).pack(side="left",padx=5)
        boton_mision = ttk.Button(navbar_frame, text="Mision", command=lambda:crear_mision(self.contenido_frame)).pack(side="left",padx=5)
        boton_acerca = ttk.Button(navbar_frame, text="Acerca De", command=lambda:acerca_de(self.contenido_frame)).pack(side="left",padx=5)
        boton_ayuda = ttk.Button(navbar_frame, text="Ayuda", command=lambda:mostrar_ayuda(self.contenido_frame)).pack(side="left",padx=5)

        self.contenido_frame = tk.Frame(self.seleccionar)
        self.contenido_frame.pack(fill="both", expand=True)

        self.mostrar_inicio()

        footer_frame = tk.Frame(self.seleccionar, bg="#2c3e50", height=100)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_text = "El aprendizaje es un tesoro que seguirá a su dueño a cualquier lugar. – Proverbio chino\n© 2025 EduWord. Todos los derechos reservados. Versión 1.1"
        footer_label = tk.Label(footer_frame, text=footer_text, font=("Helvetica", 12), fg="white", bg="#2c3e50", anchor="center", justify="center")
        footer_label.pack(pady=20)

    def mostrar_seleccion_alumno(self):
        self.seleccionar.withdraw()
        ventana_alumno = tk.Toplevel(self.seleccionar)
        Seleccion_Alumno(ventana_alumno, self.seleccionar)

    def mostrar_seleccion_maestro(self):
        self.seleccionar.withdraw()
        ventana_maestro = tk.Toplevel(self.seleccionar)
        Seleccion_Maestro(ventana_maestro, self.seleccionar)
        

    def mostrar_inicio(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()

        label = tk.Label(self.contenido_frame, text="¡Bienvenido a EduWord!", font=("Arial", 18))
        label.pack()

        mensaje_label = tk.Label(self.contenido_frame, text='"Selecciona tu rol para comenzar"', font=("Arial", 14))
        mensaje_label.pack(pady=10)

        boton_alumno = ttk.Button(self.contenido_frame, text="Alumno", command=self.mostrar_seleccion_alumno)
        boton_alumno.pack(pady=5)

        boton_maestro = ttk.Button(self.contenido_frame, text="Maestro", command=self.mostrar_seleccion_maestro)
        boton_maestro.pack(pady=5)



    









