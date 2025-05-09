import argparse

from graph_representations import (
    create_adjacency_matrix, 
    create_adjacency_list, 
    create_graph_matrix
)
from topological_sort_dfs import dfs_adj_matrix, dfs_graph_matrix
from topological_sort_kahn import kahn_adj_matrix, kahn_graph_matrix
from file_handler import read_graph_from_file


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{cell:4}" for cell in row))


def main():
    parser = argparse.ArgumentParser(description='Sortowanie topologiczne grafów')
    parser.add_argument('-f', '--file', required=True, help='Ścieżka do pliku z danymi grafu')
    parser.add_argument('-a', '--algorithm', required=True, choices=['dfs_adj', 'dfs_graph', 'kahn_adj', 'kahn_graph'],
                      help='Algorytm sortowania: dfs_adj (DFS na macierzy sąsiedztwa), dfs_graph (DFS na macierzy grafu), '
                           'kahn_adj (Kahn na macierzy sąsiedztwa), kahn_graph (Kahn na macierzy grafu)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Wyświetl dodatkowe informacje')
    
    args = parser.parse_args()
    
    num_vertices, edges = read_graph_from_file(args.file)
    if num_vertices is None or edges is None:
        return
    
    print(f"Wczytano graf z {num_vertices} wierzchołkami i {len(edges)} krawędziami.")
    
    if args.verbose:
        print("Krawędzie grafu:")
        for edge in edges:
            print(f"{edge[0]} -> {edge[1]}")
    
    adj_list = create_adjacency_list(edges, num_vertices)
    
    result = None
    
    if args.algorithm == 'dfs_adj':
        print("\nSortowanie topologiczne metodą DFS na macierzy sąsiedztwa:")
        adj_matrix = create_adjacency_matrix(edges, num_vertices)
        
        if args.verbose:
            print("\nMacierz sąsiedztwa:")
            print_matrix(adj_matrix)
        
        result = dfs_adj_matrix(adj_matrix)
        
    elif args.algorithm == 'dfs_graph':
        print("\nSortowanie topologiczne metodą DFS na macierzy grafu:")
        graph_matrix = create_graph_matrix(adj_list)
        
        if args.verbose:
            print("\nMacierz grafu:")
            print_matrix(graph_matrix)
        
        result = dfs_graph_matrix(graph_matrix)
        
    elif args.algorithm == 'kahn_adj':
        print("\nSortowanie topologiczne algorytmem Kahna na macierzy sąsiedztwa:")
        adj_matrix = create_adjacency_matrix(edges, num_vertices)
        
        if args.verbose:
            print("\nMacierz sąsiedztwa:")
            print_matrix(adj_matrix)
        
        result = kahn_adj_matrix(adj_matrix)
        
    elif args.algorithm == 'kahn_graph':
        print("\nSortowanie topologiczne algorytmem Kahna na macierzy grafu:")
        graph_matrix = create_graph_matrix(adj_list)
        
        if args.verbose:
            print("\nMacierz grafu:")
            print_matrix(graph_matrix)
        
        result = kahn_graph_matrix(graph_matrix)
    
    if result is not None:
        print("\nPorządek topologiczny:")
        print(" -> ".join(map(str, result)))


if __name__ == "__main__":
    main()
