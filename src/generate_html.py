#!/usr/bin/env python3
"""
Generuje křížovku a uloží ji do HTML souboru.
"""

import sys
from generator import CrosswordGenerator, load_words
from visualizer import save_html

def main():
    print("Generátor HTML křížovky")
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

        # Ulož s řešením
        output_with_solution = '../output/krizovka_reseni.html'
        save_html(grid, output_with_solution, show_letters=True, title="Křížovka - Řešení")

        # Ulož bez řešení (prázdná)
        output_empty = '../output/krizovka_zadani.html'
        save_html(grid, output_empty, show_letters=False, title="Křížovka - Zadání")

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
