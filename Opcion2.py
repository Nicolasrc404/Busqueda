#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taller: Red Social y Modelos de Búsqueda con IA
Algoritmos: BPA, BPP, CU
"""

import sys

# ==================================================
# GRAFO DE LA RED SOCIAL
# ==================================================

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

# ==================================================
# ALGORITMO BPA (Búsqueda Primero en Anchura)
# ==================================================

def bpa(grafo, inicio, objetivo):
    """Encuentra la ruta más corta en pasos (cola FIFO)"""
    cola = [(inicio, [inicio])]
    visitados = set()
    orden = []
    
    print("\n=== BPA (Búsqueda Primero en Anchura) ===")
    
    while cola:
        nodo, camino = cola.pop(0)
        
        if nodo not in visitados:
            visitados.add(nodo)
            orden.append(nodo)
            
            if nodo == objetivo:
                print(f"Orden de visita: {' → '.join(orden)}")
                print(f"Ruta: {' → '.join(camino)} ({len(camino)-1} pasos)")
                return camino
            
            for vecino, _ in grafo[nodo]:
                if vecino not in visitados:
                    cola.append((vecino, camino + [vecino]))
    
    return None

# ==================================================
# ALGORITMO BPP (Búsqueda Primero en Profundidad)
# ==================================================

def bpp(grafo, inicio, objetivo):
    """Explora en profundidad (pila LIFO)"""
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
            print(f"Orden de visita: {' → '.join(orden)}")
            print(f"Ruta: {' → '.join(camino)} ({len(camino)-1} pasos)")
            return camino
        
        for vecino, _ in reversed(grafo[nodo]):
            if vecino not in visitados:
                pila.append((vecino, camino + [vecino]))
    
    return None

# ==================================================
# ALGORITMO CU (Búsqueda de Costo Uniforme)
# ==================================================

def cu(grafo, inicio, objetivo):
    """Encuentra la ruta de menor costo (cola de prioridad)"""
    cola = [(0, inicio, [inicio])]
    visitados = set()
    orden = []
    
    print("\n=== CU (Búsqueda de Costo Uniforme) ===")
    
    while cola:
        cola.sort(key=lambda x: (x[0], x[1]))
        costo, nodo, camino = cola.pop(0)
        
        if nodo not in visitados:
            visitados.add(nodo)
            orden.append(nodo)
            
            if nodo == objetivo:
                print(f"Orden de visita: {' → '.join(orden)}")
                print(f"Ruta: {' → '.join(camino)} ({len(camino)-1} pasos)")
                print(f"Costo total: {costo}")
                return camino, costo
            
            for vecino, costo_arista in grafo[nodo]:
                if vecino not in visitados:
                    cola.append((costo + costo_arista, vecino, camino + [vecino]))
    
    return None, float('inf')

# ==================================================
# FUNCIÓN PRINCIPAL
# ==================================================

def main():
    print("="*60)
    print("TALLER: Red Social y Búsqueda con IA")
    print("="*60)
    
    grafo = crear_grafo()
    
    # Obtener nodos inicial y objetivo
    if len(sys.argv) >= 3:
        inicio = sys.argv[1].upper()
        objetivo = sys.argv[2].upper()
    else:
        print("\nNodos disponibles: A, B, C, D, E, F, G, H, I, J")
        inicio = input("Nodo inicial: ").upper()
        objetivo = input("Nodo objetivo: ").upper()
    
    # Validar nodos
    if inicio not in grafo or objetivo not in grafo:
        print("Error: Nodo inválido")
        return
    if inicio == objetivo:
        print("Error: Los nodos deben ser diferentes")
        return
    
    print(f"\nBúsqueda: {inicio} → {objetivo}")
    print("="*60)
    
    # Ejecutar algoritmos
    camino_bpa = bpa(grafo, inicio, objetivo)
    camino_bpp = bpp(grafo, inicio, objetivo)
    camino_cu, costo_cu = cu(grafo, inicio, objetivo)
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN COMPARATIVO")
    print("="*60)
    
    if camino_bpa:
        print(f"BPA: {' → '.join(camino_bpa)} ({len(camino_bpa)-1} pasos)")
    if camino_bpp:
        print(f"BPP: {' → '.join(camino_bpp)} ({len(camino_bpp)-1} pasos)")
    if camino_cu:
        print(f"CU:  {' → '.join(camino_cu)} ({len(camino_cu)-1} pasos, costo {costo_cu})")
    
    # Análisis
    print("\nCONCLUSIONES:")
    print("• BPA: Encuentra la ruta MÁS CORTA en pasos ✓")
    print("• BPP: NO garantiza optimalidad ✗")
    print("• CU:  Encuentra la ruta de MENOR COSTO ✓")
    
    if camino_bpa and camino_cu and camino_bpa == camino_cu:
        print(f"\n✓ BPA y CU encontraron la misma ruta óptima")
    
    if camino_bpp and camino_bpa and len(camino_bpp) > len(camino_bpa):
        print(f"⚠ BPP encontró una ruta {len(camino_bpp)-len(camino_bpa)} pasos más larga")
    
    print("="*60)

if __name__ == "__main__":
    main()