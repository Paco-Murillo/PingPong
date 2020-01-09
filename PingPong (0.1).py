# Jose Francsisco Murillo
# jfmurillol@gmail.com
# Juego Ping Pong sencillo 1ra version

import pygame
from random import randrange
from enum import IntEnum


class Pantalla(IntEnum):
    inicio = 1
    preferencias = 2
    juego = 3
    victoria = 4
    derrota = 5


class Modo(IntEnum):
    solo = 1
    versus = 2

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 800

# velocidad de Movimiento de Barras y Bola
velBar = 20
velBall = 10
velBarStart = velBar
velBallStart = velBall


# Checa colisiones entre bola y pared
def checkCollisionBall(ballPos, direccion):
    top = ballPos[1]
    bottom = top+ballPos[3]

    if top-velBall <= 100:
        if direccion == 1:
            direccion = 2
        else:
            direccion = 3
    elif bottom+velBall >= ALTO-2:
        if direccion == 2:
            direccion = 1
        else:
            direccion = 4

    return direccion


# Checa colisiones entre bola y ( ping o pong )
def checkCollision(pingPos, pongPos, ballPos, direccion, sonido, keys):

    global velBall
    global velBar

    # Referencia a la Posicion de Ping
    pingRight = pingPos[0] + pingPos[2]
    pingTop = pingPos[1]
    pingBottom = pingTop + pingPos[3]

    # Referencia a la Posicion de Pong
    pongLeft = pongPos[0]
    pongTop = pongPos[1]
    pongBottom = pongTop + pongPos[3]

    # Referencia a la Posicion de la Bola
    ballLeft = ballPos[0]
    ballRight = ballLeft + ballPos[2]
    ballTop = ballPos[1]
    ballBottom = ballTop + ballPos[3]

    if ballBottom > pingTop and ballTop < pingBottom and ballLeft - velBall <= pingRight <= ballLeft:

        pygame.mixer.Sound.play(sonido)

        if velBall < 30:
            velBall += 5

        if velBar < 30:
            velBar += 1

        if keys[pygame.K_w]:
            direccion = 1
        elif keys[pygame.K_s]:
            direccion = 2
        else:
            if direccion == 4:
                direccion = 1
            else:             # if direccion == 3
                direccion = 2

    elif ballBottom > pongTop and ballTop < pongBottom and ballRight <= pongLeft <= ballRight + velBall:

        pygame.mixer.Sound.play(sonido)

        if velBall < 30:
            velBall += 5

        if velBar < 30:
            velBar += 1

        if keys[pygame.K_UP]:
            direccion = 4
        elif keys[pygame.K_DOWN]:
            direccion = 3
        else:
            if direccion == 1:
                direccion = 4
            else:             # if direccion == 2
                direccion = 3

    return direccion


def movBall(ballPos, direccion):
    if direccion == 1:
        ballPos[0] += velBall
        ballPos[1] -= velBall
    elif direccion == 2:
        ballPos[0] += velBall
        ballPos[1] += velBall
    elif direccion == 3:
        ballPos[0] -= velBall
        ballPos[1] += velBall
    elif direccion == 4:
        ballPos[0] -= velBall
        ballPos[1] -= velBall


def checkGoal(ballPos, puntaje, direccion):
    # ballPos = [390, (ALTO+100)//2-10, 20, 20]

    global velBall
    global velBar

    ballLeft = ballPos[0]
    ballRight = ballLeft + ballPos[2]

    if ballLeft <= 1:
        ballPos[0] = 390
        ballPos[1] = (ALTO+100)//2-10
        ballPos[2] = 20
        ballPos[3] = 20
        puntaje["pong"] += 1
        velBall = velBallStart
        velBar = velBarStart
        return randrange(1, 5)
    elif ballRight >= 798:
        ballPos[0] = 390
        ballPos[1] = (ALTO + 100) // 2 - 10
        ballPos[2] = 20
        ballPos[3] = 20
        puntaje["ping"] += 1
        velBall = velBallStart
        velBar = velBarStart
        return randrange(1, 5)

    return direccion


def score(font, puntaje):
    ventana = pygame.display.get_surface()

    ventana.blit(font.render("%02d" % puntaje["ping"], False, (255, 255, 255)), (10, 10))
    ventana.blit(font.render("%02d" % puntaje["pong"], False, (255, 255, 255)), (740, 10))


def movBar(keys, pingPos, pongPos, modo):

    if keys[pygame.K_UP] and pongPos[1]-velBar >= 101:
        pongPos[1] -= velBar
    elif keys[pygame.K_DOWN] and pongPos[1]+pongPos[3]+velBar <= ALTO-1:
        pongPos[1] += velBar
    if modo == Modo.versus:
        if keys[pygame.K_w] and pingPos[1]-velBar >= 101:
            pingPos[1] -= velBar
        elif keys[pygame.K_s] and pingPos[1]+pingPos[3]+velBar <= ALTO-1:
            pingPos[1] += velBar


def juego(font, modo, posiciones, direccion, sonido, puntaje):

    pingPos = posiciones["pingPos"]
    pongPos = posiciones["pongPos"]
    ballPos = posiciones["ballPos"]

    ventana = pygame.display.get_surface()

    # Mapa
    pygame.draw.line(ventana, (127, 127, 127), (0, 100), (ALTO-1, 100))
    pygame.draw.line(ventana, (127, 127, 127), (0, ALTO-1), (ALTO-1, ALTO-1))
    pygame.draw.line(ventana, (127, 127, 127), (0, 100), (0, ALTO-1))
    pygame.draw.line(ventana, (127, 127, 127), (ALTO-1, 100), (ALTO-1, ALTO-1))

    # Objetos
    pygame.draw.rect(ventana, (255, 255, 255), pingPos)
    pygame.draw.rect(ventana, (255, 255, 255), pongPos)
    pygame.draw.rect(ventana, (255, 255, 255), ballPos)

    keys = pygame.key.get_pressed()

    # Logica del juego
    direccion = checkCollision(pingPos, pongPos, ballPos, direccion, sonido, keys)
    direccion = checkCollisionBall(ballPos, direccion)
    movBall(ballPos, direccion)
    movBar(keys, pingPos, pongPos, modo)
    direccion = checkGoal(ballPos, puntaje, direccion)
    score(font, puntaje)


    return direccion


def juego_init():

    #Inicializacion del modulo de Pygame
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana de dibujo
    pygame.display.set_caption("ピングッポング (Ping Pong)")
    reloj = pygame.time.Clock()  # Para limitar los fps
    termina = False

    font = pygame.font.Font("8-BIT WONDER.TTF", 30)

    #Inicializacion de musica
    pygame.mixer.init()
    sonido = pygame.mixer.Sound("Ping Pong.wav")

    #Inicio de Modo de Juego y Modo
    modoDeJuego = Pantalla.juego
    modo = Modo.versus

    #Posiciones iniciales
    pingPos = [40, (ALTO+100)//2-60, 20, 120]
    pongPos = [740, (ALTO+100)//2-60, 20, 120]
    ballPos = [390, (ALTO+100)//2-10, 20, 20]
    direccion = randrange(1, 5)
    posiciones = {"pingPos": list(pingPos), "pongPos": list(pongPos), "ballPos": list(ballPos)}
    puntaje = {"ping": 0, "pong": 0}

    while not termina:

        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                termina = True

        ventana.fill([0, 0, 0])

        if modoDeJuego == Pantalla.juego:
            direccion = juego(font, modo, posiciones, direccion, sonido, puntaje)

        reloj.tick(40)

        pygame.display.update()


def main():
    
    juego_init()


main()
