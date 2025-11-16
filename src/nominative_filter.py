#!/usr/bin/env python3
"""
Filtr pro redukci substantiv na nominativ singuláru nebo plurálu.
Používá jednoduchou heuristiku pro odfiltrování zjevných ne-nominativních tvarů.
"""

import re
from typing import List, Set

# Typické koncovky ne-nominativních pádů
NON_NOMINATIVE_ENDINGS = [
    # Genitiv/lokál plurál
    'ích',  # mezinárodních, bezpečnostních
    'ech',  # záležitostech
    'ách',  # knihách

    # Genitiv singuláru maskulin/neutrum
    'ova',  # prezidenta -> nechci
    'ora',  # profesora -> nechci
    'ela',  # anděla -> nechci

    # Dativ/lokál singuláru
    'osti',  # představivosti, zodpovědnosti
    'osti',  # radosti

    # Instrumentál
    'stvím', # prostřednictvím
    'ností',  # pravděpodobností
]

# Výjimky - slova, která končí na tyto koncovky, ale jsou v nominativu
EXCEPTIONS = {
    'host', 'most', 'rost', 'kost',  # Končí na -ost, ale nominativ
    'list', 'ústí',
}

def is_likely_nominative(word: str) -> bool:
    """
    Jednoduchá heuristika - zkontroluje, zda slovo pravděpodobně není v nominativu.

    Args:
        word: Slovo k ověření

    Returns:
        True pokud slovo pravděpodobně JE v nominativu
    """
    word_lower = word.lower()

    # Výjimky
    if word_lower in EXCEPTIONS:
        return True

    # Kontrola ne-nominativních koncovek
    for ending in NON_NOMINATIVE_ENDINGS:
        if word_lower.endswith(ending):
            return False

    # Speciální pravidla pro -a končící slova (maskulina v genitivu)
    if len(word) > 5 and word.endswith('a'):
        # Slova končící na -enta, -anta, -ista jsou často genitiv
        if word.endswith(('enta', 'anta')):
            # viceprezidenta, studenta
            return False

    # Pravděpodobně nominativ
    return True

def filter_nominatives(words: List[str]) -> List[str]:
    """
    Filtruje slova a nechá jen ta, která jsou pravděpodobně v nominativu.

    Args:
        words: Seznam slov

    Returns:
        Filtrovaný seznam
    """
    filtered = []
    removed_count = 0

    for word in words:
        if is_likely_nominative(word):
            filtered.append(word)
        else:
            removed_count += 1

    print(f"Odfiltrováno {removed_count} ne-nominativních tvarů")
    return filtered

def main():
    """Hlavní funkce pro testování."""
    # Testovací slova
    test_words = [
        'pes', 'psa', 'psu',  # Nominativ, genitiv, dativ
        'kočka', 'kočky',  # Nominativ, genitiv
        'bezpečnostních',  # Genitiv plurál
        'představivosti',  # Genitiv/dativ/lokál
        'viceprezidenta',  # Genitiv
        'spravedlnost',  # Nominativ
        'spravedlnosti',  # Genitiv
        'prostřednictvím',  # Instrumentál
        'host',  # Nominativ (výjimka)
        'radost',  # Nominativ
    ]

    print("Test filtrace:")
    for word in test_words:
        is_nom = is_likely_nominative(word)
        status = "✓ NOMINATIV" if is_nom else "✗ odfiltrováno"
        print(f"{word:20s} {status}")

if __name__ == '__main__':
    main()
