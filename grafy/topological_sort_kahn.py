from collections import deque

def kahn_adj_matrix(adj_matrix):
    n = len(adj_matrix)
    result = []
    in_degree = [0] * n
    for i in range(n):
        for j in range(n):
            if adj_matrix[j][i] == 1:
                in_degree[i] += 1
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    while queue:
        v = queue.popleft()
        result.append(v + 1)
        for u in range(n):
            if adj_matrix[v][u] == 1:
                in_degree[u] -= 1
                if in_degree[u] == 0:
                    queue.append(u)
    if len(result) != n:
        print("Graf zawiera cykl. Sortowanie niemożliwe.")
        return None
    return result

def detect_cycle_graph_matrix(graph_matrix):
    n = len(graph_matrix)
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            val = graph_matrix[i][j]
            if 0 < val <= n:
                adj_matrix[i][val-1] = 1
            elif 2*n+1 <= val <= 3*n:
                cycle_node = val - (2*n+1)
                if cycle_node < n:
                    return True
        if graph_matrix[i][n] > 0 and graph_matrix[i][n] <= n:
            adj_matrix[i][graph_matrix[i][n]-1] = 1
    visited = [0] * n
    def dfs(v):
        visited[v] = 1
        for u in range(n):
            if adj_matrix[v][u] == 1:
                if visited[u] == 1:
                    return True
                elif visited[u] == 0:
                    if dfs(u):
                        return True
        visited[v] = 2
        return False
    for v in range(n):
        if visited[v] == 0:
            if dfs(v):
                return True
    return False

def kahn_graph_matrix(graph_matrix):
    if detect_cycle_graph_matrix(graph_matrix):
        print("Graf zawiera cykl. Sortowanie niemożliwe.")
        return None
    n = len(graph_matrix)
    result = []
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        first_succ = graph_matrix[i][n]
        if first_succ > 0 and first_succ <= n:
            adj_matrix[i][first_succ-1] = 1
        for j in range(n):
            val = graph_matrix[i][j]
            if 0 < val <= n:
                adj_matrix[i][val-1] = 1
    in_degree = [0] * n
    for i in range(n):
        for j in range(n):
            if adj_matrix[j][i] == 1:
                in_degree[i] += 1
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    while queue:
        v = queue.popleft()
        result.append(v + 1)
        for u in range(n):
            if adj_matrix[v][u] == 1:
                in_degree[u] -= 1
                if in_degree[u] == 0:
                    queue.append(u)
    if len(result) != n:
        print("Graf zawiera cykl. Sortowanie niemożliwe.")
        return None
    return result
