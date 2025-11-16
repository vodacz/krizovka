#!/usr/bin/env python3
"""
Validní generátor křížovek - všechna slova musí být z databáze.
"""

import random
from typing import List, Optional, Set, Tuple
from grid import Grid, Direction, Word

class ValidCrosswordGenerator:
    """Generátor validních křížovek - každé slovo v mřížce musí být z databáze."""

    def __init__(self, words: List[str]):
        """
        Args:
            words: Seznam platných slov
        """
        self.words = words
        self.word_set = set(w.lower() for w in words)  # Pro rychlé vyhledávání
        self.grid = Grid(50)
        self.used_words: Set[str] = set()

    def extract_word_at(self, row: int, col: int, direction: Direction) -> str:
        """
        Extrahuje slovo z mřížky začínající na dané pozici.

        Returns:
            Extrahované slovo nebo prázdný string
        """
        word = []
        r, c = row, col

        while True:
            if r >= self.grid.size or c >= self.grid.size:
                break
            if self.grid.cells[r][c] == ' ':
                break
            word.append(self.grid.cells[r][c])

            if direction == Direction.HORIZONTAL:
                c += 1
            else:
                r += 1

        return ''.join(word)

    def get_perpendicular_sequences(self, word: str, row: int, col: int,
                                   direction: Direction) -> List[Tuple[str, int, int, Direction]]:
        """
        Získá všechny kolmé sekvence písmen, které by vznikly umístěním slova.

        Returns:
            List of (sequence, start_row, start_col, perpendicular_direction)
        """
        sequences = []

        for i in range(len(word)):
            if direction == Direction.HORIZONTAL:
                # Slovo je vodorovné, kontroluji svislé sekvence
                r, c = row, col + i
                perp_dir = Direction.VERTICAL

                # Najdi začátek svislé sekvence
                start_r = r
                while start_r > 0 and self.grid.cells[start_r - 1][c] != ' ':
                    start_r -= 1

                # Extrahuj celou svislou sekvenci (včetně nového písmene)
                seq = []
                curr_r = start_r
                while curr_r < self.grid.size:
                    if curr_r == r:
                        seq.append(word[i])  # Nové písmeno
                    elif self.grid.cells[curr_r][c] != ' ':
                        seq.append(self.grid.cells[curr_r][c])
                    else:
                        break
                    curr_r += 1

                if len(seq) > 1:  # Ignoruj jednotlivá písmena
                    sequences.append((''.join(seq), start_r, c, perp_dir))

            else:
                # Slovo je svislé, kontroluji vodorovné sekvence
                r, c = row + i, col
                perp_dir = Direction.HORIZONTAL

                # Najdi začátek vodorovné sekvence
                start_c = c
                while start_c > 0 and self.grid.cells[r][start_c - 1] != ' ':
                    start_c -= 1

                # Extrahuj celou vodorovnou sekvenci
                seq = []
                curr_c = start_c
                while curr_c < self.grid.size:
                    if curr_c == c:
                        seq.append(word[i])
                    elif self.grid.cells[r][curr_c] != ' ':
                        seq.append(self.grid.cells[r][curr_c])
                    else:
                        break
                    curr_c += 1

                if len(seq) > 1:
                    sequences.append((''.join(seq), r, start_c, perp_dir))

        return sequences

    def is_valid_placement(self, word: str, row: int, col: int, direction: Direction) -> bool:
        """
        Kontroluje, zda umístění slova vytvoří pouze validní slova z databáze.
        """
        # Základní kontrola pozice
        if not self.grid.can_place_word(word, row, col, direction):
            return False

        # Kontrola, že slovo už není použité
        if word.lower() in self.used_words:
            return False

        # Získej všechny kolmé sekvence, které by vznikly
        perp_sequences = self.get_perpendicular_sequences(word, row, col, direction)

        # Každá kolmá sekvence musí být:
        # 1. Součást již umístěného slova (již validována)
        # 2. Nebo nové platné slovo z databáze (které ještě není použité)
        for seq, seq_row, seq_col, seq_dir in perp_sequences:
            seq_lower = seq.lower()

            # Zkontroluj, zda tato sekvence odpovídá již umístěnému slovu
            is_existing = False
            for existing_word in self.grid.words:
                if (existing_word.row == seq_row and
                    existing_word.col == seq_col and
                    existing_word.direction == seq_dir and
                    existing_word.text.lower() == seq_lower):
                    is_existing = True
                    break

            if is_existing:
                continue  # OK, je to již umístěné slovo

            # Musí to být nové platné slovo z databáze
            if seq_lower not in self.word_set:
                return False  # Není v databázi

            if seq_lower in self.used_words:
                return False  # Už bylo použité

        return True

    def place_word_with_validation(self, word: str, row: int, col: int,
                                   direction: Direction) -> bool:
        """
        Umístí slovo s plnou validací.
        """
        if not self.is_valid_placement(word, row, col, direction):
            return False

        # Získej kolmé sekvence
        perp_sequences = self.get_perpendicular_sequences(word, row, col, direction)

        # Umísti hlavní slovo
        if not self.grid.place_word(word, row, col, direction):
            return False

        self.used_words.add(word.lower())

        # Označ kolmé sekvence jako použitá slova
        for seq, seq_row, seq_col, seq_dir in perp_sequences:
            seq_lower = seq.lower()

            # Zkontroluj, zda už není v words (jako existující)
            already_placed = False
            for existing_word in self.grid.words[:-1]:  # Bez právě přidaného
                if (existing_word.row == seq_row and
                    existing_word.col == seq_col and
                    existing_word.direction == seq_dir):
                    already_placed = True
                    break

            if not already_placed:
                # Přidej jako nové slovo
                word_obj = Word(seq, seq_row, seq_col, seq_dir)
                self.grid.words.append(word_obj)
                self.used_words.add(seq_lower)

        return True

    def generate(self, max_words: int = 30) -> Optional[Grid]:
        """Generuje validní křížovku."""
        # Seřaď slova podle délky
        sorted_words = sorted(self.words, key=len, reverse=True)

        # Umísti první slovo
        if sorted_words:
            first_word = sorted_words[0]
            start_row = self.grid.size // 2
            start_col = (self.grid.size - len(first_word)) // 2
            self.place_word_with_validation(first_word, start_row, start_col,
                                          Direction.HORIZONTAL)

        placed = 1
        attempts = 0
        max_attempts = max_words * 500

        while placed < max_words and attempts < max_attempts:
            # Náhodné slovo
            word = random.choice(sorted_words[:500])

            if word.lower() in self.used_words:
                attempts += 1
                continue

            # Najdi křížení
            intersections = self.grid.find_intersections(word)

            if intersections:
                random.shuffle(intersections)
                placed_any = False

                for row, col, direction, _, _ in intersections[:20]:
                    if self.place_word_with_validation(word, row, col, direction):
                        placed += 1
                        attempts = 0
                        placed_any = True
                        break

                if not placed_any:
                    attempts += 1
            else:
                attempts += 1

        return self.grid

