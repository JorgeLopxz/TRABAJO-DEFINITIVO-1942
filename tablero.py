"""
Created by Jorge López in  
Universidad Carlos III de Madrid
"""
import random
import pyxel
import time
from Proyectil import proyectil
from Proyectil import misil_REGULAR
from Proyectil import MisilSuperbombardero
from avion import avion
import constantes
from enemigos import Regular
from enemigos import Rojo
from enemigos import Superbombardero
from enemigos import Bombardero
from islas import islas



class Tablero:
    def __init__(self, ancho: int, alto: int):
        """ Estos parámetros son el ancho y el alto del tablero"""
        self.ancho = ancho
        self.alto = alto

        pyxel.init(self.ancho, self.alto, title="1942")

        """Aquí damos el valor inicial del avión y de seguido creamos una 
        tupla con los enemigos iniciales(Regulares)"""
        self.avion = avion((self.ancho // 2), 200)
        self.proyectil = proyectil(self.avion.x + 6, self.avion.y - 10)
        self.sprite = (0, 6, 4, 22, 16)
        self.size_avion_x = self.sprite[3]
        self.size_avion_y = self.sprite[4]

        self.sizeRegular_x = constantes.SPRITE_REGULAR[3]
        self.sizeRegular_y = constantes.SPRITE_REGULAR[4]

        self.elemento = Regular

        self.contadorReg = 0

        #Aquí creamos una lista para los misiles de cada enemigo
        self.misilesavion_list = []
        self.misilesregular_list = []
        self.misilesbombardero_list = []
        self.misilesSuperbombardero_list = []

        # Con esto indicamos cuantos misiles tienen que recibir estos dos
        # tipos de enemigos para desaparecer.
        self.contador_bombardero = 6
        self.contador_superbombardero = 10

        # Esto da valor al marcador de puntuacion
        self.puntuacion = 0
        self.recordpuntuacion = 9999

        #Aquí creamos una variable para que los misiles de cada enemigo tengan
        # su tipo de clas
        self.regMisil = misil_REGULAR
        self.bombMisil = misil_REGULAR
        self.supBombMisil = MisilSuperbombardero
        self.choice = 1

        self.islas = []
        # Este bucle for rellena la lista islas para que luego estas aparezcan
        for i in constantes.islas:
            self.islas.append(islas(*i))

        # Contadores y listas de enemigos
        self.entities = []
        self.regList = []
        self.numReg = 0
        self.rojoList = []
        self.numRojo = 0
        self.bombarderoList = []
        self.numBombardero = 0
        self.superBombarderoList = []
        self.numSuperBombardero = 0

        # atributos de cada clase de enemigos
        self.rojo = Rojo
        self.regular = Regular
        self.bombardero = Bombardero
        self.superBombardero = Superbombardero
        # atributo especial para aviones rojos
        self.timeRojo = False

        # variable que inicializa el programa
        self.inicio = False
        pyxel.run(self.update, self.draw)

    # Creamos métodos para pintar los diferentes componentes del juego.
    #este metodo pinta la portada
    def __pintarportada(self):
        self.sprite1 = (1, 56, 128, 191, 128)
        self.sprite2 = (2, 0, 128, 64, 128)
        pyxel.blt(5, 40, *self.sprite1,
                      colkey=8)
        pyxel.blt(198, 40, *self.sprite2,
                      colkey=8)

        pyxel.load("usedAssets/my_resource.pyxres")

    # estos metodos pintan los misiles de los aviones
    def __pintarmisil(self):
        for i in self.misilesavion_list :
            i.mover()
            pyxel.blt(i.x, i.y, *i.sprite, colkey=8)
        pyxel.load("usedAssets/my_resource.pyxres")

    def __pintarMisilBombardero(self):
        for i in self.misilesbombardero_list:
            pyxel.blt(i.x, i.y, *i.sprite, colkey=8)

        pyxel.load("usedAssets/my_resource.pyxres")
    def __pintarMisilSuperBombardero(self):
        for l in range(3):
            for i in self.misilesbombardero_list:
                pyxel.blt(i.x, i.y, *i.sprite, colkey=8)

        pyxel.load("usedAssets/my_resource.pyxres")

    def __pintarmisilregular(self):
        for i in self.misilesregular_list:
            pyxel.blt(i.x, i.y, *i.sprite, colkey=8)

        pyxel.load("usedAssets/my_resource.pyxres")

    # este metodo pinta las islas
    def __pintarislas(self):
        for i in self.islas:
            y = pyxel.frame_count % (pyxel.height + 550)
            pyxel.blt(i.x, i.y + y, *i.sprite, colkey=0)
        pyxel.load("usedAssets/my_resource.pyxres")

    # estos metodos pintan los diferentes aviones
    def __pintarAvion(self):
        if pyxel.frame_count % 4 == 0:
            pyxel.blt(self.avion.x, self.avion.y, *self.avion.sprite1,
                      colkey=8)
        else:
            pyxel.blt(self.avion.x, self.avion.y, *self.avion.sprite2,
                      colkey=8)
        pyxel.load("usedAssets/my_resource.pyxres")

    def pintarRegulares(self):
        for enemy in self.regList:
            if enemy.volver:
                pyxel.blt(enemy.x, enemy.y, *enemy.sprite1, colkey=8)
            else:
                pyxel.blt(enemy.x, enemy.y, *enemy.sprite2, colkey=8)

        pyxel.load("usedAssets/my_resource.pyxres")

    def pintarRojos(self):
        for enemy in self.rojoList:
            pyxel.blt(enemy.x, enemy.y, *enemy.sprite, colkey=8)
        pyxel.load("usedAssets/my_resource.pyxres")

    def pintarBombarderos(self):
        for enemy in self.bombarderoList:
            pyxel.blt(enemy.x, enemy.y, *enemy.sprite, colkey=8)

        pyxel.load("usedAssets/my_resource.pyxres")

    def pintarSuperBombarderos(self):
        for enemy in self.superBombarderoList:
            pyxel.blt(enemy.x, enemy.y, *enemy.sprite, colkey=8)

        pyxel.load("usedAssets/example.pyxres")

    # Estos métodos controlan el número de enemigos
    def numRegulares(self):
        if self.inicio:
            if self.numReg < 5:
                self.numReg = 5
            elif self.numReg >= 5:
                if pyxel.frame_count % 120 == 0:
                    self.numReg += 3

    def numRojos(self):
        if self.inicio:
            if pyxel.frame_count % 150 == 0:
                self.timeRojo = True
            if self.numRojo == 5:
                self.timeRojo = False
            if self.timeRojo == True:
                if self.numRojo == 0:
                    self.numRojo = 5
                    self.timeRojo = False

    def numBombarderos(self):
        if self.inicio:
            if pyxel.frame_count % 300 == 0:
                self.numBombardero += 1

    def numSuperBombarderos(self):
        if self.inicio:
            if pyxel.frame_count % 350 == 0:
                self.numSuperBombardero += 1
    # Estos métodos controlan tanto las colisiones por proyectil como las
    # colisiones por contacto y mandan a los aviones a coordenadas infinitas
    def colisiones(self):
        for proyectil in self.misilesavion_list:
            for enemy in self.regList:
                if (enemy.x + 18 > proyectil.x and enemy.x < proyectil.x
                    + 10) and (
                        enemy.y + 10 >= proyectil.y and enemy.y < proyectil.y):
                    enemy.x = 5000000
                    enemy.y = 5000000
                    proyectil.x = 300000
                    proyectil.y = 389000
                    self.puntuacion += 10

        for proyectil in self.misilesavion_list:
            for enemy in self.rojoList:
                if (enemy.x + 16 > proyectil.x and enemy.x < proyectil.x
                    + 10) and (
                        enemy.y + 10 >= proyectil.y and enemy.y < proyectil.y):
                    enemy.x = 500000
                    enemy.y = 500000
                    proyectil.x = 300000
                    proyectil.y = 389000
                    self.numRojo -=1
                    self.puntuacion += 15
                    if self.numRojo == 0:
                        self.rojoList.clear()

        for proyectil in self.misilesavion_list:
            for enemy in self.bombarderoList:

                if (enemy.x + 24 > proyectil.x and enemy.x < proyectil.x
                    + 14) and (
                        enemy.y + 12 >= proyectil.y and enemy.y < proyectil.y):
                    if 0 < self.contador_bombardero <= 6:
                        self.contador_bombardero -= 1
                        proyectil.x = 300000
                        proyectil.y = 389000
                    else:

                        enemy.x = 500000
                        enemy.y = 500000
                        proyectil.x = 300000
                        proyectil.y = 389000
                        self.contador_bombardero = 6
                        self.puntuacion += 25

        for proyectil in self.misilesavion_list:
            for enemy in self.superBombarderoList:
                if (enemy.x + 28 > proyectil.x and enemy.x < proyectil.x
                    + 28) and (
                        enemy.y + 30 >= proyectil.y and enemy.y < proyectil.y):
                    if 0 < self.contador_superbombardero <= 10:
                        self.contador_superbombardero -= 1
                        proyectil.x = 300000
                        proyectil.y = 389000
                    else:

                        enemy.x = 500000
                        enemy.y = 500000
                        proyectil.x = 300000
                        proyectil.y = 389000
                        self.puntuacion += 50

    def colisionesEnemigos(self):
        for proyectil in self.misilesregular_list:
                if (self.avion.x + 18 > proyectil.x and self.avion.x < proyectil.x
                    + 10) and (
                        self.avion.y + 10 >= proyectil.y and self.avion.y <
                        proyectil.y):
                    if self.avion.vidas >0:
                        self.avion.vidas -= 1
                        proyectil.x = 300000
                        proyectil.y = 389000
                    elif self.avion.vidas == 0:
                        self.avion.x = 500000
                        self.avion.y = 500000
                        proyectil.x = 300000
                        proyectil.y = 389000

        for proyectil in self.misilesbombardero_list:
            if (self.avion.x + 18 > proyectil.x and self.avion.x < proyectil.x
                + 10) and (
                    self.avion.y + 10 >= proyectil.y and self.avion.y <
                    proyectil.y):
                    if self.avion.vidas > 0:
                        self.avion.vidas -= 1
                        proyectil.x = 300000
                        proyectil.y = 389000
                    elif self.avion.vidas == 0:
                        self.avion.x = 500000
                        self.avion.y = 500000
                        proyectil.x = 300000
                        proyectil.y = 389000

        for proyectil in self.misilesSuperbombardero_list:
            if (self.avion.x + 18 > proyectil.x and self.avion.x < proyectil.x
                + 10) and (
                    self.avion.y + 10 >= proyectil.y and self.avion.y <
                    proyectil.y):
                    if self.avion.vidas > 0:
                        self.avion.vidas -= 1
                        proyectil.x = 300000
                        proyectil.y = 389000
                    elif self.avion.vidas == 0:
                        self.avion.x = 500000
                        self.avion.y = 500000
                        proyectil.x = 300000
                        proyectil.y = 389000


    def colisionesbtwAviones(self):
        for enemy in self.regList:
            if (enemy.x + 18 > self.avion.x and enemy.x < self.avion.x
                ) and (
                    enemy.y + 10 >= self.avion.y and enemy.y < self.avion.y):
                enemy.x = 5000000
                enemy.y = 5000000
                self.avion.vidas -= 1
                if self.avion.vidas == 0:
                    self.avion.x = 300000
                    self.avion.y = 389000

        for enemy in self.bombarderoList:
            if (enemy.x + 18 > self.avion.x and enemy.x < self.avion.x
                + 10) and (
                    enemy.y + 10 >= self.avion.y and enemy.y < self.avion.y):
                enemy.x = 5000000
                enemy.y = 5000000
                self.avion.vidas -= 1
                if self.avion.vidas == 0:
                    self.avion.x = 300000
                    self.avion.y = 389000

        for enemy in self.superBombarderoList:
            if (enemy.x + 18 > self.avion.x and enemy.x < self.avion.x
                + 10) and (
                    enemy.y + 10 >= self.avion.y and enemy.y < self.avion.y):
                enemy.x = 5000000
                enemy.y = 5000000
                self.avion.vidas -= 1
                if self.avion.vidas == 0:
                    self.avion.x = 300000
                    self.avion.y = 389000


    def draw(self):
        if not self.inicio:
            pyxel.cls(13)
            pyxel.bltm(0, 0, 0, 0, 0, 0, 0)
            self.__pintarportada()
            pyxel.text(90, 210, " PULSE M PARA EMPEZAR", 0)
        else:
            pyxel.cls(5)
            pyxel.bltm(0, 0, 0, 0, 0, 0, 0)

            self.__pintarislas()
            pyxel.text(90, 245, " @ 1984 CAPCOM", 6)
            pyxel.text(105, 1, "HIGH SCORE ", 10)
            pyxel.text(70, 1, "1UP ", 7)
            pyxel.text(170, 1, "2UP ", 6)
            pyxel.text(90, 10, "%i" % (self.puntuacion), 6)
            pyxel.text(150, 10, "%i" % (self.recordpuntuacion), 6)
            self.__pintarAvion()
            self.__pintarmisil()
            self.__pintarmisilregular()
            self.__pintarMisilBombardero()
            self.__pintarMisilSuperBombardero()
            self.pintarRegulares()
            self.pintarRojos()
            self.pintarBombarderos()
            self.pintarSuperBombarderos()

    def update(self):
        # Este if cierra el juego
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_M):
            self.inicio = True
            pyxel.frame_count = 1
        else:
            pyxel.frame_count += 1

        # A continuación como mover el avion
        if pyxel.btn(pyxel.KEY_RIGHT):
            # esto para el avion
            self.avion.mover('derecha', self.ancho)

        if pyxel.btn(pyxel.KEY_LEFT):
            # esto pra el avion
            self.avion.mover('izquierda', self.ancho)

        if pyxel.btn(pyxel.KEY_UP):
            # esto pra el avion
            self.avion.mover('arriba', self.alto)

        if pyxel.btn(pyxel.KEY_DOWN):
            # esto pra el avion
            self.avion.mover('abajo', self.alto)
        # para disparar misiles
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.misilesavion_list.append(proyectil(self.proyectil.x,
                                                      self.proyectil.y))
            self.proyectil = proyectil(self.avion.x + 6, self.avion.y - 10)
        """los tres siguientes bucles añaden misiles a las listas de los 
        diferentes enemigos"""
        if pyxel.frame_count % 90 == 0:
            for enemy in self.regList:
                if enemy.municion == 1:
                    self.misilesregular_list.append(misil_REGULAR(enemy.x, enemy.y))
                    enemy.municion -= 1

        for enemy in self.bombarderoList:
            if enemy.municion <= 3 and enemy.municion >= 0:
                if pyxel.frame_count % 90 == 0:
                    self.misilesbombardero_list.append(
                        misil_REGULAR(enemy.x, enemy.y))
                    enemy.municion -= 1

        for enemy in self.superBombarderoList:
            if pyxel.frame_count % 90 == 0:
                if pyxel.frame_count % 5 == 0:
                    self.misilesbombardero_list.append(
                    MisilSuperbombardero(enemy.x, enemy.y))

        # esto para la puntuacion
        if self.puntuacion > self.recordpuntuacion:
            self.recordpuntuacion = self.puntuacion

        # Llamamos a los métodos que contabilizan el número de enemigos
        self.numRegulares()
        self.numRojos()
        self.numBombarderos()
        self.numSuperBombarderos()
        """Los siguientes condicionales añaden enemigos a sus respectivas 
        listas y les dan unas coordenadas de aparición"""
        if len(self.regList) < self.numReg:
            for i in range(3):
                opciones = (-20, -40, -50)
                x = random.randint(0, 255)
                y = opciones[i]
                self.regList.append(Regular(x, y, "REGULAR"))

        if len(self.rojoList) < self.numRojo:
            for i in range(5):
                opciones = (-10, -30, -50, -70, -90)
                x = opciones[i]
                y = 50
                self.rojoList.append(Rojo(x, y, "ROJO"))

        if len(self.bombarderoList) < self.numBombardero:
            x = 50
            y = -20
            self.bombarderoList.append(Bombardero(x, y, "BOMBARDERO"))

        if len(self.superBombarderoList) < self.numSuperBombardero:
            x = random.randint(20, 220)
            y = random.randint(255, 260)
            self.superBombarderoList.append(Superbombardero(x, y,
                                                            "SUPERBOMBARDERO"))
        """Los siguientes bucles sirven para llevar a cabo el movimiento de 
        cada enemigo"""
        for rojo in self.rojoList:
            self.rojo = rojo
            self.rojo.movimiento()

        for regular in self.regList:
            self.regular = regular
            z = self.regular.y
            u = self.avion.x
            v = self.regular.x
            self.regular.movimiento(z, u, v)

        for superBombardero in self.superBombarderoList:
            self.superBombardero = superBombardero
            z = self.superBombardero.y
            y = random.randint(40, 100)
            self.superBombardero.movimiento(z, y)

        for bombardero in self.bombarderoList:
            self.bombardero = bombardero
            y = self.bombardero.y
            self.bombardero.movimiento(y)

        """Los siguientes bucles sirven para llevar a cabo el movimiento de 
                cada misil"""
        for regMisil in self.misilesregular_list:
            self.regMisil = regMisil
            x = self.avion.x + 5
            y = self.avion.y + 5
            self.regMisil.movimiento(x, y)

        for bombMisil in self.misilesbombardero_list:
            self.bombMisil = bombMisil
            x = self.avion.x + 5
            y = self.avion.y + 5
            self.bombMisil.movimiento(x, y)

            for supBombMisil in self.misilesSuperbombardero_list:
                if self.choice == 1:
                    self.supBombMisil = supBombMisil
                    self.supBombMisil.movimiento1()
                if self.choice == 2:
                    self.supBombMisil = supBombMisil
                    self.supBombMisil.movimiento2()
                if self.choice == 3:
                    self.supBombMisil = supBombMisil
                    self.supBombMisil.movimiento3()
                self.choice += 1

            self.choice = 1

        self.colisiones()
        self.colisionesEnemigos()
        self.colisionesbtwAviones()
        # si el avion se queda sin vidas se termina el juego
        if self.avion.vidas == 0:
            time.sleep(1)
            pyxel.quit()
