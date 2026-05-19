import pygame
import sys

from config import TAM, AZUL

from renderer import desenhar, desenhar_pontos


def animar_agente(tela, caminho, inicio, fim, grid):

    for cell in caminho:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        desenhar(tela, grid, caminho)
        desenhar_pontos(tela, inicio, fim)

        x = cell.i * TAM + TAM // 2
        y = cell.j * TAM + TAM // 2

        pygame.draw.circle(tela, AZUL, (x, y), TAM // 5)

        pygame.display.update()

        pygame.time.delay(40)