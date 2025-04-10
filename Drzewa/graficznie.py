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
        self.bf = 0
        self.pos = (0, 0)


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        def update_balance(node):
            if node.bf < -1:
                if node.right.bf > 0:
                    self.rotate_right(node.right)
                return self.rotate_left(node)
            elif node.bf > 1:
                if node.left.bf < 0:
                    self.rotate_left(node.left)
                return self.rotate_right(node)
            return node

        def insert_node(root, node):
            if not root:
                return node
            if node.key < root.key:
                root.left = insert_node(root.left, node)
                root.left.up = root
                root.bf += 1
            else:
                root.right = insert_node(root.right, node)
                root.right.up = root
                root.bf -= 1
            return update_balance(root)

        new_node = AVLNode(key)
        self.root = insert_node(self.root, new_node)

    def rotate_left(self, A):
        B = A.right
        A.right = B.left
        if B.left:
            B.left.up = A
        B.left = A
        A.up = B

        if A == self.root:
            self.root = B

        A.bf = A.bf + 1 - min(B.bf, 0)
        B.bf = B.bf + 1 + max(A.bf, 0)
        return B

    def rotate_right(self, A):
        B = A.left
        A.left = B.right
        if B.right:
            B.right.up = A
        B.right = A
        B.up = A.up
        A.up = B

        if A == self.root:
            self.root = B

        A.bf = A.bf - 1 - max(B.bf, 0)
        B.bf = B.bf - 1 + min(A.bf, 0)
        return B

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

        # Check if the tree is empty
        if max_depth == 0:
            return levels  # Return empty levels if the tree is empty

        # Reduce horizontal spacing even further (less wide)
        horizontal_spacing = (window_width - 100) // (max_depth * 3)  # Reduce further by changing factor
        vertical_spacing = (window_height - 100) // (max_depth + 1)

        def dfs(node, depth, x):
            if not node:
                return x
            x = dfs(node.left, depth + 1, x)
            # Adjust node positioning dynamically with reduced width
            node.pos = (x * horizontal_spacing + 100, depth * vertical_spacing + 50)
            if depth not in levels:
                levels[depth] = []
            levels[depth].append(node)
            x += 1
            x = dfs(node.right, depth + 1, x)
            return x

        dfs(self.root, 0, 0)
        return levels

    def remove_all_post_order(self):
        def post_order_traversal(node):
            if node:
                yield from post_order_traversal(node.left)
                yield from post_order_traversal(node.right)
                yield node  # Yield the node before deletion
                self.remove(node.key)

        return post_order_traversal(self.root)

    def remove(self, key):
        def delete_node(node, key):
            if not node:
                return node
            elif key < node.key:
                node.left = delete_node(node.left, key)
            elif key > node.key:
                node.right = delete_node(node.right, key)
            else:
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left

                min_larger_node = node.right
                while min_larger_node.left:
                    min_larger_node = min_larger_node.left

                node.key = min_larger_node.key
                node.right = delete_node(node.right, min_larger_node.key)

            return node

        self.root = delete_node(self.root, key)

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
            current = current.left  # Min value is always on the leftmost path
        return path

    def find_max_path(self):
        path = []
        current = self.root
        while current:
            path.append(current)
            current = current.right  # Max value is always on the rightmost path
        return path

    def remove_multiple(self, keys):
        for key in keys:
            self.remove(key)
            
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
        return None  # Key not found
    
    def find_node(self, key):
        current = self.root
        while current:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None  # Key not found


def draw_tree(tree, highlight_nodes=[], path_nodes=[], deleting_nodes=[]):
    screen.fill(WHITE)
    levels = tree.get_nodes_positions()

    def draw_node(node, color=BLACK):
        pygame.draw.circle(screen, color, node.pos, NODE_RADIUS)
        text_color = WHITE if color not in [YELLOW, PURPLE] else BLACK
        text = FONT.render(str(node.key), True, text_color)
        text_rect = text.get_rect(center=node.pos)
        screen.blit(text, text_rect)

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
        if node not in deleting_nodes:  # Don't overwrite deleting nodes
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
        # Determine which nodes to highlight based on current mode
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
        
        # Draw buttons
        for name, rect in buttons.items():
            pygame.draw.rect(screen, BLUE, rect)
            label = name.replace("_", " ").title()
            txt = FONT.render(label, True, WHITE)
            screen.blit(txt, txt.get_rect(center=rect.center))

        # Draw input box if active
        if input_active:
            input_rect = pygame.Rect(50, HEIGHT - 120, 300, 30)
            pygame.draw.rect(screen, WHITE, input_rect)
            pygame.draw.rect(screen, BLACK, input_rect, 2)
            txt_surface = FONT.render(input_text, True, BLACK)
            screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
            
            # Draw instruction text
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

        # Handle traversals
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
                print(f"Deleting node: {node.key}")  # Print before deletion
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
                    delete_all_iter = iter(tree.remove_all_post_order())
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