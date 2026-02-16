"""
Taller: Red Social y Modelos de Búsqueda con IA
Algoritmos: BPA, BPP, CU
Autores:
- Angel Sebastian Castillo Leon
- Cristhian David Leon Rico
- Nicolas Rubiano Cortes
"""

# ==================================================
# GRAFO (DIRIGIDO) SEGÚN TABLA: Amigo 1 -> Amigo 2
# Representación: nodo -> {vecino: costo}
# ==================================================

def crear_grafo_dirigido():
    """Crea el grafo dirigido (flujo estricto Amigo 1 -> Amigo 2)."""
    grafo = {
        'A': {'B': 2, 'C': 4, 'D': 6},
        'B': {'E': 3, 'F': 5},
        'C': {'G': 7, 'H': 2, 'J': 5},
        'D': {'I': 4, 'J': 5},
        'E': {'G': 6, 'J': 3},
        'F': {'H': 3, 'I': 5},
        'G': {'I': 2},
        'H': {'J': 4},
        'I': {},
        'J': {}
    }
    return grafo

# ==================================================
# UTILIDADES DE IMPRESIÓN (prints básicos)
# ==================================================

def imprimir_lista(titulo, lista):
    """Imprime una lista separada por coma: A, B, C."""
    if titulo != "":
        print(titulo)

    if len(lista) == 0:
        print("(vacío)")
        return

    salida = ""
    i = 0
    while i < len(lista):
        salida = salida + str(lista[i])
        if i != len(lista) - 1:
            salida = salida + ", "
        i = i + 1
    print(salida)

def imprimir_ruta_guion(lista):
    """Imprime ruta separada por ' - '."""
    if len(lista) == 0:
        print("(vacío)")
        return

    salida = ""
    i = 0
    while i < len(lista):
        salida = salida + str(lista[i])
        if i != len(lista) - 1:
            salida = salida + " - "
        i = i + 1
    print(salida)

# ==================================================
# BPA (Búsqueda Primero en Anchura) - Cola FIFO
# ==================================================

def bpa(grafo, inicio, objetivo):
    frontera = [[inicio]]  # cola FIFO de caminos
    visitados = set()
    expandidos = []

    while len(frontera) > 0:
        camino = frontera.pop(0)
        nodo = camino[-1]

        if nodo in visitados:
            continue

        expandidos.append(nodo)
        visitados.add(nodo)

        if nodo == objetivo:
            nodos_frontera = []
            for ruta in frontera:
                n = ruta[-1]
                if n not in nodos_frontera:
                    nodos_frontera.append(n)

            return camino, expandidos, nodos_frontera

        for vecino in grafo[nodo]:
            if vecino not in visitados:
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                frontera.append(nuevo_camino)

    return None, expandidos, []

# ==================================================
# BPP (Búsqueda Primero en Profundidad) - Pila LIFO
# ==================================================

def bpp(grafo, inicio, objetivo):
    frontera = [[inicio]]   # pila LIFO de caminos
    generados = {inicio}    # nodos ya generados 
    expandidos = []

    while len(frontera) > 0:
        camino = frontera.pop()
        nodo = camino[-1]

        expandidos.append(nodo)

        if nodo == objetivo:
            nodos_frontera = []
            for ruta in frontera:
                n = ruta[-1]
                if n not in nodos_frontera:
                    nodos_frontera.append(n)

            return camino, expandidos, nodos_frontera

        vecinos = list(grafo[nodo].keys())
        vecinos.reverse()

        i = 0
        while i < len(vecinos):
            vecino = vecinos[i]
            if vecino not in generados:
                generados.add(vecino)
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                frontera.append(nuevo_camino)
            i = i + 1

    return None, expandidos, []

# ==================================================
# CU (Búsqueda de Costo Uniforme)
# ==================================================

