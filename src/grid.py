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
        # Sledování hranic slov pro tučné linky
        self.word_boundaries_h = set()  # Horizontální hranice (tučné linky vlevo od buňky)
        self.word_boundaries_v = set()  # Vertikální hranice (tučné linky nahoře od buňky)

    def _is_continuous_sequence(self, row: int, col: int, direction: Direction) -> bool:
        """
        Kontroluje, zda na dané pozici v daném směru není přerušená sekvence.
        Přerušená sekvence = písmeno-mezera-písmeno, což je nevalidní.

        Args:
            row, col: pozice ke kontrole
            direction: směr kontroly

        Returns:
            True pokud je sekvence kontinuální (bez mezer uprostřed)
        """
        # Kontrola: nesmí být situace "písmeno - mezera - písmeno" v daném směru

        if direction == Direction.VERTICAL:
            # Kontrola svisle (nahoru a dolů)
            # Pokud je nad pozicí mezera a pak písmeno -> nekontinuální
            if row > 0 and self.cells[row][col] == ' ':
                # Mezera na aktuální pozici, podívej se nahoru
                if row > 1 and self.cells[row - 1][col] == ' ' and self.cells[row - 2][col] != ' ':
                    return False  # písmeno - mezera - (nová pozice)
                # Podívej se dolů
                if row < self.size - 1 and self.cells[row + 1][col] != ' ':
                    # Kontroluj, jestli není písmeno - (nová pozice) - mezera - písmeno
                    for r in range(row + 2, self.size):
                        if self.cells[r][col] != ' ':
                            return False  # Našli jsme písmeno přes mezeru
                        elif r > row + 1:  # Našli jsme další mezeru, konec sekvence
                            break
        else:
            # Kontrola vodorovně (vlevo a vpravo)
            if col > 0 and self.cells[row][col] == ' ':
                # Mezera na aktuální pozici, podívej se vlevo
                if col > 1 and self.cells[row][col - 1] == ' ' and self.cells[row][col - 2] != ' ':
                    return False
                # Podívej se vpravo
                if col < self.size - 1 and self.cells[row][col + 1] != ' ':
                    for c in range(col + 2, self.size):
                        if self.cells[row][c] != ' ':
                            return False
                        elif c > col + 1:
                            break

        return True

    def can_place_word(self, word: str, row: int, col: int, direction: Direction) -> bool:
        """Kontroluje, zda lze slovo umístit na danou pozici."""
        # Kontrola hranic
        if direction == Direction.HORIZONTAL:
            if col + len(word) > self.size:
                return False
        else:
            if row + len(word) > self.size:
                return False

        # V české klasické křížovce jsou slova oddělena jen tučnými linkami,
        # takže slova mohou být těsně vedle sebe bez prázdných polí mezi nimi.
        # Nekontroluji tedy pole před/za slovem.

        # Kontrola každého písmene
        for i, char in enumerate(word):
            r, c = (row, col + i) if direction == Direction.HORIZONTAL else (row + i, col)
            cell_value = self.cells[r][c]

            # Buď musí být prázdné, nebo musí být stejné písmeno (křížení)
            if cell_value != ' ' and cell_value != char:
                return False

            # NOVÉ: Kontrola kontinuity v kolmém směru
            # Nesmí vzniknout přerušená sekvence (písmeno-mezera-písmeno)
            if cell_value == ' ':  # Pouze pokud umisťujeme nové písmeno
                perp_direction = Direction.VERTICAL if direction == Direction.HORIZONTAL else Direction.HORIZONTAL

                # Kontrola kontinuity v kolmém směru
                if direction == Direction.HORIZONTAL:
                    # Slovo je vodorovné, kontroluji svisle
                    # Nesmí být písmeno nad s mezerou mezi, nebo písmeno pod s mezerou mezi
                    if r > 0 and self.cells[r - 1][c] == ' ':
                        # Nad je mezera, zkontroluj jestli ještě výš není písmeno
                        if r > 1 and self.cells[r - 2][c] != ' ':
                            return False  # písmeno - mezera - nové_písmeno
                    if r < self.size - 1 and self.cells[r + 1][c] == ' ':
                        # Pod je mezera, zkontroluj jestli ještě níž není písmeno
                        if r < self.size - 2 and self.cells[r + 2][c] != ' ':
                            return False  # nové_písmeno - mezera - písmeno
                else:
                    # Slovo je svislé, kontroluji vodorovně
                    if c > 0 and self.cells[r][c - 1] == ' ':
                        # Vlevo je mezera, zkontroluj jestli ještě víc vlevo není písmeno
                        if c > 1 and self.cells[r][c - 2] != ' ':
                            return False  # písmeno - mezera - nové_písmeno
                    if c < self.size - 1 and self.cells[r][c + 1] == ' ':
                        # Vpravo je mezera, zkontroluj jestli ještě víc vpravo není písmeno
                        if c < self.size - 2 and self.cells[r][c + 2] != ' ':
                            return False  # nové_písmeno - mezera - písmeno

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

        # Zaznamenej hranice slova pro vizualizaci tučných linek
        if direction == Direction.HORIZONTAL:
            # Hranice před slovem (vlevo)
            if col > 0:
                self.word_boundaries_h.add((row, col))
            # Hranice za slovem (vpravo)
            if col + len(word) < self.size:
                self.word_boundaries_h.add((row, col + len(word)))
        else:
            # Hranice před slovem (nahoře)
            if row > 0:
                self.word_boundaries_v.add((row, col))
            # Hranice za slovem (dole)
            if row + len(word) < self.size:
                self.word_boundaries_v.add((row + len(word), col))

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
