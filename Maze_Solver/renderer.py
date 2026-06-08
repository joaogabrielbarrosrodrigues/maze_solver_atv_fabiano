import pygame

from config import (
    TAM,
    FUNDO, COR_CELULA, COR_PAREDE,
    COR_CAMINHO, COR_CAMINHO_HALO,
    COR_INICIO, COR_FIM,
    BRANCO,
)


def desenhar(tela, grid, caminho=None):
    tela.fill(FUNDO)

    # Fundo de cada célula
    for linha in grid:
        for cell in linha:
            x = cell.i * TAM
            y = cell.j * TAM
            pygame.draw.rect(tela, COR_CELULA, (x + 1, y + 1, TAM - 2, TAM - 2))

    # Caminho sugerido pelo A*
    if caminho:
        for cell in caminho:
            cx = cell.i * TAM + TAM // 2
            cy = cell.j * TAM + TAM // 2
            # halo externo
            pygame.draw.circle(tela, COR_CAMINHO_HALO, (cx, cy), TAM // 5)
            # ponto central
            pygame.draw.circle(tela, COR_CAMINHO, (cx, cy), TAM // 8)

    # Paredes
    espessura = 2
    for linha in grid:
        for cell in linha:
            x = cell.i * TAM
            y = cell.j * TAM
            if cell.paredes["top"]:
                pygame.draw.line(tela, COR_PAREDE, (x, y), (x + TAM, y), espessura)
            if cell.paredes["bottom"]:
                pygame.draw.line(tela, COR_PAREDE, (x, y + TAM), (x + TAM, y + TAM), espessura)
            if cell.paredes["left"]:
                pygame.draw.line(tela, COR_PAREDE, (x, y), (x, y + TAM), espessura)
            if cell.paredes["right"]:
                pygame.draw.line(tela, COR_PAREDE, (x + TAM, y), (x + TAM, y + TAM), espessura)


def _bandeira(tela, cx, cy, cor):
    """Desenha um símbolo de bandeirinha simples."""
    raio = TAM // 3

    # círculo base
    pygame.draw.circle(tela, cor, (cx, cy), raio)
    # anel
    pygame.draw.circle(tela, BRANCO, (cx, cy), raio, 2)

    # letra (S para início, F para fim)
    fonte = pygame.font.SysFont("consolas", raio, bold=True)
    letra = "S" if cor == COR_INICIO else "F"
    surf = fonte.render(letra, True, BRANCO)
    tela.blit(surf, (cx - surf.get_width() // 2, cy - surf.get_height() // 2))


def desenhar_pontos(tela, inicio, fim):
    _bandeira(
        tela,
        inicio.i * TAM + TAM // 2,
        inicio.j * TAM + TAM // 2,
        COR_INICIO,
    )
    _bandeira(
        tela,
        fim.i * TAM + TAM // 2,
        fim.j * TAM + TAM // 2,
        COR_FIM,
    )
