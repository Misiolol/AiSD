import pygame
import sys
from collections import deque

pygame.init()

WIDTH, HEIGHT = 1000, 600
NODE_RADIUS = 20
FONT = pygame.font.SysFont("Arial", 16)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("BST Tree Visualizer")

class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.up = None
        self.pos = (0, 0)

class BSTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        def _insert(node, key):
            if not node:
                return BSTNode(key)
            
            if key < node.key:
                node.left = _insert(node.left, key)
                node.left.up = node
            else:
                node.right = _insert(node.right, key)
                node.right.up = node

            return node

        self.root = _insert(self.root, key)

    def remove(self, key):
        def _remove(node, key):
            if not node:
                return node

            if key < node.key:
                node.left = _remove(node.left, key)
            elif key > node.key:
                node.right = _remove(node.right, key)
            else:
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left

                temp = self.get_min_node(node.right)
                node.key = temp.key
                node.right = _remove(node.right, temp.key)

            return node

        self.root = _remove(self.root, key)

    # DSW Algorithm with animation
    def balance_tree(self):
        print("\nPre-order before balancing:")
        self.print_pre_order()
        
        # Create backbone with animation
        backbone_iter = self.create_backbone_with_animation()
        # Create perfect balance with animation
        balance_iter = self.create_perfect_balance_with_animation()
        
        return backbone_iter, balance_iter

    def create_backbone_with_animation(self):
        current = self.root
        while current:
            if current.left:
                right_child = current.left
                yield current  # Yield current node for animation
                self.rotate_right(current)
                current = right_child
            else:
                current = current.right

    def create_perfect_balance_with_animation(self):
        n = self.count_nodes()
        m = 2 ** (n.bit_length() - 1) - 1
        yield from self.make_rotations_with_animation(n - m)
        
        while m > 1:
            m = m // 2
            yield from self.make_rotations_with_animation(m)

    def make_rotations_with_animation(self, count):
        current = self.root
        for _ in range(count):
            child = current.right
            if child:
                yield current  # Yield current node for animation
                self.rotate_left(current)
                current = child.right
            else:
                break

    def rotate_left(self, node):
        right_child = node.right
        if not right_child:
            return

        node.right = right_child.left
        if right_child.left:
            right_child.left.up = node

        right_child.up = node.up
        if not node.up:
            self.root = right_child
        elif node == node.up.left:
            node.up.left = right_child
        else:
            node.up.right = right_child

        right_child.left = node
        node.up = right_child

    def rotate_right(self, node):
        left_child = node.left
        if not left_child:
            return

        node.left = left_child.right
        if left_child.right:
            left_child.right.up = node

        left_child.up = node.up
        if not node.up:
            self.root = left_child
        elif node == node.up.right:
            node.up.right = left_child
        else:
            node.up.left = left_child

        left_child.right = node
        node.up = left_child

    def count_nodes(self):
        count = 0
        stack = []
        current = self.root
        
        while True:
            if current:
                stack.append(current)
                current = current.left
            elif stack:
                current = stack.pop()
                count += 1
                current = current.right
            else:
                break
        return count

    def print_pre_order(self):
        stack = [self.root]
        while stack:
            node = stack.pop()
            if node:
                print(node.key, end=" ")
                stack.append(node.right)
                stack.append(node.left)
        print()

    def get_min_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def get_max_node(self, node):
        current = node
        while current.right:
            current = current.right
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

        if not self.root:
            return levels

        horizontal_spacing = window_width / (2 ** (max_depth + 1))
        vertical_spacing = window_height / (max_depth + 2)

        queue = deque([(self.root, 0, window_width / 2, horizontal_spacing*10)])
        
        while queue:
            node, depth, x, spacing = queue.popleft()
            
            node.pos = (x, (depth + 1) * vertical_spacing)
            
            if depth not in levels:
                levels[depth] = []
            levels[depth].append(node)
            
            new_spacing = spacing / 2
            if node.left:
                queue.append((node.left, depth + 1, x - new_spacing, new_spacing))
            if node.right:
                queue.append((node.right, depth + 1, x + new_spacing, new_spacing))

        return levels

    def remove_all_post_order(self):
        def post_order_delete(node):
            if node:
                yield from post_order_delete(node.left)
                yield from post_order_delete(node.right)
                print(f"POST-ORDER DELETION: Removing node {node.key}")
                yield node
                self.remove(node.key)

        return post_order_delete(self.root)

    def remove_multiple(self, keys):
        for key in keys:
            node = self.find_node(key)
            if node:
                print(f"DELETING NODE: {node.key}")
                yield node
                self.remove(key)
            else:
                print(f"NODE NOT FOUND: {key}")
                yield None

    def in_order_traversal(self):
        def traverse(node):
            if node:
                yield from traverse(node.left)
                print(f"IN-ORDER TRAVERSAL: Visiting node {node.key}")
                yield node
                yield from traverse(node.right)

        return traverse(self.root)

    def pre_order_traversal(self, start_node=None):
        def traverse(node):
            if node:
                print(f"PRE-ORDER TRAVERSAL: Visiting node {node.key}")
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
                print(f"POST-ORDER TRAVERSAL: Visiting node {node.key}")
                yield node

        return traverse(self.root)

    def find_min_path(self):
        path = []
        current = self.root
        while current:
            path.append(current)
            current = current.left
        print("MIN PATH:", " -> ".join(str(node.key) for node in path))
        return path

    def find_max_path(self):
        path = []
        current = self.root
        while current:
            path.append(current)
            current = current.right
        print("MAX PATH:", " -> ".join(str(node.key) for node in path))
        return path

    def find_path(self, key):
        path = []
        current = self.root
        while current:
            path.append(current)
            if key == current.key:
                print("SEARCH PATH:", " -> ".join(str(node.key) for node in path))
                return path
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        print(f"KEY NOT FOUND: {key}")
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

