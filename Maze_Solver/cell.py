class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j

        self.paredes = {
            "top": True,
            "bottom": True,
            "left": True,
            "right": True
        }

        self.visitado = False

    def __lt__(self, outro):
        return False