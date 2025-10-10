import tkinter as tk
import pyttsx3
from tkinter import simpledialog, messagebox
from PyDictionary import PyDictionary

from tkinter import PhotoImage
from PIL import Image, ImageTk
from metodos.glosario import abrir_glosario

class Lector_Texto:
    def __init__(self, lector, ventana_interfaz):
        self.lector = lector
        self.lector.title("Lector de Texto")
        self.lector.geometry("1000x700")
        self.ventana_interfaz = ventana_interfaz

        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1)
        self.glosario_dict = {}
        self.dictionary = PyDictionary()

        banner_frame = tk.Frame(self.lector, bg="#3498db", height=100)
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

        self.texto = tk.Text(self.lector, wrap=tk.WORD, height=10, width=50)
        self.texto.insert(tk.END, """Había una vez un conejito soñador que vivía en una casita en medio del bosque, rodeado de libros y fantasía, pero no tenía amigos. Todos le habían dado de lado porque se pasaba el día contando historias imaginarias sobre hazañas caballerescas, aventuras submarinas y expediciones extraterrestres. Siempre estaba inventando aventuras como si las hubiera vivido de verdad, hasta que sus amigos se cansaron de escucharle y acabó quedándose solo.
                     
        Al principio el conejito se sintió muy triste y empezó a pensar que sus historias eran muy aburridas y por eso nadie las quería escuchar. Pero pese a eso continuó escribiendo.
                     
        Las historias del conejito eran increíbles y le permitían vivir todo tipo de aventuras. Se imaginaba vestido de caballero salvando a inocentes princesas o sintiendo el frío del mar sobre su traje de buzo mientras exploraba las profundidades del océano.

        Se pasaba el día escribiendo historias y dibujando los lugares que imaginaba. De vez en cuando, salía al bosque a leer en voz alta, por si alguien estaba interesado en compartir sus relatos.

        Un día, mientras el conejito soñador leía entusiasmado su último relato, apareció por allí una hermosa conejita que parecía perdida. Pero nuestro amigo estaba tan entregado a la interpretación de sus propios cuentos que ni se enteró de que alguien lo escuchaba. Cuando acabó, la conejita le aplaudió con entusiasmo.

        -Vaya, no sabía que tenía público- dijo el conejito soñador a la recién llegada -. ¿Te ha gustado mi historia?
        -Ha sido muy emocionante -respondió ella-. ¿Sabes más historias?
        -¡Claro!- dijo emocionado el conejito -. Yo mismo las escribo.
        - ¿De verdad? ¿Y son todas tan apasionantes?
        - ¿Tu crees que son apasionantes? Todo el mundo dice que son aburridísimas…
        - Pues eso no es cierto, a mi me ha gustado mucho. Ojalá yo supiera saber escribir historias como la tuya pero no se...

        El conejito soñadorl conejito se dio cuenta de que la conejita se había puesto de repente muy triste así que se acercó y, pasándole la patita por encima del hombro, le dijo con dulzura:
        - Yo puedo enseñarte si quieres a escribirlas. Seguro que aprendes muy rápido
        - ¿Sí? ¿Me lo dices en serio?
        - ¡Claro que sí! ¡Hasta podríamos escribirlas juntos!
        - ¡Genial! Estoy deseando explorar esos lugares, viajar a esos mundos y conocer a todos esos villanos y malandrines -dijo la conejita-

        Los conejitos se hicieron muy amigos y compartieron juegos y escribieron cientos de libros que leyeron a niños de todo el mundo.""")
        self.texto.pack()
        self.texto.bind("<ButtonRelease-1>", self.obtener_palabra_seleccionada)

        boton_leer = tk.Button(self.lector, text="Leer Texto", command=self.leer_texto)
        boton_leer.pack(pady=10)

        boton_detener = tk.Button(self.lector, text="Detener Lectura", command=self.detener_lectura)
        boton_detener.pack(pady=10)

        boton_glosario = tk.Button(self.lector, text="Abrir Glosario", command=lambda:abrir_glosario(self.glosario_dict))
        boton_glosario.pack(pady=10)

        boton_volver = tk.Button(self.lector, text="Volver", command=self.volver)
        boton_volver.pack(pady=10)

        footer_frame = tk.Frame(self.lector, bg="#2c3e50", height=100)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_text = "El aprendizaje es un tesoro que seguirá a su dueño a cualquier lugar. – Proverbio chino\n© 2025 EduWord. Todos los derechos reservados. Versión 1.1"
        footer_label = tk.Label(footer_frame, text=footer_text, font=("Helvetica", 12), fg="white", bg="#2c3e50", anchor="center", justify="center")
        footer_label.pack(pady=20)



    def leer_texto(self):
        text = self.texto.get("1.0", tk.END)
        self.engine.say(text)
        self.engine.runAndWait()

    def detener_lectura(self):
        self.engine.stop()

    def mostrar_significado(self, palabra):
        if palabra in self.glosario_dict:
            messagebox.showinfo("Significado", f"Significado de '{palabra}': {self.glosario_dict[palabra]}")
        else:
            significado = self.dictionary.meaning(palabra)
            if significado:
                mensaje = "\n".join([f"{key}: {value}" for key, value in significado.items()])
                messagebox.showinfo("Significado", f"Significado de '{palabra}': \n{mensaje}")
            else:
                messagebox.showinfo("Significado", f"No se encontró el significado para '{palabra}'.")

    def guardar_en_glosario(self, palabra):
        significado = simpledialog.askstring("Añadir al Glosario", f"Ingrese el significado de '{palabra}:")
        if significado:
            self.glosario_dict[palabra] = significado
            messagebox.showinfo("Glosario", f"Palabra '{palabra}' guardada en el glosario.")

    def obtener_palabra_seleccionada(self, event):
        index = self.texto.index(tk.CURRENT)
        palabra = self.texto.get(f"{index} wordstart", f"{index} wordend")
        if palabra:  
            self.mostrar_opciones(palabra)

    def mostrar_opciones(self, palabra):
        def opcion_1():
            self.mostrar_significado(palabra)
            opciones_ventana.destroy()
        def opcion_2():
            self.guardar_en_glosario(palabra)
            opciones_ventana.destroy()

        opciones_ventana = tk.Toplevel(self.lector)
        opciones_ventana.title("Opciones")

        label_opciones = tk.Label(opciones_ventana, text=f"¿Que deseas hacer con la palabra '{palabra}'?", padx=20, pady=20).pack()

        btn_ver_significado = tk.Button(opciones_ventana, text="Ver Significado", command=opcion_1)
        btn_ver_significado.pack(padx=10, pady=10)

        btn_agregar_significado = tk.Button(opciones_ventana, text="Agregar Significado", command=opcion_2)
        btn_agregar_significado.pack(padx=10, pady=10)

    def volver(self):
        self.lector.destroy()
        self.ventana_interfaz.deiconify()

    
