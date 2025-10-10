import tkinter as tk
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("eduwordConfigFB.json") 
firebase_admin.initialize_app(cred)

db = firestore.client()

def mostrar_usuarios():
    usuarios_ref = db.collection("Usuarios") 
    docs = usuarios_ref.stream()

    resultado = ""
    for doc in docs:
        data = doc.to_dict()
        resultado += f"{data.get('Nombre', 'Sin Nombre')} - {data.get('Correo', 'Sin Correo')}\n"

    texto_label.config(text=resultado)

root = tk.Tk()
root.title("Conexión con Firebase")
root.geometry("400x300")

tk.Label(root, text="Usuarios en Firebase", font=("Comic Sans MS", 14, "bold")).pack(pady=10)
texto_label = tk.Label(root, text="", font=("Comic Sans MS", 12), wraplength=350)
texto_label.pack(pady=10)

tk.Button(root, text="Mostrar Usuarios", command=mostrar_usuarios).pack(pady=10)

root.mainloop()
