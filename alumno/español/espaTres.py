import pygame
import random
import os

# Inicialización de pygame
pygame.init()
pygame.mixer.init()  # Para efectos de sonido

# Configuración de pantalla
ANCHO, ALTO = 1000, 700
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tarjetas de Memoria - EduGame")

# Paleta de colores moderna
COLOR_FONDO = (240, 240, 245)  # Gris muy claro
COLOR_TARJETA = (93, 173, 226)  # Azul cielo
COLOR_TARJETA_HOVER = (72, 201, 176)  # Verde agua
COLOR_TARJETA_REVELADA = (253, 203, 110)  # Amarillo claro
COLOR_TEXTO = (50, 50, 80)  # Azul oscuro
COLOR_TEXTO_REVELADO = (30, 30, 30)  # Negro suave
COLOR_EXITO = (46, 204, 113)  # Verde brillante
COLOR_BOTON = (155, 89, 182)  # Morado
COLOR_BOTON_HOVER = (142, 68, 173)  # Morado oscuro

# Fuentes mejoradas
try:
    fuente_principal = pygame.font.Font(None, 36)
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_tarjeta = pygame.font.Font(None, 32)
except:
    fuente_principal = pygame.font.SysFont("Arial", 36)
    fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
    fuente_tarjeta = pygame.font.SysFont("Arial", 32, bold=True)

# Efectos de sonido (opcional)
try:
    sonido_voltear = pygame.mixer.Sound("flip.wav")
    sonido_match = pygame.mixer.Sound("match.wav")
    sonido_win = pygame.mixer.Sound("win.wav")
    tiene_sonido = True
except:
    tiene_sonido = False

# Datos del juego
cartas = [
    {"palabra": "coche", "imagen": "img/juegos/coche.png", "color": (231, 76, 60)},
    {"palabra": "gato", "imagen": "img/juegos/gato.png", "color": (41, 128, 185)},
    {"palabra": "flor", "imagen": "img/juegos/flor.png", "color": (39, 174, 96)},
    {"palabra": "perro", "imagen": "img/juegos/perro.png", "color": (142, 68, 173)},
    {"palabra": "pato", "imagen": "img/juegos/pato.png", "color": (243, 156, 18)},
    {"palabra": "pelota", "imagen": "img/juegos/pelota.png", "color": (211, 84, 0)},
]

def cargar_imagen(ruta, tamaño):
    """Carga una imagen con manejo de errores"""
    try:
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, tamaño)
    except:
        # Crear una imagen de reemplazo
        superficie = pygame.Surface(tamaño)
        superficie.fill((200, 200, 200))
        pygame.draw.rect(superficie, (150, 150, 150), (0, 0, *tamaño), 2)
        texto = fuente_tarjeta.render("Imagen", True, (100, 100, 100))
        superficie.blit(texto, (tamaño[0]//2 - texto.get_width()//2, tamaño[1]//2 - texto.get_height()//2))
        return superficie

def mostrar_texto(texto, color, x, y, fuente=None, centrado=False, sombra=False):
    """Función mejorada para mostrar texto"""
    if fuente is None:
        fuente = fuente_principal
        
    texto_renderizado = fuente.render(texto, True, color)
    
    if sombra:
        texto_sombra = fuente.render(texto, True, (0, 0, 0))
        pos_sombra = (x+2, y+2) if not centrado else (x, y)
        if centrado:
            rect_sombra = texto_sombra.get_rect(center=(x+2, y+2))
            screen.blit(texto_sombra, rect_sombra)
        else:
            screen.blit(texto_sombra, pos_sombra)
    
    if centrado:
        rect = texto_renderizado.get_rect(center=(x, y))
        screen.blit(texto_renderizado, rect)
    else:
        screen.blit(texto_renderizado, (x, y))

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color, color_hover):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.hover = False
        
    def dibujar(self):
        color = self.color_hover if self.hover else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=10)
        mostrar_texto(self.texto, (255, 255, 255), self.rect.centerx, self.rect.centery, fuente_principal, True)
        
    def actualizar(self, eventos):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.hover:
                return True
        return False

