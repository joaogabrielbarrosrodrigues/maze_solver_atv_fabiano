import random

from cell import Cell
from config import LINHAS


def criar_grid():
    return [[Cell(i, j) for j in range(LINHAS)] for i in range(LINHAS)]


def gerar_labirinto(grid):
    stack = []

    atual = grid[0][0]
    atual.visitado = True

    while True:
        vizinhos_nv = []

        i, j = atual.i, atual.j

        if i > 0 and not grid[i - 1][j].visitado:
            vizinhos_nv.append(grid[i - 1][j])

        if i < LINHAS - 1 and not grid[i + 1][j].visitado:
            vizinhos_nv.append(grid[i + 1][j])

        if j > 0 and not grid[i][j - 1].visitado:
            vizinhos_nv.append(grid[i][j - 1])

        if j < LINHAS - 1 and not grid[i][j + 1].visitado:
            vizinhos_nv.append(grid[i][j + 1])

        if vizinhos_nv:
            proximo = random.choice(vizinhos_nv)

            stack.append(atual)

            dx = atual.i - proximo.i
            dy = atual.j - proximo.j

            if dx == 1:
                atual.paredes["left"] = False
                proximo.paredes["right"] = False

            elif dx == -1:
                atual.paredes["right"] = False
                proximo.paredes["left"] = False

            elif dy == 1:
                atual.paredes["top"] = False
                proximo.paredes["bottom"] = False

            elif dy == -1:
                atual.paredes["bottom"] = False
                proximo.paredes["top"] = False

            atual = proximo
            atual.visitado = True

        elif stack:
            atual = stack.pop()

        else:
            break

    grid[0][0].paredes["top"] = False
    grid[LINHAS - 1][LINHAS - 1].paredes["bottom"] = False