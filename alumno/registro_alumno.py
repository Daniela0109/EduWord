import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from metodos.registro_me import actualizar_edad_label, ir_login_alumno, registrar_y_redirigirAlumno

class Registro_Alumno:
    def __init__(self, registro, ventana_seleccion):
        self.registro = registro
        self.registro.title("Registro de Usuario Alumno")
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
        self.entry_nombre = tk.Entry(scrollbar_frame, font=("Comic Sans MS", 12))
        self.entry_nombre.pack(pady=5)

        label_apellido = tk.Label(scrollbar_frame, text="Apellido:", font=("Comic Sans MS", 12)).pack()
        self.entry_apellido = tk.Entry(scrollbar_frame, font=("Comic Sans MS", 12))
        self.entry_apellido.pack(pady=5)

        label_correo_tutor = tk.Label(scrollbar_frame, text="Correo del tutor:", font=("Comic Sans MS", 12)).pack()
        self.entry_correo_tutor = tk.Entry(scrollbar_frame, font=("Comic Sans MS", 12))
        self.entry_correo_tutor.pack(pady=5)

        self.slider_edad = tk.Scale(scrollbar_frame, from_=4, to=100, orient="horizontal", font=("Comic Sans MS", 12))
        self.slider_edad.pack(pady=5)

        self.grado_var = tk.StringVar(scrollbar_frame)
        self.grado_var.set("1ro")
        grado_menu = tk.OptionMenu(scrollbar_frame, self.grado_var, "1ro", "2do", "3ro")
        grado_menu.pack(pady=5)

        self.grupo_var = tk.StringVar(scrollbar_frame)
        self.grupo_var.set("A")
        grupo_menu = tk.OptionMenu(scrollbar_frame, self.grupo_var, "A", "B")
        grupo_menu.pack(pady=5)

        btn_registrar = tk.Button(scrollbar_frame, text="Registrarse", font=("Comic Sans MS", 12, "bold"), command=lambda: registrar_y_redirigirAlumno(self))
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