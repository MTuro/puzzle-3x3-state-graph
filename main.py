from collections import deque

# movimentos possíveis por posição (1..9)
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

def gera_vizinhos(cfg):
    vazia = next(k for k, v in cfg.items() if v == 0)
    for pos in movimentos_validos[vazia]:
        nova = cfg.copy()
        nova[vazia], nova[pos] = nova[pos], nova[vazia]
        yield nova

def montaGrafoEstados(cfg_inicial):
    # Monta grafo de estados alcançáveis a partir do inicial.
    H = {}
    C = []
    GrafoJogo = {}

    t0 = tuple(cfg_inicial.values())
    H[t0] = 0
    C.append(cfg_inicial.copy())
    GrafoJogo[0] = {"cfg": t0, "viz": []}

    fila = deque([0])

    while fila:
        u = fila.popleft()
        cfg_u = C[u]

        for viz in gera_vizinhos(cfg_u):
            tv = tuple(viz.values())

            if tv not in H:
                idv = len(C)
                H[tv] = idv
                C.append(viz.copy())
                GrafoJogo[idv] = {"cfg": tv, "viz": []}
                fila.append(idv)
            else:
                idv = H[tv]

            # adiciona aresta não-direcionada
            if idv not in GrafoJogo[u]["viz"]:
                GrafoJogo[u]["viz"].append(idv)
            if u not in GrafoJogo[idv]["viz"]:
                GrafoJogo[idv]["viz"].append(u)

    return GrafoJogo, H, C

def bfs_distencia(grafo, inicio_id):
    dist = {inicio_id: 0}
    q = deque([inicio_id])
    while q:
        u = q.popleft()
        for v in grafo[u]["viz"]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def formata_cfg_tuple(t):
    s = ""
    for i in range(9):
        s += f"{t[i]} "
        if (i+1) % 3 == 0:
            s = s.rstrip() + ("\n" if i < 8 else "")
    return s

# configuração alvo cfg*
cfg_star = {
    1:1, 2:2, 3:3,
    4:4, 5:5, 6:6,
    7:7, 8:8, 9:0
}

GrafoJogo, H, C = montaGrafoEstados(cfg_star)

num_nos = len(GrafoJogo)
num_arestas = sum(len(GrafoJogo[i]["viz"]) for i in GrafoJogo) // 2

id_alvo = H.get(tuple(cfg_star.values()))
if id_alvo is None:
    print("configuração não encontrada no grafo.")
else:
    # distâncias a partir de cfg_star
    dist = bfs_distencia(GrafoJogo, id_alvo)

    # encontra a(s) maior(es) distância(s)
    maior_dist = max(dist.values())
    nos_mais_distantes = [nid for nid, d in dist.items() if d == maior_dist]

    # escolhe um estado mais difícil (pega o primeiro)
    id_mais_dificil = nos_mais_distantes[0]
    cfg_mais_dificil_tuple = GrafoJogo[id_mais_dificil]["cfg"]

    print("nos no grafo:", num_nos)
    print("arestas no grafo:", num_arestas)
    print("configuração inicial com maior número de movimentos:")
    print(formata_cfg_tuple(cfg_mais_dificil_tuple))
    print("representação em tupla:", cfg_mais_dificil_tuple)
    print()
    print("número de movimentos necessários (distância mínima):", maior_dist)