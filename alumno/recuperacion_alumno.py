import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import firebase_admin
import base64
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import messagebox
from db.conexionFirebase import obtener_db
db = obtener_db()

def enviar_correo(correo_destino, asunto, mensaje):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    remitente = "daniela.dp600@gmail.com"
    contrasena = "ezlu kqad cqhl xxkj"

    msg = MIMEMultipart()
    msg["From"] = remitente
    msg["To"] = correo_destino
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje, "plain", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(remitente, contrasena)
        server.sendmail(remitente, correo_destino, msg.as_string())

def descifrar_contraseña_base64(contraseña_cifrada):
    return base64.b64decode(contraseña_cifrada).decode()

class Recuperacion_Alumno:
    def __init__(self, recuperacion, ventana_loguin):
        self.recuperacion = recuperacion
        self.recuperacion.title("Recuperacion de Contraseña Alumno")
        self.recuperacion.geometry("1000x700")

        self.ventana_loguin = ventana_loguin

        banner_frame = tk.Frame(self.recuperacion, bg="#3498db", height=100)
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

        label_presentacion = tk.Label(self.recuperacion, text="Recuperacion de Contraseña", font=("Comic Sans MS", 16, "bold")).pack(pady=20)

        label_correo = tk.Label(self.recuperacion, text="Correo del tutor:", font=("Comic Sans MS", 12)).pack()

        self.entry_correo = tk.Entry(self.recuperacion, font=("Comic Sans MS", 12))
        self.entry_correo.pack(pady=5)

        btn_recuperacion = tk.Button(self.recuperacion, text="Iniciar recuperación", font=("Comic Sans MS", 12, "bold"), command=self.iniciar_recuperacion)
        btn_recuperacion.pack(pady=10)
        
        btn_volver = tk.Button(self.recuperacion, text="Volver", font=("Comic Sans MS", 12), command=self.volver)
        btn_volver.pack(pady=10)

        footer_frame = tk.Frame(self.recuperacion, bg="#2c3e50", height=100)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_text = "El aprendizaje es un tesoro que seguirá a su dueño a cualquier lugar. – Proverbio chino\n© 2025 EduWord. Todos los derechos reservados. Versión 1.1"
        footer_label = tk.Label(footer_frame, text=footer_text, font=("Helvetica", 12), fg="white", bg="#2c3e50", anchor="center", justify="center")
        footer_label.pack(pady=20)

    def iniciar_recuperacion(self):
        correo = self.entry_correo.get().strip()

        if not correo:
            messagebox.showwarning("Campo vacío", "Por favor, ingresa el correo del tutor.")
            return

        try:
            query = db.collection('alumno').where('correo_tutor', '==', correo).limit(1)
            results = query.get()

            if results:
                alumno = results[0].to_dict()
                contraseña_cifrada = alumno.get('contraseña')

                if contraseña_cifrada:
                    contraseña_descifrada = descifrar_contraseña_base64(contraseña_cifrada)
                    mensaje = f"Hola,\n\nTu contraseña recuperada es: {contraseña_descifrada}\n\nSaludos,\nEquipo de EduWord"
                    enviar_correo(correo, "Recuperación de Contraseña", mensaje)
                    messagebox.showinfo("Correo enviado", "La contraseña ha sido enviada exitosamente al correo del tutor.")
                else:
                    messagebox.showwarning("Sin contraseña", "El usuario no tiene una contraseña registrada.")
            else:
                messagebox.showerror("Correo no encontrado", "No se encontró un alumno con ese correo.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al recuperar los datos: {e}")
            print(f"Error al recuperar datos: {e}")
            
    def volver(self):
        self.recuperacion.destroy()
        self.ventana_loguin.deiconify()