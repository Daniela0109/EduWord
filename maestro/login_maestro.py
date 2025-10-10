import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, firestore
from metodos.login_me import abrir_interfaz_maestro, abrir_recuperacion_maestro
import base64  

if not firebase_admin._apps:
    cred = credentials.Certificate("db\\eduwordConfigFB.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

class Login_Maestro:
    def __init__(self, login, ventana_seleccion):
        self.login = login
        self.login.title("Inicio de Sesion Maestro")
        self.login.geometry("1000x700")

        self.ventana_seleccion = ventana_seleccion

        banner_frame = tk.Frame(self.login, bg="#3498db", height=100)
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

        label_presentacion = tk.Label(self.login, text="Iniciar sesión", font=("Comic Sans MS", 16, "bold")).pack(pady=20)
        label_correo = tk.Label(self.login, text="Correo del Maestro:", font=("Comic Sans MS", 12)).pack()
        self.entry_correo = tk.Entry(self.login, font=("Comic Sans MS", 12))
        self.entry_correo.pack(pady=5)

        label_pass = tk.Label(self.login, text="Contraseña:", font=("Comic Sans MS", 12)).pack()

        frame_contraseña = tk.Frame(self.login)
        frame_contraseña.pack(pady=5)

        self.entry_pass = tk.Entry(frame_contraseña, font=("Comic Sans MS", 12), show="*")
        self.entry_pass.pack(side="left")

        self.icono_ojo_abierto = PhotoImage(file="img/ojo_abierto.png").subsample(4, 4)
        self.icono_ojo_cerrado = PhotoImage(file="img/ojo_cerrado.png").subsample(4, 4)

        self.btn_mostrar = tk.Button(frame_contraseña, image=self.icono_ojo_cerrado, bd=0, command=self.alternar_contraseñas)
        self.btn_mostrar.pack(side="right")

        enlace_olvidaste = tk.Label(self.login, text="¿Olvidaste tu contraseña?", fg="blue", cursor="hand2")
        enlace_olvidaste.pack(pady=5)
        enlace_olvidaste.bind("<Button-1>", lambda e: abrir_recuperacion_maestro(self.login))

        btn_iniciar_sesion = tk.Button(self.login, text="Iniciar sesión", font=("Comic Sans MS", 12, "bold"), command=self.iniciar_sesion)
        btn_iniciar_sesion.pack(pady=10)

        btn_volver = tk.Button(self.login, text="Volver", font=("Comic Sans MS", 12), command=self.volver)
        btn_volver.pack(pady=10)

        footer_frame = tk.Frame(self.login, bg="#2c3e50", height=100)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_text = "El aprendizaje es un tesoro que seguirá a su dueño a cualquier lugar. – Proverbio chino\n© 2025 EduWord. Todos los derechos reservados. Versión 1.1"
        footer_label = tk.Label(footer_frame, text=footer_text, font=("Helvetica", 12), fg="white", bg="#2c3e50", anchor="center", justify="center")
        footer_label.pack(pady=20)

    def alternar_contraseñas(self):
        if self.entry_pass.cget('show') == '*':
            self.entry_pass.config(show='')
            self.btn_mostrar.config(image=self.icono_ojo_abierto)
        else:
            self.entry_pass.config(show="*")
            self.btn_mostrar.config(image=self.icono_ojo_cerrado)

    def volver(self):
        self.login.destroy()
        self.ventana_seleccion.deiconify()

    def iniciar_sesion(self):
        correo = self.entry_correo.get()
        contraseña = self.entry_pass.get()

        if not correo or not contraseña:
            messagebox.showwarning("Campos Vacíos", "Por favor ingrese su correo y contraseña.")
            return

        maestros_ref = db.collection('maestro') 
        query = maestros_ref.where('correo', '==', correo).limit(1)  
        results = query.stream()

        user_found = False
        correo_incorrecto = True

        for user in results:
            correo_incorrecto = False
            user_data = user.to_dict()
            stored_password = user_data.get("password")

            try:
                descifrada = self.descifrar_contraseña_base64(stored_password)
            except Exception as e:
                messagebox.showerror("Error", "Error al descifrar la contraseña.")
                return

            if descifrada == contraseña:
                user_found = True
                break

        if correo_incorrecto:
            messagebox.showerror("Error", "El correo electrónico ingresado no existe.")
        elif user_found:
            messagebox.showinfo("Éxito", "¡Inicio de sesión exitoso!")
            abrir_interfaz_maestro(self.login)
        else:
            messagebox.showerror("Error", "La contraseña ingresada es incorrecta.")
            
    def descifrar_contraseña_base64(self, contraseña_cifrada):
        return base64.b64decode(contraseña_cifrada).decode()