def cu(grafo, inicio, objetivo):
    frontera = [(0, [inicio])]  # (costo acumulado, camino)
    visitados = set()
    expandidos = []
    mejor_costo = {inicio: 0}

    while len(frontera) > 0:
        # buscar manualmente el menor costo
        indice_menor = 0
        i = 1
        while i < len(frontera):
            if frontera[i][0] < frontera[indice_menor][0]:
                indice_menor = i
            i = i + 1

        costo, camino = frontera.pop(indice_menor)
        nodo = camino[-1]

        if nodo in visitados:
            continue

        expandidos.append(nodo)
        visitados.add(nodo)

        if nodo == objetivo:
            # Construir lista (costo, nodo) para ordenar frontera por costo
            pares = []
            for (c, ruta) in frontera:
                n = ruta[-1]
                if n not in visitados:
                    pares.append((c, n))

            # Ordenar 'pares' por costo (y si empata, por nombre)
            ordenados = []
            while len(pares) > 0:
                idx = 0
                j = 1
                while j < len(pares):
                    if pares[j][0] < pares[idx][0]:
                        idx = j
                    elif pares[j][0] == pares[idx][0]:
                        if pares[j][1] < pares[idx][1]:
                            idx = j
                    j = j + 1
                ordenados.append(pares.pop(idx))

            # Sacar solo nodos, sin repetidos (por si aparecen)
            nodos_frontera = []
            k = 0
            while k < len(ordenados):
                n = ordenados[k][1]
                if n not in nodos_frontera:
                    nodos_frontera.append(n)
                k = k + 1

            return camino, costo, expandidos, nodos_frontera

        for vecino in grafo[nodo]:
            peso = grafo[nodo][vecino]
            nuevo_costo = costo + peso

            if vecino not in mejor_costo or nuevo_costo < mejor_costo[vecino]:
                mejor_costo[vecino] = nuevo_costo
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                frontera.append((nuevo_costo, nuevo_camino))

    return None, 0, expandidos, []

# ==================================================
# MAIN 
# ==================================================

def main():
    grafo = crear_grafo_dirigido()

    print("--- SISTEMA DE BÚSQUEDA EN RED SOCIAL ---")
    print("Nodos disponibles: A, B, C, D, E, F, G, H, I, J")
    inicio = input("Ingrese el nodo inicial: ").upper()
    objetivo = input("Ingrese el nodo objetivo: ").upper()

    if inicio not in grafo or objetivo not in grafo:
        print("Error: Nodo inválido")
        return
    if inicio == objetivo:
        print("Error: Los nodos deben ser diferentes")
        return

    print("\n" + "=" * 60)
    print("ANÁLISIS DE RUTA:", inicio, "->", objetivo)
    print("=" * 60)

    # 1) BPA
    camino_bpa, ne_bpa, nf_bpa = bpa(grafo, inicio, objetivo)
    print("\n1) BPA (Búsqueda Primero en Anchura)")
    if camino_bpa is not None:
        print("Ruta encontrada:")
        imprimir_ruta_guion(camino_bpa)
        print("Nodos expandidos:")
        imprimir_lista("", ne_bpa)
        print("Nodos frontera:")
        if len(nf_bpa) == 0:
            print("(vacío)")
        else:
            imprimir_lista("", nf_bpa)
    else:
        print("No se encontró ruta.")

    # 2) BPP
    camino_bpp, ne_bpp, nf_bpp = bpp(grafo, inicio, objetivo)
    print("\n2) BPP (Búsqueda Primero en Profundidad)")
    if camino_bpp is not None:
        print("Ruta encontrada:")
        imprimir_ruta_guion(camino_bpp)
        print("Nodos expandidos:")
        imprimir_lista("", ne_bpp)
        print("Nodos frontera:")
        if len(nf_bpp) == 0:
            print("(vacío)")
        else:
            imprimir_lista("", nf_bpp)
    else:
        print("No se encontró ruta.")

    # 3) CU
    camino_cu, costo_cu, ne_cu, nf_cu = cu(grafo, inicio, objetivo)
    print("\n3) CU (Búsqueda de Costo Uniforme)")
    if camino_cu is not None:
        print("Ruta encontrada:")
        imprimir_ruta_guion(camino_cu)
        print("Nodos expandidos:")
        imprimir_lista("", ne_cu)
        print("Nodos frontera (ordenado por costo):")
        if len(nf_cu) == 0:
            print("(vacío)")
        else:
            imprimir_lista("", nf_cu)
    else:
        print("No se encontró ruta.")

    print("\n" + "=" * 60)

main()
