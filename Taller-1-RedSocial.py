"""
Taller: Red Social y Modelos de Búsqueda con IA
Algoritmos: BPA, BPP, CU
Autores:
- Angel Sebastian Castillo Leon
- Cristhian David Leon Rico
- Nicolas Rubiano Cortes
"""

# GRAFO DE LA RED SOCIAL

def crear_grafo():
    return {
        'A': [('B', 2), ('C', 4), ('D', 6)],
        'B': [('A', 2), ('E', 3), ('F', 5)],
        'C': [('A', 4), ('G', 7), ('H', 2), ('J', 5)],
        'D': [('A', 6), ('I', 4), ('J', 5)],
        'E': [('B', 3), ('G', 6), ('J', 3)],
        'F': [('B', 5), ('H', 3), ('I', 5)],
        'G': [('C', 7), ('E', 6), ('I', 2)],
        'H': [('C', 2), ('F', 3), ('J', 4)],
        'I': [('D', 4), ('F', 5), ('G', 2)],
        'J': [('C', 5), ('D', 5), ('E', 3), ('H', 4)]
    }

# UTILIDADES DE IMPRESIÓN 

def imprimir_lista(titulo, lista):
    if titulo != "":
        print(titulo, end=" ")
    for i in range(len(lista)):
        print(lista[i], end="")
        if i != len(lista) - 1:
            print(" -> ", end="")
    print()

def imprimir_vacio_si_corresponde(lista):
    if len(lista) == 0:
        print("(vacío)")
        return True
    return False

# ALGORITMO BPA (Búsqueda Primero en Anchura)

def bpa(grafo, inicio, objetivo):
    cola = [(inicio, [inicio])]
    visitados = set()
    en_cola = {inicio}
    orden = []

    print("\n=== BPA (Búsqueda Primero en Anchura) ===")

    while cola:
        nodo, camino = cola.pop(0)

        if nodo in visitados:
            continue

        visitados.add(nodo)
        orden.append(nodo)

        if nodo == objetivo:
            frontera = []
            for item in cola:
                frontera.append(item[0])

            print("\nOrden de visita:")
            imprimir_lista("", orden)

            print("Ruta encontrada:")
            imprimir_lista("", camino)

            print("Nodos frontera:")
            if not imprimir_vacio_si_corresponde(frontera):
                imprimir_lista("", frontera)

            return camino

        for vecino, _ in grafo[nodo]:
            if vecino not in visitados and vecino not in en_cola:
                cola.append((vecino, camino + [vecino]))
                en_cola.add(vecino)

    return None


# ALGORITMO BPP (Búsqueda Primero en Profundidad)

def bpp(grafo, inicio, objetivo):
    pila = [(inicio, [inicio])]
    visitados = set()
    orden = []

    print("\n=== BPP (Búsqueda Primero en Profundidad) ===")

    while pila:
        nodo, camino = pila.pop()

        if nodo in visitados:
            continue

        visitados.add(nodo)
        orden.append(nodo)

        if nodo == objetivo:
            frontera = []
            for item in reversed(pila):
                frontera.append(item[0])

            print("\nOrden de visita:")
            imprimir_lista("", orden)

            print("Ruta encontrada:")
            imprimir_lista("", camino)

            print("Nodos frontera:")
            if len(frontera) == 0:
                print("(vacío)")
            else:
                imprimir_lista("", frontera)

            return camino

        en_frontera = set()
        for item in pila:
            en_frontera.add(item[0])

        for vecino, _ in reversed(grafo[nodo]):
            if vecino in visitados:
                continue
            if vecino in en_frontera:
                continue
            pila.append((vecino, camino + [vecino]))

    return None

# ALGORITMO CU (Búsqueda de Costo Uniforme)

def cu(grafo, inicio, objetivo):
    # La cola guarda (costo_acumulado, nodo_actual, camino_recorrido)
    cola = [(0, inicio, [inicio])]
    visitados = set()
    orden = []
    # Diccionario para rastrear el menor costo conocido a cada nodo
    mejor_costo = {inicio: 0}

    print("\n=== CU (Búsqueda de Costo Uniforme) ===")

    while cola:
        # 1. Siempre extraemos el nodo con el menor costo acumulado (Prioridad)
        cola.sort(key=lambda x: (x[0], x[1]))
        costo, nodo, camino = cola.pop(0)

        # Si el nodo ya fue visitado con un costo menor, lo ignoramos
        if nodo in visitados:
            continue

        visitados.add(nodo)
        orden.append(nodo)

        # 2. Verificamos si llegamos al objetivo
        if nodo == objetivo:
            # Ordenamos la cola restante para mostrar la frontera correctamente
            cola.sort(key=lambda x: (x[0], x[1]))

            frontera = []
            vistos_en_frontera = set()
            for item in cola:
                n_frontera = item[1]
                # CORRECCIÓN: El objetivo y los ya visitados no deben estar en la frontera
                if n_frontera != objetivo and n_frontera not in visitados and n_frontera not in vistos_en_frontera:
                    vistos_en_frontera.add(n_frontera)
                    frontera.append(n_frontera)

            print("\nOrden de visita:")
            imprimir_lista("", orden)

            print("Ruta encontrada:")
            imprimir_lista("", camino)

            print("Nodos frontera:")
            if not imprimir_vacio_si_corresponde(frontera):
                imprimir_lista("", frontera)

            return camino, costo

        # 3. Explorar vecinos
        for vecino, costo_arista in grafo[nodo]:
            nuevo_costo = costo + costo_arista
            # Si encontramos un camino más corto hacia el vecino, lo actualizamos
            if vecino not in mejor_costo or nuevo_costo < mejor_costo[vecino]:
                mejor_costo[vecino] = nuevo_costo
                cola.append((nuevo_costo, vecino, camino + [vecino]))

    return None, float('inf')

# FUNCIÓN PRINCIPAL

def main():
    print("=" * 60)
    print("TALLER: Red Social y Búsqueda con IA")
    print("=" * 60)

    grafo = crear_grafo()

    print("\nNodos disponibles: A, B, C, D, E, F, G, H, I, J")
    inicio = input("Nodo inicial: ").upper()
    objetivo = input("Nodo objetivo: ").upper()

    if inicio not in grafo or objetivo not in grafo:
        print("Error: Nodo inválido")
        return
    if inicio == objetivo:
        print("Error: Los nodos deben ser diferentes")
        return

    print("\nBúsqueda:", inicio, "->", objetivo)
    print("=" * 60)

    camino_bpa = bpa(grafo, inicio, objetivo)
    camino_bpp = bpp(grafo, inicio, objetivo)
    camino_cu, costo_cu = cu(grafo, inicio, objetivo)

main()