class Carta:
    def __init__(self, palabra, imagen, color, x, y):
        self.palabra = palabra
        self.imagen = cargar_imagen(imagen, (120, 120))
        self.color = color
        self.x = x
        self.y = y
        self.ancho = 120
        self.alto = 160
        self.mostrada = False
        self.revelada = False
        self.hover = False
        self.angulo = 0  # Para efecto de volteo
        
    def dibujar(self):
        # Fondo de la carta con bordes redondeados
        rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
        if self.mostrada or self.revelada:
            # Carta revelada
            pygame.draw.rect(screen, COLOR_TARJETA_REVELADA, rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=10)
            
            # Imagen centrada
            img_rect = self.imagen.get_rect(center=(self.x + self.ancho//2, self.y + self.alto//2 - 10))
            screen.blit(self.imagen, img_rect)
            
            # Texto de la palabra debajo de la imagen
            mostrar_texto(self.palabra, COLOR_TEXTO_REVELADO, self.x + self.ancho//2, self.y + self.alto - 25, fuente_tarjeta, True)
        else:
            # Carta oculta
            color = COLOR_TARJETA_HOVER if self.hover else COLOR_TARJETA
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=10)
            
            # Mostrar símbolo de interrogación
            mostrar_texto("?", (255, 255, 255), self.x + self.ancho//2, self.y + self.alto//2, fuente_titulo, True, True)
            
            # Pequeño círculo de color para ayudar a emparejar
            pygame.draw.circle(screen, self.color, (self.x + self.ancho//2, self.y + 20), 8)

def juego_de_memoria():
    # Crear pares de cartas
    cartas_juego = []
    for carta in cartas:
        cartas_juego.append(Carta(carta["palabra"], carta["imagen"], carta["color"], 0, 0))
        cartas_juego.append(Carta(carta["palabra"], carta["imagen"], carta["color"], 0, 0))
    
    random.shuffle(cartas_juego)
    
    # Posicionar cartas en una cuadrícula 4x3
    for i, carta in enumerate(cartas_juego):
        carta.x = 150 + (i % 4) * 180  # Espaciado horizontal
        carta.y = 150 + (i // 4) * 180  # Espaciado vertical
    
    carta_seleccionada = []
    juego_terminado = False
    intentos = 0
    pares_encontrados = 0
    
    # Botón de reinicio
    boton_reinicio = Boton(ANCHO - 150, 50, 120, 50, "Reiniciar", COLOR_BOTON, COLOR_BOTON_HOVER)
    
    # Efecto de partículas para celebraciones
    particulas = []
    
    while True:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
        
        screen.fill(COLOR_FONDO)
        
        # Dibujar título
        mostrar_texto("Juego de Memoria", COLOR_TEXTO, ANCHO//2, 50, fuente_titulo, True)
        mostrar_texto(f"Intentos: {intentos} | Pares: {pares_encontrados}/{len(cartas)}", COLOR_TEXTO, ANCHO//2, 100, fuente_principal, True)
        
        # Actualizar y dibujar botón de reinicio
        if boton_reinicio.actualizar(eventos):
            return juego_de_memoria()  # Reiniciar juego
        
        boton_reinicio.dibujar()
        
        # Actualizar estado hover de las cartas
        mouse_pos = pygame.mouse.get_pos()
        for carta in cartas_juego:
            carta.hover = not carta.mostrada and not carta.revelada and \
                         carta.x <= mouse_pos[0] <= carta.x + carta.ancho and \
                         carta.y <= mouse_pos[1] <= carta.y + carta.alto
        
        # Manejar clics en cartas
        if not juego_terminado and len(carta_seleccionada) < 2:
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for carta in cartas_juego:
                        if carta.hover and carta not in carta_seleccionada and not carta.mostrada and not carta.revelada:
                            carta.mostrada = True
                            carta_seleccionada.append(carta)
                            if tiene_sonido:
                                sonido_voltear.play()
                            break
        
        # Verificar parejas
        if len(carta_seleccionada) == 2:
            intentos += 1
            carta1, carta2 = carta_seleccionada
            if carta1.palabra == carta2.palabra:
                if tiene_sonido:
                    sonido_match.play()
                carta1.revelada = True
                carta2.revelada = True
                pares_encontrados += 1
                
                # Añadir partículas de celebración
                for _ in range(20):
                    particulas.append({
                        'x': carta1.x + carta1.ancho//2,
                        'y': carta1.y + carta1.alto//2,
                        'color': random.choice([(255, 255, 0), (255, 165, 0), (255, 215, 0)]),
                        'size': random.randint(3, 8),
                        'speed_x': random.uniform(-3, 3),
                        'speed_y': random.uniform(-3, 3),
                        'life': 30
                    })
            else:
                pygame.time.delay(800)  # Breve pausa para memorizar
                carta1.mostrada = False
                carta2.mostrada = False
            
            carta_seleccionada = []
        
        # Dibujar cartas
        for carta in cartas_juego:
            carta.dibujar()
        
        # Actualizar y dibujar partículas
        for particula in particulas[:]:
            pygame.draw.circle(screen, particula['color'], 
                             (int(particula['x']), int(particula['y'])), 
                             particula['size'])
            particula['x'] += particula['speed_x']
            particula['y'] += particula['speed_y']
            particula['life'] -= 1
            if particula['life'] <= 0:
                particulas.remove(particula)
        
        # Verificar si el juego ha terminado
        juego_terminado = all(carta.revelada for carta in cartas_juego)
        if juego_terminado and pares_encontrados == len(cartas):
            if tiene_sonido:
                sonido_win.play()
            
            # Mensaje de victoria
            pygame.draw.rect(screen, (0, 0, 0, 150), (ANCHO//2 - 200, ALTO//2 - 100, 400, 200), border_radius=20)
            mostrar_texto("¡Felicidades!", COLOR_EXITO, ANCHO//2, ALTO//2 - 50, fuente_titulo, True)
            mostrar_texto(f"Completaste el juego en {intentos} intentos", (255, 255, 255), ANCHO//2, ALTO//2 + 20, fuente_principal, True)
            
            # Botón para jugar nuevamente
            boton_jugar = Boton(ANCHO//2 - 100, ALTO//2 + 60, 200, 50, "Jugar de nuevo", COLOR_BOTON, COLOR_BOTON_HOVER)
            if boton_jugar.actualizar(eventos):
                return juego_de_memoria()
            boton_jugar.dibujar()
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Iniciar el juego
if __name__ == "__main__":
    juego_de_memoria()
    pygame.quit()