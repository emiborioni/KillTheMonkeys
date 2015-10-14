#! /usr/bin/env python
# -*- coding: utf-8 -*-
#Probando github
import pilasengine
import random

TIEMPO = 6
fin_de_juego = False

pilas = pilasengine.iniciar()
# Usar un fondo estándar
pilas.fondos.Pasto()
# Añadir un marcador
puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.rojo)
puntos.magnitud = 40
# Añadir el conmutador de Sonido
pilas.actores.Sonido()

# Variables y Constantes
balas_simples = pilas.actores.Bala
monos = []

# Funciones
#Elimina el actor Mono cuando una bala impacta en él
def mono_destruido(bala, enemigo):
    enemigo.eliminar()
    bala.eliminar()
    
    a = monos.index(enemigo)
    del monos[a]

    puntos.escala=[1, 0, 5, 1], .1
    puntos.aumentar(1)

#Finaliza el juego cuando un actor Mono impacta en la torreta
def perder(torreta, enemigo):
    global fin_de_juego
    torreta.eliminar()
    enemigo.sonreir()
    texto1=pilas.actores.Texto("GAME OVER")
    texto1.y= 100
    texto2=pilas.actores.Texto("Perdiste conseguiste %d puntos" % (puntos.obtener()))
    texto2.y= -100
    fin_de_juego=True

#Crea nuevos enemigos y les da sus características
def crear_mono():
    global fin_de_juego
    efecto=random.uniform(.25,.75)
    # Crear un enemigo nuevo
    enemigo = pilas.actores.Mono()
    # Hacer que se aparición sea con un efecto bonito
    abc=random.uniform(0.25, 0.75)
    ##la escala varíe entre 0,25 y 0,75 (Ojo con el radio de colisión)
    enemigo.escala=(1,efecto),1
    enemigo.radio_de_colision= efecto*50
    # Dotarle de la habilidad de que explote al ser alcanzado por un disparo
    enemigo.aprender(pilas.habilidades.PuedeExplotar)
    # Situarlo en una posición al azar, no demasiado cerca del jugador
    x = random.randrange(-320, 320)
    y = random.randrange(-240, 240)
    if x >= 0 and x <= 100:
        x = 180
    elif x <= 0 and x >= -100:
        x = -180
    if y >= 0 and y <= 100:
        y = 180
    elif y <= 0 and y >= -100:
        y = -180
    enemigo.x = x
    enemigo.y = y
    # Dotarlo de un movimiento irregular más impredecible
    tipo_interpolacion = ['lineal',
                            'aceleracion_gradual',
                            'desaceleracion_gradual',
                            'rebote_inicial',
                            'rebote_final']
    
    duracion = 1 +random.random()*4
    
    pilas.utils.interpolar(enemigo, 'x', 0, duracion)
    pilas.utils.interpolar(enemigo, 'y', 0, duracion)
    #enemigo.x = pilas.interpolar(0,tiempo,tipo=random.choice(tipo_interpolacion))
    #enemigo.y = pilas.interpolar(0, tiempo,tipo=random.choice(tipo_interpolacion))
    # Añadirlo a la lista de enemigos
    monos.append(enemigo)
    # Permitir la creación de enemigos mientras el juego esté en activo
    if fin_de_juego:
        return False
    else:
        return True


# Añadir la torreta del jugador
torreta = pilas.actores.Torreta(enemigos=monos, cuando_elimina_enemigo=mono_destruido)

crear = pilas.tareas.agregar(1, crear_mono)

#Colision de los enemigos con la torreta
pilas.colisiones.agregar(torreta, monos, perder)


# Arrancar el juego
pilas.ejecutar()