def load_words(filename: str) -> List[str]:
    """Načte slova ze souboru."""
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    """Hlavní funkce."""
    print("Generátor validních křížovek")
    print("=" * 50)

    words = load_words('../data/czech_words_large_nominative.txt')
    print(f"Načteno {len(words)} slov (pouze nominativ)")

    print("\nGeneruji validní křížovku...")
    generator = ValidCrosswordGenerator(words)
    grid = generator.generate(max_words=30)

    if grid:
        print(f"Úspěch! Vygenerováno {len(grid.words)} slov")
        print(f"Použito {len(generator.used_words)} unikátních slov")

        # Statistiky
        min_row, max_row, min_col, max_col = grid.get_bounds()
        width = max_col - min_col + 1
        height = max_row - min_row + 1

        print(f"Velikost: {width} × {height}")

        print("\nSlova v křížovce:")
        for i, word in enumerate(grid.words, 1):
            dir_symbol = "→" if word.direction == Direction.HORIZONTAL else "↓"
            print(f"{i:2d}. {word.text:15s} {dir_symbol}")

        # Zobraz mřížku
        print("\nMřížka:")
        print("-" * 50)
        from visualizer import visualize_ascii
        print(visualize_ascii(grid))
    else:
        print("Nepodařilo se vygenerovat křížovku")

if __name__ == '__main__':
    main()
