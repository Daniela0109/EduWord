import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.pdfgen import canvas
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

class GenerarCertificado:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Generar Certificado")
        self.ventana.geometry("900x600")

        tk.Label(ventana, text="Nombre del Alumno:", font=("Comic Sans MS", 12)).pack(pady=5)
        self.entry_nombre = tk.Entry(ventana, font=("Comic Sans MS", 12))
        self.entry_nombre.pack(pady=5)

        tk.Label(ventana, text="Apellido del Alumno:", font=("Comic Sans MS", 12)).pack(pady=5)
        self.entry_apellido = tk.Entry(ventana, font=("Comic Sans MS", 12))
        self.entry_apellido.pack(pady=5)

        tk.Label(ventana, text="Materia:", font=("Comic Sans MS", 12)).pack(pady=5)
        self.entry_materia = tk.Entry(ventana, font=("Comic Sans MS", 12))
        self.entry_materia.pack(pady=5)

        tk.Label(ventana, text="Calificación Final:", font=("Comic Sans MS", 12)).pack(pady=5)
        self.entry_calificacion = tk.Entry(ventana, font=("Comic Sans MS", 12))
        self.entry_calificacion.pack(pady=5)

        tk.Label(ventana, text="Clave Privada (archivo):", font=("Comic Sans MS", 12)).pack(pady=5)
        self.btn_cargar_clave = tk.Button(ventana, text="Seleccionar Archivo .pem", command=self.cargar_clave_privada)
        self.btn_cargar_clave.pack(pady=5)

        self.btn_generar = tk.Button(ventana, text="Generar Certificado", command=self.generar_certificado, font=("Comic Sans MS", 12, "bold"))
        self.btn_generar.pack(pady=20)

        self.clave_privada = None  

        self.btn_limpiar = tk.Button(ventana, text="Generar Otro Certificado", command=self.limpiar_campos, font=("Comic Sans MS", 12))
        self.btn_limpiar.pack(pady=10)


    def cargar_clave_privada(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
        if ruta_archivo:
            try:
                with open(ruta_archivo, "rb") as f:
                    self.clave_privada = serialization.load_pem_private_key(
                        f.read(),
                        password=None,
                        backend=default_backend()
                    )
                messagebox.showinfo("Clave Cargada", "Clave privada cargada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la clave privada: {e}")

    def generar_certificado(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        materia = self.entry_materia.get()
        calificacion = self.entry_calificacion.get()

        if not all([nombre, apellido, materia, calificacion, self.clave_privada]):
            messagebox.showwarning("Faltan Datos", "Por favor llena todos los campos y carga la clave privada.")
            return

        contenido = f"{nombre} {apellido} - {materia} - Calificación: {calificacion}".encode("utf-8")

        try:
            firma = self.clave_privada.sign(
                contenido,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo firmar el certificado: {e}")
            return

        ruta_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if ruta_pdf:
            c = canvas.Canvas(ruta_pdf)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, 750, "CERTIFICADO DE FINALIZACIÓN")

            c.setFont("Helvetica", 12)
            c.drawString(100, 700, f"Alumno: {nombre} {apellido}")
            c.drawString(100, 680, f"Materia: {materia}")
            c.drawString(100, 660, f"Calificación final: {calificacion}")
            c.drawString(100, 630, "Este documento ha sido firmado digitalmente.")


            firma_hex = firma.hex()[:64] 
            c.setFont("Helvetica-Oblique", 8)
            c.drawString(100, 610, f"Hash de la firma: {firma_hex}...")

            c.save()
            
            ruta_firma = filedialog.asksaveasfilename(defaultextension=".sig", filetypes=[("Signature files", "*.sig")], title="Guardar archivo de firma .sig")
            if ruta_firma:
                try:
                    with open(ruta_firma, "wb") as sig_file:
                        sig_file.write(firma)
                    messagebox.showinfo("Firma guardada", "Firma digital guardada como archivo .sig.")
                except Exception as e:
                    messagebox.showerror("Error al guardar firma", f"No se pudo guardar el archivo .sig: {e}")
            
            ruta_contenido = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Guardar contenido firmado")
            if ruta_contenido:
                try:
                    with open(ruta_contenido, "w", encoding="utf-8") as f:
                        f.write(f"{nombre} {apellido} - {materia} - Calificación: {calificacion}")
                    messagebox.showinfo("Contenido guardado", "Contenido firmado guardado como .txt.")
                except Exception as e:
                    messagebox.showerror("Error al guardar contenido", f"No se pudo guardar el archivo .txt: {e}")

                    
            messagebox.showinfo("Éxito", "Certificado generado y firmado correctamente.")

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_materia.delete(0, tk.END)
        self.entry_calificacion.delete(0, tk.END)
        self.clave_privada = None
        messagebox.showinfo("Formulario limpio", "Todos los campos han sido limpiados.")
