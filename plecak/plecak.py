import pygame
import sys
import math
import time
import random
from dataclasses import dataclass
from typing import List, Tuple, Dict
from enum import Enum
import os

# Inicjalizacja pygame
pygame.init()

# Kolory
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 102, 102)
    GREEN = (102, 255, 102)
    BLUE = (102, 178, 255)
    YELLOW = (255, 255, 102)
    PURPLE = (178, 102, 255)
    ORANGE = (255, 178, 102)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (64, 64, 64)
    BACKGROUND = (30, 30, 40)
    PANEL = (50, 50, 65)
    ACCENT = (255, 215, 0)

class State(Enum):
    MENU = 1
    ALGORITHM_SELECTION = 2
    VISUALIZATION = 3
    RESULTS = 4

@dataclass
class Item:
    """Klasa reprezentująca przedmiot"""
    id: int
    size: int
    value: int
    ratio: float = 0.0
    color: tuple = None
    x: float = 0
    y: float = 0
    selected: bool = False
    animation_progress: float = 0.0
    
    def __post_init__(self):
        self.ratio = self.value / self.size if self.size > 0 else 0
        if self.color is None:
            # Generowanie koloru na podstawie opłacalności
            hue = min(self.ratio * 30, 255)
            self.color = self.hsv_to_rgb(hue, 0.8, 0.9)
    
    @staticmethod
    def hsv_to_rgb(h, s, v):
        """Konwersja HSV do RGB"""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

@dataclass
class Solution:
    """Klasa reprezentująca rozwiązanie"""
    items: List[Item]
    total_value: int
    total_size: int
    execution_time: float
    algorithm: str
    color: tuple

