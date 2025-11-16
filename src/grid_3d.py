#!/usr/bin/env python3
"""
Třída pro reprezentaci 3D mřížky křížovky.
"""

from typing import List, Tuple, Optional
from enum import Enum

class Direction3D(Enum):
    """Směr slova v 3D mřížce."""
    X = 0  # Vodorovně (→)
    Y = 1  # Svisle (↓)
    Z = 2  # Do hloubky (⊙)

class Word3D:
    """Reprezentace slova v 3D mřížce."""
    def __init__(self, text: str, x: int, y: int, z: int, direction: Direction3D):
        self.text = text
        self.x = x
        self.y = y
        self.z = z
        self.direction = direction
        self.number = 0

    def get_positions(self) -> List[Tuple[int, int, int]]:
        """Vrátí seznam pozic (x, y, z) pro každé písmeno."""
        positions = []
        for i in range(len(self.text)):
            if self.direction == Direction3D.X:
                positions.append((self.x + i, self.y, self.z))
            elif self.direction == Direction3D.Y:
                positions.append((self.x, self.y + i, self.z))
            else:  # Direction3D.Z
                positions.append((self.x, self.y, self.z + i))
        return positions

    def __repr__(self):
        dir_str = {Direction3D.X: "→", Direction3D.Y: "↓", Direction3D.Z: "⊙"}[self.direction]
        return f"Word3D('{self.text}' @ ({self.x},{self.y},{self.z}) {dir_str})"

