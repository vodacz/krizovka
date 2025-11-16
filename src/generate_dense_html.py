#!/usr/bin/env python3
"""
Generuje hustou křížovku a uloží ji do HTML souboru.
"""

import sys
from dense_generator import DenseCrosswordGenerator, load_words
from visualizer import save_html

def main():
    print("Generátor husté HTML křížovky")
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

        trimmed = grid.get_trimmed_grid()
        filled_cells = sum(1 for row in trimmed for cell in row if cell != ' ')
        fill_percentage = (filled_cells / total_cells) * 100 if total_cells > 0 else 0

        print(f"Velikost mřížky: {width} × {height}")
        print(f"Vyplněno: {filled_cells}/{total_cells} polí ({fill_percentage:.1f}%)")

        # Ulož s řešením
        output_with_solution = '../output/krizovka_husta_reseni.html'
        save_html(grid, output_with_solution, show_letters=True, title="Hustá křížovka - Řešení")

        # Ulož bez řešení (prázdná)
        output_empty = '../output/krizovka_husta_zadani.html'
        save_html(grid, output_empty, show_letters=False, title="Hustá křížovka - Zadání")

        print(f"\nSoubory vytvořeny:")
        print(f"  - {output_with_solution}")
        print(f"  - {output_empty}")
    else:
        print("Nepodařilo se vygenerovat křížovku")
        sys.exit(1)

if __name__ == '__main__':
    import os
    os.makedirs('../output', exist_ok=True)
    main()
