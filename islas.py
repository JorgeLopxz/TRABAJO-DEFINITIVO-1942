"""
Created by Jorge López in  
Universidad Carlos III de Madrid
"""


class islas:
    def __init__(self, x: int, y: int, tipo: str):
        self.x = x
        self.y = y
        self.tipo = tipo

        if tipo == "isla1":
            self.sprite = (0, 0, 0, 27, 67)

        elif tipo == "isla2":
            self.sprite = (0, 16, 86, 66, 58)

        elif tipo == "isla3":
            self.sprite = (0, 4, 145, 208, 105)

        elif tipo == "nube1":
            self.sprite = (0, 45, 22, 36, 19)

        elif tipo == "nube2":
            self.sprite = (0, 60, 50, 30, 14)

        elif tipo == "nube3":
            self.sprite = (0, 120, 17, 29, 18)
