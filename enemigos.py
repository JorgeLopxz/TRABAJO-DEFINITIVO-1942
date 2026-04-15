"""
Created by Jorge López in  
Universidad Carlos III de Madrid
"""

import random
import constantes
import threading as th
import pyxel

class Enemigos:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        #valores por defecto
        self.direccion = 1
        self.velocidad = 1
        self.vidas = 1

    # Este método servirá para que se muevan a una determinada velocidad y
    # dirección
    def mover(self, direccion: str):

        if (direccion.lower() == "derecha"):
            self.x += self.velocidad
        elif (direccion.lower() == "izquierda"):
            self.x -= self.velocidad
        elif (direccion.lower() == "arriba"):
            self.y -= self.velocidad
        elif (direccion.lower() == "abajo"):
            self.y += self.velocidad

    # métodos que llaman al metodo mover(simplemente son para facilitar la
    # lectura y escritura del código)
    def izquierda(self):
        self.mover('izquierda')

    def arriba(self):
        self.mover('arriba')

    def derecha(self):
        self.mover('derecha')

    def abajo(self):
        self.mover('abajo')

class Regular(Enemigos):
    def __init__(self, x, y, tipo):
        super().__init__(x, y, tipo)

        self.sprite = (0, 6, 4, 24, 16)
        self.size_avion_x = self.sprite[3]
        self.size_avion_y = self.sprite[4]
        self.volver = False

        self.velocidad = 2.4
        self.municion = 1

        if self.tipo == "REGULAR":
            self.sprite1 = constantes.SPRITE_REGULAR
            self.sprite2 = (0, 8, 80, 18, -18)

    def movimiento(self, z, u, v):
        # Recibirá tres parámetros: z(posición del regular) v y u( posiciones en el eje x de los dos aviones).
        if self.volver == False:
            self.abajo()
            if z > random.randint(140, 170):
                self.volver = True
            if v < u - self.size_avion_x:
                self.derecha()
            if v > u + self.size_avion_x:
                self.izquierda()
        if self.volver == True:
            self.velocidad = 2.5
            self.arriba()

class Rojo(Enemigos):
    def __init__(self, x, y, tipo):
        super().__init__(x, y, tipo)

        self.sprite = (0, 6, 4, 22, 16)
        self.size_avion_x = self.sprite[3]
        self.size_avion_y = self.sprite[4]

        self.velocidad = 1.5

        if self.tipo == "ROJO":
            self.sprite = constantes.SPRITE_ROJO
    """estos enemigos describan una trayectoria horizontal 
    cuya dirección cambiará en un ángulo de 180 grados al llegar al borde de la pantalla"""
    def movimiento(self):
        self.x += self.velocidad * self.direccion
        if self.x >= 255 - self.size_avion_x:
            self.direccion = -1
        elif self.x <= 0:
            self.direccion = 1

class Bombardero(Enemigos):
    def __init__(self, x, y, tipo):
        super().__init__(x, y, tipo)

        self.sprite = (0, 6, 4, 22, 16)
        self.size_avion_x = self.sprite[3]
        self.size_avion_y = self.sprite[4]

        self.contador = 0
        self.velocidad = 1.5
        self.municion = 999

        if self.tipo == "BOMBARDERO":
            self.sprite = constantes.SPRITE_BOMBARDERO
    """el bombardero describe una trayectoria descendente hasta la posición 
    y = 150, donde comenzará a describir un cuadrado de 100 píxeles de lado
     y posteriormente desaparecerá del mapa por la parte inferior."""
    def movimiento(self, y):
        if y < 150 and self.contador < 1:
            self.abajo()
        else:
            if self.contador < 100:
                self.derecha()
                self.contador += 1.5
            if self.contador >= 100 and self.contador < 200:
                self.arriba()
                self.contador += 1.5
            if self.contador >= 200 and self.contador < 300:
                self.izquierda()
                self.contador += 1.5
            if self.contador >= 300:
                self.abajo()

class Superbombardero(Enemigos):
    def __init__(self, x, y, tipo):
        super().__init__(x, y, tipo)

        self.sprite = (0, 6, 4, 22, 16)
        self.size_avion_x = self.sprite[3]
        self.size_avion_y = self.sprite[4]
        self.vuelta = False

        if self.tipo == "SUPERBOMBARDERO":
            self.sprite = constantes.SPRITE_SUPERBOMBARDERO

    """hace que el superbombardero, que aparece por la parte inferior de la pantalla,
     suba hasta una posición recibida por el parámetro y. 
     Después de esto hará un movimiento similar al de los enemigos rojos."""
    def movimiento(self, z, y):
        if self.vuelta == False:
            self.arriba()
        if z < y:
            self.vuelta = True
        if self.vuelta == True:
            self.x += self.velocidad * self.direccion
            if self.x >= 255 - self.size_avion_x:
                self.direccion = -1
            elif self.x <= 0:
                self.direccion = 1


class MiniBoss(Enemigos):
    def __init__(self, x, y, tipo="MINIBOSS"):
        super().__init__(x, y, tipo)
        self.size_avion_x = 48
        self.size_avion_y = 28
        self.velocidad = 1.2
        self.vidas = 40
        self.entrada_completa = False
        self.disparo_cooldown = 0
        self.fase = 0.0

    def movimiento(self):
        if not self.entrada_completa:
            self.y += 0.8
            if self.y >= 28:
                self.entrada_completa = True
            return

        self.fase += 0.04
        self.x += self.velocidad * self.direccion
        self.y += pyxel.sin(self.fase * 30) * 0.2
        if self.x >= 255 - self.size_avion_x:
            self.direccion = -1
        elif self.x <= 0:
            self.direccion = 1