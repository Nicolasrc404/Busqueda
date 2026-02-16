"""
Taller: Red Social y Modelos de Búsqueda con IA
Algoritmos: BPA, BPP, CU
Autores:
- Angel Sebastian Castillo Leon
- Cristhian David Leon Rico
- Nicolas Rubiano Cortes
"""

# GRAFO DE LA RED SOCIAL (no dirigido, con pesos)

def crear_grafo():
    """Crea el grafo como diccionario: nodo -> lista de (vecino, costo)."""
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

# UTILIDADES DE IMPRESIÓN (prints básicos, sin end="")

def imprimir_ruta(titulo, lista):
    """Imprime una lista en formato: A -> B -> C (sin usar join ni end="")."""
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
            salida = salida + " -> "
        i = i + 1
    print(salida)

def imprimir_vacio_si_corresponde(lista):
    """Imprime '(vacío)' si la lista está vacía. Retorna True si imprimió vacío."""
    if len(lista) == 0:
        print("(vacío)")
        return True
    return False

# BPA (Búsqueda Primero en Anchura)

def bpa(grafo, inicio, objetivo):
    cola = [(inicio, [inicio])]  # (nodo, camino)
    visitados = set()
    en_cola = {inicio}           # para no duplicar en frontera
    orden = []

    print("=== BPA (Búsqueda Primero en Anchura) ===")

    while len(cola) > 0:
        # FIFO: saco el primer elemento
        nodo, camino = cola.pop(0)

        if nodo in visitados:
            continue

        visitados.add(nodo)
        orden.append(nodo)

        # Si llegamos al objetivo, mostramos resultados
        if nodo == objetivo:
            frontera = []
            for item in cola:
                frontera.append(item[0])

            print("Orden de visita:")
            imprimir_ruta("", orden)

            print("Ruta encontrada:")
            imprimir_ruta("", camino)

            print("Nodos frontera:")
            if not imprimir_vacio_si_corresponde(frontera):
                imprimir_ruta("", frontera)

            return camino

        # Encolar vecinos en el orden dado por el grafo
        for vecino, _ in grafo[nodo]:
            if vecino not in visitados and vecino not in en_cola:
                cola.append((vecino, camino + [vecino]))
                en_cola.add(vecino)

    return None

# BPP (Búsqueda Primero en Profundidad)

def bpp(grafo, inicio, objetivo):
    pila = [(inicio, [inicio])]  # (nodo, camino)
    visitados = set()
    orden = []

    print("=== BPP (Búsqueda Primero en Profundidad) ===")

    while len(pila) > 0:
        # LIFO: saco el último elemento
        nodo, camino = pila.pop()

        if nodo in visitados:
            continue

        visitados.add(nodo)
        orden.append(nodo)

        # Si llegamos al objetivo, mostramos resultados
        if nodo == objetivo:
            frontera = []
            # La frontera "visual" se muestra desde el tope hacia abajo
            for item in reversed(pila):
                frontera.append(item[0])

            print("Orden de visita:")
            imprimir_ruta("", orden)

            print("Ruta encontrada:")
            imprimir_ruta("", camino)

            print("Nodos frontera:")
            if len(frontera) == 0:
                print("(vacío)")
            else:
                imprimir_ruta("", frontera)

            return camino

        # Para evitar duplicados en pila, recolectamos nodos ya en frontera
        en_frontera = set()
        for item in pila:
            en_frontera.add(item[0])

        # Reversed para que el recorrido quede consistente con el orden esperado
        for vecino, _ in reversed(grafo[nodo]):
            if vecino in visitados:
                continue
            if vecino in en_frontera:
                continue
            pila.append((vecino, camino + [vecino]))

    return None

# CU (Búsqueda de Costo Uniforme)

# CU (Búsqueda de Costo Uniforme) - versión simple sin lambda

def cu(grafo, inicio, objetivo):
    cola = [(0, inicio, [inicio])]  # (costo, nodo, camino)
    visitados = set()
    orden = []
    mejor_costo = {inicio: 0}

    print("=== CU (Búsqueda de Costo Uniforme) ===")

    while len(cola) > 0:

        # Buscar manualmente el elemento con menor costo
        indice_menor = 0
        i = 1
        while i < len(cola):
            if cola[i][0] < cola[indice_menor][0]:
                indice_menor = i
            i = i + 1

        # Sacar el de menor costo
        costo, nodo, camino = cola.pop(indice_menor)

        if nodo in visitados:
            continue

        visitados.add(nodo)
        orden.append(nodo)

        # Si llegamos al objetivo
        if nodo == objetivo:

            # Construir frontera simple
            frontera = []
            for item in cola:
                if item[1] not in visitados:
                    if item[1] not in frontera:
                        frontera.append(item[1])

            print("Orden de visita:")
            imprimir_ruta("", orden)

            print("Ruta encontrada:")
            imprimir_ruta("", camino)

            print("Nodos frontera:")
            if not imprimir_vacio_si_corresponde(frontera):
                imprimir_ruta("", frontera)

            return camino, costo

        # Expandir vecinos
        for vecino, costo_arista in grafo[nodo]:
            nuevo_costo = costo + costo_arista

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