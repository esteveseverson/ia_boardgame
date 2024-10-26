import pygame
import random
import time

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

# Função para atualizar a posição do personagem
def mover_personagem(movimentos, posicao_inicial):
    x, y = posicao_inicial
    for movimento in movimentos:
        if movimento == "direita":
            y += 1
        elif movimento == "esquerda":
            y -= 1
        elif movimento == "baixo":
            x += 1
        elif movimento == "cima":
            x -= 1
        yield x, y  # Retorna a nova posição a cada movimento

# Loop principal
def jogo_principal(matriz, posicao_inicial, amigos, movimentos):
    posicao_personagem = posicao_inicial
    rodando = True
    
    # Loop de execução dos movimentos
    for nova_posicao in mover_personagem(movimentos, posicao_inicial):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Atualiza a posição do personagem
        posicao_personagem = nova_posicao

        # Redesenha o mapa e os personagens
        screen.fill((0, 0, 0))  # Limpa a tela
        desenhar_mapa(matriz)
        desenhar_personagens(posicao_personagem, amigos)
        
        # Atualiza a tela e espera 0.1s antes do próximo movimento
        pygame.display.flip()
        time.sleep(0.05)
    
    # Encerra o Pygame ao sair do loop
    pygame.quit()

# Configurações iniciais e execução
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

INICIO = (22, 18)  # Posição inicial do personagem
PERSONAGENS = [(4, 12), (5, 34), (9, 8), (23, 37), (35, 14), (36, 36)]
MOVIMENTOS = ['direita', 'direita', 'baixo', 'baixo', 'baixo', 'baixo', 'baixo', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'baixo', 'baixo', 'baixo', 'baixo', 'baixo', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'baixo', 'baixo', 'baixo', 'baixo', 'baixo', 'baixo', 'baixo', 'baixo', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'cima', 'cima', 'cima', 'esquerda', 'esquerda', 'esquerda', 'cima', 'cima', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'baixo', 'baixo', 'direita', 'direita', 'direita', 'direita', 'direita', 'cima', 'cima', 'esquerda', 'esquerda', 'direita', 'direita', 'baixo', 'baixo', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'cima', 'cima', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'baixo', 'baixo', 'direita', 'direita', 'direita', 'baixo', 'baixo', 'baixo', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'cima', 'cima', 'cima', 'cima', 'direita', 'direita', 'esquerda', 'esquerda', 'cima', 'cima', 'cima', 'cima', 'direita', 'direita', 'direita', 'direita', 'direita', 'cima', 'cima', 'cima', 'cima', 'cima', 'cima', 'cima', 'cima', 'cima', 'esquerda', 'esquerda', 'direita', 'direita', 'cima', 'cima', 'cima', 'cima', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'cima', 'cima', 'cima', 'cima', 'cima', 'cima', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'cima', 'cima', 'cima', 'cima', 'cima', 'cima', 'direita', 'cima', 'cima', 'esquerda', 'baixo', 'baixo', 'baixo', 'baixo', 'baixo', 'baixo', 'baixo', 'baixo', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'cima', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'cima', 'cima', 'cima', 'cima', 'cima', 'cima', 'cima', 'cima', 'baixo', 'baixo', 'baixo', 'esquerda', 'esquerda', 'esquerda', 'esquerda', 'baixo', 'baixo', 'baixo', 'baixo', 'direita', 'direita', 'direita', 'direita', 'direita', 'direita', 'baixo', 'baixo', 'baixo', 'direita', 'baixo', 'baixo', 'baixo', 'baixo', 'baixo', 'direita', 'direita', 'direita', 'direita', 'direita', 'baixo', 'baixo', 'baixo', 'esquerda', 'esquerda']  # Lista de movimentos gerada pelo A*

jogo_principal(MATRIZ, INICIO, PERSONAGENS, MOVIMENTOS)
