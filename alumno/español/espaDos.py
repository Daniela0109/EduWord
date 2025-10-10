import pygame
import random
import sys

pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 1000, 700  # Pantalla más grande
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Rimas - EduWord")

# Colores mejorados
BLANCO = (255, 255, 255)
NEGRO = (50, 50, 50)
AZUL_CLARO = (100, 175, 255)
AZUL_OSCURO = (0, 100, 200)
VERDE = (100, 255, 150)
ROJO = (255, 100, 100)
GRIS = (200, 200, 200)
MORADO = (150, 100, 255)

# Fuentes
fuente_grande = pygame.font.SysFont("Arial", 40, bold=True)
fuente_mediana = pygame.font.SysFont("Arial", 32)
fuente_chica = pygame.font.SysFont("Arial", 24)

# Diccionario de palabras y rimas
palabras = {
    "gato": ["zapato", "plato", "trato", "retrato"],
    "perro": ["hierro", "cerro", "terco", "barro"],
    "pato": ["zapato", "trato", "rato", "retrato"],
    "flor": ["color", "dolor", "amor", "calor"],
    "sol": ["col", "rol", "bol", "gol"]
}

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_normal, color_hover, accion=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_actual = color_normal
        self.accion = accion
        self.hover = False
        
    def dibujar(self, superficie):
        # Dibuja el botón con efecto hover
        color = self.color_hover if self.hover else self.color_normal
        pygame.draw.rect(superficie, color, self.rect, border_radius=10)
        pygame.draw.rect(superficie, NEGRO, self.rect, 2, border_radius=10)  # Borde
        
        # Centrar texto en el botón
        texto_rend = fuente_mediana.render(self.texto, True, NEGRO)
        texto_rect = texto_rend.get_rect(center=self.rect.center)
        superficie.blit(texto_rend, texto_rect)
        
    def actualizar(self, eventos):
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())
        
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and self.hover and self.accion:
                self.accion()
                return True
        return False

def mostrar_texto(texto, color, x, y, fuente=fuente_grande, centrado=False):
    texto_renderizado = fuente.render(texto, True, color)
    if centrado:
        rect = texto_renderizado.get_rect(center=(x, y))
        screen.blit(texto_renderizado, rect)
    else:
        screen.blit(texto_renderizado, (x, y))

def dibujar_fondo_degradado():
    # Fondo con degradado simple
    for y in range(ALTO):
        factor = y / ALTO
        r = int(200 + (55 * factor))
        g = int(230 + (25 * factor))
        b = int(255 - (55 * factor))
        pygame.draw.line(screen, (r, g, b), (0, y), (ANCHO, y))

def juego_de_rimas():
    palabra_base = random.choice(list(palabras.keys()))
    rimas_correctas = palabras[palabra_base]
    
    # Crear opciones (3 correctas + 3 incorrectas)
    opciones = rimas_correctas[:3] + random.sample([
        "casa", "árbol", "libro", "agua", "cielo", 
        "tierra", "fuego", "viento", "mesa", "silla"
    ], 3)
    random.shuffle(opciones)
    
    # Crear botones
    botones = []
    ancho_boton = 200
    alto_boton = 80
    margen = 20
    
    for i, opcion in enumerate(opciones):
        fila = i // 3
        columna = i % 3
        x = (ANCHO // 2 - ancho_boton * 1.5 - margen) + columna * (ancho_boton + margen)
        y = 250 + fila * (alto_boton + margen)
        
        botones.append(Boton(
            x, y, ancho_boton, alto_boton, 
            opcion, 
            AZUL_CLARO, 
            VERDE if opcion in rimas_correctas else MORADO,
            lambda op=opcion: None
        ))
    
    respuesta = None
    mensaje = ""
    color_mensaje = NEGRO
    
    reloj = pygame.time.Clock()
    
    while True:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Actualizar botones de opciones
        for boton in botones:
            if boton.actualizar(eventos) and not respuesta:
                if boton.texto in rimas_correctas:
                    respuesta = True
                    mensaje = "¡Correcto! " + random.choice(["Excelente!", "Bien hecho!", "Perfecto!"])
                    color_mensaje = VERDE
                else:
                    respuesta = False
                    mensaje = "Incorrecto. Intenta otra vez."
                    color_mensaje = ROJO
        
        # Dibujar todo
        dibujar_fondo_degradado()
        
        # Título y pregunta
        mostrar_texto("Juego de Rimas", NEGRO, ANCHO//2, 50, fuente_grande, True)
        mostrar_texto(f"¿Qué palabra rima con '{palabra_base}'?", NEGRO, ANCHO//2, 150, fuente_mediana, True)
        
        # Dibujar botones de opciones
        for boton in botones:
            boton.dibujar(screen)
            if respuesta and boton.texto in rimas_correctas:
                pygame.draw.rect(screen, VERDE, boton.rect, 3, border_radius=10)
        
        # Mostrar mensaje y botón continuar SOLO cuando hay respuesta
        if respuesta is not None:
            mostrar_texto(mensaje, color_mensaje, ANCHO//2, 450, fuente_mediana, True)
            
            # Botón Continuar - POSICIÓN CORREGIDA y COLOR MEJORADO
            boton_continuar = Boton(
                ANCHO//2 - 100,  # Centrado horizontalmente
                520,             # Posición vertical más abajo
                200, 
                60, 
                "Continuar", 
                AZUL_OSCURO, 
                VERDE,
                lambda: None
            )
            
            # Dibujar y actualizar el botón continuar
            boton_continuar.dibujar(screen)
            
            # Verificar clic en botón continuar
            continuar_clickeado = False
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN and boton_continuar.rect.collidepoint(evento.pos):
                    continuar_clickeado = True
            
            if continuar_clickeado:
                return juego_de_rimas()  # Reiniciar juego
        
        pygame.display.flip()
        reloj.tick(60)

# Iniciar el juego
juego_de_rimas()
pygame.quit()