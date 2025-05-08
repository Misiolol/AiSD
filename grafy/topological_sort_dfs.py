"""
Implementacja algorytmów sortowania topologicznego
wykorzystujących przechodzenie w głąb (DFS).
"""


def dfs_adj_matrix(adj_matrix):
    """
    Sortowanie topologiczne z wykorzystaniem DFS na macierzy sąsiedztwa.
    
    Args:
        adj_matrix: Macierz sąsiedztwa
    
    Returns:
        Lista wierzchołków w porządku topologicznym lub None, jeśli istnieje cykl
    """
    n = len(adj_matrix)
    visited = [0] * n  # 0: nie odwiedzony, 1: w trakcie przetwarzania, 2: zakończony
    result = []
    
    def dfs_visit(v):
        if visited[v] == 1:  # Wierzchołek jest obecnie na stosie - wykryto cykl
            return False
        if visited[v] == 2:  # Wierzchołek już przetworzony
            return True
        
        visited[v] = 1  # Oznaczamy jako przetwarzany
        
        # Sprawdzamy wszystkich następników
        for u in range(n):
            if adj_matrix[v][u] == 1:  # Istnieje krawędź v -> u
                if not dfs_visit(u):
                    return False
        
        visited[v] = 2  # Oznaczamy jako zakończony
        result.append(v + 1)  # Dodajemy do wyniku (indeks od 1)
        return True
    
    # Uruchamiamy DFS dla każdego nieodwiedzonego wierzchołka
    for v in range(n):
        if visited[v] == 0:
            if not dfs_visit(v):
                print("Graf zawiera cykl. Sortowanie niemożliwe.")
                return None
    
    # Odwracamy wynik, ponieważ wierzchołki dodawane są w odwrotnej kolejności
    result.reverse()
    return result


def dfs_graph_matrix(graph_matrix):
    n = len(graph_matrix)
    visited = [0] * n  # 0: nieodwiedzony, 1: przetwarzany, 2: zakończony
    result = []
    has_cycle = [False]  # Używamy listy aby móc modyfikować w zagnieżdżonej funkcji

    def dfs_visit(v):
        if visited[v] == 1:
            has_cycle[0] = True
            return
        if visited[v] == 2:
            return
            
        visited[v] = 1
        
        # Sprawdzamy kolumnę cykli (|V|+4)
        cycle_node = graph_matrix[v][n + 3]
        if cycle_node > 0:
            has_cycle[0] = True
        
        # Przetwarzamy następników
        first_successor = graph_matrix[v][n]  # Kolumna |V|+1
        if first_successor > 0:
            dfs_visit(first_successor - 1)
            
            # Sprawdzamy główną część macierzy dla kolejnych następników
            for u in range(n):
                value = graph_matrix[v][u]
                if 0 < value <= n:  # Wartości w tym zakresie to następnicy
                    dfs_visit(value - 1)
        
        visited[v] = 2
        result.append(v + 1)

    for v in range(n):
        if visited[v] == 0 and not has_cycle[0]:
            dfs_visit(v)
    
    if has_cycle[0]:
        print("Graf zawiera cykl. Sortowanie niemożliwe.")
        return None
        
    result.reverse()
    return result