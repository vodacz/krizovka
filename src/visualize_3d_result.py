#!/usr/bin/env python3
"""
Skript pro vizualizaci 3D křížovky.
"""

from generator_3d import CrosswordGenerator3D, load_words
from visualizer_3d import visualize_all_layers, visualize_compact, generate_html_3d

def main():
    # Načti slova
    words = load_words('../data/czech_words_large_nominative.txt')
    print(f"Načteno {len(words)} slov\n")

    # Generuj 3D křížovku
    generator = CrosswordGenerator3D(words, size=5)
    grid = generator.generate(target_fill=100.0, max_attempts=20000)

    # Vizualizace v terminálu
    print("\n" + "=" * 60)
    print("KOMPAKTNÍ VIZUALIZACE")
    print("=" * 60)
    print(visualize_compact(grid))

    # Generuj HTML
    print("\nGeneruji HTML...")
    generate_html_3d(grid, '../outputs/crossword_3d.html')
    print("HTML vygenerováno: outputs/crossword_3d.html")

    # Detailní vizualizace po vrstvách
    print("\n" + "=" * 60)
    print("VRSTVY (Z-OSA)")
    print("=" * 60)
    print(visualize_all_layers(grid))

if __name__ == '__main__':
    main()
