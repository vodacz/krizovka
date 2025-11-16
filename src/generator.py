#!/usr/bin/env python3
"""
Generátor křížovek.
"""

import random
from typing import List, Optional
from grid import Grid, Direction

class CrosswordGenerator:
    """Generátor křížovek."""

    def __init__(self, words: List[str], grid_size: int = 30):
        """
        Inicializuje generátor.

        Args:
            words: Seznam slov pro křížovku
            grid_size: Velikost mřížky
        """
        self.words = words
        self.grid_size = grid_size
        self.grid = Grid(grid_size)

    def generate(self, max_words: int = 20, max_attempts: int = 100) -> Optional[Grid]:
        """
        Generuje křížovku.

        Args:
            max_words: Maximální počet slov v křížovce
            max_attempts: Maximální počet pokusů o umístění slova

        Returns:
            Vygenerovaná mřížka nebo None, pokud se nepodařilo
        """
        self.grid = Grid(self.grid_size)

        # Seřaď slova podle délky (od nejdelších)
        sorted_words = sorted(self.words, key=len, reverse=True)

        # Umísti první slovo doprostřed (vodorovně)
        if sorted_words:
            first_word = sorted_words[0]
            start_row = self.grid_size // 2
            start_col = (self.grid_size - len(first_word)) // 2
            if not self.grid.place_word(first_word, start_row, start_col, Direction.HORIZONTAL):
                return None
            used_words = {first_word}
        else:
            return None

        # Postupně přidávej další slova
        placed = 1
        attempts = 0
        word_idx = 1

        while placed < max_words and word_idx < len(sorted_words) and attempts < max_attempts * max_words:
            word = sorted_words[word_idx]

            # Přeskoč již použitá slova
            if word in used_words:
                word_idx += 1
                continue

            # Najdi možná křížení s existujícími slovy
            intersections = self.grid.find_intersections(word)

            if intersections:
                # Vyber náhodné křížení
                random.shuffle(intersections)
                row, col, direction, _, _ = intersections[0]

                if self.grid.place_word(word, row, col, direction):
                    used_words.add(word)
                    placed += 1
                    word_idx += 1
                    attempts = 0
                else:
                    attempts += 1
            else:
                # Žádné křížení nenalezeno, zkus další slovo
                word_idx += 1
                attempts += 1

        return self.grid

def load_words(filename: str) -> List[str]:
    """Načte slova ze souboru."""
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    """Hlavní funkce."""
    print("Generátor křížovek")
    print("=" * 50)

    # Načti slova
    words = load_words('../data/czech_words_clean.txt')
    print(f"Načteno {len(words)} slov")

    # Generuj křížovku
    print("\nGeneruji křížovku...")
    generator = CrosswordGenerator(words, grid_size=50)
    grid = generator.generate(max_words=15, max_attempts=200)

    if grid:
        print(f"Úspěch! Vygenerováno {len(grid.words)} slov")
        print("\nSlova v křížovce:")
        for i, word in enumerate(grid.words, 1):
            dir_symbol = "→" if word.direction == Direction.HORIZONTAL else "↓"
            print(f"{i:2d}. {word.text:15s} {dir_symbol} ({word.row}, {word.col})")

        # Zobraz mřížku
        print("\nMřížka:")
        print("-" * 50)
        from visualizer import visualize_ascii
        print(visualize_ascii(grid))
    else:
        print("Nepodařilo se vygenerovat křížovku")

if __name__ == '__main__':
    main()
