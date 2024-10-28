import pygame
import random
import time

inicio_prog = time.time()

#classes
class Node:
    def __init__(self, x: int, y: int, custo_acumulado=0, custo_heuristico=0, parent = None):
        #localizações
        self.x = x
        self.y = y
        #custos
        self.custo_acumulado = custo_acumulado
        self.custo_heuristico = custo_heuristico
        self.f = custo_acumulado + custo_heuristico # f = g + h
        self.parent = parent
        
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other) -> bool:
        return self.f < other.f
    
#funções backend

#função de sorteio de amigos
def sorteio_amigos(amigos):
    aceitos = random.sample(amigos, 3)
    nao_aceitos = [amigo for amigo in amigos if amigo not in aceitos]
    return aceitos, nao_aceitos

#menor distancia em uma matriz horinzontal/vertical
def distancia_manhattan(ponto1: Node, ponto2: Node) -> int:
    return abs(ponto1.x - ponto2.x) + abs(ponto1.y - ponto2.y)

def obter_vizinhos(no: Node, matriz_terreno: list) -> list:
    vizinhos = []
    movimentos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for movimento in movimentos:
        novo_x = no.x + movimento[0]
        novo_y = no.y + movimento[1]
        
        if 0 <= novo_x < len(matriz_terreno) and 0 <= novo_y < len(matriz_terreno[0]) and matriz_terreno[novo_x][novo_y] < float('inf'):
            vizinhos.append(Node(novo_x, novo_y, 0, 0, no))
            
    return vizinhos

def AStar(origem: Node, destino: Node, matriz_terreno: list) -> tuple:
    lista_aberta = []
    lista_fechada = []
    
    lista_aberta.append(origem)
    
    while lista_aberta:
        atual: Node = min(lista_aberta, key=lambda n: n.f)
        
        if atual == destino:
            custo = atual.custo_acumulado
            caminho = []
            
            while atual.parent:
                dx, dy = atual.x - atual.parent.x, atual.y - atual.parent.y
                
                if dx == 0 and dy == 1:
                    caminho.append('direita')
                    
                if dx == 1 and dy == 0:
                    caminho.append('baixo')
                    
                if dx == 0 and dy == -1:
                    caminho.append('esquerda')
                    
                if dx == -1 and dy == 0:
                    caminho.append('cima')
                    
                atual = atual.parent
                
            return custo, caminho[::-1]
        
        lista_aberta.remove(atual)
        lista_fechada.append(atual)
        
        for vizinho in obter_vizinhos(atual, matriz_terreno):
            g = atual.custo_acumulado + matriz_terreno[vizinho.x][vizinho.y]
            h = distancia_manhattan(vizinho, destino)
            vizinho.custo_heuristico = h
            
            if vizinho in lista_fechada:
                continue
            
            if vizinho not in lista_aberta:
                lista_aberta.append(vizinho)
                vizinho.custo_acumulado = g
                vizinho.f = g + h
            else:
                if g < vizinho.custo_acumulado:
                    vizinho.custo_acumulado = g
                    vizinho.f = g + h
                    
    return None, []

def encontrar_amigo_mais_proximo(atual: Node, amigos: list) -> Node:
    amigos_mais_proximo = None
    menor_distancia = float('inf')
    
    for amigo in amigos:
        distancia = distancia_manhattan(atual, amigo)
        if distancia < menor_distancia:
            menor_distancia = distancia
            amigos_mais_proximo = amigo
            
    return amigos_mais_proximo

def busca_amigos(origem: Node, amigos: list[Node], matriz_terreno: list) -> list:
    aceitos, nao_aceitos = sorteio_amigos(amigos)
    aceitos_encontrados = 0
    retorno = origem
    custo_total = 0
    todos_movimentos = []
    
    while aceitos_encontrados < 3:
        amigo_mais_proximo = encontrar_amigo_mais_proximo(origem, amigos)
        
        custo, movimentos = AStar(origem, amigo_mais_proximo, matriz_terreno)
        custo_total += custo
        origem = amigo_mais_proximo
        
        for movimento in movimentos:
            todos_movimentos.append(movimento)
            
        aceitou = amigo_mais_proximo in aceitos
        print(f'Custo para encontrar o amigo {amigo_mais_proximo.x, amigo_mais_proximo.y}: {custo}, aceitou? {'Sim' if aceitou == True else 'Não'}')
        
        if aceitou:
            aceitos_encontrados += 1
            if aceitos_encontrados >= 3:
                print('3 amigos encontrados, vamos retornar para a casa!')
                
        amigos.remove(amigo_mais_proximo)
        
    custo_retorno, movimentos_retorno = AStar(origem, retorno, matriz_terreno)
    custo_total += custo_retorno
    
    for movimento in movimentos_retorno:
        todos_movimentos.append(movimento)
        
    print(f'Retornamos para a casa e o custo foi: {custo}')
    print(f'O custo total foi: {custo_total}')
    return aceitos, todos_movimentos

# parametros do jogo:

pygame.init()

# Definindo as cores
CORES = {
    1: (32, 32, 32),            # Cinza
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
def desenhar_personagens(personagem, amigos, amigos_aceitos):
    # personagem inicial
    pygame.draw.circle(screen, (0, 0, 255), 
                       (personagem[1] * tamanho_celula + tamanho_celula // 2, personagem[0] * tamanho_celula + tamanho_celula // 2),
                       tamanho_celula // 2)

    # amigos
    for amigo in amigos:
        cor = (255, 0, 0) if amigo not in amigos_aceitos else (0, 0, 255)
        x = amigo[1] * tamanho_celula
        y = amigo[0] * tamanho_celula
        pontos_triangulo = [(x + tamanho_celula // 2, y), (x, y + tamanho_celula), (x + tamanho_celula, y + tamanho_celula)]
        pygame.draw.polygon(screen, cor, pontos_triangulo)

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
def jogo_principal(matriz, posicao_inicial, amigos, amigos_aceitos, movimentos):
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
        desenhar_personagens(posicao_personagem, amigos, amigos_aceitos)
        
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

INICIO = Node(22, 18)
PERSONAGENS = [Node(4, 12), Node(5, 34), Node(9, 8), Node(23, 37), Node(35, 14), Node(36, 36)]
#PERSONAGENS = [Node(23, 37), Node(35, 14), Node(36, 36)] #caminho mais curto

start = (INICIO.x, INICIO.y)
lista_amigos = []
lista_amigos_aceitos = []

for personagem in PERSONAGENS:
    lista_amigos.append((personagem.x, personagem.y))

aceitos, movimentos = busca_amigos(INICIO, PERSONAGENS, MATRIZ)

for aceito in aceitos:
    lista_amigos_aceitos.append((aceito.x, aceito.y))

print("Amigos que aceitaram:", [(amigo.x, amigo.y) for amigo in aceitos])
print(f"Total de movimentos: {len(movimentos)}")

fim_prog = time.time()

print(fim_prog - inicio_prog)

jogo_principal(MATRIZ, start, lista_amigos, lista_amigos_aceitos, movimentos)