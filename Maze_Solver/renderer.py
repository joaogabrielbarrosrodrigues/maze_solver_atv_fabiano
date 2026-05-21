import pygame

from config import (
    TAM,
    PRETO,
    BRANCO,
    VERDE,
    VERMELHO
)


def desenhar(tela, grid, caminho=None):

    tela.fill(BRANCO)

    espessura = 2

    for linha in grid:
        for cell in linha:

            x = cell.i * TAM
            y = cell.j * TAM

            if cell.paredes["top"]:
                pygame.draw.line(tela, PRETO, (x, y), (x + TAM, y), espessura)

            if cell.paredes["bottom"]:
                pygame.draw.line(tela, PRETO, (x, y + TAM), (x + TAM, y + TAM), espessura)

            if cell.paredes["left"]:
                pygame.draw.line(tela, PRETO, (x, y), (x, y + TAM), espessura)

            if cell.paredes["right"]:
                pygame.draw.line(tela, PRETO, (x + TAM, y), (x + TAM, y + TAM), espessura)

    if caminho:
        for cell in caminho:

            cx = cell.i * TAM + TAM // 2
            cy = cell.j * TAM + TAM // 2

            pygame.draw.circle(tela, (180, 255, 180), (cx, cy), TAM // 6)
            pygame.draw.circle(tela, VERDE, (cx, cy), TAM // 9)


def desenhar_pontos(tela, inicio, fim):

    pygame.draw.circle(
        tela,
        VERDE,
        (
            inicio.i * TAM + TAM // 2,
            inicio.j * TAM + TAM // 2
        ),
        TAM // 3
    )

    pygame.draw.circle(
        tela,
        VERMELHO,
        (
            fim.i * TAM + TAM // 2,
            fim.j * TAM + TAM // 2
        ),
        TAM // 3
    )