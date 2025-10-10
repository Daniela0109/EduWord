import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk

from metodos.select_mas_me import abrir_login, abrir_registro

class Seleccion_Maestro:
    def __init__(self, maestro_select, ventana_user):
        self.maestro_select = maestro_select
        self.maestro_select.title("Seleccionar Accion")
        self.maestro_select.geometry("1000x700")

        self.ventana_user = ventana_user

        banner_frame = tk.Frame(self.maestro_select, bg="#3498db", height=100)
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

        label = tk.Label(self.maestro_select, text="¿Qué deseas hacer?", font=("Arial", 16))
        label.pack(pady=20)

        btn_login = ttk.Button(self.maestro_select, text="Iniciar Sesión", command=lambda:abrir_login(self.maestro_select))
        btn_login.pack(pady=10)

        btn_registro = ttk.Button(self.maestro_select, text="Registrarse", command=lambda:abrir_registro(self.maestro_select))
        btn_registro.pack(pady=10)

        btn_volver = tk.Button(self.maestro_select, text="Volver", font=("Comic Sans MS", 12), command=self.volver)
        btn_volver.pack(pady=10)

        footer_frame = tk.Frame(self.maestro_select, bg="#2c3e50", height=100)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_text = "El aprendizaje es un tesoro que seguirá a su dueño a cualquier lugar. – Proverbio chino\n© 2025 EduWord. Todos los derechos reservados. Versión 1.1"
        footer_label = tk.Label(footer_frame, text=footer_text, font=("Helvetica", 12), fg="white", bg="#2c3e50", anchor="center", justify="center")
        footer_label.pack(pady=20)

    def volver(self):
        self.maestro_select.destroy()
        self.ventana_user.deiconify()

        

