import pygame
import random
import sys

pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 1000, 700
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Adivina la Palabra - EduWord")

# Paleta de colores mejorada
COLOR_FONDO = (240, 248, 255)  # Azul claro muy suave
COLOR_TEXTO = (50, 50, 80)      # Azul oscuro
COLOR_BOTON = (100, 175, 255)   # Azul medio
COLOR_BOTON_HOVER = (70, 130, 180)
COLOR_ACIERTO = (100, 255, 150) # Verde claro
COLOR_ERROR = (255, 150, 150)   # Rojo suave
COLOR_BORDE = (200, 220, 255)   # Borde azul claro

# Cargar fuentes con manejo de errores
try:
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_texto = pygame.font.Font(None, 36)
    fuente_letras = pygame.font.Font(None, 32)
except:
    print("Error cargando fuentes personalizadas. Usando fuentes del sistema...")
    fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
    fuente_texto = pygame.font.SysFont("Arial", 36)
    fuente_letras = pygame.font.SysFont("Arial", 32, bold=True)

# Datos del juego
palabras = [
    {
        "palabra": "gato", 
        "pista": "Es un animal que maúlla", 
        "imagen": "img/juegos/gato.png",
        "categoria": "Animales"
    },
    {
        "palabra": "perro", 
        "pista": "Es un animal que ladra", 
        "imagen": "img/juegos/perro.png",
        "categoria": "Animales"
    },
    {
        "palabra": "flor", 
        "pista": "Es una planta colorida", 
        "imagen": "img/juegos/flor.png",
        "categoria": "Plantas"
    },
]

class BotonLetra:
    def __init__(self, x, y, letra, idx):
        self.rect = pygame.Rect(x, y, 70, 70)
        self.letra = letra
        self.idx = idx  # Identificador único para cada botón
        self.seleccionado = False
        self.hover = False
        self.activo = True
        
    def dibujar(self):
        if not self.activo:
            return
            
        # Color del botón según estado
        if self.seleccionado:
            color = COLOR_ACIERTO
        elif self.hover:
            color = COLOR_BOTON_HOVER
        else:
            color = COLOR_BOTON
            
        # Dibujar botón con bordes redondeados
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, COLOR_BORDE, self.rect, 3, border_radius=10)
        
        # Dibujar letra centrada
        texto = fuente_letras.render(self.letra.upper(), True, COLOR_TEXTO)
        texto_rect = texto.get_rect(center=self.rect.center)
        screen.blit(texto, texto_rect)
        
    def actualizar(self, eventos, indices_seleccionados):
        if not self.activo or self.seleccionado:
            return None
        
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
    
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.hover and self.idx not in indices_seleccionados:
                    return self.idx
        return None
    
def mostrar_texto(texto, color, x, y, fuente=None, centrado=False):
    """Función mejorada con manejo de errores para mostrar texto"""
    try:
        if fuente is None:
            fuente = fuente_texto
            
        texto_renderizado = fuente.render(texto, True, color)
        if centrado:
            rect = texto_renderizado.get_rect(center=(x, y))
            screen.blit(texto_renderizado, rect)
        else:
            screen.blit(texto_renderizado, (x, y))
    except Exception as e:
        print(f"Error al mostrar texto: {e}")
        fuente_fallback = pygame.font.SysFont("Arial", 24)
        texto_renderizado = fuente_fallback.render(texto, True, color)
        screen.blit(texto_renderizado, (x, y))

def dibujar_fondo():
    """Dibuja el fondo con un patrón sutil"""
    screen.fill(COLOR_FONDO)
    for i in range(0, ANCHO, 40):
        pygame.draw.line(screen, (230, 240, 255), (i, 0), (i, ALTO), 1)
    for i in range(0, ALTO, 40):
        pygame.draw.line(screen, (230, 240, 255), (0, i), (ANCHO, i), 1)

def cargar_imagen(ruta, tamaño=(200, 200)):
    """Carga una imagen con manejo de errores"""
    try:
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, tamaño)
    except:
        print(f"Error al cargar imagen: {ruta}")
        superficie = pygame.Surface(tamaño)
        superficie.fill((200, 200, 200))
        pygame.draw.rect(superficie, (150, 150, 150), (0, 0, *tamaño), 2)
        return superficie

