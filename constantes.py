"""
Created by Jorge López in  
Universidad Carlos III de Madrid
"""
import random

ANCHO = 224
ALTO = 256

# Avión
AVION_INICIAL = (ANCHO / 2, 200)
AVION_SPRITE = (1, 0, 0, 25, 16)

# Enemigos
SPRITE_REGULAR = (0, 9, 84, 16, 10)
SPRITE_ROJO = (0, 4, 160, 18, 18)
SPRITE_SUPERBOMBARDERO = (0, 130, 39, 33, 32)
SPRITE_BOMBARDERO = (0, 127, 22, 30, 16)
ENEMIGOS_INICIAL = ((random.randint(0, 200), random.randint(0, 100),
                     "REGULAR"),
                    (random.randint(0, 200), random.randint(0, 100),
                     "REGULAR"),
                    (random.randint(0, 200), random.randint(0, 100),
                     "REGULAR"),
                    (random.randint(0, 200), random.randint(0, 100),
                     "REGULAR"))
ENEMIGOS_REGULAR = ((random.randint(0, 200), random.randint(0, 100),
                     "REGULAR"),
                    (random.randint(0, 200), random.randint(0, 100),
                     "REGULAR"))

ENEMIGOS_ROJO = (random.randint(0, 200), random.randint(0, 100), "ROJO")
ENEMIGOS_SUPERBOMBARDERO = (random.randint(0, 200), random.randint(0, 100),
                            "SUPERBOMBARDERO")
ENEMIGOS_BOMBARDERO = (random.randint(0, 200),
                       random.randint(0, 100), "BOMBARDERO")


#misiles

proyectiles_avion = []

# islas

islas = ((0, -70, "isla1"), (140, -200,"isla2"), (15, -500, "isla3"),
         (40, -240,"nube1"),(120,-500, "nube2"),(180,-300,"nube3"))
