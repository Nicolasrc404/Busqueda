# ================================================================
# TALLER: RED SOCIAL Y MODELOS DE BÚSQUEDA CON IA
# Algoritmos de búsqueda no informada: BPA, BPP, CU
# Caso: Encontrar ruta de A a D
# ================================================================

# ==================================================
# DEFINICIÓN DEL GRAFO (Red Social)
# ==================================================

def crear_grafo():
    """
    Crea el grafo de la red social con las conexiones y costos.
    Estructura: diccionario donde cada nodo tiene lista de tuplas (vecino, costo).
    Los vecinos están ordenados alfabéticamente según las especificaciones.
    """
    grafo = {
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
    return grafo

# ==================================================
# ALGORITMO 1: BÚSQUEDA PRIMERO EN ANCHURA (BPA)
# ==================================================

def bpa(grafo, inicio, objetivo):
    """
    Búsqueda Primero en Anchura (Breadth-First Search)
    
    CARACTERÍSTICAS:
    - Explora nivel por nivel (nodos menos profundos primero)
    - Garantiza encontrar la solución más corta en número de pasos
    - Usa cola FIFO (First In, First Out)
    - Completitud: Sí (si b es finito)
    - Optimalidad: Sí (si costos unitarios)
    - Complejidad tiempo: O(b^d)
    - Complejidad espacio: O(b^d)
    """
    print("\n" + "="*70)
    print("ALGORITMO: BÚSQUEDA PRIMERO EN ANCHURA (BPA)")
    print("="*70)
    print("\nCARACTERÍSTICAS:")
    print("- Estructura: Cola FIFO (First In, First Out)")
    print("- Estrategia: Expandir el nodo MENOS profundo")
    print("- Orden de encolado: Lexicográfico (A, B, C, ...)")
    print("\n" + "-"*70)
    
    # Cola FIFO: cada elemento es (nodo_actual, camino_recorrido, costo_acumulado)
    cola = [(inicio, [inicio], 0)]
    visitados = set()
    orden_visita = []
    paso = 0
    
    print("\nPROCESO DE BÚSQUEDA:\n")
    
    while cola:
        paso += 1
        # Mostrar estado de la cola antes de decolar
        print(f"Paso {paso}:")
        print(f"  Cola: {[nodo for nodo, _, _ in cola]}")
        
        # DECOLAR: Extraer el primer elemento (FIFO)
        nodo_actual, camino, costo_acum = cola.pop(0)
        
        print(f"  → Decolando: {nodo_actual}")
        print(f"  → Camino hasta {nodo_actual}: {' → '.join(camino)}")
        
        # Registrar visita
        if nodo_actual not in visitados:
            orden_visita.append(nodo_actual)
            print(f"  → Nodo visitado: {nodo_actual}")
            
            # ¿Es el objetivo?
            if nodo_actual == objetivo:
                print(f"\n  ✓ ¡OBJETIVO ENCONTRADO EN {nodo_actual}!")
                print("-"*70)
                print("\nRESULTADO:")
                print(f"  Orden de visita: {' → '.join(orden_visita)}")
                print(f"  Ruta más corta: {' → '.join(camino)}")
                print(f"  Número de pasos: {len(camino) - 1}")
                print(f"  Costo total (unitario): {len(camino) - 1}")
                return camino, orden_visita
            
            # Marcar como visitado
            visitados.add(nodo_actual)
            
            # ENCOLAR vecinos (en orden lexicográfico)
            vecinos_agregados = []
            for vecino, costo in grafo[nodo_actual]:
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    nuevo_costo = costo_acum + costo
                    cola.append((vecino, nuevo_camino, nuevo_costo))
                    vecinos_agregados.append(vecino)
            
            if vecinos_agregados:
                print(f"  → Encolando vecinos: {vecinos_agregados}")
        else:
            print(f"  → Nodo {nodo_actual} ya visitado, se omite")
        
        print()
    
    print("\n✗ No se encontró camino al objetivo")
    print("-"*70)
    return None, orden_visita

# ==================================================
# ALGORITMO 2: BÚSQUEDA PRIMERO EN PROFUNDIDAD (BPP)
# ==================================================

def bpp(grafo, inicio, objetivo):
    """
    Búsqueda Primero en Profundidad (Depth-First Search)
    
    CARACTERÍSTICAS:
    - Explora un camino completamente antes de retroceder
    - NO garantiza encontrar la solución óptima
    - Usa pila LIFO (Last In, First Out)
    - Completitud: No (puede quedar atrapado en ciclos)
    - Optimalidad: No
    - Complejidad tiempo: O(b^m)
    - Complejidad espacio: O(bm) - lineal
    """
    print("\n" + "="*70)
    print("ALGORITMO: BÚSQUEDA PRIMERO EN PROFUNDIDAD (BPP)")
    print("="*70)
    print("\nCARACTERÍSTICAS:")
    print("- Estructura: Pila LIFO (Last In, First Out)")
    print("- Estrategia: Expandir el nodo MÁS profundo")
    print("- Orden de apilado: Lexicográfico INVERSO (para que salgan en orden)")
    print("\n" + "-"*70)
    
    # Pila LIFO: solo nodos (simplificado)
    pila = [inicio]
    visitados_lista = []
    visitados_set = set()
    camino_dict = {inicio: [inicio]}
    paso = 0
    
    print("\nPROCESO DE BÚSQUEDA:\n")
    
    while pila:
        paso += 1
        # Mostrar estado de la pila antes de desapilar
        print(f"Paso {paso}:")
        print(f"  Pila: {pila}")
        
        # DESAPILAR: Extraer el último elemento (LIFO)
        nodo_actual = pila.pop()
        
        # Verificar si ya fue visitado
        if nodo_actual in visitados_set:
            print(f"  → {nodo_actual} ya visitado, se omite\n")
            continue
        
        # Marcar como visitado
        visitados_lista.append(nodo_actual)
        visitados_set.add(nodo_actual)
        camino = camino_dict[nodo_actual]
        
        print(f"  → Desapilando y visitando: {nodo_actual}")
        print(f"  → Camino hasta {nodo_actual}: {' → '.join(camino)}")
        print(f"  → Nodo visitado: {nodo_actual}")
        
        # ¿Es el objetivo?
        if nodo_actual == objetivo:
            print(f"\n  ✓ ¡OBJETIVO ENCONTRADO EN {nodo_actual}!")
            print("-"*70)
            print("\nRESULTADO:")
            print(f"  Orden de visita: {' → '.join(visitados_lista)}")
            print(f"  Ruta encontrada: {' → '.join(camino)}")
            print(f"  Número de pasos: {len(camino) - 1}")
            print(f"  NOTA: Esta NO es necesariamente la ruta más corta")
            return camino, visitados_lista
        
        # APILAR vecinos en orden INVERSO (para que salgan en orden alfabético)
        vecinos = grafo[nodo_actual]
        vecinos_agregados = []
        
        # Obtener vecinos no visitados y no en pila
        for vecino, costo in reversed(vecinos):
            if vecino not in visitados_set and vecino not in pila:
                pila.append(vecino)
                camino_dict[vecino] = camino + [vecino]
                vecinos_agregados.append(vecino)
        
        if vecinos_agregados:
            print(f"  → Apilando vecinos (orden inverso): {list(reversed(vecinos_agregados))}")
        
        print()
    
    print("\n✗ No se encontró camino al objetivo")
    print("-"*70)
    return None, visitados_lista

# ==================================================
# ALGORITMO 3: BÚSQUEDA DE COSTO UNIFORME (CU)
# ==================================================

def cu(grafo, inicio, objetivo):
    """
    Búsqueda de Costo Uniforme (Uniform Cost Search)
    
    CARACTERÍSTICAS:
    - Expande el nodo con MENOR COSTO acumulado
    - Garantiza encontrar la solución de menor costo
    - Usa cola de prioridad ordenada por g(n) - costo acumulado
    - Completitud: Sí (si costo finito)
    - Optimalidad: Sí
    - Complejidad tiempo: O(b^(C*/ε))
    - Complejidad espacio: O(b^(C*/ε))
    """
    print("\n" + "="*70)
    print("ALGORITMO: BÚSQUEDA DE COSTO UNIFORME (CU)")
    print("="*70)
    print("\nCARACTERÍSTICAS:")
    print("- Estructura: Cola de prioridad ordenada por COSTO g(n)")
    print("- Estrategia: Expandir el nodo de MENOR COSTO acumulado")
    print("- Orden: Por costo acumulado (desempate lexicográfico)")
    print("\n" + "-"*70)
    
    # Cola de prioridad: lista de (costo_acumulado, nodo_actual, camino_recorrido)
    cola_prioridad = [(0, inicio, [inicio])]
    visitados = set()
    orden_visita = []
    paso = 0
    
    print("\nPROCESO DE BÚSQUEDA:\n")
    
    while cola_prioridad:
        paso += 1
        # Ordenar por costo acumulado (y alfabéticamente en caso de empate)
        cola_prioridad.sort(key=lambda x: (x[0], x[1]))
        
        # Mostrar estado de la cola de prioridad
        print(f"Paso {paso}:")
        print(f"  Cola de prioridad:")
        for costo, nodo, _ in cola_prioridad[:5]:  # Mostrar primeros 5
            print(f"    {nodo}({costo})", end=" ")
        if len(cola_prioridad) > 5:
            print(f"... ({len(cola_prioridad)-5} más)")
        else:
            print()
        
        # Extraer nodo con menor costo
        costo_actual, nodo_actual, camino = cola_prioridad.pop(0)
        
        print(f"  → Expandiendo: {nodo_actual} con costo acumulado g({nodo_actual})={costo_actual}")
        print(f"  → Camino: {' → '.join(camino)}")
        
        # Verificar si ya fue visitado
        if nodo_actual not in visitados:
            orden_visita.append(nodo_actual)
            print(f"  → Nodo visitado: {nodo_actual}")
            
            # ¿Es el objetivo?
            if nodo_actual == objetivo:
                print(f"\n  ✓ ¡OBJETIVO ENCONTRADO EN {nodo_actual}!")
                print("-"*70)
                print("\nRESULTADO:")
                print(f"  Orden de visita: {' → '.join(orden_visita)}")
                print(f"  Ruta de menor costo: {' → '.join(camino)}")
                print(f"  Número de pasos: {len(camino) - 1}")
                print(f"  Costo total óptimo: {costo_actual}")
                
                # Mostrar desglose de costos
                print(f"\n  Desglose de costos:")
                costo_parcial = 0
                for i in range(len(camino) - 1):
                    nodo_origen = camino[i]
                    nodo_destino = camino[i+1]
                    # Buscar el costo de la arista
                    for vecino, costo in grafo[nodo_origen]:
                        if vecino == nodo_destino:
                            costo_parcial += costo
                            print(f"    {nodo_origen} → {nodo_destino}: {costo} (acumulado: {costo_parcial})")
                            break
                
                return camino, costo_actual, orden_visita
            
            # Marcar como visitado
            visitados.add(nodo_actual)
            
            # Agregar vecinos con su costo acumulado
            vecinos_agregados = []
            for vecino, costo_arista in grafo[nodo_actual]:
                if vecino not in visitados:
                    nuevo_costo = costo_actual + costo_arista
                    nuevo_camino = camino + [vecino]
                    cola_prioridad.append((nuevo_costo, vecino, nuevo_camino))
                    vecinos_agregados.append(f"{vecino}({nuevo_costo})")
            
            if vecinos_agregados:
                print(f"  → Agregando vecinos: {', '.join(vecinos_agregados)}")
        else:
            print(f"  → Nodo {nodo_actual} ya visitado, se omite")
        
        print()
    
    print("\n✗ No se encontró camino al objetivo")
    print("-"*70)
    return None, float('inf'), orden_visita

# ==================================================
# PROGRAMA PRINCIPAL
# ==================================================

import sys

def obtener_nodo_valido(grafo, mensaje, nodo_excluido=None):
    """
    Solicita al usuario un nodo válido del grafo
    """
    nodos_disponibles = sorted(grafo.keys())
    
    while True:
        print(f"\n{mensaje}")
        print(f"Nodos disponibles: {', '.join(nodos_disponibles)}")
        
        try:
            nodo = input("Ingresa el nodo (letra mayúscula): ").strip().upper()
        except EOFError:
            print("\n❌ Error: No se pudo leer la entrada.")
            return None
        
        if nodo not in grafo:
            print(f"❌ Error: '{nodo}' no es un nodo válido. Intenta de nuevo.")
            continue
        
        if nodo_excluido and nodo == nodo_excluido:
            print(f"❌ Error: El nodo objetivo no puede ser igual al nodo inicial.")
            continue
        
        return nodo

def main():
    """
    Función principal que ejecuta los tres algoritmos
    """
    print("="*70)
    print("  TALLER: RED SOCIAL Y MODELOS DE BÚSQUEDA CON IA")
    print("="*70)
    print("\n📋 INFORMACIÓN DEL PROBLEMA:")
    print("  • Búsqueda de rutas en red social")
    print("  • Red social de Ana (A) y sus amigos")
    
    print("\n📊 GRAFO DE LA RED SOCIAL:")
    print("\n  Conexiones (Amigo1 - Amigo2: Interacciones):")
    print("  " + "-"*50)
    
    conexiones = [
        "A-B: 2    B-E: 3    C-G: 7    D-I: 4    E-G: 6",
        "A-C: 4    B-F: 5    C-H: 2    D-J: 5    E-J: 3",
        "A-D: 6              C-J: 5              F-H: 3",
        "                                        F-I: 5",
        "                                        G-I: 2",
        "                                        H-J: 4"
    ]
    
    for linea in conexiones:
        print(f"  {linea}")
    
    # Crear el grafo
    grafo = crear_grafo()
    
    # Verificar si se pasaron argumentos de línea de comandos
    if len(sys.argv) >= 3:
        inicio = sys.argv[1].upper()
        objetivo = sys.argv[2].upper()
        
        # Validar nodos
        if inicio not in grafo:
            print(f"\n❌ Error: '{inicio}' no es un nodo válido.")
            print(f"Nodos disponibles: {', '.join(sorted(grafo.keys()))}")
            return
        
        if objetivo not in grafo:
            print(f"\n❌ Error: '{objetivo}' no es un nodo válido.")
            print(f"Nodos disponibles: {', '.join(sorted(grafo.keys()))}")
            return
        
        if inicio == objetivo:
            print(f"\n❌ Error: El nodo inicial y objetivo no pueden ser iguales.")
            return
        
        print("\n" + "="*70)
        print("  CONFIGURACIÓN DE LA BÚSQUEDA (Argumentos)")
        print("="*70)
        print(f"\n  🔵 Nodo inicial: {inicio}")
        print(f"  🎯 Nodo objetivo: {objetivo}")
        
    else:
        # Solicitar nodo inicial y objetivo al usuario
        print("\n" + "="*70)
        print("  CONFIGURACIÓN DE LA BÚSQUEDA")
        print("="*70)
        print("\n💡 Tip: También puedes ejecutar con argumentos:")
        print("   python red_social_busqueda.py A D")
        
        inicio = obtener_nodo_valido(grafo, "🔵 ¿Cuál es el NODO INICIAL?")
        if inicio is None:
            print("\n❌ Ejecución cancelada. Usa: python red_social_busqueda.py A D")
            return
        
        objetivo = obtener_nodo_valido(grafo, "🎯 ¿Cuál es el NODO OBJETIVO?", nodo_excluido=inicio)
        if objetivo is None:
            print("\n❌ Ejecución cancelada. Usa: python red_social_busqueda.py A D")
            return
    
    print("\n" + "="*70)
    print(f"  ✓ Configuración: {inicio} → {objetivo}")
    print("="*70)
    
    # ==================================================
    # PREGUNTA 1: BPA - Ruta más corta (costo unitario)
    # ==================================================
    print("\n\n" + "#"*70)
    print("# PREGUNTA 1: BÚSQUEDA PRIMERO EN ANCHURA (BPA)")
    print("#"*70)
    print("\n❓ ¿Cuál es la ruta más corta considerando costo unitario?")
    print("   (Cada conexión cuenta como 1 paso)")
    
    input("\n⏸️  Presiona ENTER para ejecutar BPA...")
    camino_bpa, orden_bpa = bpa(grafo, inicio, objetivo)
    
    # ==================================================
    # PREGUNTA 2: BPP - Exploración en profundidad
    # ==================================================
    print("\n\n" + "#"*70)
    print("# PREGUNTA 2: BÚSQUEDA PRIMERO EN PROFUNDIDAD (BPP)")
    print("#"*70)
    print("\n❓ ¿Qué ocurre si exploro en profundidad antes de considerar costos?")
    
    input("\n⏸️  Presiona ENTER para ejecutar BPP...")
    camino_bpp, orden_bpp = bpp(grafo, inicio, objetivo)
    
    # ==================================================
    # PREGUNTA 3: CU - Ruta de menor costo
    # ==================================================
    print("\n\n" + "#"*70)
    print("# PREGUNTA 3: BÚSQUEDA DE COSTO UNIFORME (CU)")
    print("#"*70)
    print("\n❓ ¿Cuál es la ruta de menor costo en términos de relación social?")
    print("   (Considerando el número de interacciones entre amigos)")
    
    input("\n⏸️  Presiona ENTER para ejecutar CU...")
    camino_cu, costo_cu, orden_cu = cu(grafo, inicio, objetivo)
    
    # ==================================================
    # RESUMEN COMPARATIVO FINAL
    # ==================================================
    print("\n\n" + "="*70)
    print("  RESUMEN COMPARATIVO DE LOS TRES ALGORITMOS")
    print("="*70)
    print(f"\n  Búsqueda: {inicio} → {objetivo}\n")
    
    print("┌" + "─"*68 + "┐")
    print("│ ALGORITMO │ RUTA ENCONTRADA          │ PASOS │ COSTO │ OPTIM. │")
    print("├" + "─"*68 + "┤")
    
    # BPA
    if camino_bpa:
        ruta_bpa = ' → '.join(camino_bpa)
        pasos_bpa = len(camino_bpa) - 1
        # Ajustar formato según longitud
        espacios = max(24 - len(ruta_bpa), 0)
        print(f"│ BPA       │ {ruta_bpa}{' '*espacios} │   {pasos_bpa}   │   -   │   Sí   │")
    else:
        print("│ BPA       │ No encontrada            │   -   │   -   │   -    │")
    
    # BPP
    if camino_bpp:
        ruta_bpp = ' → '.join(camino_bpp)
        pasos_bpp = len(camino_bpp) - 1
        # Si es muy larga, truncar
        if len(ruta_bpp) > 24:
            ruta_bpp_mostrar = ruta_bpp[:21] + "..."
        else:
            ruta_bpp_mostrar = ruta_bpp
        espacios = max(24 - len(ruta_bpp_mostrar), 0)
        print(f"│ BPP       │ {ruta_bpp_mostrar}{' '*espacios} │   {pasos_bpp}   │   -   │   NO   │")
    else:
        print("│ BPP       │ No encontrada            │   -   │   -   │   -    │")
    
    # CU
    if camino_cu:
        ruta_cu = ' → '.join(camino_cu)
        pasos_cu = len(camino_cu) - 1
        espacios = max(24 - len(ruta_cu), 0)
        print(f"│ CU        │ {ruta_cu}{' '*espacios} │   {pasos_cu}   │   {costo_cu}   │   Sí   │")
    else:
        print("│ CU        │ No encontrada            │   -   │   -   │   -    │")
    
    print("└" + "─"*68 + "┘")
    
    # Análisis y conclusiones
    print("\n📌 ANÁLISIS Y CONCLUSIONES:\n")
    
    print("1️⃣  BPA (Búsqueda Primero en Anchura):")
    print("   ✓ Encuentra la ruta con MENOR NÚMERO DE PASOS")
    print("   ✓ Garantiza optimalidad cuando todos los costos son iguales (unitarios)")
    if camino_bpa:
        print(f"   → Ruta: {' → '.join(camino_bpa)} ({len(camino_bpa)-1} pasos)")
    
    print("\n2️⃣  BPP (Búsqueda Primero en Profundidad):")
    print("   ✗ NO garantiza encontrar la ruta más corta")
    print("   ✗ Puede encontrar rutas muy ineficientes")
    print("   ✓ Útil cuando solo se necesita UNA solución, no la mejor")
    if camino_bpp:
        print(f"   → Ruta: {' → '.join(camino_bpp)} ({len(camino_bpp)-1} pasos)")
        if camino_bpa and len(camino_bpp) > len(camino_bpa):
            diferencia = len(camino_bpp) - len(camino_bpa)
            print(f"   ⚠️  Esta ruta tiene {diferencia} paso{'s' if diferencia > 1 else ''} MÁS que BPA")
    
    print("\n3️⃣  CU (Búsqueda de Costo Uniforme):")
    print("   ✓ Encuentra la ruta de MENOR COSTO TOTAL")
    print("   ✓ Garantiza optimalidad considerando costos variables")
    print("   ✓ IDEAL para este problema (relaciones sociales con diferentes fuerzas)")
    if camino_cu:
        print(f"   → Ruta: {' → '.join(camino_cu)} (costo total: {costo_cu})")
    
    # Análisis específico del caso
    print(f"\n🎯 PARA ESTE CASO ESPECÍFICO ({inicio} → {objetivo}):")
    
    if camino_bpa and camino_cu and camino_bpa == camino_cu:
        print("   • BPA y CU encontraron LA MISMA RUTA")
        print("   • Esto indica que la ruta encontrada es:")
        print(f"     - La más corta en número de pasos ({len(camino_bpa)-1} paso{'s' if len(camino_bpa)-1 != 1 else ''})")
        print(f"     - La de menor costo total (costo = {costo_cu})")
    elif camino_bpa and camino_cu:
        print("   • BPA y CU encontraron RUTAS DIFERENTES")
        print(f"   • BPA encontró la ruta más corta en pasos: {' → '.join(camino_bpa)}")
        print(f"   • CU encontró la ruta de menor costo: {' → '.join(camino_cu)} (costo {costo_cu})")
    
    if camino_bpp and camino_bpa and len(camino_bpp) > len(camino_bpa):
        factor = len(camino_bpp) / len(camino_bpa)
        print(f"   • BPP encontró una ruta {factor:.1f}x MÁS LARGA que BPA")
        print("   • Esto demuestra que BPP NO es apropiado para encontrar rutas óptimas")
    
    print("\n" + "="*70)
    print("                        FIN DEL ANÁLISIS")
    print("="*70)

# ==================================================
# EJECUCIÓN DEL PROGRAMA
# ==================================================

if __name__ == "__main__":
    main()