import sys
import os
from file_handler import read_graph_from_file
from graph_representations import (
    create_adjacency_matrix,
    create_adjacency_list,
    create_graph_matrix
)

sys.path.insert(0, os.path.abspath('.'))
from topological_sort_dfs import dfs_adj_matrix, dfs_graph_matrix
from topological_sort_kahn import kahn_adj_matrix, kahn_graph_matrix

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{cell:4}" for cell in row))

def test_graph(filename):
    print(f"\nTestowanie grafu z pliku: {filename}")
    print("=" * 50)
    
    num_vertices, edges = read_graph_from_file(filename)
    if num_vertices is None or edges is None:
        return
    
    print(f"Wczytano graf z {num_vertices} wierzchołkami i {len(edges)} krawędziami.")
    
    print("\nKrawędzie grafu:")
    for edge in edges:
        print(f"{edge[0]} -> {edge[1]}")
    
    adj_list = create_adjacency_list(edges, num_vertices)
    adj_matrix = create_adjacency_matrix(edges, num_vertices)
    graph_matrix = create_graph_matrix(adj_list)
    
    print("\nMacierz sąsiedztwa:")
    print_matrix(adj_matrix)
    
    print("\nMacierz grafu:")
    print_matrix(graph_matrix)
    
    print("\nSortowanie topologiczne metodą DFS na macierzy sąsiedztwa:")
    result_dfs_adj = dfs_adj_matrix(adj_matrix)
    if result_dfs_adj:
        print("Porządek topologiczny:", " -> ".join(map(str, result_dfs_adj)))
    else:
        print("Nie udało się znaleźć porządku topologicznego.")
    
    print("\nSortowanie topologiczne metodą DFS na macierzy grafu:")
    result_dfs_graph = dfs_graph_matrix(graph_matrix)
    if result_dfs_graph:
        print("Porządek topologiczny:", " -> ".join(map(str, result_dfs_graph)))
    else:
        print("Nie udało się znaleźć porządku topologicznego.")
    
    print("\nSortowanie topologiczne algorytmem Kahna na macierzy sąsiedztwa:")
    result_kahn_adj = kahn_adj_matrix(adj_matrix)
    if result_kahn_adj:
        print("Porządek topologiczny:", " -> ".join(map(str, result_kahn_adj)))
    else:
        print("Nie udało się znaleźć porządku topologicznego.")
    
    print("\nSortowanie topologiczne algorytmem Kahna na macierzy grafu:")
    result_kahn_graph = kahn_graph_matrix(graph_matrix)
    if result_kahn_graph:
        print("Porządek topologiczny:", " -> ".join(map(str, result_kahn_graph)))
    else:
        print("Nie udało się znaleźć porządku topologicznego.")
    
    print("=" * 50)

if __name__ == "__main__":
    test_graph("example_graph.txt")
    test_graph("example_cyclic_graph.txt")
