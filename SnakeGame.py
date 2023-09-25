import pygame
from pygame.locals import *
import sys
from random import choice
from collections import deque

# Clase fruta
class Fruta:
    def __init__(self):
        self.lista_posiciones = list(range(0, 601, 50))
        self.posicion_x = choice(self.lista_posiciones)
        self.posicion_y = choice(self.lista_posiciones)
        self.posicion_fruta = (self.posicion_x, self.posicion_y)
    
    def imprimir_fruta(self):
        # Se crea la fruta como un objeto y se imprime
        fruta = pygame.Rect(self.posicion_x, self.posicion_y, 50, 50)
        pygame.draw.rect(ventana, color_fruta, fruta )
    
    def actualizar_posicion(self):
        self.posicion_x = choice(self.lista_posiciones)
        self.posicion_y = choice(self.lista_posiciones)
        self.posicion_fruta = (self.posicion_x, self.posicion_y)

# Clase serpiente
class Serpiente:
    def __init__(self):
        self.cuerpo_serpiente = deque([(300, 400), (300, 350), (300, 300)])
        self.movimiento_x = 0
        self.movimiento_y = -50
        self.donde = "arriba"

    def imprimir_serpiente(self):
        # Se itera sobre las diferentes posiciones del cuerpo de la serpiente
        for posicion in self.cuerpo_serpiente:
            posicion_x = posicion[0]
            posicion_y = posicion[1]
            # Se crea un pedacito de la serpiente como objeto y se imprime
            # Si es la cabeza
            if posicion == self.cuerpo_serpiente[-1]:
                bloque = pygame.Rect(posicion_x, posicion_y, 50, 50)
                pygame.draw.rect(ventana, color_cabeza, bloque)
            else:
                bloque = pygame.Rect(posicion_x, posicion_y, 50, 50)
                pygame.draw.rect(ventana, color_serpiente, bloque)
    
    def mover_serpiente(self):
        # Si el movimiento es valido:
        # Quitamos la cola
        self.cuerpo_serpiente.popleft()

        #Definimos a la nueva cabeza
        cabeza_antigua_x, cabeza_antigua_y = self.cuerpo_serpiente[-1]
        nueva_cabeza = (cabeza_antigua_x + self.movimiento_x, cabeza_antigua_y + self.movimiento_y)
        self.cuerpo_serpiente.append(nueva_cabeza)

    def incrementar_tamaño(self):
        cola = self.cuerpo_serpiente[0]
        self.mover_serpiente()
        self.cuerpo_serpiente.appendleft(cola)

    
    def colision_fruta(self, posicion_fruta):
        if self.cuerpo_serpiente[-1] == posicion_fruta:
            fruta.actualizar_posicion()
            return True
    
    def colision_cuerpo(self):
        cabeza = self.cuerpo_serpiente[-1]
        for posicion in range(len(self.cuerpo_serpiente) - 1):
            if cabeza == self.cuerpo_serpiente[posicion]:
                return True
            else:
                continue






# Se inicializan todas las funciones del modulo de pygame
pygame.init()

# Creamos nuestra ventana del juego:
ancho = 650 
alto = 650
ventana = pygame.display.set_mode((ancho, alto))

# Nombre de la ventana
pygame.display.set_caption("Snake Game")

# Colores:
color_fondo = (0, 0, 0)
color_fruta = (255, 0, 0)
color_serpiente = (0, 255, 0)
color_cabeza = (100, 154, 200)

# Limitante de fps:
reloj = pygame.time.Clock()

# Creamos un objeto del tipo Fruta
fruta = Fruta()

# Creamos el objeto de serpiente
serpiente = Serpiente()

# Empezamos el bucle del juego:
while(True):

    # Se da el color del fondo
    ventana.fill(color_fondo)

    # Se dibuja la fruta
    fruta.imprimir_fruta()

    # Se dibuja la serpiente
    serpiente.imprimir_serpiente()

    # Eventos:
    for event in pygame.event.get():
        # El primer evento del juego, cerrarlo con la x:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        # Cuando el jugador pulsa las teclas:
        elif event.type == pygame.KEYDOWN:
            if event.key == K_UP and serpiente.donde != "abajo":
                serpiente.movimiento_x = 0
                serpiente.movimiento_y = -50
                serpiente.donde = "arriba"

            elif event.key == K_DOWN and serpiente.donde != "arriba":
                serpiente.movimiento_x = 0
                serpiente.movimiento_y = 50
                serpiente.donde = "abajo"
            
            elif event.key == K_RIGHT and serpiente.donde != "izquierda":
                serpiente.movimiento_x = 50
                serpiente.movimiento_y = 0
                serpiente.donde = "derecha"
            
            elif event.key == K_LEFT and serpiente.donde != "derecha":
                serpiente.movimiento_x = -50
                serpiente.movimiento_y = 0
                serpiente.donde = "izquierda"
        
    # Colisiones:
    # Con la fruta:
    if serpiente.colision_fruta(fruta.posicion_fruta):
        while(fruta.posicion_fruta in serpiente.cuerpo_serpiente):
            serpiente.colision_fruta(fruta.posicion_fruta)
        serpiente.incrementar_tamaño()
    
    # Con la serpiente y la pared
    if serpiente.colision_cuerpo() or serpiente.cuerpo_serpiente[-1][0] >= 650 or serpiente.cuerpo_serpiente[-1][1] >= 650 or serpiente.cuerpo_serpiente[-1][0] < 0 or serpiente.cuerpo_serpiente[-1][1] < 0:
        ventana.fill(color_fruta)
        mi_fuente = pygame.font.Font(r'C:\Users\Alejandro Montoya V\Desktop\EDD\Snake game\gnarly_skeleton\fuente.otf', 50)
        texto = mi_fuente.render("Game over", True, (0, 0, 0))
        ventana.blit(texto, (210, 300))
        

    # Se actualiza la serpiente
    serpiente.mover_serpiente()


    # Se actualiza la ventana
    pygame.display.update()
    reloj.tick(15)



