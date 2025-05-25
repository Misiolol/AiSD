import pygame
from collections import defaultdict
from typing import List, Optional

from button import Button
from constants import Colors
from src.graph import Graph


class AlgoController:

    def __init__(self, graph: Graph):
        self.graph = graph

    def clear_after_vis(self, time: int = 3000):
        pygame.time.wait(time)
        for v in self.graph.vertex_dict.values():
            v.color = Colors.GREY
            v.border_color = Colors.BLACK
        for e in self.graph.edge_arr:
            e.color = Colors.BLACK

    def redraw_window(self, win: pygame.Surface):
        win.fill(Colors.GREY)
        self.graph.draw(win)
        pygame.display.update()
        pygame.time.wait(500)

    def show_no_cycle_message(self, win: pygame.Surface, cycle_type: str):
        win.fill(Colors.GREY)
        message = f"Graf wejściowy nie zawiera cyklu {cycle_type}"
        Button(message, 25, (100, 300, 800, 60), Colors.RED, Colors.RED).draw(win)
        self.graph.draw(win)
        pygame.display.update()
        pygame.time.wait(3000)

    def highlight_cycle_path(self, win: pygame.Surface, cycle: List[int]):
        colors = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW, Colors.CYAN, Colors.PINK]
        for i, vertex_num in enumerate(cycle):
            if i == len(cycle) - 1:
                break
            color = colors[i % len(colors)]
            self.graph.vertex_dict[vertex_num].color = color
            self.graph.vertex_dict[vertex_num].border_color = Colors.BLACK
            next_vertex = cycle[i + 1]
            edge = self.graph.find_edge(vertex_num, next_vertex)
            if edge:
                edge.color = color
            self.redraw_window(win)


class HamiltonCycleVis(AlgoController):

    def __init__(self, graph: Graph):
        super().__init__(graph)
        self.cycle = []
        self.visited = set()
        self.adj_matrix = {}
        self.adj_list = {}

    def draw_hamilton_vis(self, win: pygame.Surface):
        if self.graph.directing:
            cycle = self.find_hamilton_cycle_directed()
            cycle_type = "Hamiltona (skierowany)"
        else:
            cycle = self.find_hamilton_cycle_undirected()
            cycle_type = "Hamiltona (nieskierowany)"
        if cycle:
            print(f"Znaleziony cykl Hamiltona: {cycle}")
            self.highlight_cycle_path(win, cycle)
            self.clear_after_vis()
        else:
            print("Graf nie zawiera cyklu Hamiltona")
            self.show_no_cycle_message(win, cycle_type)

    def build_adjacency_matrix(self):
        vertices = list(self.graph.vertex_dict.keys())
        self.adj_matrix = {v: {u: 0 for u in vertices} for v in vertices}
        for edge in self.graph.edge_arr:
            v1, v2 = edge.start.number, edge.end.number
            self.adj_matrix[v1][v2] = 1
            if not self.graph.directing:
                self.adj_matrix[v2][v1] = 1

    def build_adjacency_list(self):
        self.adj_list = defaultdict(list)
        for edge in self.graph.edge_arr:
            self.adj_list[edge.start.number].append(edge.end.number)

    def find_hamilton_cycle_undirected(self) -> Optional[List[int]]:
        self.build_adjacency_matrix()
        vertices = list(self.graph.vertex_dict.keys())
        if len(vertices) == 0:
            return None
        start_vertex = vertices[0]
        path = [start_vertex]
        visited = {start_vertex}
        if self.hamilton_backtrack_undirected(path, visited, start_vertex):
            return path
        return None

    def hamilton_backtrack_undirected(self, path: List[int], visited: set, start_vertex: int) -> bool:
        if len(path) == len(self.graph.vertex_dict):
            last_vertex = path[-1]
            if self.adj_matrix[last_vertex][start_vertex] == 1:
                path.append(start_vertex)
                return True
            return False
        current_vertex = path[-1]
        for next_vertex in self.adj_matrix[current_vertex]:
            if self.adj_matrix[current_vertex][next_vertex] == 1 and next_vertex not in visited:
                path.append(next_vertex)
                visited.add(next_vertex)
                if self.hamilton_backtrack_undirected(path, visited, start_vertex):
                    return True
                path.pop()
                visited.remove(next_vertex)
        return False

    def find_hamilton_cycle_directed(self) -> Optional[List[int]]:
        self.build_adjacency_list()
        vertices = list(self.graph.vertex_dict.keys())
        if len(vertices) == 0:
            return None
        start_vertex = vertices[0]
        path = [start_vertex]
        visited = {start_vertex}
        if self.hamilton_backtrack_directed(path, visited, start_vertex):
            return path
        return None

    def hamilton_backtrack_directed(self, path: List[int], visited: set, start_vertex: int) -> bool:
        if len(path) == len(self.graph.vertex_dict):
            last_vertex = path[-1]
            if start_vertex in self.adj_list[last_vertex]:
                path.append(start_vertex)
                return True
            return False
        current_vertex = path[-1]
        for next_vertex in self.adj_list[current_vertex]:
            if next_vertex not in visited:
                path.append(next_vertex)
                visited.add(next_vertex)
                if self.hamilton_backtrack_directed(path, visited, start_vertex):
                    return True
                path.pop()
                visited.remove(next_vertex)
        return False