def draw_tree(tree, highlight_nodes=[], path_nodes=[], deleting_nodes=[], rotating_nodes=[]):
    screen.fill(WHITE)
    levels = tree.get_nodes_positions()

    def draw_node(node, color=BLACK):
        pygame.draw.circle(screen, color, node.pos, NODE_RADIUS)
        text_color = WHITE if color not in [YELLOW, PURPLE, ORANGE] else BLACK
        key_text = FONT.render(str(node.key), True, text_color)
        key_rect = key_text.get_rect(center=node.pos)
        screen.blit(key_text, key_rect)

    for level in levels.values():
        for node in level:
            if node.left and node.left in [n for lvl in levels.values() for n in lvl]:
                pygame.draw.line(screen, BLACK, node.pos, node.left.pos, 2)
            if node.right and node.right in [n for lvl in levels.values() for n in lvl]:
                pygame.draw.line(screen, BLACK, node.pos, node.right.pos, 2)

    for level in levels.values():
        for node in level:
            if node in rotating_nodes:
                draw_node(node, ORANGE)
            elif node in deleting_nodes:
                draw_node(node, PURPLE)
            elif node in path_nodes:
                draw_node(node, YELLOW)
            elif node in highlight_nodes:
                draw_node(node, GREEN)
            else:
                draw_node(node)

    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    tree = BSTree()
    
    keys = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
    for key in keys:
        tree.insert(key)

    min_path, max_path = [], []
    in_order_nodes, pre_order_nodes, post_order_nodes = [], [], []
    input_active = False
    input_text = ""
    search_path = []
    deleting_nodes = []
    rotating_nodes = []
    current_mode = None
    subtree_pre_order_nodes = []
    delete_all_iter = None
    delete_multiple_iter = None
    balance_backbone_iter = None
    balance_rotate_iter = None
    
    buttons = {
        "min_path": pygame.Rect(10, HEIGHT - 40, 120, 30),
        "max_path": pygame.Rect(140, HEIGHT - 40, 120, 30),
        "search": pygame.Rect(270, HEIGHT - 40, 120, 30),
        "delete": pygame.Rect(400, HEIGHT - 40, 120, 30),
        "in_order": pygame.Rect(530, HEIGHT - 40, 120, 30),
        "pre_order": pygame.Rect(660, HEIGHT - 40, 120, 30),
        "post_order": pygame.Rect(790, HEIGHT - 40, 120, 30),
        "delete_all": pygame.Rect(10, HEIGHT - 80, 120, 30),
        "balance": pygame.Rect(140, HEIGHT - 80, 120, 30),
    }

    in_order_iter = None
    pre_order_iter = None
    post_order_iter = None
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
            
        draw_tree(tree, highlight_nodes, search_path, deleting_nodes, rotating_nodes)
        
        for name, rect in buttons.items():
            pygame.draw.rect(screen, BLUE, rect)
            label = name.replace("_", " ").title()
            txt = FONT.render(label, True, WHITE)
            screen.blit(txt, txt.get_rect(center=rect.center))

        if input_active:
            input_rect = pygame.Rect(50, HEIGHT - 80, 300, 30)
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
            screen.blit(instr_surface, (50, HEIGHT - 110))

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
                deleting_nodes = []
            except StopIteration:
                delete_all_iter = None
                deleting_nodes = []

        if delete_multiple_iter is not None:
            try:
                node = next(delete_multiple_iter)
                if node:
                    deleting_nodes = [node]
                    pygame.time.wait(traversal_delay)
                    deleting_nodes = []
            except StopIteration:
                delete_multiple_iter = None
                deleting_nodes = []

        if balance_backbone_iter is not None:
            try:
                node = next(balance_backbone_iter)
                rotating_nodes = [node]
                pygame.time.wait(traversal_delay)
                rotating_nodes = []
            except StopIteration:
                balance_backbone_iter = None
                print("\nPre-order after backbone creation:")
                tree.print_pre_order()
                balance_rotate_iter = tree.create_perfect_balance_with_animation()

        if balance_rotate_iter is not None:
            try:
                node = next(balance_rotate_iter)
                rotating_nodes = [node]
                pygame.time.wait(traversal_delay)
                rotating_nodes = []
            except StopIteration:
                balance_rotate_iter = None
                print("\nPre-order after balancing:")
                tree.print_pre_order()

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
                    search_path = min_path
                    current_mode = "min_path"
                elif buttons["max_path"].collidepoint(pos):
                    max_path = tree.find_max_path()
                    min_path = []
                    search_path = max_path
                    current_mode = "max_path"
                elif buttons["search"].collidepoint(pos):
                    input_active = True
                    input_text = ""
                    current_mode = "search"
                elif buttons["delete"].collidepoint(pos):
                    input_active = True
                    input_text = ""
                    current_mode = "delete"
                elif buttons["in_order"].collidepoint(pos):
                    in_order_nodes = []
                    in_order_iter = iter(tree.in_order_traversal())
                    current_mode = "in_order"
                elif buttons["pre_order"].collidepoint(pos):
                    pre_order_nodes = []
                    pre_order_iter = iter(tree.pre_order_traversal())
                    current_mode = "pre_order"
                elif buttons["post_order"].collidepoint(pos):
                    post_order_nodes = []
                    post_order_iter = iter(tree.post_order_traversal())
                    current_mode = "post_order"
                elif buttons["delete_all"].collidepoint(pos):
                    delete_all_iter = tree.remove_all_post_order()
                    current_mode = "delete_all"
                elif buttons["balance"].collidepoint(pos):
                    print("\nPre-order before balancing:")
                    tree.print_pre_order()
                    balance_backbone_iter, _ = tree.balance_tree()
                    current_mode = "balance"

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    try:
                        if current_mode == "search":
                            key = int(input_text)
                            search_path = tree.find_path(key)
                            if not search_path:
                                print(f"Key {key} not found")
                        elif current_mode == "delete":
                            keys_to_delete = [int(k.strip()) for k in input_text.split(",") if k.strip()]
                            if keys_to_delete:
                                delete_multiple_iter = tree.remove_multiple(keys_to_delete)
                        elif current_mode == "subtree_pre_order":
                            key = int(input_text)
                            subtree_root = tree.find_node(key)
                            if subtree_root:
                                subtree_pre_order_iter = iter(tree.pre_order_traversal(subtree_root))
                                current_mode = "subtree_pre_order"
                            else:
                                print(f"Subtree root {key} not found")
                    except ValueError:
                        print("Invalid input")
                    input_text = ""
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    input_text = ""
                    input_active = False
                elif event.unicode.isdigit() or event.unicode == ',':
                    input_text += event.unicode

        clock.tick(60)

if __name__ == '__main__':
    main()