import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, firestore
import sys
import os
import threading
from maestro.certificado_maestro import GenerarCertificado
from maestro.validarCertificado import ValidadorCertificado

if not firebase_admin._apps: 
    cred = credentials.Certificate("db\\eduwordConfigFB.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

class Interfaz_Maestro:
    def __init__(self, inter_maestro, login):
        self.inter_maestro = inter_maestro
        self.inter_maestro.title("Interfaz Maestro")
        self.inter_maestro.geometry("1000x700")

        self.ventana_login = login

        banner_frame = tk.Frame(self.inter_maestro, bg="#3498db", height=100)
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

        label_bienvenido = tk.Label(self.inter_maestro, text=f"¡Bienvenido!", font=("Comic Sans MS", 16, "bold"), bg="lightblue").pack(pady=20)

        btn_notificaciones = tk.Button(self.inter_maestro, text="Notificaciones", font=("Comic Sans MS", 12))
        btn_notificaciones.pack(pady=5)

        btn_gestion = tk.Button(self.inter_maestro, text="Gestión de certificados", font=("Comic Sans MS", 12), command=self.abrir_gestion_certificados)
        btn_gestion.pack(pady=5)
        
        btn_validacion = tk.Button(self.inter_maestro, text="Validación de certificados", font=("Comic Sans MS", 12), command=self.abrir_validacion_certificados)
        btn_validacion.pack(pady=5)

        btn_reportes = tk.Button(self.inter_maestro, text="Reportes", font=("Comic Sans MS", 12))
        btn_reportes.pack(pady=5)

        btn_salir = tk.Button(self.inter_maestro, text="Cerrar sesión", font=("Comic Sans MS", 12), command=self.cerrar_sesion)
        btn_salir.pack(pady=10)

        footer_frame = tk.Frame(self.inter_maestro, bg="#2c3e50", height=100)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_text = "El aprendizaje es un tesoro que seguirá a su dueño a cualquier lugar. – Proverbio chino\n© 2025 EduWord. Todos los derechos reservados. Versión 1.1"
        footer_label = tk.Label(footer_frame, text=footer_text, font=("Helvetica", 12), fg="white", bg="#2c3e50", anchor="center", justify="center")
        footer_label.pack(pady=20)

    def cerrar_sesion(self):
        messagebox.showinfo("Sesión cerrada", "Tu sesión ha expirado.")

        self.inter_maestro.after(100, self.inter_maestro.destroy)
        threading.Thread(target=self.ejecutar_cargar).start()
        
    def abrir_gestion_certificados(self):
        ventana_certificados = tk.Toplevel(self.inter_maestro)
        GenerarCertificado(ventana_certificados)
        
    def abrir_validacion_certificados(self):
        ventana_validacion = tk.Toplevel(self.inter_maestro) 
        ValidadorCertificado(ventana_validacion)