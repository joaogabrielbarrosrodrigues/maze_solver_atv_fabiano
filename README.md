# maze_solver_atv_fabiano

# Maze Solver - A*

Projeto em Python com Pygame que gera um labirinto automaticamente e permite controlar um agente usando as teclas `W`, `A`, `S` e `D`.

O jogo também mostra o caminho ideal até a saída por meio de bolinhas verdes. Conforme o agente passa pelas bolinhas, elas desaparecem, em um estilo parecido com Pac-Man.

## Funcionalidades

- Geração automática de labirinto
- Movimento manual com `W`, `A`, `S` e `D`
- Caminho ideal exibido ao iniciar o movimento
- Bolinhas do caminho somem quando o agente passa por elas
- Reinício do labirinto com a tecla `R`
- Algoritmo A* usado para calcular o melhor caminho

## Tecnologias

- Python
- Pygame

## Requisitos

- Python 3.11
- Pygame

Baixe o Python 3.11 pelo site oficial:

[Download Python 3.11](https://www.python.org/downloads/release/python-3119/)

## Como executar

1. Clone o repositório:

```bash
git clone URL_DO_SEU_REPOSITORIO

py -3.11 -m pip install pygame
py -3.11 main.py
