# ------------------------------------------------------------
# Punto 2 (A-D) - Modelos de búsqueda (BPA, BPP, Costo Uniforme)
# Implementados siguiendo el pseudocódigo del profe:
# - Frontier: Queue / Stack / PriorityQueue
# - Explored: Set
# - Regla: si neighbor no está en frontier ni explored => insertar
# - En CU: si neighbor está en frontier y el nuevo costo es menor => decrease-key
# ------------------------------------------------------------

import heapq

# -----------------------------
# Grafo (red social) con costos
# -----------------------------
# Formato: grafo[nodo] = {vecino: costo, ...}
grafo = {
    'A': {'B': 2, 'C': 4, 'D': 6},
    'B': {'A': 2, 'E': 3, 'F': 5},
    'C': {'A': 4, 'G': 7, 'H': 2, 'J': 5},
    'D': {'A': 6, 'I': 4, 'J': 5},
    'E': {'B': 3, 'G': 6, 'J': 3},
    'F': {'B': 5, 'H': 3, 'I': 5},
    'G': {'C': 7, 'E': 6, 'I': 2},
    'H': {'C': 2, 'F': 3, 'J': 4},
    'I': {'D': 4, 'F': 5, 'G': 2},
    'J': {'C': 5, 'D': 5, 'E': 3, 'H': 4}
}

# ---------------------------------------
# Reconstrucción de ruta usando "parent"
# ---------------------------------------
def reconstruir_ruta(parent, goal):
    ruta = []
    actual = goal
    while actual is not None:
        ruta.append(actual)
        actual = parent.get(actual)
    ruta.reverse()
    return ruta

# ============================================================
# A) BPA / BFS (Queue FIFO) - según pseudocódigo del profe
# ============================================================
def breadth_first_search(initial_state, goal_test):
    frontier = [initial_state]       # Queue
    explored = set()                 # Set
    parent = {initial_state: None}
    orden_visita = []

    while len(frontier) > 0:
        state = frontier.pop(0)      # dequeue
        explored.add(state)
        orden_visita.append(state)

        if goal_test(state):
            return True, orden_visita, reconstruir_ruta(parent, state)

        # vecinos en orden lexicográfico (como se usa en los ejemplos del profe)
        for neighbor in sorted(grafo[state].keys()):
            if (neighbor not in frontier) and (neighbor not in explored):
                parent[neighbor] = state
                frontier.append(neighbor)  # enqueue

    return False, orden_visita, None

# ============================================================
# B) BPP / DFS (Stack LIFO) - según pseudocódigo del profe
# Nota: para respetar "orden lexicográfico al revés" en pila,
#       empujamos en orden inverso para que salga el menor primero
#       cuando se hace pop().
# ============================================================
def depth_first_search(initial_state, goal_test):
    frontier = [initial_state]       # Stack
    explored = set()                 # Set
    parent = {initial_state: None}
    orden_visita = []

    while len(frontier) > 0:
        state = frontier.pop()       # pop (LIFO)
        explored.add(state)
        orden_visita.append(state)

        if goal_test(state):
            return True, orden_visita, reconstruir_ruta(parent, state)

        # Para que el stack explore primero el "lexicográficamente menor",
        # se apila en orden inverso.
        for neighbor in sorted(grafo[state].keys(), reverse=True):
            if (neighbor not in frontier) and (neighbor not in explored):
                parent[neighbor] = state
                frontier.append(neighbor)  # push

    return False, orden_visita, None

# ============================================================
# C) CU / Uniform Cost Search (Priority Queue por g(n))
# - "frontier.deleteMin()" (heapq)
# - "decrease-key" cuando aparece un mejor costo para un nodo en frontier
# ============================================================
def uniform_cost_search(initial_state, goal_test):
    explored = set()
    parent = {initial_state: None}
    g_cost = {initial_state: 0}

    # frontier = Heap priority queue of (cost, node)
    heap = [(0, initial_state)]
    frontier_best = {initial_state: 0}  # para saber si un nodo está en frontier y su mejor costo

    orden_visita = []

    while len(heap) > 0:
        cost, state = heapq.heappop(heap)  # deleteMin()

        # Lazy deletion: si este estado ya tiene un mejor costo registrado, lo ignoramos
        if state in frontier_best and cost != frontier_best[state]:
            continue

        # sacarlo "formalmente" de frontier
        frontier_best.pop(state, None)

        explored.add(state)
        orden_visita.append(state)

        if goal_test(state):
            return True, orden_visita, reconstruir_ruta(parent, state), cost

        for neighbor in sorted(grafo[state].keys()):
            step = grafo[state][neighbor]
            new_cost = cost + step

            if (neighbor not in explored) and (neighbor not in frontier_best):
                # insertar nuevo
                parent[neighbor] = state
                g_cost[neighbor] = new_cost
                frontier_best[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor))

            elif neighbor in frontier_best:
                # decrease-key si el nuevo camino es mejor
                if new_cost < frontier_best[neighbor]:
                    parent[neighbor] = state
                    g_cost[neighbor] = new_cost
                    frontier_best[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor))  # nuevo par, el viejo se ignorará

    return False, orden_visita, None, None

# ============================================================
# D) Consola (interactivo)
# ============================================================
def main():
    while True:
        print("\n--- Punto 2: Modelos de Búsqueda ---")
        print("1) BPA (Anchura)")
        print("2) BPP (Profundidad)")
        print("3) Costo Uniforme")
        print("4) Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "4":
            print("Saliendo del programa...")
            break

        inicio = input("Nodo inicial (A-J): ").strip().upper()
        objetivo = input("Nodo objetivo (A-J): ").strip().upper()

        if inicio not in grafo or objetivo not in grafo:
            print("❌ Nodo inválido. Intente nuevamente.")
            continue

        goal_test = lambda s: s == objetivo

        if opcion == "1":
            ok, orden, ruta = breadth_first_search(inicio, goal_test)
            print("\n--- RESULTADOS BPA ---")
            print("Orden de visita:", orden)
            print("Ruta encontrada:", ruta)

        elif opcion == "2":
            ok, orden, ruta = depth_first_search(inicio, goal_test)
            print("\n--- RESULTADOS BPP ---")
            print("Orden de visita:", orden)
            print("Ruta encontrada:", ruta)

        elif opcion == "3":
            ok, orden, ruta, costo = uniform_cost_search(inicio, goal_test)
            print("\n--- RESULTADOS COSTO UNIFORME ---")
            print("Orden de visita:", orden)
            print("Ruta encontrada:", ruta)
            print("Costo total:", costo)

        else:
            print("❌ Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
