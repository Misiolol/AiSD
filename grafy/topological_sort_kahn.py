"""
Poprawiona implementacja algorytmu sortowania topologicznego Kahna
dla macierzy grafu, która poprawnie wykrywa cykle.
"""
from collections import deque


def kahn_adj_matrix(adj_matrix):
    """
    Sortowanie topologiczne z wykorzystaniem algorytmu Kahna na macierzy sąsiedztwa.
    
    Args:
        adj_matrix: Macierz sąsiedztwa
    
    Returns:
        Lista wierzchołków w porządku topologicznym lub None, jeśli istnieje cykl
    """
    n = len(adj_matrix)
    result = []
    
    # Obliczamy stopień wejściowy dla każdego wierzchołka
    in_degree = [0] * n
    for i in range(n):
        for j in range(n):
            if adj_matrix[j][i] == 1:
                in_degree[i] += 1
    
    # Dodajemy wierzchołki o zerowym stopniu wejściowym do kolejki
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Przetwarzamy wierzchołki w kolejce
    while queue:
        v = queue.popleft()
        result.append(v + 1)  # Dodajemy do wyniku (indeks od 1)
        
        # Usuwamy krawędzie wychodzące z v
        for u in range(n):
            if adj_matrix[v][u] == 1:
                in_degree[u] -= 1
                if in_degree[u] == 0:
                    queue.append(u)
    
    # Jeśli nie udało się odwiedzić wszystkich wierzchołków, to graf zawiera cykl
    if len(result) != n:
        print("Graf zawiera cykl. Sortowanie niemożliwe.")
        return None
    
    return result


def detect_cycle_graph_matrix(graph_matrix):
    """
    Wykrywanie cykli w grafie reprezentowanym przez macierz grafu.
    
    Args:
        graph_matrix: Macierz grafu
    
    Returns:
        True jeśli graf zawiera cykl, False w przeciwnym przypadku
    """
    n = len(graph_matrix)
    
    # Konwertujemy macierz grafu na macierz sąsiedztwa
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    # Przetwarzamy główną część macierzy
    for i in range(n):
        for j in range(n):
            val = graph_matrix[i][j]
            
            # Bezpośredni łuk i -> j
            if 0 < val <= n:
                adj_matrix[i][val-1] = 1
            
            # Cykl (oba łuki)
            elif 2*n+1 <= val <= 3*n:
                cycle_node = val - (2*n+1)
                if cycle_node < n:
                    return True  # Znaleziono bezpośredni cykl
        
        # Sprawdzamy pierwszego następnika z kolumny n
        if graph_matrix[i][n] > 0 and graph_matrix[i][n] <= n:
            adj_matrix[i][graph_matrix[i][n]-1] = 1
    
    # Wykonujemy DFS, aby wykryć cykle
    visited = [0] * n  # 0: nieodwiedzony, 1: w trakcie odwiedzania, 2: odwiedzony
    
    def dfs(v):
        visited[v] = 1  # Oznaczamy jako "w trakcie odwiedzania"
        
        # Sprawdzamy wszystkich sąsiadów
        for u in range(n):
            if adj_matrix[v][u] == 1:
                if visited[u] == 1:  # Jeśli wierzchołek jest już odwiedzany, znaleźliśmy cykl
                    return True
                elif visited[u] == 0:  # Jeśli wierzchołek nie był odwiedzany
                    if dfs(u):
                        return True
        
        visited[v] = 2  # Oznaczamy jako "odwiedzony"
        return False
    
    # Wywołujemy DFS dla każdego nieodwiedzonego wierzchołka
    for v in range(n):
        if visited[v] == 0:
            if dfs(v):
                return True
    
    return False


def kahn_graph_matrix(graph_matrix):
    """
    Poprawiony algorytm Kahna dla macierzy grafu, który najpierw sprawdza
    czy graf zawiera cykl, a następnie wykonuje sortowanie topologiczne.
    
    Args:
        graph_matrix: Macierz grafu
    
    Returns:
        Lista wierzchołków w porządku topologicznym lub None, jeśli istnieje cykl
    """
    # Najpierw sprawdzamy, czy graf zawiera cykl
    if detect_cycle_graph_matrix(graph_matrix):
        print("Graf zawiera cykl. Sortowanie niemożliwe.")
        return None
    
    n = len(graph_matrix)
    result = []
    
    # Konwertujemy macierz grafu na macierz sąsiedztwa dla łatwiejszego przetwarzania
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    # Wypełniamy macierz sąsiedztwa
    for i in range(n):
        # Sprawdzamy pierwszy następnik z kolumny dodatkowej
        first_succ = graph_matrix[i][n]
        if first_succ > 0 and first_succ <= n:
            adj_matrix[i][first_succ-1] = 1
        
        # Przetwarzamy główną część macierzy
        for j in range(n):
            val = graph_matrix[i][j]
            
            # Łuk i -> j (wartość z przedziału <0,n>)
            if 0 < val <= n:
                adj_matrix[i][val-1] = 1
    
    # Teraz wykonujemy standardowy algorytm Kahna na macierzy sąsiedztwa
    # Obliczamy stopień wejściowy dla każdego wierzchołka
    in_degree = [0] * n
    for i in range(n):
        for j in range(n):
            if adj_matrix[j][i] == 1:
                in_degree[i] += 1
    
    # Dodajemy wierzchołki o zerowym stopniu wejściowym do kolejki
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Przetwarzamy wierzchołki w kolejce
    while queue:
        v = queue.popleft()
        result.append(v + 1)  # Dodajemy do wyniku (indeks od 1)
        
        # Usuwamy krawędzie wychodzące z v
        for u in range(n):
            if adj_matrix[v][u] == 1:
                in_degree[u] -= 1
                if in_degree[u] == 0:
                    queue.append(u)
    
    # Jeśli nie udało się odwiedzić wszystkich wierzchołków, to graf zawiera cykl
    # (dodatkowa weryfikacja, choć już sprawdziliśmy wcześniej)
    if len(result) != n:
        print("Graf zawiera cykl. Sortowanie niemożliwe.")
        return None
    
    return result