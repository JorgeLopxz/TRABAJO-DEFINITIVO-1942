"""
Created by Jorge López in  
Universidad Carlos III de Madrid
"""

import pyxel
from Proyectil import proyectil


# x, y, sprite(lista)-->(tupletupla), vidas


class avion:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.sprite1 = (0, 5, 5, 25, 17)
        self.sprite2 = (0, 38, 5, 25, 17)

        self.vidas = 3

    def mover(self, direccion: str, size: int):
        size_avion_x = self.sprite1[3] or self.sprite2[3]
        size_avion_y = self.sprite1[4] or self.sprite2[4]

        if (direccion.lower() == "derecha" and
                self.x < size - size_avion_x):
            self.x += 3.25
        elif (direccion.lower() == "izquierda" and
              self.x > 0):
            self.x -= 3.25
        elif (direccion.lower() == "arriba" and
              self.y):
            self.y -= 3.25
        elif (direccion.lower() == "abajo" and
              self.y < size - size_avion_y):
            self.y += 3.25
