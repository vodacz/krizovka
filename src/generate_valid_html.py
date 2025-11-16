#!/usr/bin/env python3
"""
Generuje validní křížovku a uloží ji do HTML.
"""

import sys
from valid_generator import ValidCrosswordGenerator, load_words
from visualizer import save_html

def main():
    print("Generátor validní křížovky")
    print("=" * 50)

    words = load_words('../data/czech_words_large_nominative.txt')
    print(f"Načteno {len(words)} slov (pouze nominativ)")

    print("\nGeneruji validní křížovku...")
    generator = ValidCrosswordGenerator(words)
    grid = generator.generate(max_words=30)

    if grid:
        print(f"Úspěch! Vygenerováno {len(grid.words)} slov")
        print(f"Použito {len(generator.used_words)} unikátních slov")

        min_row, max_row, min_col, max_col = grid.get_bounds()
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        print(f"Velikost: {width} × {height}")

        # Ulož
        output_solution = '../output/krizovka_validni_reseni.html'
        save_html(grid, output_solution, show_letters=True,
                 title="Validní křížovka - Řešení")

        output_empty = '../output/krizovka_validni_zadani.html'
        save_html(grid, output_empty, show_letters=False,
                 title="Validní křížovka - Zadání")

        print(f"\nSoubory vytvořeny:")
        print(f"  - {output_solution}")
        print(f"  - {output_empty}")

        # Výpis všech slov
        print(f"\nVšechna slova ({len(grid.words)}):")
        h_words = [w for w in grid.words if w.direction.value == 0]
        v_words = [w for w in grid.words if w.direction.value == 1]
        print(f"  Vodorovně ({len(h_words)}): {', '.join(w.text for w in h_words)}")
        print(f"  Svisle ({len(v_words)}): {', '.join(w.text for w in v_words)}")
    else:
        print("Nepodařilo se vygenerovat křížovku")
        sys.exit(1)

if __name__ == '__main__':
    import os
    os.makedirs('../output', exist_ok=True)
    main()
