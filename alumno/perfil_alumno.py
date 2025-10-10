import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from metodos.perfil_me import cargar_imagenes, ir_solicitar_cambio_alumno
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps: 
    cred = credentials.Certificate("db\\eduwordConfigFB.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

class Perfil_Alumno:
    def __init__(self, perfil, ventana_interfaz):
        self.perfil = perfil
        self.perfil.title("Perfil del Alumno")
        self.perfil.geometry("1000x800")

        self.ventana_interfaz = ventana_interfaz

        main_container = tk.Frame(self.perfil)
        main_container.pack(fill="both", expand=True)

        banner_frame = tk.Frame(main_container, bg="#3498db", height=100)
        banner_frame.pack(fill=tk.X, side="top")

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

        content_frame = tk.Frame(main_container)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.imagenes_perfil = cargar_imagenes()
        
        if self.imagenes_perfil:
            self.imagen_actual = 0
            self.imagenes_redimensionadas = []
            
            for img in self.imagenes_perfil:
                img_redim = img.subsample(4, 4) 
                self.imagenes_redimensionadas.append(img_redim)

            img_controls_frame = tk.Frame(content_frame)
            img_controls_frame.pack(pady=20)

            self.imagen_label = tk.Label(img_controls_frame, image=self.imagenes_redimensionadas[self.imagen_actual])
            self.imagen_label.pack()

            controls_frame = tk.Frame(img_controls_frame)
            controls_frame.pack(pady=10)

            try:
                icono_izquierda = Image.open("img/iconIzquierda.png").resize((30,30))
                self.icono_izquierda = ImageTk.PhotoImage(icono_izquierda)
                
                icono_derecha = Image.open("img/iconDerecha.png").resize((30,30))
                self.icono_derecha = ImageTk.PhotoImage(icono_derecha)
            except Exception as e:
                print(f"Error cargando iconos: {str(e)}")
                self.icono_izquierda = None
                self.icono_derecha = None

            if self.icono_izquierda and self.icono_derecha:
                tk.Button(controls_frame, image=self.icono_izquierda, command=lambda: self.mover_imagen("izquierda")).pack(side="left", padx=20)
                tk.Button(controls_frame, image=self.icono_derecha, command=lambda: self.mover_imagen("derecha")).pack(side="right", padx=20)
        else:
            tk.Label(content_frame, text="No hay imágenes de perfil disponibles.").pack()

        info_frame = tk.Frame(content_frame)
        info_frame.pack(pady=20)

        nombre_label = tk.Label(info_frame, text="Nombre:", font=("Helvetica", 12))
        nombre_label.pack()

        apellido_label = tk.Label(info_frame, text="Apellido:", font=("Helvetica", 12))
        apellido_label.pack()

        solicitar_button = tk.Button(info_frame, text="Solicitar Cambio", font=("Helvetica", 12), command=lambda:ir_solicitar_cambio_alumno(self.perfil))
        solicitar_button.pack(pady=10)

        boton_volver = tk.Button(info_frame, text="Volver", font=("Helvetica", 12), command=self.volver)
        boton_volver.pack(padx=10)

        footer_frame = tk.Frame(main_container, bg="#2c3e50", height=100)
        footer_frame.pack(side="bottom", fill=tk.X, expand=False)

        footer_text = "El aprendizaje es un tesoro que seguirá a su dueño a cualquier lugar. – Proverbio chino\n© 2025 EduWord. Todos los derechos reservados. Versión 1.1"
        footer_label = tk.Label(footer_frame, text=footer_text, font=("Helvetica", 12), fg="white", bg="#2c3e50", anchor="center", justify="center")
        footer_label.pack(pady=10)


    def mover_imagen(self, direccion):
        if direccion == "izquierda":
            self.imagen_actual = (self.imagen_actual - 1) % len(self.imagenes_redimensionadas)
        else:
            self.imagen_actual = (self.imagen_actual + 1) % len(self.imagenes_redimensionadas)
        
        self.imagen_label.config(image=self.imagenes_redimensionadas[self.imagen_actual])
        self.imagen_label.image = self.imagenes_redimensionadas[self.imagen_actual]

    def volver(self):
        self.perfil.destroy()
        self.ventana_interfaz.deiconify()
