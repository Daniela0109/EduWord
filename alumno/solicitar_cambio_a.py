import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps: 
    cred = credentials.Certificate("db\\eduwordConfigFB.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

class Solicitar_Cambio_A:
    def __init__(self, cambio, ventana_perfil):
        self.cambio = cambio
        self.cambio.title("Solicitar Cambio")
        self.cambio.geometry("1000x700")

        self.ventana_perfil = ventana_perfil

        banner_frame = tk.Frame(self.cambio, bg="#3498db", height=100)
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

        mensaje = tk.Label(self.cambio, text="¿Está mal escrito tu nombre y/o apellido? Escribe los nuevos datos:", font=("Helvetica", 12))
        mensaje.pack()

        nombre_label = tk.Label(self.cambio, text="Nombre:", font=("Helvetica", 12))
        nombre_label.pack(pady=20)

        nuevo_nombre = tk.Entry(self.cambio,width=50)
        nuevo_nombre.pack(pady=20)

        Apellido_label = tk.Label(self.cambio, text="Apellido:", font=("Helvetica", 12))
        Apellido_label.pack(pady=20)

        nuevo_apellido = tk.Entry(self.cambio, width=50)
        nuevo_apellido.pack(pady=20)

        confirmar_cambio = tk.Button(cambio, text="Confirmar")
        confirmar_cambio.pack(pady=20)

        footer_frame = tk.Frame(self.cambio, bg="#2c3e50", height=100)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_text = "El aprendizaje es un tesoro que seguirá a su dueño a cualquier lugar. – Proverbio chino\n© 2025 EduWord. Todos los derechos reservados. Versión 1.1"
        footer_label = tk.Label(footer_frame, text=footer_text, font=("Helvetica", 12), fg="white", bg="#2c3e50", anchor="center", justify="center")
        footer_label.pack(pady=20)