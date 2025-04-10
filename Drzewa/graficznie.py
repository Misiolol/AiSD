import pygame
import sys
import random
from collections import deque

pygame.init()

WIDTH, HEIGHT = 1400, 700
NODE_RADIUS = 20
FONT = pygame.font.SysFont("Arial", 16)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)  # Color for highlighting nodes
YELLOW = (255, 255, 0)  # Color for path highlighting
PURPLE = (128, 0, 128)  # Color for deletion highlighting

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("AVL Tree Visualizer")


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.up = None
        self.height = 1  # Wysokość poddrzewa - ważne dla AVL
        self.bf = 0      # Współczynnik równowagi (balance factor)
        self.pos = (0, 0)


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def update_height_and_bf(self, node):
        if not node:
            return
        left_height = self.get_height(node.left)
        right_height = self.get_height(node.right)
        node.height = 1 + max(left_height, right_height)
        node.bf = left_height - right_height

    def rotate_left(self, z):
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update parent references
        if T2:
            T2.up = z
        y.up = z.up
        z.up = y

        # Update heights and balance factors
        self.update_height_and_bf(z)
        self.update_height_and_bf(y)

        return y

    def rotate_right(self, z):
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update parent references
        if T3:
            T3.up = z
        y.up = z.up
        z.up = y

        # Update heights and balance factors
        self.update_height_and_bf(z)
        self.update_height_and_bf(y)

        return y

    def balance(self, node):
        # Left Heavy
        if node.bf > 1:
            # Left-Right Case
            if node.left.bf < 0:
                node.left = self.rotate_left(node.left)
            # Left-Left Case
            return self.rotate_right(node)
        
        # Right Heavy
        elif node.bf < -1:
            # Right-Left Case
            if node.right.bf > 0:
                node.right = self.rotate_right(node.right)
            # Right-Right Case
            return self.rotate_left(node)
        
        # No rotation needed
        return node

    def insert(self, key):
        def _insert(node, key):
            # Standard BST insert
            if not node:
                return AVLNode(key)
            
            if key < node.key:
                node.left = _insert(node.left, key)
                node.left.up = node
            else:
                node.right = _insert(node.right, key)
                node.right.up = node

            # Update height and balance factor
            self.update_height_and_bf(node)

            # Balance the node if needed
            return self.balance(node)

        self.root = _insert(self.root, key)

    def remove(self, key):
        def _remove(node, key):
            # Standard BST delete
            if not node:
                return node

            if key < node.key:
                node.left = _remove(node.left, key)
            elif key > node.key:
                node.right = _remove(node.right, key)
            else:
                # Node with only one child or no child
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left

                # Node with two children: get inorder successor
                temp = self.get_min_node(node.right)
                node.key = temp.key
                node.right = _remove(node.right, temp.key)

            # If the tree had only one node then return
            if not node:
                return node

            # Update height and balance factor
            self.update_height_and_bf(node)

            # Balance the node if needed
            return self.balance(node)

        self.root = _remove(self.root, key)

    def get_min_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def get_tree_depth(self, node):
        if not node:
            return 0
        left_depth = self.get_tree_depth(node.left)
        right_depth = self.get_tree_depth(node.right)
        return max(left_depth, right_depth) + 1

    def get_nodes_positions(self):
        levels = {}
        window_width, window_height = screen.get_size()
        max_depth = self.get_tree_depth(self.root)

        if max_depth == 0:
            return levels

        # Zmniejszamy przestrzeń poziomą - używamy mniejszego mnożnika
        horizontal_spacing = (window_width - 100) // (max_depth*10)
        vertical_spacing = (window_height - 100) // (max_depth + 1)

        # Używamy kolejki do poziomowego przechodzenia (BFS)
        queue = deque()
        if self.root:
            # Początkowy zakres dla korzenia
            left = 0
            right = 2 ** max_depth - 1
            x = (left + right) // 2
            self.root.pos = (x * horizontal_spacing + 50, 50)
            levels[0] = [self.root]
            queue.append((self.root, 0, left, right))

        while queue:
            node, depth, left, right = queue.popleft()
            next_depth = depth + 1
            
            if node.left:
                # Lewe dziecko - bierzemy lewą połowę zakresu rodzica
                new_left = left
                new_right = (left + right) // 2
                x = (new_left + new_right) // 2
                node.left.pos = (x * horizontal_spacing + 50, next_depth * vertical_spacing + 50)
                
                if next_depth not in levels:
                    levels[next_depth] = []
                levels[next_depth].append(node.left)
                queue.append((node.left, next_depth, new_left, new_right))

            if node.right:
                # Prawe dziecko - bierzemy prawą połowę zakresu rodzica
                new_left = (left + right) // 2 + 1
                new_right = right
                x = (new_left + new_right) // 2
                node.right.pos = (x * horizontal_spacing + 50, next_depth * vertical_spacing + 50)
                
                if next_depth not in levels:
                    levels[next_depth] = []
                levels[next_depth].append(node.right)
                queue.append((node.right, next_depth, new_left, new_right))

        return levels

    def remove_all_post_order(self):
        # First collect all nodes in post-order
        nodes_to_delete = list(self.post_order_traversal())
        # Then delete them one by one
        for node in nodes_to_delete:
            yield node
            self.remove(node.key)

    def remove_multiple(self, keys):
        for key in keys:
            self.remove(key)

    def in_order_traversal(self):
        def traverse(node):
            if node:
                yield from traverse(node.left)
                yield node
                yield from traverse(node.right)

        return traverse(self.root)

    def pre_order_traversal(self, start_node=None):
        def traverse(node):
            if node:
                yield node
                yield from traverse(node.left)
                yield from traverse(node.right)

        if start_node is None:
            start_node = self.root
        return traverse(start_node)

    def post_order_traversal(self):
        def traverse(node):
            if node:
                yield from traverse(node.left)
                yield from traverse(node.right)
                yield node

        return traverse(self.root)

    def find_min_path(self):
        path = []
        current = self.root
        while current:
            path.append(current)
            current = current.left
        return path

    def find_max_path(self):
        path = []
        current = self.root
        while current:
            path.append(current)
            current = current.right
        return path

    def find_path(self, key):
        path = []
        current = self.root
        while current:
            path.append(current)
            if key == current.key:
                return path
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None

    def find_node(self, key):
        current = self.root
        while current:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None