class EulerCycleVis(AlgoController):

    def __init__(self, graph: Graph):
        super().__init__(graph)
        self.adj_matrix = {}
        self.adj_list = {}

    def draw_euler_vis(self, win: pygame.Surface):
        if self.graph.directing:
            cycle = self.find_euler_cycle_directed()
            cycle_type = "Eulera (skierowany)"
        else:
            cycle = self.find_euler_cycle_undirected()
            cycle_type = "Eulera (nieskierowany)"
        if cycle:
            print(f"Znaleziony cykl Eulera: {cycle}")
            self.highlight_cycle_path(win, cycle)
            self.clear_after_vis()
        else:
            print("Graf nie zawiera cyklu Eulera")
            self.show_no_cycle_message(win, cycle_type)

    def build_adjacency_matrix_euler(self):
        vertices = list(self.graph.vertex_dict.keys())
        self.adj_matrix = {v: {u: 0 for u in vertices} for v in vertices}
        for edge in self.graph.edge_arr:
            v1, v2 = edge.start.number, edge.end.number
            self.adj_matrix[v1][v2] += 1
            if not self.graph.directing:
                self.adj_matrix[v2][v1] += 1

    def build_adjacency_list_euler(self):
        self.adj_list = defaultdict(list)
        for edge in self.graph.edge_arr:
            self.adj_list[edge.start.number].append(edge.end.number)

    def has_euler_cycle_undirected(self) -> bool:
        vertices = list(self.graph.vertex_dict.keys())
        for vertex in vertices:
            degree = sum(self.adj_matrix[vertex].values())
            if degree % 2 != 0:
                return False
        return self.is_connected_undirected()

    def has_euler_cycle_directed(self) -> bool:
        vertices = list(self.graph.vertex_dict.keys())
        for vertex in vertices:
            out_degree = len(self.adj_list[vertex])
            in_degree = sum(1 for v in vertices if vertex in self.adj_list[v])
            if in_degree != out_degree:
                return False
        return self.is_strongly_connected()

    def is_connected_undirected(self) -> bool:
        vertices = list(self.graph.vertex_dict.keys())
        if not vertices:
            return True
        vertices_with_edges = []
        for vertex in vertices:
            if sum(self.adj_matrix[vertex].values()) > 0:
                vertices_with_edges.append(vertex)
        if not vertices_with_edges:
            return True
        visited = set()
        stack = [vertices_with_edges[0]]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                for neighbor in self.adj_matrix[vertex]:
                    if self.adj_matrix[vertex][neighbor] > 0 and neighbor not in visited:
                        stack.append(neighbor)
        return len(visited) == len(vertices_with_edges)

    def is_strongly_connected(self) -> bool:
        vertices = list(self.graph.vertex_dict.keys())
        if not vertices:
            return True
        vertices_with_edges = [v for v in vertices if self.adj_list[v]]
        if not vertices_with_edges:
            return True
        for start in vertices_with_edges:
            visited = set()
            stack = [start]
            while stack:
                vertex = stack.pop()
                if vertex not in visited:
                    visited.add(vertex)
                    for neighbor in self.adj_list[vertex]:
                        if neighbor not in visited:
                            stack.append(neighbor)
            if len(visited) != len(vertices_with_edges):
                return False
        return True

    def find_euler_cycle_undirected(self) -> Optional[List[int]]:
        self.build_adjacency_matrix_euler()
        if not self.has_euler_cycle_undirected():
            return None
        vertices = list(self.graph.vertex_dict.keys())
        if not vertices:
            return None
        start_vertex = None
        for vertex in vertices:
            if sum(self.adj_matrix[vertex].values()) > 0:
                start_vertex = vertex
                break
        if start_vertex is None:
            return None
        return self.hierholzer_undirected(start_vertex)

    def find_euler_cycle_directed(self) -> Optional[List[int]]:
        self.build_adjacency_list_euler()
        if not self.has_euler_cycle_directed():
            return None
        vertices = list(self.graph.vertex_dict.keys())
        if not vertices:
            return None
        start_vertex = None
        for vertex in vertices:
            if self.adj_list[vertex]:
                start_vertex = vertex
                break
        if start_vertex is None:
            return None
        return self.hierholzer_directed(start_vertex)

    def hierholzer_undirected(self, start_vertex: int) -> List[int]:
        adj_copy = {}
        vertices = list(self.graph.vertex_dict.keys())
        for v in vertices:
            adj_copy[v] = {}
            for u in vertices:
                adj_copy[v][u] = self.adj_matrix[v][u]
        def has_unused_edge(vertex):
            return any(adj_copy[vertex][neighbor] > 0 for neighbor in adj_copy[vertex])
        def get_next_neighbor(vertex):
            for neighbor in adj_copy[vertex]:
                if adj_copy[vertex][neighbor] > 0:
                    return neighbor
            return None
        circuit = []
        curr_path = [start_vertex]
        while curr_path:
            curr_vertex = curr_path[-1]
            if has_unused_edge(curr_vertex):
                next_vertex = get_next_neighbor(curr_vertex)
                if next_vertex is not None:
                    adj_copy[curr_vertex][next_vertex] -= 1
                    adj_copy[next_vertex][curr_vertex] -= 1
                    curr_path.append(next_vertex)
            else:
                circuit.append(curr_path.pop())
        circuit.reverse()
        return circuit

    def hierholzer_directed(self, start_vertex: int) -> List[int]:
        adj_copy = defaultdict(list)
        for vertex in self.adj_list:
            adj_copy[vertex] = self.adj_list[vertex].copy()
        circuit = []
        curr_path = [start_vertex]
        while curr_path:
            curr_vertex = curr_path[-1]
            if adj_copy[curr_vertex]:
                next_vertex = adj_copy[curr_vertex].pop()
                curr_path.append(next_vertex)
            else:
                circuit.append(curr_path.pop())
        circuit.reverse()
        return circuit
