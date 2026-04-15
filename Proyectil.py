"""
Created by Jorge López in  
Universidad Carlos III de Madrid
"""



"""Esta clase esta orientada a los proyectiles del avion del jugador"""
class proyectil:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.sprite = (0, 92, 80, 13, 16)

    # con def mover describimos el movimiento que toma el misil
    def mover(self):
        self.y -= 12

"""Esta clase está orientada a los misiles de cualquiera de los enemigos 
(menos el superBombardero), 
aunque en su nombre indique solamente enemigos regulares"""
class misil_REGULAR:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.sprite = (0, 123, 90, 4, 4)
        self.size_avion_x = self.sprite[3]
        self.size_avion_y = self.sprite[4]
        self.velocidad = 2
        self.direccion = 10
        self.municion = 1
        self.contador = 0
    #el funcionamiento es prácticamente idéntico al de la clase enemigos
    def mover(self, direccion: str):

        if (direccion.lower() == "derecha"):
            self.x += self.velocidad
        elif (direccion.lower() == "izquierda"):
            self.x -= self.velocidad
        elif (direccion.lower() == "arriba"):
            self.y -= self.velocidad
        elif (direccion.lower() == "abajo"):
            self.y += self.velocidad

    def izquierda(self):
        self.mover('izquierda')

    def arriba(self):
        self.mover('arriba')

    def derecha(self):
        self.mover('derecha')

    def abajo(self):
        self.mover('abajo')
    # Este método sirve para que los misiles se muevan con función de
    # autoguiado hacia el avion del jugador durante poco mas de un segundo y
    # despues se mueven hacia abajo
    def movimiento(self, avionX, avionY):
        if self.contador >= 30:
            self.abajo()
            self.contador += 1.5
        if self.contador < 30:
            if self.x < avionX and self.y < avionY:
                self.derecha()
                self.abajo()
                self.contador += 1.5

            if self.x > avionX and self.y < avionY:
                self.izquierda()
                self.abajo()
                self.contador -= 1.5

            if self.x < avionX and self.y > avionY:
                self.derecha()
                self.arriba()
                self.contador -= 1.5

            if self.x > avionX and self.y > avionY:
                self.izquierda()
                self.arriba()
                self.contador -= 1.5

            self.contador += 1.5

class MisilSuperbombardero(misil_REGULAR):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocidad = 2

    def movimiento1(self):
            self.abajo()
            self.izquierda()
    def movimiento2(self):
            self.abajo()
    def movimiento3(self):
            self.abajo()
            self.derecha()
