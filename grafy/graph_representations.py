def create_adjacency_matrix(edges, num_vertices):
    adj_matrix = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
    for from_vertex, to_vertex in edges:
        adj_matrix[from_vertex-1][to_vertex-1] = 1
    return adj_matrix

def create_adjacency_list(edges, num_vertices):
    adj_list = {i+1: [] for i in range(num_vertices)}
    for from_vertex, to_vertex in edges:
        adj_list[from_vertex].append(to_vertex)
    return adj_list

def detect_cycles(adj_list):
    num_vertices = len(adj_list)
    visited = [0] * (num_vertices + 1)
    def dfs_cycle_check(vertex):
        if visited[vertex] == 1:
            return True
        if visited[vertex] == 2:
            return False
        visited[vertex] = 1
        for neighbor in adj_list[vertex]:
            if dfs_cycle_check(neighbor):
                return True
        visited[vertex] = 2
        return False
    for v in range(1, num_vertices + 1):
        if visited[v] == 0:
            if dfs_cycle_check(v):
                return True
    return False

def create_graph_matrix(adj_list):
    num_vertices = len(adj_list)
    successors = {i+1: [] for i in range(num_vertices)}
    predecessors = {i+1: [] for i in range(num_vertices)}
    non_incident = {i+1: [] for i in range(num_vertices)}
    cycles = {i+1: [] for i in range(num_vertices)}
    for vertex, neighbors in adj_list.items():
        successors[vertex] = neighbors.copy()
    for vertex, neighbors in adj_list.items():
        for neighbor in neighbors:
            predecessors[neighbor].append(vertex)
    cycles_to_process = {}
    for vertex, neighbors in adj_list.items():
        if vertex in neighbors:
            count = neighbors.count(vertex)
            for _ in range(count):
                if vertex not in cycles[vertex]:
                    cycles[vertex].append(vertex)
            if vertex not in cycles_to_process:
                cycles_to_process[vertex] = {}
            cycles_to_process[vertex][vertex] = count
        for neighbor in neighbors:
            if vertex in adj_list.get(neighbor, []) and vertex != neighbor:
                count_v_to_n = neighbors.count(neighbor)
                count_n_to_v = adj_list[neighbor].count(vertex)
                min_count = min(count_v_to_n, count_n_to_v)
                for _ in range(min_count):
                    if neighbor not in cycles[vertex]:
                        cycles[vertex].append(neighbor)
                if vertex not in cycles_to_process:
                    cycles_to_process[vertex] = {}
                cycles_to_process[vertex][neighbor] = min_count
    for v1, neighbors in cycles_to_process.items():
        for v2, count in neighbors.items():
            for _ in range(count):
                if v2 in successors[v1]:
                    successors[v1].remove(v2)
                if v1 in predecessors[v2]:
                    predecessors[v2].remove(v1)
                if v1 != v2:
                    if v1 in successors[v2]:
                        successors[v2].remove(v1)
                    if v2 in predecessors[v1]:
                        predecessors[v1].remove(v2)
    for v1 in range(1, num_vertices + 1):
        for v2 in range(1, num_vertices + 1):
            if v2 not in successors[v1] and v1 not in successors[v2] and v2 not in cycles[v1]:
                non_incident[v1].append(v2)
    matrix = [[0 for _ in range(num_vertices + 4)] for _ in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(num_vertices):
            vi = i + 1
            vj = j + 1
            is_successor = vj in successors[vi]
            is_predecessor = vi in successors[vj]
            is_cycle = vj in cycles[vi]
            if is_cycle:
                pass
            elif is_successor and is_predecessor:
                matrix[i][j] = 2
            elif is_successor:
                matrix[i][j] = 5
            elif is_predecessor:
                matrix[i][j] = 3
            else:
                matrix[i][j] = -1
    for i in range(num_vertices):
        vi = i + 1
        if successors[vi]:
            matrix[i][num_vertices] = successors[vi][0]
            for j in range(num_vertices):
                vj = j + 1
                if vj in successors[vi]:
                    idx = successors[vi].index(vj)
                    if idx + 1 < len(successors[vi]):
                        matrix[i][j] = successors[vi][idx + 1]
                    else:
                        matrix[i][j] = successors[vi][-1]
    for i in range(num_vertices):
        vi = i + 1
        if predecessors[vi]:
            matrix[i][num_vertices + 1] = predecessors[vi][0]
            for j in range(num_vertices):
                vj = j + 1
                if vj in predecessors[vi]:
                    idx = predecessors[vi].index(vj)
                    if idx + 1 < len(predecessors[vi]):
                        next_pred = predecessors[vi][idx + 1]
                    else:
                        next_pred = predecessors[vi][-1]
                    matrix[i][j] = next_pred + num_vertices
    for i in range(num_vertices):
        vi = i + 1
        if non_incident[vi]:
            matrix[i][num_vertices + 2] = non_incident[vi][0]
            for j in range(num_vertices):
                vj = j + 1
                if vj in non_incident[vi]:
                    idx = non_incident[vi].index(vj)
                    if idx + 1 < len(non_incident[vi]):
                        next_non = non_incident[vi][idx + 1]
                    else:
                        next_non = non_incident[vi][-1]
                    matrix[i][j] = -next_non
    for i in range(num_vertices):
        vi = i + 1
        if cycles[vi]:
            matrix[i][num_vertices + 3] = cycles[vi][0]
            for j in range(num_vertices):
                vj = j + 1
                if vj in cycles[vi]:
                    idx = cycles[vi].index(vj)
                    if idx + 1 < len(cycles[vi]):
                        next_cycle = cycles[vi][idx + 1]
                    else:
                        next_cycle = cycles[vi][-1]
                    matrix[i][j] = next_cycle + 2 * num_vertices
    return matrix
