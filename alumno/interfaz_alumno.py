import tkinter as tk
from tkinter import messagebox, Menu
from PIL import Image, ImageTk
import subprocess
import threading
from metodos.interfaz_me import ir_perfil_alumno, abrir_rima, abrir_adivinar_qr, abrir_memorama, abrir_lector_texto, abrir_lector_qr
from metodos.sesiones import Session

temporizador = None 

class Interfaz_Alumno:
    def __init__(self, inter_alumno, ventana_login):
        self.inter_alumno = inter_alumno
        self.inter_alumno.title("Interfaz Alumno")
        self.inter_alumno.geometry("1000x700")
        self.ventana_login = ventana_login

        self.usuario_actual = Session.obtener_usuario()
        nombre_usuario = self.usuario_actual["nombre"] if self.usuario_actual else "Usuario"

        banner_frame = tk.Frame(self.inter_alumno, bg="#3498db", height=100)
        banner_frame.pack(fill=tk.X)

        try:
            imagen_banner = Image.open("img/logo.png").resize((80, 80))
            self.logo = ImageTk.PhotoImage(imagen_banner)
        except FileNotFoundError:
            print("Error: El archivo de la imagen no fue encontrado")
            self.logo = None

        if self.logo:
            logo_label = tk.Label(banner_frame, image=self.logo, bg="#3498db")
            logo_label.image = self.logo
            logo_label.grid(row=0, column=0, padx=10, pady=10)

        titulo_label = tk.Label(banner_frame, text="EduWord", font=("Helvetica", 30, "bold"), fg="white", bg="#3498db")
        titulo_label.grid(row=0, column=1, padx=20, pady=10)

        menu_bar = Menu(self.inter_alumno)
        
        categorias_menu = Menu(menu_bar, tearoff=0)
        categorias_menu.add_command(label="Rima", command=abrir_rima)
        categorias_menu.add_command(label="Adivina la Palabra", command=abrir_adivinar_qr)
        categorias_menu.add_command(label="Memorama", command=abrir_memorama)
        menu_bar.add_cascade(label="Categorias", menu=categorias_menu)

        terminos_menu = Menu(menu_bar, tearoff=0)
        terminos_menu.add_cascade(label="Términos y Uso de Software")
        terminos_menu.add_command(label="Acuerdo de confidencialidad")
        terminos_menu.add_command(label="Aviso de privacidad")
        menu_bar.add_cascade(label="Términos Legales", menu=terminos_menu)

        herramientas_menu = Menu(menu_bar, tearoff=0)
        herramientas_menu.add_command(label="Lector QR", command=abrir_lector_qr)
        herramientas_menu.add_command(label="Lector de texto", command=lambda: abrir_lector_texto(self.inter_alumno))
        menu_bar.add_cascade(label="Herramientas", menu=herramientas_menu)

        self.inter_alumno.config(menu=menu_bar)

        self.label_bienvenida = tk.Label(self.inter_alumno, text=f"¡Bienvenido, {nombre_usuario}!", font=("Comic Sans MS", 16, "bold"), bg="lightblue")
        self.label_bienvenida.pack(pady=20)

        btn_perfil = tk.Button(self.inter_alumno, text="Perfil del Alumno", font=("Comic Sans MS", 12), command=lambda: ir_perfil_alumno(self.inter_alumno))
        btn_perfil.pack(pady=10)

        btn_salir = tk.Button(self.inter_alumno, text="Cerrar sesión", font=("Comic Sans MS", 12), command=self.cerrar_sesion)
        btn_salir.pack(pady=10)

        footer_frame = tk.Frame(self.inter_alumno, bg="#2c3e50", height=100)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_text = "El aprendizaje es un tesoro que seguirá a su dueño a cualquier lugar. – Proverbio chino\n© 2025 EduWord. Todos los derechos reservados. Versión 1.1"
        footer_label = tk.Label(footer_frame, text=footer_text, font=("Helvetica", 12), fg="white", bg="#2c3e50", anchor="center", justify="center")
        footer_label.pack(pady=20)

        self.resetear_temporizador()
        self.inter_alumno.bind("<Motion>", self.reiniciar_temporizador)
        self.inter_alumno.bind("<Key>", self.reiniciar_temporizador)

    def cerrar_sesion(self):
        global temporizador
        if temporizador:
            temporizador.cancel()

        messagebox.showinfo("Sesión cerrada", "Tu sesión ha expirado.")

        self.inter_alumno.after(100, self.inter_alumno.destroy)
        threading.Thread(target=self.ejecutar_cargar).start()

    def ejecutar_cargar(self):
        subprocess.Popen(["python", "app.py"])

    def resetear_temporizador(self):
        global temporizador
        if temporizador:
            temporizador.cancel()
        temporizador = threading.Timer(120, self.cerrar_sesion)
        temporizador.start()

    def reiniciar_temporizador(self, event=None):
        self.resetear_temporizador()

