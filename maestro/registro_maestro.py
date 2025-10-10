import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import base64
import firebase_admin
from firebase_admin import credentials, firestore
from metodos.registro_me import ir_loguin_maestro
from metodos.firmaDigital import generar_claves
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import ssl
import os

if not firebase_admin._apps:
    cred = credentials.Certificate("db\\eduwordConfigFB.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def cifrar_contraseña_base64(contraseña):
    return base64.b64encode(contraseña.encode()).decode()

def enviar_claves_por_correo(correo_destino, clave_privada, clave_publica):
                        smtp_server = "smtp.gmail.com"
                        smtp_port = 465
                        remitente = "daniela.dp600@gmail.com"
                        contrasena = "ezlu kqad cqhl xxkj"
                        with open("clave_privada.pem", "wb") as f:
                            f.write(clave_privada)

                        with open("clave_publica.pem", "wb") as f:
                            f.write(clave_publica)

                        msg = MIMEMultipart()
                        msg["From"] = remitente
                        msg["To"] = correo_destino
                        msg["Subject"] = "Tus claves digitales - EduWord"

                        cuerpo_mensaje = f"""Hola,

                    Gracias por registrarte en EduWord. A continuación, te enviamos tus claves digitales personales.

                    🔐 Clave PRIVADA (guárdala en un lugar seguro, no la compartas):
                    {clave_privada.decode()}

                    🔓 Clave PÚBLICA (puedes compartirla si es necesario):
                    {clave_publica.decode()}

                    Saludos,
                    Equipo EduWord
                    """
                        msg.attach(MIMEText(cuerpo_mensaje, "plain", "utf-8"))
                        
                        for archivo in ["clave_privada.pem", "clave_publica.pem"]:
                            with open(archivo, "rb") as f:
                                parte = MIMEBase("application", "octet-stream")
                                parte.set_payload(f.read())
                                encoders.encode_base64(parte)
                                parte.add_header("Content-Disposition", f"attachment; filename={archivo}")
                                msg.attach(parte)

                        context = ssl.create_default_context()
                        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                            server.login(remitente, contrasena)
                            server.sendmail(remitente, correo_destino, msg.as_string())
                            
                        os.remove("clave_privada.pem")
                        os.remove("clave_publica.pem")

class Registro_Maestro:
    def __init__(self, registro, ventana_seleccion):
        self.registro = registro
        self.registro.title("Registro de Usuario Maestro")
        self.registro.geometry("1000x700")

        self.ventana_seleccion = ventana_seleccion

        banner_frame = tk.Frame(self.registro, bg="#3498db", height=100)
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

        main_frame = tk.Frame(self.registro)
        main_frame.pack(fill="both", expand=True)

        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill="both", expand=True, pady=20)

        canvas = tk.Canvas(form_frame)
        scrollbar = tk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollbar_frame = tk.Frame(canvas)

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=scrollbar_frame, anchor="nw")

        scrollbar_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig("all", width=e.width))

        label_registro = tk.Label(scrollbar_frame, text="Registro", font=("Comic Sans MS", 16, "bold")).pack(pady=10)

        label_nombre = tk.Label(scrollbar_frame, text="Nombre:", font=("Comic Sans MS", 12)).pack()
        entry_nombre = tk.Entry(scrollbar_frame, font=("Comic Sans MS", 12))
        entry_nombre.pack(pady=5)

        label_Apellido = tk.Label(scrollbar_frame, text="Apellido:", font=("Comic Sans MS", 12)).pack()
        entry_apellido = tk.Entry(scrollbar_frame, font=("Comic Sans MS", 12))
        entry_apellido.pack(pady=5)

        label_correo = tk.Label(scrollbar_frame, text="Correo:", font=("Comic Sans MS", 12)).pack()
        entry_correo = tk.Entry(scrollbar_frame, font=("Comic Sans MS", 12))
        entry_correo.pack(pady=5)

        label_contraseña = tk.Label(scrollbar_frame, text="Contraseña:", font=("Comic Sans MS", 12)).pack()
        entry_password_maestro = tk.Entry(scrollbar_frame, font=("Comic Sans MS", 12), show="*")
        entry_password_maestro.pack(pady=5)

        label_contraseña_confirm = tk.Label(scrollbar_frame, text="Confirmar contraseña:", font=("Comic Sans MS", 12)).pack()
        entry_password_confirmar = tk.Entry(scrollbar_frame, font=("Comic Sans MS", 12), show="*")
        entry_password_confirmar.pack(pady=5)

        label_telefono = tk.Label(scrollbar_frame, text="Teléfono:", font=("Comic Sans MS", 12)).pack()
        entry_telefono_maestro = tk.Entry(scrollbar_frame, font=("Comic Sans MS", 12))
        entry_telefono_maestro.pack(pady=5)

        label_asignatura = tk.Label(scrollbar_frame, text="Asignatura:", font=("Comic Sans MS", 12)).pack()
        asignatura_options = ["Español", "Matemáticas", "Inglés"]
        asignatura_var = tk.StringVar(scrollbar_frame)
        asignatura_var.set(asignatura_options[0])
        asignatura_menu = tk.OptionMenu(scrollbar_frame, asignatura_var, *asignatura_options)
        asignatura_menu.pack(pady=5)

        def registrar_maestro():
            nombre = entry_nombre.get()
            apellido = entry_apellido.get()
            correo = entry_correo.get()
            password = entry_password_maestro.get()
            telefono = entry_telefono_maestro.get()
            asignatura = asignatura_var.get()

            if nombre and apellido and correo and password and telefono and asignatura:
                password_cifrada = cifrar_contraseña_base64(password)

                try:
                    clave_privada, clave_publica = generar_claves()

                    clave_publica_texto = clave_publica.decode("utf-8") 

                    maestro_ref = db.collection("maestro").document(correo)
                    maestro_ref.set({
                        "nombre": nombre,
                        "apellido": apellido,
                        "correo": correo,
                        "password": password_cifrada,  
                        "telefono": telefono,
                        "asignatura": asignatura,
                        "clave_publica": clave_publica_texto 
                    })

                    try:

                        enviar_claves_por_correo(correo, clave_privada, clave_publica)
                    except Exception as e:
                        messagebox.showwarning("Aviso", f"Registro completado, pero no se pudo enviar el correo: {e}")

                    messagebox.showinfo("Éxito", "¡Registro exitoso!")
                    ir_loguin_maestro(self.registro, self.ventana_seleccion)

                except Exception as e:
                    messagebox.showerror("Error", f"Hubo un error al registrar: {e}")
            else:
                messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")

        btn_registrar = tk.Button(scrollbar_frame, text="Registrarse", font=("Comic Sans MS", 12, "bold"), command=registrar_maestro)
        btn_registrar.pack(pady=10)

        btn_volver = tk.Button(scrollbar_frame, text="Volver", font=("Comic Sans MS", 12), command=self.volver)
        btn_volver.pack(pady=5)

        scrollbar_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        footer_frame = tk.Frame(self.registro, bg="#2c3e50", height=100)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_text = "El aprendizaje es un tesoro que seguirá a su dueño a cualquier lugar. – Proverbio chino\n© 2025 EduWord. Todos los derechos reservados. Versión 1.1"
        footer_label = tk.Label(footer_frame, text=footer_text, font=("Helvetica", 12), fg="white", bg="#2c3e50", anchor="center", justify="center")
        footer_label.pack(pady=20)

    def volver(self):
        self.registro.destroy()
        self.ventana_seleccion.deiconify()