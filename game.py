import pygame
import random

pygame.init()

# Definindo as cores
CORES = {
    1: (169, 169, 169),         # Cinza
    3: (139, 69, 19),           # Marrom
    5: (0, 128, 0),             # Verde
    10: (255, 255, 255),        # Branco
    float('inf'): (255, 165, 0) # Laranja
}

# configurações de tela
tamanho_celula = 19  # Definindo o tamanho de cada quadradinho
LARGURA_TELA, ALTURA_TELA = tamanho_celula * 42, tamanho_celula * 42 # tela do tamanho do tabueliro

# Criando a tela
screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Board Game com A*")

# Posição inicial do personagem
posicao_personagem = (22, 18)  # Posição inicial do personagem (círculo)

# Lista de amigos com coordenadas de exemplo
amigos = [(4, 12), (5, 34), (9, 8), (23, 37), (35, 14), (36, 36)]

# Função para desenhar o grid do mapa com borda preta em cada célula
def desenhar_mapa(matriz):
    for i, linha in enumerate(matriz):
        for j, custo in enumerate(linha):
            cor = CORES.get(custo, (255, 255, 255)) #cor / cor para valor nao digitado
            pygame.draw.rect(screen, cor, (j * tamanho_celula, i * tamanho_celula, tamanho_celula, tamanho_celula))
            # bordas
            pygame.draw.rect(screen, (0, 0, 0), (j * tamanho_celula, i * tamanho_celula, tamanho_celula, tamanho_celula), 1)

