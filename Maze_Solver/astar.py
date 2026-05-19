import pygame
import sys

from queue import PriorityQueue

from config import LINHAS


def heuristica(a, b):
    return abs(a.i - b.i) + abs(a.j - b.j)


def vizinhos(cell, grid):
    lista = []

    i, j = cell.i, cell.j

    if j > 0 and not cell.paredes["top"] and not grid[i][j - 1].paredes["bottom"]:
        lista.append(grid[i][j - 1])

    if j < LINHAS - 1 and not cell.paredes["bottom"] and not grid[i][j + 1].paredes["top"]:
        lista.append(grid[i][j + 1])

    if i > 0 and not cell.paredes["left"] and not grid[i - 1][j].paredes["right"]:
        lista.append(grid[i - 1][j])

    if i < LINHAS - 1 and not cell.paredes["right"] and not grid[i + 1][j].paredes["left"]:
        lista.append(grid[i + 1][j])

    return lista


def a_star(grid, inicio, fim):
    count = 0

    fila = PriorityQueue()
    fila.put((0, count, inicio))

    came_from = {}

    g_score = {cell: float("inf") for linha in grid for cell in linha}
    g_score[inicio] = 0

    f_score = {cell: float("inf") for linha in grid for cell in linha}
    f_score[inicio] = heuristica(inicio, fim)

    open_set_hash = {inicio}

    while not fila.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        atual = fila.get()[2]
        open_set_hash.remove(atual)

        if atual == fim:
            caminho = []

            while atual in came_from:
                caminho.append(atual)
                atual = came_from[atual]

            caminho.append(inicio)
            caminho.reverse()

            return caminho

        for vizinho in vizinhos(atual, grid):

            temp_g = g_score[atual] + 1

            if temp_g < g_score[vizinho]:

                came_from[vizinho] = atual

                g_score[vizinho] = temp_g
                f_score[vizinho] = temp_g + heuristica(vizinho, fim)

                if vizinho not in open_set_hash:
                    count += 1

                    fila.put((f_score[vizinho], count, vizinho))
                    open_set_hash.add(vizinho)

    return []