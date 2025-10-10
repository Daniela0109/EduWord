import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk

def mostrar_glosario(glosario):
    ventana_glosario = tk.Toplevel() 
    ventana_glosario.title("Glosario")
    ventana_glosario.geometry("500x500")

    banner_frame = tk.Frame(ventana_glosario, bg="#3498db", height=100)
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

    if not glosario:
        messagebox.showinfo("Glosario", "El glosario está vacío.")
        return

    for i, (palabra, significado) in enumerate(glosario.items()):
        label = tk.Label(ventana_glosario, text=f"{palabra}: {significado}", font=("Arial", 12))
        label.pack(pady=5)
    
    ventana_glosario.mainloop()

def abrir_glosario(glosario):
    mostrar_glosario(glosario)