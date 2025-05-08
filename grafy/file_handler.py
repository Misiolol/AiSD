"""
Moduł do obsługi plików wejściowych.
"""


def read_graph_from_file(filename):
    """
    Wczytuje graf z pliku tekstowego w formacie listy krawędzi.
    
    Args:
        filename: Nazwa pliku wejściowego
    
    Returns:
        Tuple (num_vertices, edges) gdzie:
        - num_vertices: liczba wierzchołków w grafie
        - edges: lista krawędzi w postaci par (from_vertex, to_vertex)
    """
    edges = []
    
    try:
        with open(filename, 'r') as file:
            # Wczytujemy pierwszą linię z informacją o liczbie wierzchołków i krawędzi
            first_line = file.readline().strip()
            num_vertices, num_edges = map(int, first_line.split())
            
            # Wczytujemy krawędzie
            for _ in range(num_edges):
                line = file.readline().strip()
                if not line:
                    continue
                
                from_vertex, to_vertex = map(int, line.split())
                edges.append((from_vertex, to_vertex))
    
    except FileNotFoundError:
        print(f"Błąd: Plik {filename} nie istnieje.")
        return None, None
    except ValueError:
        print(f"Błąd: Nieprawidłowy format danych w pliku {filename}.")
        return None, None
    
    return num_vertices, edges