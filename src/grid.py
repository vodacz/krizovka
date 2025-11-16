#!/usr/bin/env python3
"""
Třída pro reprezentaci mřížky křížovky.
"""

from typing import List, Tuple, Optional
from enum import Enum

class Direction(Enum):
    """Směr slova v mřížce."""
    HORIZONTAL = 0
    VERTICAL = 1

class Word:
    """Reprezentace slova v mřížce."""
    def __init__(self, text: str, row: int, col: int, direction: Direction):
        self.text = text
        self.row = row
        self.col = col
        self.direction = direction
        self.number = 0  # Číslo v křížovce (vyplní se později)

    def get_positions(self) -> List[Tuple[int, int]]:
        """Vrátí seznam pozic (řádek, sloupec) pro každé písmeno."""
        positions = []
        for i in range(len(self.text)):
            if self.direction == Direction.HORIZONTAL:
                positions.append((self.row, self.col + i))
            else:
                positions.append((self.row + i, self.col))
        return positions

    def __repr__(self):
        dir_str = "→" if self.direction == Direction.HORIZONTAL else "↓"
        return f"Word('{self.text}' @ ({self.row},{self.col}) {dir_str})"

class Grid:
    """Mřížka křížovky."""

    def __init__(self, size: int = 30):
        """Inicializuje prázdnou mřížku."""
        self.size = size
        self.cells = [[' ' for _ in range(size)] for _ in range(size)]
        self.words: List[Word] = []
        self.min_row = size
        self.max_row = 0
        self.min_col = size
        self.max_col = 0

    def can_place_word(self, word: str, row: int, col: int, direction: Direction) -> bool:
        """Kontroluje, zda lze slovo umístit na danou pozici."""
        # Kontrola hranic
        if direction == Direction.HORIZONTAL:
            if col + len(word) > self.size:
                return False
        else:
            if row + len(word) > self.size:
                return False

        # Kontrola, zda pole před slovem není obsazené
        if direction == Direction.HORIZONTAL and col > 0:
            if self.cells[row][col - 1] != ' ':
                return False
        elif direction == Direction.VERTICAL and row > 0:
            if self.cells[row - 1][col] != ' ':
                return False

        # Kontrola, zda pole za slovem není obsazené
        if direction == Direction.HORIZONTAL:
            if col + len(word) < self.size and self.cells[row][col + len(word)] != ' ':
                return False
        else:
            if row + len(word) < self.size and self.cells[row + len(word)][col] != ' ':
                return False

        # Kontrola každého písmene
        for i, char in enumerate(word):
            r, c = (row, col + i) if direction == Direction.HORIZONTAL else (row + i, col)
            cell_value = self.cells[r][c]

            # Buď musí být prázdné, nebo musí být stejné písmeno (křížení)
            if cell_value != ' ' and cell_value != char:
                return False

            # Kontrola okolí - nesmí se dotýkat jiných slov (kromě křížení)
            if cell_value == ' ':
                if direction == Direction.HORIZONTAL:
                    # Kontrola nad a pod
                    if r > 0 and self.cells[r - 1][c] != ' ':
                        return False
                    if r < self.size - 1 and self.cells[r + 1][c] != ' ':
                        return False
                else:
                    # Kontrola vlevo a vpravo
                    if c > 0 and self.cells[r][c - 1] != ' ':
                        return False
                    if c < self.size - 1 and self.cells[r][c + 1] != ' ':
                        return False

        return True

    def place_word(self, word: str, row: int, col: int, direction: Direction) -> bool:
        """Umístí slovo do mřížky."""
        if not self.can_place_word(word, row, col, direction):
            return False

        # Umísti slovo
        for i, char in enumerate(word):
            r, c = (row, col + i) if direction == Direction.HORIZONTAL else (row + i, col)
            self.cells[r][c] = char

        # Ulož slovo
        word_obj = Word(word, row, col, direction)
        self.words.append(word_obj)

        # Aktualizuj hranice
        self.min_row = min(self.min_row, row)
        self.max_row = max(self.max_row, row + (len(word) - 1 if direction == Direction.VERTICAL else 0))
        self.min_col = min(self.min_col, col)
        self.max_col = max(self.max_col, col + (len(word) - 1 if direction == Direction.HORIZONTAL else 0))

        return True

    def find_intersections(self, word: str) -> List[Tuple[int, int, Direction, int, int]]:
        """
        Najde všechny možné pozice, kde se slovo může křížit s existujícími slovy.
        Vrací: (row, col, direction, word_char_idx, existing_char_idx)
        """
        intersections = []

        for existing_word in self.words:
            # Zkus křížit každé písmeno nového slova s každým písmenem existujícího
            for new_idx, new_char in enumerate(word):
                for exist_idx, exist_char in enumerate(existing_word.text):
                    if new_char == exist_char:
                        # Spočítej pozici pro křížení
                        if existing_word.direction == Direction.HORIZONTAL:
                            # Existující slovo je vodorovné, nové bude svislé
                            row = existing_word.row - new_idx
                            col = existing_word.col + exist_idx
                            direction = Direction.VERTICAL
                        else:
                            # Existující slovo je svislé, nové bude vodorovné
                            row = existing_word.row + exist_idx
                            col = existing_word.col - new_idx
                            direction = Direction.HORIZONTAL

                        # Kontrola, zda pozice je validní
                        if (0 <= row < self.size and 0 <= col < self.size and
                            self.can_place_word(word, row, col, direction)):
                            intersections.append((row, col, direction, new_idx, exist_idx))

        return intersections

    def get_bounds(self) -> Tuple[int, int, int, int]:
        """Vrátí hranice použité části mřížky (min_row, max_row, min_col, max_col)."""
        if not self.words:
            return 0, 0, 0, 0
        return self.min_row, self.max_row, self.min_col, self.max_col

    def get_trimmed_grid(self) -> List[List[str]]:
        """Vrátí oříznutou mřížku (bez prázdných okrajů)."""
        if not self.words:
            return [[]]

        min_row, max_row, min_col, max_col = self.get_bounds()
        trimmed = []
        for r in range(min_row, max_row + 1):
            row = []
            for c in range(min_col, max_col + 1):
                row.append(self.cells[r][c])
            trimmed.append(row)
        return trimmed
