import tkinter as tk
from tkinter import filedialog, messagebox
import firebase_admin
from firebase_admin import credentials, firestore
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

if not firebase_admin._apps:
    cred = credentials.Certificate("db\\eduwordConfigFB.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

class ValidadorCertificado:
    def __init__(self, root):
        self.root = root
        self.root.title("Validar Certificado")
        self.root.geometry("600x400")

        tk.Label(root, text="Validar Certificado Digital", font=("Helvetica", 16, "bold")).pack(pady=20)

        #tk.Button(root, text="Cargar Certificado (PDF)", command=self.cargar_certificado).pack(pady=10)
        tk.Button(root, text="Cargar Firma (.sig)", command=self.cargar_firma).pack(pady=10)
        
        tk.Button(root, text="Cargar Contenido (.txt)", command=self.cargar_contenido).pack(pady=10)

        tk.Label(root, text="Correo del maestro:", font=("Helvetica", 12)).pack(pady=10)
        self.entry_correo = tk.Entry(root, width=40)
        self.entry_correo.pack()

        tk.Button(root, text="Validar", command=self.validar_firma).pack(pady=20)

        self.resultado_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"))
        self.resultado_label.pack()
        
        tk.Button(root, text="Validar Otro Certificado", command=self.limpiar_campos).pack(pady=10)

        # self.ruta_certificado = None
        self.ruta_firma = None
        self.ruta_contenido = None
        
    def cargar_contenido(self):
        self.ruta_contenido = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.ruta_contenido:
            messagebox.showinfo("Archivo Cargado", "Contenido cargado correctamente.")

    # def cargar_certificado(self):
    #     self.ruta_certificado = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    #     if self.ruta_certificado:
    #         messagebox.showinfo("Archivo Cargado", "Certificado cargado correctamente.")

    def cargar_firma(self):
        self.ruta_firma = filedialog.askopenfilename(filetypes=[("Signature files", "*.sig")])
        if self.ruta_firma:
            messagebox.showinfo("Archivo Cargado", "Firma cargada correctamente.")

    def validar_firma(self):
        correo_maestro = self.entry_correo.get()

        if not all([self.ruta_contenido, self.ruta_firma, correo_maestro]):
            messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")
            return

        try:
            doc = db.collection("maestro").document(correo_maestro).get()
            if not doc.exists:
                self.resultado_label.config(text="No se encontró al maestro en la base de datos.", fg="red")
                return

            clave_publica_pem = doc.to_dict().get("clave_publica", "").encode()
            public_key = serialization.load_pem_public_key(clave_publica_pem)

            with open(self.ruta_contenido, "rb") as f:
                datos_contenido = f.read()

            with open(self.ruta_firma, "rb") as f:
                firma = f.read()

            public_key.verify(
                firma,
                datos_contenido,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256()
            )

            self.resultado_label.config(text="✔ Certificado válido y auténtico", fg="green")

        except Exception as e:
            print("Error:", e)
            self.resultado_label.config(text="✘ Certificado no válido o alterado", fg="red")
    
    def limpiar_campos(self):
        self.entry_correo.delete(0, tk.END)
        self.ruta_firma = None
        self.ruta_contenido = None
        self.resultado_label.config(text="")
        messagebox.showinfo("Formulario limpio", "Todos los campos han sido limpiados para una nueva validación.")

