import pygame
import random
import time

# Ustawienia okna wizualizacji
WIDTH, HEIGHT = 800, 600
BAR_WIDTH = 20
BACKGROUND_COLOR = (30, 30, 30)
BAR_COLOR = (100, 200, 255)
SORTED_COLOR = (100, 255, 100)

# Inicjalizacja pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shell Sort Visualization")

def draw_bars(arr, highlight_indices=[]):
    screen.fill(BACKGROUND_COLOR)
    max_val = max(arr)
    bar_height_multiplier = HEIGHT / max_val
    
    for i, val in enumerate(arr):
        x = i * BAR_WIDTH
        y = HEIGHT - val * bar_height_multiplier
        color = SORTED_COLOR if i in highlight_indices else BAR_COLOR
        pygame.draw.rect(screen, color, (x, y, BAR_WIDTH - 2, val * bar_height_multiplier))
    
    pygame.display.update()
    time.sleep(0.1)  # Opóźnienie dla lepszej widoczności

def shell_sort_visual(arr):
    n = len(arr)
    h = 1
    while h < n // 3:
        h = 3 * h + 1  # Obliczanie odstępu (Knuth sequence)
    
    while h >= 1:
        for i in range(h, n):
            j = i
            while j >= h and arr[j] < arr[j - h]:
                arr[j], arr[j - h] = arr[j - h], arr[j]  # Zamiana elementów
                draw_bars(arr, highlight_indices=[j, j - h])
                j -= h
        h //= 3  # Zmniejszenie odstępu

def main():
    num_bars = WIDTH // BAR_WIDTH
    array = [random.randint(10, HEIGHT - 50) for _ in range(num_bars)]
    
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_bars(array)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shell_sort_visual(array)
        
    pygame.quit()

if __name__ == "__main__":
    main()