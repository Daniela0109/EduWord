import tkinter as tk
from tkinter import ttk

def mostrar_ayuda(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    label = tk.Label(frame, text="Ayuda", font=("Arial", 18))
    label.pack(pady=10)

    ayuda_text = tk.Label(frame, text="Para más información, visita nuestra página de soporte.", font=("Arial", 14))
    ayuda_text.pack(pady=10)

def acerca_de(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    info = """EduWord es un software educativo creado para ayudar a estudiantes a mejorar sus habilidades lingüísticas. 
    Este software está diseñado para ofrecer una experiencia interactiva y amigable."""

    label_info = tk.Label(frame, text=info, font=("Helvetica", 12), justify="left", padx=20, pady=20)
    label_info.pack()

def crear_mision(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    
    titulo = tk.Label(frame, text="Nuestra Misión", font=("Helvetica", 24, "bold"), fg="#4A90E2")
    titulo.pack(pady=10)

    mision_texto = """
    En EduWord, queremos ayudar a los niños a aprender de una manera divertida y emocionante. 
    A través de actividades de matemáticas, inglés y español, queremos que cada niño se sienta 
    inspirado y motivado para explorar el mundo del conocimiento.
    """

    mision_label = tk.Label(frame, text=mision_texto, font=("Helvetica", 14), justify="left", padx=20, pady=10, wraplength=600)
    mision_label.pack()

    boton_continuar = tk.Button(frame, text="¡Continuar aprendiendo!", font=("Helvetica", 16), bg="#4A90E2", fg="white", command=lambda: print("Continuar..."))
    boton_continuar.pack(pady=20)