def draw_tree(tree, highlight_nodes=[], path_nodes=[], deleting_nodes=[]):
    screen.fill(WHITE)
    levels = tree.get_nodes_positions()

    def draw_node(node, color=BLACK):
        pygame.draw.circle(screen, color, node.pos, NODE_RADIUS)
        # Draw key
        text_color = WHITE if color not in [YELLOW, PURPLE] else BLACK
        key_text = FONT.render(str(node.key), True, text_color)
        key_rect = key_text.get_rect(center=(node.pos[0], node.pos[1] - 5))
        screen.blit(key_text, key_rect)
        
        # Draw balance factor below the key in RED
        bf_text = FONT.render(f"bf:{node.bf}", True, RED)
        bf_rect = bf_text.get_rect(center=(node.pos[0], node.pos[1] + 15))
        screen.blit(bf_text, bf_rect)

    for level in levels.values():
        for node in level:
            if node.left and node.left.key != "deleted":
                pygame.draw.line(screen, BLACK, node.pos, node.left.pos, 2)
            if node.right and node.right.key != "deleted":
                pygame.draw.line(screen, BLACK, node.pos, node.right.pos, 2)

    # Draw deleting nodes first (in purple)
    for node in deleting_nodes:
        draw_node(node, PURPLE)

    # Then draw path nodes (in yellow)
    for node in path_nodes:
        if node not in deleting_nodes:
            draw_node(node, YELLOW)

    # Then draw highlighted nodes (in green)
    for node in highlight_nodes:
        if node not in path_nodes and node not in deleting_nodes:
            draw_node(node, GREEN)

    # Finally draw all other nodes
    for level in levels.values():
        for node in level:
            if (node not in highlight_nodes and 
                node not in path_nodes and 
                node not in deleting_nodes):
                draw_node(node)

    pygame.display.flip()


