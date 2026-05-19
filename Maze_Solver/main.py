import pygame
import sys

from config import LARGURA, TAM, AZUL

from maze_generator import criar_grid, gerar_labirinto
from renderer import desenhar, desenhar_pontos
from astar import a_star


pygame.init()

tela = pygame.display.set_mode((LARGURA, LARGURA))
pygame.display.set_caption("Maze Solver - A*")


def mover_jogador(grid, jogador, tecla):
    i, j = jogador.i, jogador.j

    movimentos = {
        pygame.K_w: ("top", 0, -1),
        pygame.K_s: ("bottom", 0, 1),
        pygame.K_a: ("left", -1, 0),
        pygame.K_d: ("right", 1, 0),
    }

    if tecla not in movimentos:
        return jogador

    parede, di, dj = movimentos[tecla]

    if jogador.paredes[parede]:
        return jogador

    return grid[i + di][j + dj]


def desenhar_jogador(tela, jogador):
    x = jogador.i * TAM + TAM // 2
    y = jogador.j * TAM + TAM // 2

    pygame.draw.circle(tela, AZUL, (x, y), TAM // 4)


def main():

    grid = criar_grid()

    gerar_labirinto(grid)

    inicio = grid[0][0]
    fim = grid[-1][-1]
    jogador = inicio

    caminho = None

    rodando = True

    while rodando:

        desenhar(tela, grid, caminho)

        desenhar_pontos(tela, inicio, fim)
        desenhar_jogador(tela, jogador)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.KEYDOWN:

                if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):

                    if caminho is None:
                        caminho = a_star(grid, inicio, fim)

                    if jogador in caminho:
                        caminho.remove(jogador)

                    jogador = mover_jogador(grid, jogador, event.key)

                    if jogador in caminho:
                        caminho.remove(jogador)

                elif event.key == pygame.K_r:

                    grid = criar_grid()

                    gerar_labirinto(grid)

                    inicio = grid[0][0]
                    fim = grid[-1][-1]
                    jogador = inicio

                    caminho = None

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