def adivina_la_palabra():
    palabra_obj = random.choice(palabras)
    palabra = palabra_obj["palabra"]
    pista = palabra_obj["pista"]
    categoria = palabra_obj.get("categoria", "")
    
    try:
        imagen = pygame.image.load(palabra_obj["imagen"])
        imagen = pygame.transform.scale(imagen, (200, 200))
    except:
        imagen = pygame.Surface((200, 200))
        imagen.fill((220, 220, 220))
        pygame.draw.rect(imagen, (180, 180, 180), (0, 0, 200, 200), 2)
        texto_fallo = fuente_texto.render("Imagen no encontrada", True, (100, 100, 100))
        imagen.blit(texto_fallo, (100 - texto_fallo.get_width()//2, 100 - texto_fallo.get_height()//2))
    
    # Preparar letras desordenadas
    letras_desordenadas = list(palabra)
    random.shuffle(letras_desordenadas)
    
    # Crear botones de letras con identificadores únicos
    botones_letras = []
    for i, letra in enumerate(letras_desordenadas):
        x = 150 + (i * 110)
        y = 300
        botones_letras.append(BotonLetra(x, y, letra, i))  # Pasamos el índice como identificador
    
    # Área para mostrar la palabra construida
    palabra_construida = []
    indices_seleccionados = []  # Para controlar qué botones están seleccionados
    area_palabra = pygame.Rect(150, 200, len(palabra) * 70, 80)
    
    # Botón de reinicio
    boton_reinicio = pygame.Rect(ANCHO - 150, 50, 120, 50)
    
    reloj = pygame.time.Clock()
    adivinada = False
    mensaje = ""
    color_mensaje = COLOR_TEXTO
    tiempo_ultimo_click = 0
    
    while True:
        tiempo_actual = pygame.time.get_ticks()
        eventos = pygame.event.get()
        
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reinicio.collidepoint(evento.pos):
                    return adivina_la_palabra()
        
        # Actualizar botones de letras
        if not adivinada and (tiempo_actual - tiempo_ultimo_click > 300):
            for boton in botones_letras:
                letra_idx_seleccionada = boton.actualizar(eventos, indices_seleccionados)
                if letra_idx_seleccionada is not None:
                    indices_seleccionados.append(letra_idx_seleccionada)
                    palabra_construida.append(botones_letras[letra_idx_seleccionada].letra)
                    boton.seleccionado = True
                    tiempo_ultimo_click = tiempo_actual
        
        # Verificar si se completó la palabra
        if not adivinada and len(palabra_construida) == len(palabra):
            adivinada = ''.join(palabra_construida) == palabra
            if adivinada:
                mensaje = f"¡Correcto! La palabra es '{palabra}'"
                color_mensaje = COLOR_ACIERTO
            else:
                mensaje = "¡Intenta nuevamente!"
                color_mensaje = COLOR_ERROR
                pygame.time.delay(1000)
                palabra_construida = []
                indices_seleccionados = []
                for boton in botones_letras:
                    boton.seleccionado = False
        
        # --- Dibujado ---
        dibujar_fondo()
        
        # Dibujar título y categoría
        mostrar_texto("Adivina la Palabra", COLOR_TEXTO, ANCHO//2, 30, fuente_titulo, True)
        if categoria:
            mostrar_texto(f"Categoría: {categoria}", (100, 100, 150), ANCHO//2, 80, fuente_texto, True)
        
        # Dibujar pista
        mostrar_texto("Pista: " + pista, COLOR_TEXTO, 20, 120)
        
        # Dibujar imagen
        screen.blit(imagen, (ANCHO - 250, 100))
        
        # Dibujar área de palabra construida
        pygame.draw.rect(screen, (255, 255, 255), area_palabra, border_radius=10)
        pygame.draw.rect(screen, COLOR_BORDE, area_palabra, 3, border_radius=10)
        
        # Mostrar letras seleccionadas
        texto_palabra = fuente_letras.render(' '.join(palabra_construida).upper(), True, COLOR_TEXTO)
        screen.blit(texto_palabra, (area_palabra.x + 20, area_palabra.centery - texto_palabra.get_height()//2))
        
        # Dibujar botones de letras
        for boton in botones_letras:
            boton.dibujar()
        
        # Dibujar mensaje de resultado
        if adivinada:
            mostrar_texto(mensaje, color_mensaje, ANCHO//2, 450, fuente_texto, True)
            
            # Botón para continuar
            pygame.draw.rect(screen, COLOR_BOTON, (ANCHO//2 - 100, 500, 200, 50), border_radius=10)
            pygame.draw.rect(screen, COLOR_BORDE, (ANCHO//2 - 100, 500, 200, 50), 3, border_radius=10)
            mostrar_texto("Continuar", COLOR_TEXTO, ANCHO//2, 525, fuente_texto, True)
            
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if pygame.Rect(ANCHO//2 - 100, 500, 200, 50).collidepoint(mouse_pos):
                    pygame.time.delay(300)
                    return adivina_la_palabra()
        
        # Dibujar botón de reinicio
        pygame.draw.rect(screen, COLOR_BOTON, boton_reinicio, border_radius=8)
        pygame.draw.rect(screen, COLOR_BORDE, boton_reinicio, 3, border_radius=8)
        mostrar_texto("Reiniciar", COLOR_TEXTO, boton_reinicio.centerx, boton_reinicio.centery, fuente_texto, True)
        
        pygame.display.flip()
        reloj.tick(60)

# Iniciar el juego
if __name__ == "__main__":
    adivina_la_palabra()
    pygame.quit()