class KnapsackSolver:
    """Klasa implementująca algorytmy rozwiązywania problemu plecakowego"""
    
    def __init__(self, capacity: int, items: List[Item]):
        self.capacity = capacity
        self.items = items
        self.n = len(items)
    
    def dynamic_programming(self) -> Solution:
        """Algorytm programowania dynamicznego (AD)"""
        start_time = time.time()
        
        # Tablica DP
        dp = [[0 for _ in range(self.capacity + 1)] for _ in range(self.n + 1)]
        
        # Wypełnianie tablicy DP
        for i in range(1, self.n + 1):
            for w in range(1, self.capacity + 1):
                if self.items[i-1].size <= w:
                    dp[i][w] = max(
                        self.items[i-1].value + dp[i-1][w - self.items[i-1].size],
                        dp[i-1][w]
                    )
                else:
                    dp[i][w] = dp[i-1][w]
        
        # Odtwarzanie rozwiązania
        selected_items = []
        w = self.capacity
        for i in range(self.n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected_items.append(self.items[i-1])
                w -= self.items[i-1].size
        
        total_value = sum(item.value for item in selected_items)
        total_size = sum(item.size for item in selected_items)
        execution_time = time.time() - start_time
        
        return Solution(selected_items, total_value, total_size, execution_time, 
                       "Programowanie Dynamiczne", Colors.RED)
    
    def greedy_algorithm(self) -> Solution:
        """Algorytm zachłanny (AZ)"""
        start_time = time.time()
        
        sorted_items = sorted(self.items, key=lambda x: x.ratio, reverse=True)
        
        selected_items = []
        current_weight = 0
        
        for item in sorted_items:
            if current_weight + item.size <= self.capacity:
                selected_items.append(item)
                current_weight += item.size
        
        total_value = sum(item.value for item in selected_items)
        total_size = sum(item.size for item in selected_items)
        execution_time = time.time() - start_time
        
        return Solution(selected_items, total_value, total_size, execution_time, 
                       "Algorytm Zachłanny", Colors.GREEN)
    
    def brute_force(self) -> Solution:
        """Algorytm siłowy (AB)"""
        start_time = time.time()
        
        best_value = 0
        best_items = []
        
        for mask in range(1 << self.n):
            current_items = []
            current_weight = 0
            current_value = 0
            
            for i in range(self.n):
                if mask & (1 << i):
                    current_items.append(self.items[i])
                    current_weight += self.items[i].size
                    current_value += self.items[i].value
            
            if current_weight <= self.capacity and current_value > best_value:
                best_value = current_value
                best_items = current_items.copy()
        
        total_size = sum(item.size for item in best_items)
        execution_time = time.time() - start_time
        
        return Solution(best_items, best_value, total_size, execution_time, 
                       "Algorytm Siłowy", Colors.BLUE)

class KnapsackVisualizer:
    """Główna klasa wizualizacji"""
    
    def __init__(self):
        self.width = 1400
        self.height = 900
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🎒 Wizualizacja Problemu Plecakowego 0-1")
        
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.state = State.MENU
        self.items = []
        self.capacity = 0
        self.solutions = []
        self.current_algorithm = 0
        self.animation_time = 0
        self.knapsack_rect = pygame.Rect(50, 200, 300, 400)
        
        # Ładowanie danych
        self.load_data()
        
    def load_data(self):
        """Ładowanie danych z pliku"""
        filename = "knapsack_data.txt"
        if not os.path.exists(filename):
            self.create_sample_file()
        
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                
            n, self.capacity = map(int, lines[0].strip().split())
            
            self.items = []
            for i in range(1, n + 1):
                size, value = map(int, lines[i].strip().split())
                item = Item(i, size, value)
                # Pozycjonowanie przedmiotów w siatce
                cols = 6
                row = (i - 1) // cols
                col = (i - 1) % cols
                item.x = 450 + col * 120
                item.y = 200 + row * 100
                self.items.append(item)
                
        except Exception as e:
            print(f"Błąd ładowania danych: {e}")
            self.create_default_items()
    
    def create_sample_file(self):
        """Tworzenie przykładowego pliku"""
        sample_data = """10 15
20 2
30 5
35 7
10 3
40 10
15 1
50 15
5 1
60 14
25 6"""
        with open("knapsack_data.txt", "w") as file:
            file.write(sample_data)
    
    def create_default_items(self):
        """Tworzenie domyślnych przedmiotów"""
        self.capacity = 15
        data = [(2, 1), (3, 4), (4, 5), (5, 7), (1, 9), (3, 4), (2, 3), (1, 2)]
        self.items = []
        for i, (size, value) in enumerate(data):
            item = Item(i + 1, size, value)
            cols = 6
            row = i // cols
            col = i % cols
            item.x = 450 + col * 120
            item.y = 200 + row * 100
            self.items.append(item)
    
    def draw_menu(self):
        """Rysowanie menu głównego"""
        self.screen.fill(Colors.BACKGROUND)
        
        # Tytuł
        title = self.font_large.render("🎒 Problem Plecakowy 0-1", True, Colors.ACCENT)
        title_rect = title.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Podtytuł
        subtitle = self.font_medium.render("Interaktywna Wizualizacja Algorytmów", True, Colors.WHITE)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Informacje o danych
        info_text = [
            f"Pojemność plecaka: {self.capacity}",
            f"Liczba przedmiotów: {len(self.items)}",
            "",
            "Kliknij, aby rozpocząć wizualizację"
        ]
        
        y_offset = 300
        for line in info_text:
            if line:
                text = self.font_small.render(line, True, Colors.WHITE)
                text_rect = text.get_rect(center=(self.width // 2, y_offset))
                self.screen.blit(text, text_rect)
            y_offset += 40
        
        # Animowany przycisk
        button_color = Colors.ACCENT if (pygame.time.get_ticks() // 500) % 2 else Colors.ORANGE
        pygame.draw.rect(self.screen, button_color, (self.width // 2 - 100, 500, 200, 60), border_radius=10)
        button_text = self.font_medium.render("START", True, Colors.BLACK)
        button_rect = button_text.get_rect(center=(self.width // 2, 530))
        self.screen.blit(button_text, button_rect)
    
    def draw_algorithm_selection(self):
        """Rysowanie ekranu wyboru algorytmu"""
        self.screen.fill(Colors.BACKGROUND)
        
        title = self.font_large.render("Wybierz Algorytm", True, Colors.ACCENT)
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)
        
        algorithms = [
            ("Programowanie Dynamiczne", "Optymalny - O(n×W)", Colors.RED),
            ("Algorytm Zachłanny", "Heurystyczny - O(n log n)", Colors.GREEN),
            ("Algorytm Siłowy", "Pełne przeszukiwanie - O(2^n)", Colors.BLUE),
            ("Porównaj Wszystkie", "Uruchom wszystkie algorytmy", Colors.PURPLE)
        ]
        
        y_start = 200
        for i, (name, desc, color) in enumerate(algorithms):
            y = y_start + i * 120
            
            # Prostokąt algorytmu
            rect = pygame.Rect(self.width // 2 - 250, y, 500, 80)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, Colors.WHITE, rect, 3, border_radius=10)
            
            # Nazwa algorytmu
            name_text = self.font_medium.render(name, True, Colors.WHITE)
            name_rect = name_text.get_rect(center=(self.width // 2, y + 25))
            self.screen.blit(name_text, name_rect)
            
            # Opis
            desc_text = self.font_small.render(desc, True, Colors.LIGHT_GRAY)
            desc_rect = desc_text.get_rect(center=(self.width // 2, y + 50))
            self.screen.blit(desc_text, desc_rect)
    
    def draw_knapsack(self, solution=None):
        """Rysowanie plecaka"""
        # Tło plecaka
        pygame.draw.rect(self.screen, Colors.PANEL, self.knapsack_rect, border_radius=15)
        pygame.draw.rect(self.screen, Colors.WHITE, self.knapsack_rect, 3, border_radius=15)
        
        # Tytuł
        title = self.font_medium.render("Plecak", True, Colors.WHITE)
        title_rect = title.get_rect(center=(self.knapsack_rect.centerx, self.knapsack_rect.top + 30))
        self.screen.blit(title, title_rect)
        
        # Pojemność
        capacity_text = f"Pojemność: {self.capacity}"
        capacity_surface = self.font_small.render(capacity_text, True, Colors.LIGHT_GRAY)
        capacity_rect = capacity_surface.get_rect(center=(self.knapsack_rect.centerx, self.knapsack_rect.top + 60))
        self.screen.blit(capacity_surface, capacity_rect)
        
        if solution:
            # Pasek wykorzystania
            usage_height = 20
            usage_rect = pygame.Rect(self.knapsack_rect.left + 20, self.knapsack_rect.top + 80, 
                                   self.knapsack_rect.width - 40, usage_height)
            pygame.draw.rect(self.screen, Colors.DARK_GRAY, usage_rect)
            
            if self.capacity > 0:
                fill_width = int((solution.total_size / self.capacity) * (self.knapsack_rect.width - 40))
                fill_rect = pygame.Rect(usage_rect.left, usage_rect.top, fill_width, usage_height)
                color = Colors.GREEN if solution.total_size <= self.capacity else Colors.RED
                pygame.draw.rect(self.screen, color, fill_rect)
            
            # Tekst wykorzystania
            usage_text = f"{solution.total_size}/{self.capacity}"
            usage_surface = self.font_small.render(usage_text, True, Colors.WHITE)
            usage_text_rect = usage_surface.get_rect(center=(self.knapsack_rect.centerx, usage_rect.centery))
            self.screen.blit(usage_surface, usage_text_rect)
            
            # Wybrane przedmioty w plecaku
            item_y = self.knapsack_rect.top + 120
            for i, item in enumerate(solution.items[:6]):  # Maksymalnie 6 przedmiotów
                item_rect = pygame.Rect(self.knapsack_rect.left + 20, item_y, 
                                      self.knapsack_rect.width - 40, 35)
                pygame.draw.rect(self.screen, item.color, item_rect, border_radius=5)
                
                # Tekst przedmiotu
                item_text = f"#{item.id}: {item.value}V/{item.size}S"
                text_surface = self.font_small.render(item_text, True, Colors.WHITE)
                text_rect = text_surface.get_rect(center=item_rect.center)
                self.screen.blit(text_surface, text_rect)
                
                item_y += 40
            
            # Jeśli więcej przedmiotów
            if len(solution.items) > 6:
                more_text = f"...i {len(solution.items) - 6} więcej"
                more_surface = self.font_small.render(more_text, True, Colors.LIGHT_GRAY)
                more_rect = more_surface.get_rect(center=(self.knapsack_rect.centerx, item_y))
                self.screen.blit(more_surface, more_rect)
    
    def draw_items(self, solution=None):
        """Rysowanie przedmiotów"""
        for item in self.items:
            # Sprawdzenie czy przedmiot jest wybrany
            selected = solution and any(sel_item.id == item.id for sel_item in solution.items)
            
            # Rozmiar prostokąta na podstawie rozmiaru przedmiotu
            size = 40 + item.size * 8
            rect = pygame.Rect(item.x - size//2, item.y - size//2, size, size)
            
            # Kolor z efektem świecenia dla wybranych
            color = item.color
            if selected:
                # Efekt pulsowania
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.3 + 0.7
                color = tuple(int(c * pulse) for c in color)
                
                # Aureola
                pygame.draw.circle(self.screen, Colors.ACCENT, rect.center, size//2 + 10, 3)
            
            # Rysowanie przedmiotu
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, Colors.WHITE, rect, 2, border_radius=8)
            
            # ID przedmiotu
            id_text = self.font_small.render(str(item.id), True, Colors.WHITE)
            id_rect = id_text.get_rect(center=(rect.centerx, rect.centery - 10))
            self.screen.blit(id_text, id_rect)
            
            # Wartość/Rozmiar
            value_text = f"{item.value}/{item.size}"
            value_surface = self.font_small.render(value_text, True, Colors.WHITE)
            value_rect = value_surface.get_rect(center=(rect.centerx, rect.centery + 8))
            self.screen.blit(value_surface, value_rect)
            
            # Współczynnik opłacalności pod przedmiotem
            ratio_text = f"{item.ratio:.1f}"
            ratio_surface = self.font_small.render(ratio_text, True, Colors.LIGHT_GRAY)
            ratio_rect = ratio_surface.get_rect(center=(rect.centerx, rect.bottom + 15))
            self.screen.blit(ratio_surface, ratio_rect)
    
    def draw_statistics(self, solution):
        """Rysowanie statystyk"""
        stats_rect = pygame.Rect(self.width - 300, 200, 250, 300)
        pygame.draw.rect(self.screen, Colors.PANEL, stats_rect, border_radius=15)
        pygame.draw.rect(self.screen, Colors.WHITE, stats_rect, 2, border_radius=15)
        
        # Tytuł
        title = self.font_medium.render("Statystyki", True, Colors.WHITE)
        title_rect = title.get_rect(center=(stats_rect.centerx, stats_rect.top + 30))
        self.screen.blit(title, title_rect)
        
        # Dane
        stats_data = [
            ("Algorytm:", solution.algorithm),
            ("Wartość:", str(solution.total_value)),
            ("Rozmiar:", f"{solution.total_size}/{self.capacity}"),
            ("Przedmioty:", str(len(solution.items))),
            ("Czas:", f"{solution.execution_time*1000:.2f}ms"),
            ("Efektywność:", f"{solution.total_value/self.capacity:.1f}")
        ]
        
        y_offset = stats_rect.top + 70
        for label, value in stats_data:
            # Label
            label_surface = self.font_small.render(label, True, Colors.LIGHT_GRAY)
            self.screen.blit(label_surface, (stats_rect.left + 20, y_offset))
            
            # Value
            value_surface = self.font_small.render(str(value), True, Colors.WHITE)
            self.screen.blit(value_surface, (stats_rect.left + 20, y_offset + 20))
            
            y_offset += 45
    
    def draw_visualization(self):
        """Rysowanie głównej wizualizacji"""
        self.screen.fill(Colors.BACKGROUND)
        
        if self.solutions:
            current_solution = self.solutions[self.current_algorithm % len(self.solutions)]
            
            # Tytuł z nazwą algorytmu
            title = self.font_large.render(current_solution.algorithm, True, current_solution.color)
            title_rect = title.get_rect(center=(self.width // 2, 50))
            self.screen.blit(title, title_rect)
            
            # Rysowanie komponentów
            self.draw_knapsack(current_solution)
            self.draw_items(current_solution)
            self.draw_statistics(current_solution)
            
            # Przyciski nawigacji
            if len(self.solutions) > 1:
                # Przycisk poprzedni
                prev_rect = pygame.Rect(50, 50, 100, 40)
                pygame.draw.rect(self.screen, Colors.GRAY, prev_rect, border_radius=5)
                prev_text = self.font_small.render("← Poprzedni", True, Colors.WHITE)
                prev_text_rect = prev_text.get_rect(center=prev_rect.center)
                self.screen.blit(prev_text, prev_text_rect)
                
                # Przycisk następny
                next_rect = pygame.Rect(self.width - 150, 50, 100, 40)
                pygame.draw.rect(self.screen, Colors.GRAY, next_rect, border_radius=5)
                next_text = self.font_small.render("Następny →", True, Colors.WHITE)
                next_text_rect = next_text.get_rect(center=next_rect.center)
                self.screen.blit(next_text, next_text_rect)
                
                # Wskaźnik
                indicator_text = f"{self.current_algorithm + 1}/{len(self.solutions)}"
                indicator_surface = self.font_small.render(indicator_text, True, Colors.WHITE)
                indicator_rect = indicator_surface.get_rect(center=(self.width // 2, 100))
                self.screen.blit(indicator_surface, indicator_rect)
        
        # Przycisk powrotu
        back_rect = pygame.Rect(50, self.height - 100, 120, 40)
        pygame.draw.rect(self.screen, Colors.RED, back_rect, border_radius=5)
        back_text = self.font_small.render("← Powrót", True, Colors.WHITE)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
    
    def run_algorithm(self, algorithm_id):
        """Uruchamianie wybranego algorytmu"""
        solver = KnapsackSolver(self.capacity, self.items)
        self.solutions = []
        
        if algorithm_id == 0:  # Programowanie dynamiczne
            solution = solver.dynamic_programming()
            self.solutions.append(solution)
        elif algorithm_id == 1:  # Zachłanny
            solution = solver.greedy_algorithm()
            self.solutions.append(solution)
        elif algorithm_id == 2:  # Siłowy
            solution = solver.brute_force()
            self.solutions.append(solution)
        elif algorithm_id == 3:  # Wszystkie
            self.solutions.append(solver.dynamic_programming())
            self.solutions.append(solver.greedy_algorithm())
            if len(self.items) <= 15:  # Ograniczenie dla algorytmu siłowego
                self.solutions.append(solver.brute_force())
        
        self.current_algorithm = 0
        self.state = State.VISUALIZATION
    
    def handle_events(self):
        """Obsługa zdarzeń"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.state == State.MENU:
                    # Kliknięcie przycisku START
                    if (self.width // 2 - 100 <= mouse_pos[0] <= self.width // 2 + 100 and
                        500 <= mouse_pos[1] <= 560):
                        self.state = State.ALGORITHM_SELECTION
                
                elif self.state == State.ALGORITHM_SELECTION:
                    # Wybór algorytmu
                    y_start = 200
                    for i in range(4):
                        y = y_start + i * 120
                        if (self.width // 2 - 250 <= mouse_pos[0] <= self.width // 2 + 250 and
                            y <= mouse_pos[1] <= y + 80):
                            self.run_algorithm(i)
                            break
                
                elif self.state == State.VISUALIZATION:
                    # Nawigacja między algorytmami
                    if len(self.solutions) > 1:
                        if (50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 90):
                            self.current_algorithm = (self.current_algorithm - 1) % len(self.solutions)
                        elif (self.width - 150 <= mouse_pos[0] <= self.width - 50 and 
                              50 <= mouse_pos[1] <= 90):
                            self.current_algorithm = (self.current_algorithm + 1) % len(self.solutions)
                    
                    # Przycisk powrotu
                    if (50 <= mouse_pos[0] <= 170 and 
                        self.height - 100 <= mouse_pos[1] <= self.height - 60):
                        self.state = State.ALGORITHM_SELECTION
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == State.VISUALIZATION:
                        self.state = State.ALGORITHM_SELECTION
                    elif self.state == State.ALGORITHM_SELECTION:
                        self.state = State.MENU
                    else:
                        return False
                
                elif event.key == pygame.K_LEFT and self.state == State.VISUALIZATION:
                    if len(self.solutions) > 1:
                        self.current_algorithm = (self.current_algorithm - 1) % len(self.solutions)
                
                elif event.key == pygame.K_RIGHT and self.state == State.VISUALIZATION:
                    if len(self.solutions) > 1:
                        self.current_algorithm = (self.current_algorithm + 1) % len(self.solutions)
        
        return True
    
    def run(self):
        """Główna pętla aplikacji"""
        running = True
        
        while running:
            running = self.handle_events()
            
            # Rysowanie odpowiedniego ekranu
            if self.state == State.MENU:
                self.draw_menu()
            elif self.state == State.ALGORITHM_SELECTION:
                self.draw_algorithm_selection()
            elif self.state == State.VISUALIZATION:
                self.draw_visualization()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

def main():
    """Funkcja główna"""
    print("🎒 Uruchamianie wizualizacji problemu plecakowego...")
    print("Wymagane biblioteki: pygame")
    print("Jeśli nie masz pygame, zainstaluj: pip install pygame")
    
    try:
        visualizer = KnapsackVisualizer()
        visualizer.run()
    except ImportError:
        print("Błąd: Nie można zaimportować pygame!")
        print("Zainstaluj pygame: pip install pygame")
    except Exception as e:
        print(f"Błąd: {e}")

if __name__ == "__main__":
    main()