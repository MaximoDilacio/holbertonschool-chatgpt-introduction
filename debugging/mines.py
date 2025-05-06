#!/usr/bin/python3
import random
import os

# Limpia la pantalla según el sistema operativo
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Minesweeper:
    def __init__(self, width=10, height=10, mines=10):
        self.width = width
        self.height = height
        # Genera posiciones de minas aleatorias
        positions = list(range(width * height))
        self.mines = set(random.sample(positions, mines))
        # Campo que almacena '*' para mina o número de minas adyacentes para cada casilla
        self.field = [[0 for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                idx = y * width + x
                if idx in self.mines:
                    self.field[y][x] = '*'
                else:
                    self.field[y][x] = self.count_mines_nearby(x, y)
        # Matriz de casillas reveladas
        self.revealed = [[False for _ in range(width)] for _ in range(height)]

    def print_board(self, reveal_all=False):
        """Imprime el tablero. Si reveal_all es True, muestra todo el campo."""
        clear_screen()
        # Encabezado de columnas
        print('   ' + ' '.join(f'{i:2}' for i in range(self.width)))
        for y in range(self.height):
            # Número de fila
            print(f'{y:2} ', end='')
            for x in range(self.width):
                if reveal_all or self.revealed[y][x]:
                    val = self.field[y][x]
                    print(f'{val:2}', end=' ')
                else:
                    print(' .', end=' ')
            print()

    def count_mines_nearby(self, x, y):
        """Cuenta minas alrededor de la posición (x, y)."""
        count = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (ny * self.width + nx) in self.mines:
                        count += 1
        return count

    def reveal(self, x, y):
        """Revela la casilla y expande si es cero."""
        idx = y * self.width + x
        # Si pisa mina
        if idx in self.mines:
            return False
        # Revela la casilla
        self.revealed[y][x] = True
        # Si no hay minas alrededor, expande revelado
        if self.field[y][x] == 0:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.width and 0 <= ny < self.height
                        and not self.revealed[ny][nx]):
                        self.reveal(nx, ny)
        return True

    def check_victory(self):
        """Verifica si todas las casillas seguras están reveladas."""
        total_cells = self.width * self.height
        # Contamos reveladas
        revealed_count = sum(
            1 for y in range(self.height) for x in range(self.width)
            if self.revealed[y][x]
        )
        # Victoria si reveladas == total - minas
        return revealed_count == (total_cells - len(self.mines))

    def play(self):
        """Bucle principal del juego."""
        while True:
            self.print_board()
            try:
                x = int(input("Coordenada x: "))
                y = int(input("Coordenada y: "))
                if not self.reveal(x, y):
                    # Pierde
                    self.print_board(reveal_all=True)
                    print("¡Game Over! Pisaste una mina.")
                    break
                if self.check_victory():
                    # Gana
                    self.print_board(reveal_all=True)
                    print("¡Felicidades! Has ganado.")
                    break
            except (ValueError, IndexError):
                print("Entrada inválida. Ingresa números válidos dentro del rango.")

if __name__ == "__main__":
    game = Minesweeper(width=10, height=10, mines=10)
    game.play()
