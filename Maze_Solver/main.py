import pygame
import sys

from config import LARGURA, TAM, AZUL, PRETO, BRANCO

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
    y = jogador.j * TAM // 2 + jogador.j * 0
    y = jogador.j * TAM + TAM // 2

    raio = TAM // 3

    pygame.draw.circle(tela, (20, 90, 255), (x, y), raio)
    pygame.draw.circle(tela, (5, 30, 120), (x, y), raio, 2)

    brilho_x = x - raio // 3
    brilho_y = y - raio // 3
    pygame.draw.circle(tela, (120, 180, 255), (brilho_x, brilho_y), max(3, raio // 4))

    olho_raio = max(2, raio // 5)
    pupila_raio = max(1, olho_raio // 2)

    olho_esquerdo = (x - raio // 4, y - raio // 5)
    olho_direito = (x + raio // 4, y - raio // 5)

    pygame.draw.circle(tela, BRANCO, olho_esquerdo, olho_raio)
    pygame.draw.circle(tela, BRANCO, olho_direito, olho_raio)

    pygame.draw.circle(tela, PRETO, olho_esquerdo, pupila_raio)
    pygame.draw.circle(tela, PRETO, olho_direito, pupila_raio)

    boca_inicio = (x - raio // 3, y + raio // 4)
    boca_fim = (x + raio // 3, y + raio // 4)

    pygame.draw.line(tela, PRETO, boca_inicio, boca_fim, 2)

def desenhar_mensagem_vitoria(tela):
    fonte_titulo = pygame.font.SysFont("arial", 24, bold=True)
    fonte_texto = pygame.font.SysFont("arial", 18)

    mensagem = fonte_titulo.render("Parabéns! Voce venceu!", True, PRETO)
    instrucao = fonte_texto.render("Pressione R para reiniciar", True, PRETO)

    largura_caixa = 360
    altura_caixa = 100
    x_caixa = (LARGURA - largura_caixa) // 2
    y_caixa = (LARGURA - altura_caixa) // 2

    pygame.draw.rect(tela, BRANCO, (x_caixa, y_caixa, largura_caixa, altura_caixa))
    pygame.draw.rect(tela, PRETO, (x_caixa, y_caixa, largura_caixa, altura_caixa), 2)

    tela.blit(
        mensagem,
        (
            (LARGURA - mensagem.get_width()) // 2,
            y_caixa + 25
        )
    )

    tela.blit(
        instrucao,
        (
            (LARGURA - instrucao.get_width()) // 2,
            y_caixa + 60
        )
    )


def main():

    grid = criar_grid()

    gerar_labirinto(grid)

    inicio = grid[0][0]
    fim = grid[-1][-1]
    jogador = inicio

    caminho = None
    venceu = False

    rodando = True

    while rodando:

        desenhar(tela, grid, caminho)

        desenhar_pontos(tela, inicio, fim)
        desenhar_jogador(tela, jogador)

        if venceu:
            desenhar_mensagem_vitoria(tela)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.KEYDOWN:

                if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d) and not venceu:

                    if caminho is None:
                        caminho = a_star(grid, inicio, fim)

                    if jogador in caminho:
                        caminho.remove(jogador)

                    jogador = mover_jogador(grid, jogador, event.key)

                    if jogador in caminho:
                        caminho.remove(jogador)

                    if jogador == fim:
                        venceu = True

                elif event.key == pygame.K_r:

                    grid = criar_grid()

                    gerar_labirinto(grid)

                    inicio = grid[0][0]
                    fim = grid[-1][-1]
                    jogador = inicio

                    caminho = None
                    venceu = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()