#imports
import random

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

#funções

#função de sorteio de amigos
def sorteio_amigos(amigos):
    aceitos = random.sample(amigos, 3)
    nao_aceitos = [amigo for amigo in amigos if amigo not in aceitos]
    return aceitos, nao_aceitos

#menor distancia em uma matriz horinzontal/vertical
def distancia_manhattan(ponto1: Node, ponto2: Node) -> int:
    return abs(ponto1.x - ponto2.x) + abs(ponto1.y - ponto2.y)

#função para obter os quadrados vizinhos
def obter_vizinhos(no: Node, matriz_terreno: list) -> list[Node] | list[str]:
    vizinhos = []
    movimentos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    direcoes = ['direita', 'baixo', 'esquerda', 'cima']
    lista_direc = []
    
    for i, movimento in enumerate(movimentos):
        novo_x = no.x + movimento[0]
        novo_y = no.y + movimento[1]
        
        if 0 <= novo_x < len(matriz_terreno) and 0 <= novo_y < len(matriz_terreno[0]) and matriz_terreno[novo_x][novo_y] < float('inf'):
            vizinhos.append(Node(novo_x, novo_y, 0, 0, no))
            lista_direc.append(direcoes[i])
    
    return vizinhos

# A*
def AStar(origem: Node, destino: Node, matriz_terreno: list) -> int | list:
    lista_aberta = []
    lista_fechada = []
    movimentos_realizados = []
    
    lista_aberta.append(origem)
    
    while lista_aberta:
        atual:Node = min(lista_aberta, key=lambda n: n.f)
        
        if atual == destino:
            custo = atual.custo_acumulado
            caminho = []
            
            while atual.parent:
                dx = atual.x - atual.parent.x
                dy = atual.y - atual.parent.y
                
                if dx == 0 and dy == 1:
                    caminho.append("direita")
                elif dx == 1 and dy == 0:
                    caminho.append("baixo")
                elif dx == 0 and dy == -1:
                    caminho.append("esquerda")
                elif dx == -1 and dy == 0:
                    caminho.append("cima")
                atual = atual.parent
                
            movimentos_realizados.extend(caminho[::-1])
            print(f'movimentos realizados: {movimentos_realizados}')
            return custo, movimentos_realizados
        
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
                
    return None

def encontrar_amigo_mais_proximo(atual: Node, amigos: list) -> Node:
    amigo_mais_proximo = None
    menor_distancia = float('inf')
    
    for amigo in amigos:
        distancia = distancia_manhattan(atual, amigo)
        if distancia < menor_distancia:
            menor_distancia = distancia
            amigo_mais_proximo = amigo
            
    return amigo_mais_proximo

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
        print(f'Custo para encontrar o amigo {amigo_mais_proximo.x, amigo_mais_proximo.y}: {custo}, aceitou? {aceitou}')
        
        if aceitou:
            aceitos_encontrados += 1
            if aceitos_encontrados >= 3:
                print('3 amigos encontrados, vamos retornar para casa')
                
        amigos.remove(amigo_mais_proximo)
    
    custo_retorno, movimentos_retorno = AStar(origem, retorno, matriz_terreno)
    custo_total += custo_retorno
    
    for movimento in movimentos_retorno:
        todos_movimentos.append(movimento)

    print(f'Retornamos para casa e o custo foi: {custo}')
    print(f'O custo total foi: {custo_total}')
    return aceitos, todos_movimentos

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

aceitos, movimentos = busca_amigos(INICIO, PERSONAGENS, MATRIZ)
print("Amigos que aceitaram:", [(amigo.x, amigo.y) for amigo in aceitos])
print(f'Foram {len(movimentos)} movimentos: {movimentos}')