def dfs_adj_matrix(adj_matrix):
    n = len(adj_matrix)
    visited = [0] * n
    result = []
    
    def dfs_visit(v):
        if visited[v] == 1:
            return False
        if visited[v] == 2:
            return True
        
        visited[v] = 1
        
        for u in range(n):
            if adj_matrix[v][u] == 1:
                if not dfs_visit(u):
                    return False
        
        visited[v] = 2
        result.append(v + 1)
        return True
    
    for v in range(n):
        if visited[v] == 0:
            if not dfs_visit(v):
                print("Graf zawiera cykl. Sortowanie niemożliwe.")
                return None
    
    result.reverse()
    return result


def dfs_graph_matrix(graph_matrix):
    n = len(graph_matrix)
    visited = [0] * n
    result = []
    has_cycle = [False]

    def dfs_visit(v):
        if visited[v] == 1:
            has_cycle[0] = True
            return
        if visited[v] == 2:
            return
            
        visited[v] = 1
        
        cycle_node = graph_matrix[v][n + 3]
        if cycle_node > 0:
            has_cycle[0] = True
        
        first_successor = graph_matrix[v][n]
        if first_successor > 0:
            dfs_visit(first_successor - 1)
            
            for u in range(n):
                value = graph_matrix[v][u]
                if 0 < value <= n:
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