# Função para desenhar o personagem e os amigos
def desenhar_personagens(personagem, amigos):
    # personagem inicial
    pygame.draw.circle(screen, (0, 0, 255), 
                       (personagem[1] * tamanho_celula + tamanho_celula // 2, personagem[0] * tamanho_celula + tamanho_celula // 2),
                       tamanho_celula // 2)

    # amigos
    for amigo in amigos:
        x = amigo[1] * tamanho_celula
        y = amigo[0] * tamanho_celula
        pontos_triangulo = [(x + tamanho_celula // 2, y), (x, y + tamanho_celula), (x + tamanho_celula, y + tamanho_celula)]
        pygame.draw.polygon(screen, (255, 0, 0), pontos_triangulo)

#matriz do tabuleiro
MATRIZ = [
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 10, 10, 10, 10, 10, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 10, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 10, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 10, 5, 5, 5, 5, 10, float('inf'), float('inf'), float('inf'), 5, 1, 5, 5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5],
    [5, 5, 10, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 10, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 10, 10, 10, 10, 10, 10, float('inf'), float('inf'), 1, 1, 1, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5],
    [5, 5, 10, float('inf'), float('inf'), 10, float('inf'), float('inf'), 10, float('inf'), float('inf'), float('inf'), abs(10), float('inf'), float('inf'), 10, float('inf'), float('inf'), float('inf'), float('inf'), 5, float('inf'), float('inf'), 1, 1, 1, 5, 5, 5, 10, 5, 5, 5, 3, 3, 3, 5, 5, 5, 10, 5, 5],
    [5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, float('inf'), float('inf'), float('inf'), 5, float('inf'), float('inf'), float('inf'), 5, 1, 5, 5, 5, 10, 5, 5, 5, 3, abs(3), 3, 5, 5, 5, 10, 5, 5],
    [5, 5, 10, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 10, 10, float('inf'), float('inf'), float('inf'), 5, 5, 5, 5, 5, 1, 5, 5, 5, 10, 5, 5, 5, 3, 3, 3, 5, 5, 5, 10, 5, 5],
    [5, 5, 10, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 10, float('inf'), float('inf'), float('inf'), float('inf'), 5, float('inf'), float('inf'), float('inf'), 5, 1, 5, 5, 5, 10, 5, 5, 5, 3, 3, 3, 5, 5, 5, 10, 5, 5],
    [5, 5, 10, 3, 3, 3, 3, 5, 5, 5, 5, 3, 3, 3, 3, 10, 10, 10, 10, 10, 10, float('inf'), float('inf'), float('inf'), 5, 1, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5],
    [5, 5, 10, 3, 3, 3, 3, 5, abs(5), 5, 5, 3, 3, 3, 3, 10, 5, 5, 5, 5, 10, float('inf'), float('inf'), 1, 1, 1, 5, 5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5],
    [5, 5, 10, 3, 3, 3, 3, 5, 5, 5, 5, 3, 3, 3, 3, 10, 5, 5, 5, 5, 10, float('inf'), float('inf'), float('inf'), 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 10, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 10, 5, 5, 5, 5, 10, float('inf'), float('inf'), float('inf'), 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 10, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 10, 5, 5, 5, 5, 10, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 1, 5, float('inf'), float('inf'), float('inf'), 5, 5, float('inf'), float('inf'), float('inf'), float('inf'), 5, 5, 1, 5, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 5, 1, 5, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 5, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 5, 5],
    [5, 5, 1, 10, 10, float('inf'), float('inf'), 5, 5, float('inf'), float('inf'), float('inf'), 1, 1, 1, 1, 5, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 5, 1, 5, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 5, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 5, 5],
    [5, 5, 1, 5, float('inf'), float('inf'), float('inf'), 5, 5, float('inf'), float('inf'), float('inf'), float('inf'), 5, 5, 1, 5, float('inf'), 1, float('inf'), float('inf'), float('inf'), 1, float('inf'), 5, 1, 5, float('inf'), float('inf'), float('inf'), float('inf'), 1, float('inf'), float('inf'), 5, float('inf'), float('inf'), 1, float('inf'), float('inf'), 5, 5],
    [5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 1, 5, 5, 5, 1, 5, 5, 1, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5],
    [5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5],
    [5, 5, 1, 10, 10, 10, 10, 10, 10, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 1, 5, 5, 5, 5, 5, 1, 5, 5, 1, 5, 10, 5, 5, 5, 1, 5, 5],
    [5, 5, 1, 10, float('inf'), float('inf'), float('inf'), float('inf'), 10, 1, 5, float('inf'), float('inf'), float('inf'), 5, 5, float('inf'), float('inf'), float('inf'), 5, 1, 5, float('inf'), float('inf'), 1, float('inf'), 5, float('inf'), float('inf'), 5, 1, 5, float('inf'), 1, float('inf'), 10, float('inf'), float('inf'), 5, 1, 5, 5],
    [5, 5, 1, 10, float('inf'), float('inf'), float('inf'), float('inf'), 10, 1, 5, float('inf'), float('inf'), float('inf'), 5, 5, float('inf'), float('inf'), abs(1), 1, 1, 5, float('inf'), float('inf'), float('inf'), float('inf'), 5, float('inf'), float('inf'), 5, 1, 5, float('inf'), float('inf'), float('inf'), 10, float('inf'), float('inf'), 5, 1, 5, 5],
    [5, 5, 1, 10, float('inf'), float('inf'), float('inf'), 10, 10, 1, 1, 1, float('inf'), float('inf'), 5, 5, float('inf'), float('inf'), float('inf'), 5, 1, 5, 5, 5, 5, 5, 5, float('inf'), 1, 1, 1, 5, 5, 5, 5, 10, float('inf'), abs(1), 1, 1, 5, 5],
    [5, 5, 1, 10, float('inf'), float('inf'), float('inf'), float('inf'), 10, 1, 5, float('inf'), float('inf'), float('inf'), 5, 5, float('inf'), float('inf'), float('inf'), 5, 1, 5, float('inf'), float('inf'), float('inf'), float('inf'), 5, float('inf'), float('inf'), 5, 1, 5, float('inf'), float('inf'), float('inf'), 10, float('inf'), float('inf'), 5, 1, 5, 5],
    [5, 5, 1, 10, float('inf'), float('inf'), float('inf'), float('inf'), 10, 1, 5, float('inf'), float('inf'), float('inf'), 5, 5, float('inf'), float('inf'), float('inf'), 5, 1, 5, float('inf'), float('inf'), 1, float('inf'), 5, float('inf'), float('inf'), 5, 1, 5, float('inf'), 1, float('inf'), 10, float('inf'), float('inf'), 5, 1, 5, 5],
    [5, 5, 1, 10, 10, 10, 10, 10, 10, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 1, 5, 5, 5, 5, 5, 1, 5, 5, 1, 5, 10, 5, 5, 5, 1, 5, 5],
    [5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5],
    [5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 10, 5, 1, 5, 10, 5, 5, 5, 10, 5, 1, 5, 5, 5, 1, 5, 5, 5, 5, 10, 5, 5, 5, 1, 5, 5],
    [5, 5, 1, 5, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 5, 1, 5, float('inf'), float('inf'), float('inf'), 10, float('inf'), 1, float('inf'), 10, float('inf'), float('inf'), float('inf'), 10, float('inf'), 1, float('inf'), 5, 5, 1, 5, float('inf'), float('inf'), float('inf'), 10, float('inf'), float('inf'), 5, 1, 5, 5],
    [5, 5, 1, 5, float('inf'), float('inf'), 1, 1, float('inf'), float('inf'), 5, 1, 5, float('inf'), 1, float('inf'), 10, float('inf'), float('inf'), float('inf'), 10, float('inf'), 1, float('inf'), 10, float('inf'), float('inf'), float('inf'), 5, 5, 1, 5, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 5, 1, 5, 5],
    [5, 5, 1, 5, 5, 5, 1, 1, 5, 5, 5, 1, 5, 5, 1, 5, 10, 5, 5, 5, 10, 5, 1, 5, 10, 5, 5, 5, 5, 5, 1, 5, 5, 1, 5, 10, 5, 5, 5, 1, 5, 5],
    [5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5],
    [5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1, 10, 10, 10, 10, 1, 5, 5],
    [5, 5, 1, 5, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 5, 1, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1, 10, float('inf'), float('inf'), 10, 1, 5, 5],
    [5, 5, 1, 5, float('inf'), 1, 1, 1, 1, 1, 1, 1, float('inf'), float('inf'), 1, 1, 1, float('inf'), float('inf'), 5, 1, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1, 10, float('inf'), float('inf'), 10, 1, 5, 5],
    [5, 5, 1, 5, float('inf'), 1, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 1, float('inf'), float('inf'), float('inf'), float('inf'), 1, float('inf'), float('inf'), 5, 1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 10, abs(10), float('inf'), 10, 1, 5, 5],
    [5, 5, 1, 5, float('inf'), 1, 1, 1, 1, float('inf'), float('inf'), 1, 1, 1, 1, 1, 1, float('inf'), float('inf'), 5, 1, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1, 10, float('inf'), float('inf'), 10, 1, 5, 5],
    [5, 5, 1, 5, float('inf'), float('inf'), float('inf'), float('inf'), 1, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 5, 1, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1, 10, float('inf'), float('inf'), 10, 1, 5, 5],
    [5, 5, 1, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1, 10, 10, 10, 10, 1, 5, 5],
    [5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
]

# Loop principal do jogo
executando = True
while executando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executando = False

    screen.fill((0, 0, 0))  # Limpa a tela
    desenhar_mapa(MATRIZ)  # Desenha o mapa
    desenhar_personagens(posicao_personagem, amigos)  # Desenha o personagem e os amigos

    pygame.display.flip()

pygame.quit()
