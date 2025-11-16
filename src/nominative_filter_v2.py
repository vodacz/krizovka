#!/usr/bin/env python3
"""
Vylepšený filtr pro redukci na nominativní tvary.
"""

from typing import List
import re

def is_likely_non_nominative(word: str) -> bool:
    """
    Detekuje slova, která jsou pravděpodobně NE v nominativu.
    Vrací True, pokud slovo má být odfiltrováno.
    """
    if len(word) < 4:
        return False  # Krátká slova necháme

    word_lower = word.lower()

    # Výjimky - nominativní tvary, které vypadají jako ne-nominativ
    exceptions = {
        'host', 'most', 'rost', 'kost', 'list', 'post',
        'radost', 'mladost', 'starost', 'dřevnost',
        'proud', 'pokrm',
    }

    if word_lower in exceptions:
        return False

    # 1. Genitiv/Lokál plurál: -ích, -ech, -ách (min 6 znaků)
    if len(word) >= 6:
        if re.search(r'(ích|ech|ách)$', word_lower):
            return True

    # 2. Instrumentál: -tvím, -ností (min 6 znaků)
    if len(word) >= 6:
        if word_lower.endswith('tvím') or word_lower.endswith('ností'):
            return True

    # 3. Dativ/Lokál singuláru: -osti (min 7 znaků, aby se neodfiltrovala "radost")
    if len(word) >= 7:
        if word_lower.endswith('osti'):
            return True

    # 4. Genitiv maskulin: -enta, -anta (min 8 znaků)
    if len(word) >= 8:
        if re.search(r'(enta|anta)$', word_lower):
            # Ale ne slova končící na -menta (dokumenta je OK, ale dokumenta je genitiv)
            if not word_lower.endswith('menta'):
                return True

    # 5. Akuzativ/Genitiv feminin plurál: dlouhá slova na -y (min 8 znaků)
    # např. "knihy" (akuzativ), ale "levy" je OK
    # Toto je velmi nespolehlivé, takže to vynechám

    return False

def filter_nominatives(input_file: str, output_file: str) -> tuple[int, int]:
    """
    Filtruje soubor se slovy a odstraní ne-nominativní tvary.

    Returns:
        (počet původních slov, počet slov po filtraci)
    """
    words = []
    with open(input_file, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]

    original_count = len(words)
    filtered_words = [w for w in words if not is_likely_non_nominative(w)]
    filtered_count = len(filtered_words)

    with open(output_file, 'w', encoding='utf-8') as f:
        for word in filtered_words:
            f.write(word + '\n')

    removed = original_count - filtered_count
    print(f"Původní počet slov: {original_count}")
    print(f"Odstraněno: {removed} ({removed/original_count*100:.1f}%)")
    print(f"Zbývá: {filtered_count}")

    return original_count, filtered_count

def main():
    """Hlavní funkce."""
    # Test na ukázkových slovech
    test_words = [
        ('pes', False),  # Nominativ - ponechat
        ('psa', False),  # Genitiv, ale krátké - ponechat
        ('kočka', False),  # Nominativ - ponechat
        ('bezpečnostních', True),  # Genitiv plurál - odstranit
        ('představivosti', True),  # Genitiv/dativ - odstranit
        ('viceprezidenta', True),  # Genitiv - odstranit
        ('spravedlnost', False),  # Nominativ - ponechat
        ('spravedlnosti', True),  # Genitiv - odstranit
        ('prostřednictvím', True),  # Instrumentál - odstranit
        ('host', False),  # Nominativ (výjimka) - ponechat
        ('radost', False),  # Nominativ - ponechat
        ('mezinárodních', True),  # Genitiv plurál - odstranit
        ('záležitostech', True),  # Lokál plurál - odstranit
    ]

    print("Test filtrace:")
    print("-" * 50)
    correct = 0
    for word, should_remove in test_words:
        is_removed = is_likely_non_nominative(word)
        expected = "ODSTRANIT" if should_remove else "ponechat"
        actual = "ODSTRANIT" if is_removed else "ponechat"
        status = "✓" if is_removed == should_remove else "✗"

        print(f"{status} {word:20s} očekáváno: {expected:10s} výsledek: {actual:10s}")

        if is_removed == should_remove:
            correct += 1

    print(f"\nÚspěšnost: {correct}/{len(test_words)} ({correct/len(test_words)*100:.0f}%)")

if __name__ == '__main__':
    main()
