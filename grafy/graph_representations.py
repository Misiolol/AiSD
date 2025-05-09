"""
Moduł zawierający implementacje różnych reprezentacji grafu.
"""

def create_adjacency_matrix(edges, num_vertices):
    """
    Tworzy macierz sąsiedztwa na podstawie listy krawędzi.
    
    Args:
        edges: Lista krawędzi w postaci listy par (from_vertex, to_vertex)
        num_vertices: Liczba wierzchołków w grafie
    
    Returns:
        Macierz sąsiedztwa gdzie adj_matrix[i][j] = 1, jeśli istnieje krawędź z i do j, w przeciwnym razie 0
    """
    # Tworzymy macierz wypełnioną zerami
    adj_matrix = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
    
    # Wypełniamy macierz na podstawie listy krawędzi
    for from_vertex, to_vertex in edges:
        # Odejmujemy 1, aby indeksować od 0
        adj_matrix[from_vertex-1][to_vertex-1] = 1
    
    return adj_matrix

def create_adjacency_list(edges, num_vertices):
    """
    Tworzy listę sąsiedztwa na podstawie listy krawędzi.
    
    Args:
        edges: Lista krawędzi w postaci listy par (from_vertex, to_vertex)
        num_vertices: Liczba wierzchołków w grafie
    
    Returns:
        Słownik, gdzie kluczami są numery wierzchołków, a wartościami listy sąsiadów
    """
    # Inicjujemy słownik z pustymi listami dla każdego wierzchołka
    adj_list = {i+1: [] for i in range(num_vertices)}
    
    # Wypełniamy listy sąsiedztwa na podstawie listy krawędzi
    for from_vertex, to_vertex in edges:
        adj_list[from_vertex].append(to_vertex)
    
    return adj_list

def detect_cycles(adj_list):
    """
    Wykrywa cykle w grafie skierowanym za pomocą DFS.
    
    Args:
        adj_list: Lista sąsiedztwa grafu
    
    Returns:
        True, jeśli graf zawiera cykl, False w przeciwnym przypadku
    """
    num_vertices = len(adj_list)
    visited = [0] * (num_vertices + 1)  # 0: nie odwiedzony, 1: w trakcie przetwarzania, 2: zakończony
    
    def dfs_cycle_check(vertex):
        if visited[vertex] == 1:  # Wierzchołek jest obecnie na stosie - wykryto cykl
            return True
        if visited[vertex] == 2:  # Wierzchołek już przetworzony
            return False
        
        visited[vertex] = 1  # Oznaczamy jako przetwarzany
        
        # Sprawdzamy wszystkich następników
        for neighbor in adj_list[vertex]:
            if dfs_cycle_check(neighbor):
                return True
        
        visited[vertex] = 2  # Oznaczamy jako zakończony
        return False
    
    # Uruchamiamy DFS dla każdego nieodwiedzonego wierzchołka
    for v in range(1, num_vertices + 1):
        if visited[v] == 0:
            if dfs_cycle_check(v):
                return True
    
    return False

