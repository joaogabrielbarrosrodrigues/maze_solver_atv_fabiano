import pygame
import sys
import math

from config import (
    LARGURA, TAM,
    FUNDO, BRANCO, PRETO,
    COR_JOGADOR, COR_JOGADOR_BORDA, COR_BRILHO,
    COR_FIM,
)
from maze_generator import criar_grid, gerar_labirinto
from renderer import desenhar, desenhar_pontos
from astar import a_star


pygame.init()

tela = pygame.display.set_mode((LARGURA, LARGURA))
pygame.display.set_caption("Maze Solver - A*")
clock = pygame.time.Clock()

# Velocidade da animação de movimento (pixels por frame)
VELOCIDADE_ANIM = TAM * 0.18


def mover_jogador(grid, jogador, tecla):
    movimentos = {
        pygame.K_w: ("top",    0, -1),
        pygame.K_s: ("bottom", 0,  1),
        pygame.K_a: ("left",  -1,  0),
        pygame.K_d: ("right",  1,  0),
    }
    if tecla not in movimentos:
        return jogador

    parede, di, dj = movimentos[tecla]
    if jogador.paredes[parede]:
        return jogador

    i, j = jogador.i, jogador.j
    return grid[i + di][j + dj]


def desenhar_jogador(tela, px, py, direcao, tick):
    """Desenha o jogador na posição pixel (px, py) com olhos virados para 'direcao'."""
    raio = TAM // 3

    # Leve "bobbing" vertical (sobe/desce suavemente)
    bob = math.sin(tick * 0.12) * 1.5
    cx, cy = int(px), int(py + bob)

    # Sombra
    sombra = pygame.Surface((raio * 2 + 6, raio * 2 + 6), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 60),
                        (0, raio + 4, raio * 2 + 6, raio // 2))
    tela.blit(sombra, (cx - raio - 3, cy - raio - 3 + raio + 6))

    # Corpo
    pygame.draw.circle(tela, COR_JOGADOR, (cx, cy), raio)
    pygame.draw.circle(tela, COR_JOGADOR_BORDA, (cx, cy), raio, 2)

    # Brilho
    pygame.draw.circle(tela, COR_BRILHO,
                       (cx - raio // 3, cy - raio // 3),
                       max(3, raio // 4))

    # Deslocamento dos olhos conforme direção
    offsets = {
        "right": ( 2, 0),
        "left":  (-2, 0),
        "down":  ( 0, 2),
        "up":    ( 0,-2),
    }
    ox, oy = offsets.get(direcao, (0, 0))

    olho_r = max(2, raio // 5)
    pupila_r = max(1, olho_r // 2)
    olho_esq = (cx - raio // 4 + ox, cy - raio // 5 + oy)
    olho_dir = (cx + raio // 4 + ox, cy - raio // 5 + oy)

    pygame.draw.circle(tela, BRANCO, olho_esq, olho_r)
    pygame.draw.circle(tela, BRANCO, olho_dir, olho_r)
    pygame.draw.circle(tela, PRETO, olho_esq, pupila_r)
    pygame.draw.circle(tela, PRETO, olho_dir, pupila_r)

    # Boca
    pygame.draw.line(tela, PRETO,
                     (cx - raio // 3, cy + raio // 4),
                     (cx + raio // 3, cy + raio // 4), 2)


def desenhar_vitoria(tela, tick):
    # Overlay escuro semi-transparente pulsante
    alpha = int(180 + 30 * math.sin(tick * 0.08))
    overlay = pygame.Surface((LARGURA, LARGURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    tela.blit(overlay, (0, 0))

    fonte_titulo = pygame.font.SysFont("consolas", 32, bold=True)
    fonte_sub    = pygame.font.SysFont("consolas", 18)

    # Título com "glow" (renderiza atrás em cor mais escura levemente deslocado)
    for dx, dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
        sombra = fonte_titulo.render("Parabéns! Você venceu!", True, (0, 120, 80))
        tela.blit(sombra, ((LARGURA - sombra.get_width())//2 + dx,
                            LARGURA//2 - 40 + dy))

    titulo = fonte_titulo.render("Parabéns! Você venceu!", True, (80, 255, 160))
    sub    = fonte_sub.render("Pressione R para reiniciar", True, (200, 200, 220))

    tela.blit(titulo, ((LARGURA - titulo.get_width()) // 2, LARGURA // 2 - 40))
    tela.blit(sub,    ((LARGURA - sub.get_width()) // 2,    LARGURA // 2 + 10))


def cell_center(cell):
    return float(cell.i * TAM + TAM // 2), float(cell.j * TAM + TAM // 2)


def main():
    grid = criar_grid()
    gerar_labirinto(grid)

    inicio = grid[0][0]
    fim    = grid[-1][-1]
    jogador = inicio

    # Posição pixel atual do jogador (animação suave)
    px, py = cell_center(inicio)

    caminho  = None
    venceu   = False
    direcao  = "right"
    tick     = 0

    rodando = True
    while rodando:
        clock.tick(60)
        tick += 1

        # Interpola posição pixel em direção ao centro da célula alvo
        alvo_x, alvo_y = cell_center(jogador)
        dx, dy = alvo_x - px, alvo_y - py
        dist = math.hypot(dx, dy)
        if dist > VELOCIDADE_ANIM:
            px += dx / dist * VELOCIDADE_ANIM
            py += dy / dist * VELOCIDADE_ANIM
        else:
            px, py = alvo_x, alvo_y

        # Desenho
        desenhar(tela, grid, caminho)
        desenhar_pontos(tela, inicio, fim)
        desenhar_jogador(tela, px, py, direcao, tick)

        if venceu:
            desenhar_vitoria(tela, tick)

        pygame.display.update()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d) and not venceu:

                    if caminho is None:
                        caminho = a_star(grid, inicio, fim)

                    if jogador in caminho:
                        caminho.remove(jogador)

                    mapa_dir = {
                        pygame.K_w: "up",
                        pygame.K_s: "down",
                        pygame.K_a: "left",
                        pygame.K_d: "right",
                    }
                    direcao = mapa_dir[event.key]

                    jogador = mover_jogador(grid, jogador, event.key)

                    if jogador in caminho:
                        caminho.remove(jogador)

                    if jogador == fim:
                        venceu = True

                elif event.key == pygame.K_r:
                    grid   = criar_grid()
                    gerar_labirinto(grid)
                    inicio = grid[0][0]
                    fim    = grid[-1][-1]
                    jogador = inicio
                    px, py  = cell_center(inicio)
                    caminho = None
                    venceu  = False
                    direcao = "right"
                    tick    = 0

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