def main():
    clock = pygame.time.Clock()
    tree = AVLTree()
    keys = list(range(1, 32))
    random.shuffle(keys)
    for key in keys:
        tree.insert(key)

    min_path, max_path, in_order_nodes, pre_order_nodes, post_order_nodes = [], [], [], [], []
    input_active = False
    input_text = ""
    delete_mode = False
    to_delete = []
    search_path = []
    deleting_nodes = []
    current_mode = None
    subtree_root_key = None
    subtree_pre_order_nodes = []
    
    buttons = {
        "min_path": pygame.Rect(50, HEIGHT - 40, 180, 30),
        "max_path": pygame.Rect(250, HEIGHT - 40, 180, 30),
        "search": pygame.Rect(450, HEIGHT - 40, 180, 30),
        "delete": pygame.Rect(650, HEIGHT - 40, 180, 30),
        "in_order": pygame.Rect(850, HEIGHT - 40, 180, 30),
        "pre_order": pygame.Rect(1050, HEIGHT - 40, 180, 30),
        "post_order": pygame.Rect(1250, HEIGHT - 40, 180, 30),
        "delete_all": pygame.Rect(50, HEIGHT - 80, 180, 30),
        "subtree_pre": pygame.Rect(250, HEIGHT - 80, 180, 30),
    }

    selected_node = None
    in_order_iter = None
    pre_order_iter = None
    post_order_iter = None
    delete_all_iter = None
    subtree_pre_order_iter = None
    traversal_delay = 500

    while True:
        highlight_nodes = []
        if current_mode == "in_order":
            highlight_nodes = in_order_nodes
        elif current_mode == "pre_order":
            highlight_nodes = pre_order_nodes
        elif current_mode == "post_order":
            highlight_nodes = post_order_nodes
        elif current_mode == "subtree_pre_order":
            highlight_nodes = subtree_pre_order_nodes
            
        draw_tree(tree, highlight_nodes, search_path, deleting_nodes)
        
        for name, rect in buttons.items():
            pygame.draw.rect(screen, BLUE, rect)
            label = name.replace("_", " ").title()
            txt = FONT.render(label, True, WHITE)
            screen.blit(txt, txt.get_rect(center=rect.center))

        if input_active:
            input_rect = pygame.Rect(50, HEIGHT - 120, 300, 30)
            pygame.draw.rect(screen, WHITE, input_rect)
            pygame.draw.rect(screen, BLACK, input_rect, 2)
            txt_surface = FONT.render(input_text, True, BLACK)
            screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
            
            if current_mode == "search":
                instr_text = "Enter key to search:"
            elif current_mode == "delete":
                instr_text = "Enter keys to delete (comma separated):"
            elif current_mode == "subtree_pre_order":
                instr_text = "Enter root key of subtree:"
            else:
                instr_text = "Enter value:"
                
            instr_surface = FONT.render(instr_text, True, BLACK)
            screen.blit(instr_surface, (50, HEIGHT - 150))

        pygame.display.flip()

        if in_order_iter is not None:
            try:
                node = next(in_order_iter)
                in_order_nodes = [node]
                pygame.time.wait(traversal_delay)
            except StopIteration:
                in_order_iter = None
                in_order_nodes = []

        if pre_order_iter is not None:
            try:
                node = next(pre_order_iter)
                pre_order_nodes = [node]
                pygame.time.wait(traversal_delay)
            except StopIteration:
                pre_order_iter = None
                pre_order_nodes = []

        if post_order_iter is not None:
            try:
                node = next(post_order_iter)
                post_order_nodes = [node]
                pygame.time.wait(traversal_delay)
            except StopIteration:
                post_order_iter = None
                post_order_nodes = []

        if delete_all_iter is not None:
            try:
                node = next(delete_all_iter)
                deleting_nodes = [node]
                pygame.time.wait(traversal_delay)
            except StopIteration:
                delete_all_iter = None
                deleting_nodes = []

        if subtree_pre_order_iter is not None:
            try:
                node = next(subtree_pre_order_iter)
                subtree_pre_order_nodes = [node]
                pygame.time.wait(traversal_delay)
            except StopIteration:
                subtree_pre_order_iter = None
                subtree_pre_order_nodes = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if buttons["min_path"].collidepoint(pos):
                    min_path = tree.find_min_path()
                    max_path = []
                    in_order_nodes = []
                    pre_order_nodes = []
                    post_order_nodes = []
                    search_path = min_path
                    current_mode = "min_path"
                    deleting_nodes = []
                    subtree_pre_order_nodes = []
                elif buttons["max_path"].collidepoint(pos):
                    max_path = tree.find_max_path()
                    min_path = []
                    in_order_nodes = []
                    pre_order_nodes = []
                    post_order_nodes = []
                    search_path = max_path
                    current_mode = "max_path"
                    deleting_nodes = []
                    subtree_pre_order_nodes = []
                elif buttons["search"].collidepoint(pos):
                    input_active = True
                    input_text = ""
                    current_mode = "search"
                    min_path = max_path = []
                    in_order_nodes = pre_order_nodes = post_order_nodes = []
                    search_path = []
                    deleting_nodes = []
                    subtree_pre_order_nodes = []
                elif buttons["delete"].collidepoint(pos):
                    input_active = True
                    input_text = ""
                    current_mode = "delete"
                    min_path = max_path = []
                    in_order_nodes = pre_order_nodes = post_order_nodes = []
                    search_path = []
                    deleting_nodes = []
                    subtree_pre_order_nodes = []
                elif buttons["in_order"].collidepoint(pos):
                    in_order_nodes = []
                    in_order_iter = iter(tree.in_order_traversal())
                    min_path = max_path = []
                    pre_order_nodes = []
                    post_order_nodes = []
                    search_path = []
                    deleting_nodes = []
                    subtree_pre_order_nodes = []
                    current_mode = "in_order"
                elif buttons["pre_order"].collidepoint(pos):
                    pre_order_nodes = []
                    pre_order_iter = iter(tree.pre_order_traversal())
                    min_path = max_path = []
                    in_order_nodes = []
                    post_order_nodes = []
                    search_path = []
                    deleting_nodes = []
                    subtree_pre_order_nodes = []
                    current_mode = "pre_order"
                elif buttons["post_order"].collidepoint(pos):
                    post_order_nodes = []
                    post_order_iter = iter(tree.post_order_traversal())
                    min_path = max_path = []
                    in_order_nodes = []
                    pre_order_nodes = []
                    search_path = []
                    deleting_nodes = []
                    subtree_pre_order_nodes = []
                    current_mode = "post_order"
                elif buttons["delete_all"].collidepoint(pos):
                    delete_all_iter = tree.remove_all_post_order()
                    min_path = max_path = []
                    in_order_nodes = pre_order_nodes = post_order_nodes = []
                    search_path = []
                    subtree_pre_order_nodes = []
                    current_mode = "delete_all"
                elif buttons["subtree_pre"].collidepoint(pos):
                    input_active = True
                    input_text = ""
                    current_mode = "subtree_pre_order"
                    min_path = max_path = []
                    in_order_nodes = pre_order_nodes = post_order_nodes = []
                    search_path = []
                    deleting_nodes = []
                    subtree_pre_order_nodes = []
                else:
                    for level in tree.get_nodes_positions().values():
                        for node in level:
                            if pygame.draw.circle(screen, BLACK, node.pos, NODE_RADIUS).collidepoint(pos):
                                break

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    try:
                        if current_mode == "search":
                            key = int(input_text)
                            search_path = tree.find_path(key)
                            if search_path is None:
                                print(f"Key {key} not found")
                                search_path = []
                        elif current_mode == "delete":
                            keys_to_delete = list(map(int, input_text.split(",")))
                            tree.remove_multiple(keys_to_delete)
                            search_path = []
                        elif current_mode == "subtree_pre_order":
                            key = int(input_text)
                            subtree_root = tree.find_node(key)
                            if subtree_root:
                                subtree_pre_order_iter = iter(tree.pre_order_traversal(subtree_root))
                                current_mode = "subtree_pre_order"
                            else:
                                print(f"Subtree root {key} not found")
                    except ValueError:
                        pass
                    input_text = ""
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    input_text = ""
                    input_active = False
                elif event.unicode.isdigit() or event.unicode == ',':
                    input_text += event.unicode

        clock.tick(30)


if __name__ == '__main__':
    main()