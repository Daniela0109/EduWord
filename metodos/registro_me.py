import tkinter as tk
from maestro.login_maestro import Login_Maestro
from alumno.login_alumno import Login_Alumno
import base64
from tkinter import messagebox
from db.conexionFirebase import obtener_db
db = obtener_db()

def actualizar_edad_label(label, val):
    label.config(text=f"Edad: {val}")

def ir_loguin_maestro(ventana_registro, ventana_seleccion):
    ventana_registro.destroy()
    ventana_login = tk.Toplevel(ventana_seleccion)
    Login_Maestro(ventana_login, ventana_seleccion)

def ir_login_alumno(ventana_registro, ventana_seleccion):
    ventana_registro.destroy()
    ventana_login = tk.Toplevel(ventana_seleccion)
    Login_Alumno(ventana_login, ventana_seleccion)
    
def cifrar_contraseña_base64(contraseña):
    return base64.b64encode(contraseña.encode()).decode()

def generar_contraseña(nombre, apellido_paterno, apellido_materno, edad):
    nombre = nombre.split()[0]
    extra = apellido_paterno[0].upper() + apellido_materno[0].upper()
    contraseña_base = f"{nombre}{extra}{edad}"
    return cifrar_contraseña_base64(contraseña_base), contraseña_base

def registrar_alumno(nombre, apellido, correo_tutor, edad, grado, grupo):
    apellidos = apellido.split()
    if len(apellidos) < 2:
        messagebox.showwarning("Error", "Por favor, ingrese apellido paterno y materno.")
        return

    apellido_paterno, apellido_materno = apellidos[0], apellidos[1]

    contraseña_encriptada, contraseña_desencriptada = generar_contraseña(nombre, apellido_paterno, apellido_materno, edad)

    usuario_data = {
        'nombre': nombre,
        'apellidos': apellido,
        'correo_tutor': correo_tutor,
        'edad': edad,
        'grado': grado,
        'grupo': grupo,
        'contraseña': contraseña_encriptada,
    }

    db.collection('alumno').add(usuario_data)

    mensaje = f"""
    ¡Felicidades {nombre}!
    
    Tu contraseña es: {contraseña_desencriptada}
    
    Recuerda, ¡es importante anotarla!
    Puedes escribirla en un lugar seguro o decírsela a tus padres.
    """
    messagebox.showinfo("Registro exitoso", mensaje)

def registrar_y_redirigirAlumno(self):
    nombre = self.entry_nombre.get().strip()
    apellido = self.entry_apellido.get().strip()
    correo_tutor = self.entry_correo_tutor.get().strip()
    edad = self.slider_edad.get()
    grado = self.grado_var.get()
    grupo = self.grupo_var.get()

    if not nombre or not apellido or not correo_tutor:
        messagebox.showwarning("Error", "Por favor, complete todos los campos.")
        return
    if "@" not in correo_tutor:
        messagebox.showwarning("Error", "Ingrese un correo válido para el tutor.")
        return

    registrar_alumno(nombre, apellido, correo_tutor, edad, grado, grupo)

    ir_login_alumno(self.registro, self.ventana_seleccion)