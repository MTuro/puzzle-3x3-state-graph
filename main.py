from itertools import permutations

movimentos_validos = {
    1: [2, 4],
    2: [1, 3, 5],
    3: [2, 6],
    4: [1, 5, 7],
    5: [2, 4, 6, 8],
    6: [3, 5, 9],
    7: [4, 8],
    8: [5, 7, 9],
    9: [6, 8]
}

def print_cfg(cfg):
    for i in range(9):
        val = cfg[i]
        print(val, end=" ")
        
        if (i + 1) % 3 == 0:
            print()  


def gera_vizinhos_tuple(cfg):
    vazia = cfg.index(0) + 1  
    vizinhos = []
    for pos in movimentos_validos[vazia]:
        lst = list(cfg)
        i, j = vazia - 1, pos - 1
        lst[i], lst[j] = lst[j], lst[i]
        vizinhos.append(tuple(lst))
    return vizinhos


#Tarefa 1
def monta_grafo_completo():
    Grafo = {}
    
    for p in permutations(range(9)): # 9! nos possiveis
        Grafo[p] = []

    
    for cfg in Grafo: #Arestas
        for v in gera_vizinhos_tuple(cfg):
            Grafo[cfg].append(v)

    return Grafo


#Tarefa 2
def BFS(G, s):
    visited = set()
    parent = {}
    L = []        
    L.append([s]) 

    visited.add(s)

    i = 1
    while True:
        L.append([])
        for u in L[i-1]:
            for v in G[u]:
                if v not in visited:
                    visited.add(v)
                    parent[v] = u
                    L[i].append(v)
        if len(L[i]) == 0:
            break
        i += 1

    return visited, parent, L


def BFS_all(G):
    visitados_global = set()
    componentes = 0

    for s in G:
        if s not in visitados_global:
            comp_visitados, _, _ = BFS(G, s)
            visitados_global |= comp_visitados
            componentes += 1

    return componentes


# Tarefa 3
cfg_star = (1,2,3,4,5,6,7,8,0)

def distancia_ate_cfg_star(G):
    visitados, parent, levels = BFS(G, cfg_star)

    maior_dist = len(levels) - 2
    mais_distantes = levels[-2]

    return maior_dist, mais_distantes


print("Montando grafo completo...")
G = monta_grafo_completo()

num_nos = len(G)
num_arestas = sum(len(G[cfg]) for cfg in G) // 2

print("Numero total de nos:", num_nos)
print("Numero total de arestas:", num_arestas)

componentes = BFS_all(G)
print("Numero de componentes conexos:", componentes)

maior_dist, mais_distantes = distancia_ate_cfg_star(G)
print("Exemplo de configuracao viavel mais distante:")
print_cfg(mais_distantes[0])
print("Quantidade de movimentos necessaria:", maior_dist)
