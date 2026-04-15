"""
Created by Jorge López in  
Universidad Carlos III de Madrid
"""

import math


# x, y, sprite(lista)-->(tupletupla), vidas


class avion:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.sprite1 = (0, 5, 5, 25, 17)
        self.sprite2 = (0, 38, 5, 25, 17)

        self.vidas = 3
        self.ultima_direccion_horizontal = "derecha"
        self.animacion = 0
        self.rodando = False
        self.rodando_frames = 0
        self.rodando_duracion = 0
        self.rodando_origen_x = x
        self.rodando_origen_y = y
        self.rodando_direccion = 1
        self.invulnerable_frames = 0

    def registrar_movimiento(self, direccion: str):
        if direccion.lower() in ("izquierda", "derecha"):
            self.ultima_direccion_horizontal = direccion.lower()
        self.animacion = (self.animacion + 1) % 120

    def iniciar_loop(self):
        if self.rodando or self.invulnerable_frames > 0:
            return False

        self.rodando = True
        self.rodando_frames = 24
        self.rodando_duracion = 24
        self.rodando_origen_x = self.x
        self.rodando_origen_y = self.y
        self.rodando_direccion = -1 if self.ultima_direccion_horizontal == "derecha" else 1
        self.invulnerable_frames = 32
        return True

    def actualizar_estado(self, size: int):
        if self.invulnerable_frames > 0:
            self.invulnerable_frames -= 1

        if self.rodando_frames > 0:
            progreso = (self.rodando_duracion - self.rodando_frames) / self.rodando_duracion
            desplazamiento_x = int(34 * progreso)
            arco_y = int(18 * math.sin(progreso * math.pi))
            self.x = self.rodando_origen_x + (self.rodando_direccion * desplazamiento_x)
            self.y = self.rodando_origen_y - arco_y
            self.x = max(0, min(self.x, size - self.sprite1[3]))
            self.y = max(0, min(self.y, size - self.sprite1[4]))
            self.rodando_frames -= 1
        elif self.rodando:
            self.rodando = False
            self.y = self.rodando_origen_y

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

        self.registrar_movimiento(direccion)

    def obtener_sprite(self, frame_count: int):
        if self.rodando:
            if frame_count % 2 == 0:
                return self.sprite1, 0, -1
            return self.sprite2, 0, 1

        if self.ultima_direccion_horizontal == "izquierda":
            if (frame_count // 3) % 2 == 0:
                return self.sprite1, -1, 0
            return self.sprite2, -2, 0

        if self.ultima_direccion_horizontal == "derecha":
            if (frame_count // 3) % 2 == 0:
                return self.sprite2, 1, 0
            return self.sprite1, 2, 0

        if (frame_count // 5) % 2 == 0:
            return self.sprite1, 0, 0
        return self.sprite2, 0, 0