class Grid3D:
    """3D mřížka křížovky."""

    def __init__(self, size: int = 10):
        """Inicializuje prázdnou 3D mřížku."""
        self.size = size
        # 3D pole: [x][y][z]
        self.cells = [[[' ' for _ in range(size)] for _ in range(size)] for _ in range(size)]
        self.words: List[Word3D] = []

        # Hranice
        self.min_x = size
        self.max_x = 0
        self.min_y = size
        self.max_y = 0
        self.min_z = size
        self.max_z = 0

    def can_place_word(self, word: str, x: int, y: int, z: int, direction: Direction3D) -> bool:
        """Kontroluje, zda lze slovo umístit na danou pozici."""
        # Kontrola hranic
        if direction == Direction3D.X:
            if x + len(word) > self.size:
                return False
        elif direction == Direction3D.Y:
            if y + len(word) > self.size:
                return False
        else:  # Direction3D.Z
            if z + len(word) > self.size:
                return False

        # Kontrola každého písmene
        for i, char in enumerate(word):
            px, py, pz = self._get_position(x, y, z, direction, i)
            cell_value = self.cells[px][py][pz]

            # Buď musí být prázdné, nebo musí být stejné písmeno (křížení)
            if cell_value != ' ' and cell_value != char:
                return False

            # Kontrola kontinuity v kolmých směrech (2 směry pro každou osu)
            if cell_value == ' ':
                if not self._check_continuity_3d(px, py, pz, direction):
                    return False

        return True

    def _get_position(self, x: int, y: int, z: int, direction: Direction3D, offset: int) -> Tuple[int, int, int]:
        """Vrátí pozici písmene na daném offsetu ve směru."""
        if direction == Direction3D.X:
            return (x + offset, y, z)
        elif direction == Direction3D.Y:
            return (x, y + offset, z)
        else:  # Direction3D.Z
            return (x, y, z + offset)

    def _check_continuity_3d(self, x: int, y: int, z: int, word_direction: Direction3D) -> bool:
        """
        Kontroluje kontinuitu ve všech 2 kolmých směrech k danému slovu.
        Nesmí vzniknout písmeno-mezera-písmeno.
        """
        # Pro každou osu kromě směru slova kontroluj kontinuitu
        perpendicular_dirs = [d for d in Direction3D if d != word_direction]

        for perp_dir in perpendicular_dirs:
            if not self._check_continuity_in_direction(x, y, z, perp_dir):
                return False

        return True

    def _check_continuity_in_direction(self, x: int, y: int, z: int, direction: Direction3D) -> bool:
        """Kontroluje kontinuitu v jednom směru."""
        # Kontrola dopředu a dozadu ve směru

        if direction == Direction3D.X:
            # Kontrola X osy
            # Dozadu (-X)
            if x > 0 and self.cells[x-1][y][z] == ' ':
                if x > 1 and self.cells[x-2][y][z] != ' ':
                    return False
            # Dopředu (+X)
            if x < self.size - 1 and self.cells[x+1][y][z] == ' ':
                if x < self.size - 2 and self.cells[x+2][y][z] != ' ':
                    return False

        elif direction == Direction3D.Y:
            # Kontrola Y osy
            if y > 0 and self.cells[x][y-1][z] == ' ':
                if y > 1 and self.cells[x][y-2][z] != ' ':
                    return False
            if y < self.size - 1 and self.cells[x][y+1][z] == ' ':
                if y < self.size - 2 and self.cells[x][y+2][z] != ' ':
                    return False

        else:  # Direction3D.Z
            # Kontrola Z osy
            if z > 0 and self.cells[x][y][z-1] == ' ':
                if z > 1 and self.cells[x][y][z-2] != ' ':
                    return False
            if z < self.size - 1 and self.cells[x][y][z+1] == ' ':
                if z < self.size - 2 and self.cells[x][y][z+2] != ' ':
                    return False

        return True

    def place_word(self, word: str, x: int, y: int, z: int, direction: Direction3D) -> bool:
        """Umístí slovo do 3D mřížky."""
        if not self.can_place_word(word, x, y, z, direction):
            return False

        # Umísti slovo
        for i, char in enumerate(word):
            px, py, pz = self._get_position(x, y, z, direction, i)
            self.cells[px][py][pz] = char

        # Ulož slovo
        word_obj = Word3D(word, x, y, z, direction)
        self.words.append(word_obj)

        # Aktualizuj hranice
        positions = word_obj.get_positions()
        for px, py, pz in positions:
            self.min_x = min(self.min_x, px)
            self.max_x = max(self.max_x, px)
            self.min_y = min(self.min_y, py)
            self.max_y = max(self.max_y, py)
            self.min_z = min(self.min_z, pz)
            self.max_z = max(self.max_z, pz)

        return True

    def find_intersections(self, word: str) -> List[Tuple[int, int, int, Direction3D, int, int]]:
        """
        Najde všechny možné pozice, kde se slovo může křížit s existujícími slovy.
        Vrací: (x, y, z, direction, word_char_idx, existing_char_idx)
        """
        intersections = []

        for existing_word in self.words:
            # Pro každou kombinaci směrů (kromě stejného)
            for new_dir in Direction3D:
                if new_dir == existing_word.direction:
                    continue  # Slova ve stejném směru se nekříží

                # Zkus křížit každé písmeno nového slova s každým písmenem existujícího
                for new_idx, new_char in enumerate(word):
                    for exist_idx, exist_char in enumerate(existing_word.text):
                        if new_char == exist_char:
                            # Spočítej pozici pro křížení
                            exist_pos = existing_word.get_positions()[exist_idx]
                            ex, ey, ez = exist_pos

                            # Vypočti start pozici nového slova
                            if new_dir == Direction3D.X:
                                nx, ny, nz = ex - new_idx, ey, ez
                            elif new_dir == Direction3D.Y:
                                nx, ny, nz = ex, ey - new_idx, ez
                            else:  # Direction3D.Z
                                nx, ny, nz = ex, ey, ez - new_idx

                            # Kontrola, zda pozice je validní
                            if (0 <= nx < self.size and 0 <= ny < self.size and 0 <= nz < self.size and
                                self.can_place_word(word, nx, ny, nz, new_dir)):
                                intersections.append((nx, ny, nz, new_dir, new_idx, exist_idx))

        return intersections

    def get_bounds(self) -> Tuple[int, int, int, int, int, int]:
        """Vrátí hranice použité části mřížky."""
        if not self.words:
            return 0, 0, 0, 0, 0, 0
        return self.min_x, self.max_x, self.min_y, self.max_y, self.min_z, self.max_z

    def get_fill_percentage(self) -> float:
        """Vrátí procento vyplněných buněk."""
        total = self.size ** 3
        filled = sum(1 for x in range(self.size) for y in range(self.size)
                    for z in range(self.size) if self.cells[x][y][z] != ' ')
        return (filled / total) * 100 if total > 0 else 0