def create_graph_matrix(adj_list):
    """
    Tworzy macierz grafu na podstawie listy sąsiedztwa, poprawnie obsługując multigrafy i pętle
    
    Args:
        adj_list: Lista sąsiedztwa w formacie {wierzchołek: [następniki]}
    
    Returns:
        Macierz grafu zgodna ze specyfikacją z wykładu
    """
    # Ustalamy liczbę wierzchołków
    num_vertices = len(adj_list)
    
    # Tworzymy głębokie kopie list sąsiedztwa, aby nie modyfikować oryginalnych danych
    successors = {i+1: [] for i in range(num_vertices)}  # Lista następników (LN)
    predecessors = {i+1: [] for i in range(num_vertices)}  # Lista poprzedników (LP)
    non_incident = {i+1: [] for i in range(num_vertices)}  # Lista braku incydencji (LB)
    cycles = {i+1: [] for i in range(num_vertices)}  # Lista cykli (LC)
    
    # Kopiujemy listy następników z listy sąsiedztwa
    # (zachowujemy dublety dla krawędzi wielokrotnych)
    for vertex, neighbors in adj_list.items():
        successors[vertex] = neighbors.copy()
    
    # Wypełniamy listy poprzedników, zachowując wielokrotne krawędzie
    for vertex, neighbors in adj_list.items():
        for neighbor in neighbors:
            predecessors[neighbor].append(vertex)
    
    # Identyfikujemy pętle (cykle długości 0) i cykle długości 1
    cycles_to_process = {}  # Słownik do przechowywania zidentyfikowanych cykli
    
    # Najpierw identyfikujemy wszystkie cykle
    for vertex, neighbors in adj_list.items():
        # Pętle (cykle długości 0)
        if vertex in neighbors:
            # Zliczamy wystąpienia danego wierzchołka w sąsiedztwie
            count = neighbors.count(vertex)
            # Dodajemy odpowiednią liczbę pętli do cykli
            for _ in range(count):
                if vertex not in cycles[vertex]:
                    cycles[vertex].append(vertex)
            
            # Dodajemy informację o cyklach do przetworzenia później
            if vertex not in cycles_to_process:
                cycles_to_process[vertex] = {}
            cycles_to_process[vertex][vertex] = count
        
        # Cykle długości 1
        for neighbor in neighbors:
            if vertex in adj_list.get(neighbor, []) and vertex != neighbor:
                # Zliczamy ilość dwukierunkowych połączeń
                count_v_to_n = neighbors.count(neighbor)
                count_n_to_v = adj_list[neighbor].count(vertex)
                min_count = min(count_v_to_n, count_n_to_v)
                
                # Dodajemy odpowiednią liczbę cykli
                for _ in range(min_count):
                    if neighbor not in cycles[vertex]:
                        cycles[vertex].append(neighbor)
                
                # Dodajemy informację o cyklach do przetworzenia później
                if vertex not in cycles_to_process:
                    cycles_to_process[vertex] = {}
                cycles_to_process[vertex][neighbor] = min_count
    
    # Przetwarzamy zidentyfikowane cykle - usuwamy odpowiednią liczbę cykli z list następników i poprzedników
    for v1, neighbors in cycles_to_process.items():
        for v2, count in neighbors.items():
            # Usuwamy określoną liczbę krawędzi z list następników i poprzedników
            for _ in range(count):
                if v2 in successors[v1]:
                    successors[v1].remove(v2)
                if v1 in predecessors[v2]:
                    predecessors[v2].remove(v1)
                
                # Dla cykli długości 1 usuwamy także krawędzie przeciwne
                if v1 != v2:
                    if v1 in successors[v2]:
                        successors[v2].remove(v1)
                    if v2 in predecessors[v1]:
                        predecessors[v1].remove(v2)
    
    # Wypełniamy listy braku incydencji (wierzchołki niepowiązane łukami)
    for v1 in range(1, num_vertices + 1):
        for v2 in range(1, num_vertices + 1):
            if v2 not in successors[v1] and v1 not in successors[v2] and v2 not in cycles[v1]:
                non_incident[v1].append(v2)
    
    # Tworzymy macierz grafu o wymiarach |V| x (|V| + 4)
    matrix = [[0 for _ in range(num_vertices + 4)] for _ in range(num_vertices)]
    
    # Wypełniamy macierz relacjami między wierzchołkami (Krok 0)
    for i in range(num_vertices):
        for j in range(num_vertices):
            vi = i + 1
            vj = j + 1
            
            # Sprawdzamy typ połączenia
            is_successor = vj in successors[vi]
            is_predecessor = vi in successors[vj]
            is_cycle = vj in cycles[vi]
            
            if is_cycle:
                # Wierzchołki są w cyklu (obsłużymy to w kroku 4)
                pass
            elif is_successor and is_predecessor:
                # vj jest następnikiem i poprzednikiem vi
                matrix[i][j] = 2
            elif is_successor:
                # vj jest następnikiem vi
                matrix[i][j] = 5
            elif is_predecessor:
                # vj jest poprzednikiem vi
                matrix[i][j] = 3
            else:
                # vi, vj nie są połączone łukiem
                matrix[i][j] = -1
    
    # Krok 1: Wypełniamy kolumnę następników (|V|+1)
    for i in range(num_vertices):
        vi = i + 1
        if successors[vi]:
            matrix[i][num_vertices] = successors[vi][0]  # Pierwszy następnik
            
            for j in range(num_vertices):
                vj = j + 1
                if vj in successors[vi]:
                    # Znajdujemy indeks następnika w liście następników
                    idx = successors[vi].index(vj)
                    # Jeśli istnieje kolejny następnik, bierzemy go, w przeciwnym razie ostatni
                    if idx + 1 < len(successors[vi]):
                        matrix[i][j] = successors[vi][idx + 1]
                    else:
                        matrix[i][j] = successors[vi][-1]
    
    # Krok 2: Wypełniamy kolumnę poprzedników (|V|+2)
    for i in range(num_vertices):
        vi = i + 1
        if predecessors[vi]:
            matrix[i][num_vertices + 1] = predecessors[vi][0]  # Pierwszy poprzednik
            
            for j in range(num_vertices):
                vj = j + 1
                if vj in predecessors[vi]:
                    # Znajdujemy indeks poprzednika w liście poprzedników
                    idx = predecessors[vi].index(vj)
                    # Jeśli istnieje kolejny poprzednik, bierzemy go, w przeciwnym razie ostatni
                    if idx + 1 < len(predecessors[vi]):
                        next_pred = predecessors[vi][idx + 1]
                    else:
                        next_pred = predecessors[vi][-1]
                    # Dodajemy liczbę wierzchołków
                    matrix[i][j] = next_pred + num_vertices
    
    # Krok 3: Wypełniamy kolumnę braku incydencji (|V|+3)
    for i in range(num_vertices):
        vi = i + 1
        if non_incident[vi]:
            matrix[i][num_vertices + 2] = non_incident[vi][0]  # Pierwszy nieincydentny
            
            for j in range(num_vertices):
                vj = j + 1
                if vj in non_incident[vi]:
                    # Znajdujemy indeks nieincydentnego w liście braku incydencji
                    idx = non_incident[vi].index(vj)
                    # Jeśli istnieje kolejny nieincydentny, bierzemy go, w przeciwnym razie ostatni
                    if idx + 1 < len(non_incident[vi]):
                        next_non = non_incident[vi][idx + 1]
                    else:
                        next_non = non_incident[vi][-1]
                    # Dodajemy minus
                    matrix[i][j] = -next_non
    
    # Krok 4: Wypełniamy kolumnę cykli (|V|+4)
    for i in range(num_vertices):
        vi = i + 1
        if cycles[vi]:
            matrix[i][num_vertices + 3] = cycles[vi][0]  # Pierwszy w cyklu
            
            for j in range(num_vertices):
                vj = j + 1
                if vj in cycles[vi]:
                    # Znajdujemy indeks cyklu w liście cykli
                    idx = cycles[vi].index(vj)
                    # Jeśli istnieje kolejny w cyklu, bierzemy go, w przeciwnym razie ostatni
                    if idx + 1 < len(cycles[vi]):
                        next_cycle = cycles[vi][idx + 1]
                    else:
                        next_cycle = cycles[vi][-1]
                    # Dodajemy 2 * liczbę wierzchołków
                    matrix[i][j] = next_cycle + 2 * num_vertices
    
    return matrix