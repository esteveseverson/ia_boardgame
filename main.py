#imports
import random

#classes
class Node:
    def __init__(self, x: int, y: int, custo_acumulado=0, custo_heuristico=0):
        #localizações
        self.x = x
        self.y = y
        #custos
        self.custo_acumulado = custo_acumulado
        self.custo_heuristico = custo_heuristico
        self.f = custo_acumulado + custo_heuristico # f = g + h
        
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other) -> bool:
        return self.f < other.f
    
def sorteio_amigos(amigos):
    aceitos = random.sample(amigos, 3)
    nao_aceitos = [amigo for amigo in amigos if amigo not in aceitos]
    return aceitos, nao_aceitos

def distancia_manhattan(ponto1: tuple, ponto2: tuple) -> int:
    return abs(ponto1.x - ponto2.x) + abs(ponto1.y - ponto2.y)

def obter_vizinhos(no: tuple, matriz_terreno: list) -> list:
    vizinhos = []
    movimentos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for movimento in movimentos:
        novo_x = no.x + movimento[0]
        novo_y = no.y + movimento[1]
        
        if 0 <= novo_x < len(matriz_terreno) and 0 <= novo_y < len(matriz_terreno[0]) and matriz_terreno[novo_x][novo_y] < float('inf'):
            vizinhos.append(Node(novo_x, novo_y, 0, 0))
            
    return vizinhos

def AStar(origem: tuple, destino: tuple, matriz_terreno: list) -> int | str:
    lista_aberta = []
    lista_fechada = []
    
    lista_aberta.append(origem)
    
    while lista_aberta:
        atual = min(lista_aberta, key=lambda n: n.f)
        
        if atual == destino:
            return atual.custo_acumulado
        
        lista_aberta.remove(atual)
        lista_fechada.append(atual)
        
        for vizinho in obter_vizinhos(atual, matriz_terreno):
            g = atual.custo_acumulado + matriz_terreno[vizinho.x][vizinho.y]
            h = distancia_manhattan(vizinho, destino)
            
            if vizinho not in lista_fechada or g < vizinho.custo_acumulado:
                if vizinho not in lista_aberta:
                    lista_aberta.append(vizinho)
                    
                vizinho.custo_acumulado = g
                vizinho.custo_heuristico = h
                
    return 'sem solução'

def busca_amigos(origem: tuple, amigos: list[tuple], matriz_terreno: list) -> list:
    aceitos, nao_aceitos = sorteio_amigos(amigos)
    aceitos_encontrados = 0
    visitado = 1
    custo_total = 0
    
    for amigo in amigos:
        custo = AStar(origem, amigo, matriz_terreno)
        custo_total = custo_total + custo
        aceitou = True if amigo in aceitos else False
        print(f'Custo para encontrar o personagem {visitado}: {custo} aceitou? {aceitou}')
        visitado += 1
        if aceitou == True:
            aceitos_encontrados += 1
            
        if aceitos_encontrados >=3:
            print("Três amigos aceitaram! Voltando a origem")
            #logica de retorno
            break
    
    print(f"O custo total da busca foi: {custo_total}")
    return aceitos

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
    [5, 5, 1, 10, float('inf'), float('inf'), float('inf'), float('inf'), 10, 1, 5, float('inf'), float('inf'), float('inf'), 5, 5, float('inf'), float('inf'), float('inf'), 1, 5, 1, float('inf'), float('inf'), 1, float('inf'), 5, float('inf'), float('inf'), 5, 1, 5, float('inf'), 1, float('inf'), 10, float('inf'), float('inf'), 5, 1, 5, 5],
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

#for i in range (len(PERSONAGENS)):
#    print(f'Distancia entre a origem e o ponto {i}: {distancia_manhattan(INICIO, PERSONAGENS[i])}')
INICIO = Node(18, 22)
PERSONAGENS = [Node(4, 12), Node(5, 34), Node(9, 8), Node(23, 37), Node(35, 14), Node(36, 36)]

aceitos = busca_amigos(INICIO, PERSONAGENS, MATRIZ)
print("Amigos que aceitaram:", [(amigo.x, amigo.y) for amigo in aceitos])