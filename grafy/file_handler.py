def read_graph_from_file(filename):
    edges = []
    
    try:
        with open(filename, 'r') as file:
            first_line = file.readline().strip()
            num_vertices, num_edges = map(int, first_line.split())
            
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
