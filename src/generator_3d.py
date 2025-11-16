#!/usr/bin/env python3
"""
Generátor 3D křížovek.
Cíl: Maximální vyplnění prostoru (ideálně 100%)
"""

import random
from typing import List, Set
from grid_3d import Grid3D, Direction3D, Word3D

class CrosswordGenerator3D:
    """Generátor 3D křížovek s krystalovou růstovou strukturou."""

    def __init__(self, words: List[str], size: int = 5):
        self.words = words
        self.size = size
        self.grid = Grid3D(size)
        self.used_words: Set[str] = set()

    def generate(self, target_fill: float = 100.0, max_attempts: int = 10000) -> Grid3D:
        """
        Generuje 3D křížovku s cílem dosáhnout target_fill% vyplnění.

        Args:
            target_fill: Cílové procento vyplnění (0-100)
            max_attempts: Maximální počet pokusů
        """
        # Seřaď slova podle délky
        sorted_words = sorted(self.words, key=len, reverse=True)

        # Preferuj slova délky 3-5 pro lepší zaplnění 5×5×5
        suitable_words = [w for w in sorted_words if 3 <= len(w) <= 5]
        if not suitable_words:
            suitable_words = sorted_words

        # Začni s prvním slovem uprostřed v ose X
        if suitable_words:
            first_word = suitable_words[0]
            start_x = (self.size - len(first_word)) // 2
            start_y = self.size // 2
            start_z = self.size // 2

            self.grid.place_word(first_word, start_x, start_y, start_z, Direction3D.X)
            self.used_words.add(first_word.lower())

        placed = 1
        attempts = 0
        last_progress = 0

        print(f"Začínám generování 3D křížovky {self.size}×{self.size}×{self.size}")
        print(f"Cílové vyplnění: {target_fill}%")
        print(f"Dostupných slov: {len(suitable_words)}")

        while attempts < max_attempts:
            current_fill = self.grid.get_fill_percentage()

            # Progress update
            if int(current_fill) > last_progress:
                last_progress = int(current_fill)
                print(f"Vyplněno: {current_fill:.1f}% ({len(self.grid.words)} slov)")

            # Pokud dosáhneme cíle, skončíme
            if current_fill >= target_fill:
                print(f"Dosaženo cílového vyplnění!")
                break

            # Vyber náhodné slovo
            word = random.choice(suitable_words[:min(100, len(suitable_words))])

            if word.lower() in self.used_words:
                attempts += 1
                continue

            # Najdi možná křížení
            intersections = self.grid.find_intersections(word)

            if intersections:
                random.shuffle(intersections)
                placed_any = False

                # Zkus prvních N křížení
                for x, y, z, direction, _, _ in intersections[:20]:
                    if self.grid.place_word(word, x, y, z, direction):
                        self.used_words.add(word.lower())
                        placed += 1
                        attempts = 0
                        placed_any = True
                        break

                if not placed_any:
                    attempts += 1
            else:
                attempts += 1

            # Pokud uvízneme, zkus agresivnější přístup
            if attempts > 1000 and attempts % 1000 == 0:
                print(f"Pokus {attempts}: Zkoušim kratší slova...")
                # Zkus velmi krátká slova (3-4 písmena)
                short_words = [w for w in self.words if 3 <= len(w) <= 4 and w.lower() not in self.used_words]
                if short_words:
                    suitable_words = short_words + suitable_words

        final_fill = self.grid.get_fill_percentage()
        print(f"\nKonečné vyplnění: {final_fill:.1f}%")
        print(f"Počet slov: {len(self.grid.words)}")
        print(f"Použito pokusů: {attempts}/{max_attempts}")

        return self.grid

def load_words(filename: str) -> List[str]:
    """Načte slova ze souboru."""
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    """Hlavní funkce."""
    print("=" * 60)
    print("Generátor 3D křížovek")
    print("=" * 60)

    # Načti slova
    words = load_words('../data/czech_words_large_nominative.txt')
    print(f"Načteno {len(words)} slov\n")

    # Generuj 3D křížovku 5×5×5
    generator = CrosswordGenerator3D(words, size=5)
    grid = generator.generate(target_fill=100.0, max_attempts=20000)

    if grid:
        print(f"\n{'=' * 60}")
        print("VÝSLEDEK")
        print(f"{'=' * 60}")

        # Statistiky
        bounds = grid.get_bounds()
        print(f"Hranice: X[{bounds[0]}-{bounds[1]}] Y[{bounds[2]}-{bounds[3]}] Z[{bounds[4]}-{bounds[5]}]")
        print(f"Vyplněno: {grid.get_fill_percentage():.1f}%")

        # Seznam slov
        print(f"\nSlova podle směrů:")
        for direction in Direction3D:
            dir_words = [w for w in grid.words if w.direction == direction]
            dir_symbol = {Direction3D.X: "→", Direction3D.Y: "↓", Direction3D.Z: "⊙"}[direction]
            print(f"\n{dir_symbol} {direction.name} ({len(dir_words)} slov):")
            for i, word in enumerate(dir_words[:10], 1):
                print(f"  {i:2d}. {word.text:12s} @ ({word.x}, {word.y}, {word.z})")
            if len(dir_words) > 10:
                print(f"  ... a dalších {len(dir_words) - 10} slov")

if __name__ == '__main__':
    main()
