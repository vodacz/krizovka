#!/usr/bin/env python3
"""
Vylepšený generátor křížovek s hustou mřížkou.
Cíl: každé políčko je součástí nějakého slova.
"""

import random
from typing import List, Optional, Set, Tuple
from grid import Grid, Direction

class DenseCrosswordGenerator:
    """Generátor hustých křížovek."""

    def __init__(self, words: List[str], target_size: int = 15):
        """
        Inicializuje generátor.

        Args:
            words: Seznam slov pro křížovku
            target_size: Cílová velikost mřížky (bude menší než grid_size)
        """
        self.words = words
        self.target_size = target_size
        self.grid = Grid(target_size + 10)  # Větší mřížka pro rezervu
        self.used_words: Set[str] = set()

    def generate(self, max_words: int = 50, min_word_length: int = 3) -> Optional[Grid]:
        """
        Generuje hustou křížovku.

        Args:
            max_words: Maximální počet slov
            min_word_length: Minimální délka slova

        Returns:
            Vygenerovaná mřížka nebo None
        """
        # Filtrace slov podle délky
        filtered_words = [w for w in self.words if len(w) >= min_word_length]

        # Seřaď slova podle délky (od nejdelších)
        sorted_words = sorted(filtered_words, key=len, reverse=True)

        # Začni s prvním slovem doprostřed
        if sorted_words:
            first_word = sorted_words[0]
            start_row = self.grid.size // 2
            start_col = (self.grid.size - len(first_word)) // 2
            if not self.grid.place_word(first_word, start_row, start_col, Direction.HORIZONTAL):
                return None
            self.used_words.add(first_word)
        else:
            return None

        placed = 1
        attempts = 0
        max_attempts = max_words * 200

        # Postupně přidávej další slova
        while placed < max_words and attempts < max_attempts:
            # Náhodně vyber slovo
            word = random.choice(sorted_words[:min(500, len(sorted_words))])

            if word in self.used_words:
                attempts += 1
                continue

            # Najdi křížení
            intersections = self.grid.find_intersections(word)

            if intersections:
                # Zkus náhodné křížení
                random.shuffle(intersections)
                placed_any = False

                for row, col, direction, _, _ in intersections[:10]:  # Zkus prvních 10
                    if self.grid.place_word(word, row, col, direction):
                        self.used_words.add(word)
                        placed += 1
                        attempts = 0
                        placed_any = True
                        break

                if not placed_any:
                    attempts += 1
            else:
                attempts += 1

        # Zkus vyplnit mezery krátkými slovy
        self._fill_gaps(sorted_words, min_word_length=3)

        return self.grid

    def _fill_gaps(self, words: List[str], min_word_length: int = 3):
        """
        Pokusí se vyplnit mezery v mřížce krátkými slovy.
        """
        short_words = [w for w in words if min_word_length <= len(w) <= 6 and w not in self.used_words]
        random.shuffle(short_words)

        min_row, max_row, min_col, max_col = self.grid.get_bounds()

        for word in short_words[:200]:  # Zkus max 200 slov
            if word in self.used_words:
                continue

            # Hledej místa, kde by slovo mohlo zaplnit mezeru
            for row in range(min_row, max_row + 1):
                for col in range(min_col, max_col + 1):
                    for direction in [Direction.HORIZONTAL, Direction.VERTICAL]:
                        if self.grid.place_word(word, row, col, direction):
                            self.used_words.add(word)
                            break

def load_words(filename: str) -> List[str]:
    """Načte slova ze souboru."""
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    """Hlavní funkce."""
    print("Generátor hustých křížovek")
    print("=" * 50)

    # Načti slova
    words = load_words('../data/czech_words_large_clean.txt')
    print(f"Načteno {len(words)} slov")

    # Generuj křížovku
    print("\nGeneruji hustou křížovku...")
    generator = DenseCrosswordGenerator(words, target_size=15)
    grid = generator.generate(max_words=50, min_word_length=3)

    if grid:
        print(f"Úspěch! Vygenerováno {len(grid.words)} slov")

        # Statistiky
        min_row, max_row, min_col, max_col = grid.get_bounds()
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        total_cells = width * height

        # Spočítej vyplněné buňky
        trimmed = grid.get_trimmed_grid()
        filled_cells = sum(1 for row in trimmed for cell in row if cell != ' ')
        fill_percentage = (filled_cells / total_cells) * 100 if total_cells > 0 else 0

        print(f"Velikost mřížky: {width} × {height} ({total_cells} polí)")
        print(f"Vyplněno: {filled_cells} polí ({fill_percentage:.1f}%)")

        print("\nSlova v křížovce:")
        for i, word in enumerate(grid.words[:20], 1):  # Zobraz prvních 20
            dir_symbol = "→" if word.direction == Direction.HORIZONTAL else "↓"
            print(f"{i:2d}. {word.text:15s} {dir_symbol}")

        if len(grid.words) > 20:
            print(f"... a dalších {len(grid.words) - 20} slov")

        # Zobraz mřížku
        print("\nMřížka:")
        print("-" * 50)
        from visualizer import visualize_ascii
        print(visualize_ascii(grid))
    else:
        print("Nepodařilo se vygenerovat křížovku")

if __name__ == '__main__':
    main()
