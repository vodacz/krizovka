#!/usr/bin/env python3
"""
Příprava seznamu slov pro křížovku.
Vyčistí slova, odstraní neplatné znaky a krátká slova.
"""

import re
from typing import List

def clean_word(word: str) -> str:
    """Vyčistí slovo od diakritiky a speciálních znaků."""
    word = word.strip().lower()
    # Odstraň nealfabetické znaky kromě českých písmen
    word = re.sub(r'[^a-záčďéěíňóřšťúůýž]', '', word)
    return word

def is_valid_word(word: str, min_length: int = 3, max_length: int = 15) -> bool:
    """Zkontroluje, zda je slovo validní pro křížovku."""
    if not word:
        return False
    if len(word) < min_length or len(word) > max_length:
        return False
    # Pouze česká a anglická písmena
    if not re.match(r'^[a-záčďéěíňóřšťúůýž]+$', word):
        return False
    return True

def load_and_clean_words(input_file: str, output_file: str, min_length: int = 3) -> List[str]:
    """Načte slova ze souboru, vyčistí je a uloží."""
    words = []
    seen = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            word = clean_word(line)
            if is_valid_word(word, min_length) and word not in seen:
                words.append(word)
                seen.add(word)

    # Seřaď podle délky (od nejdelších)
    words.sort(key=len, reverse=True)

    # Ulož vyčištěná slova
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in words:
            f.write(word + '\n')

    return words

if __name__ == '__main__':
    words = load_and_clean_words(
        '../data/czech_words.txt',
        '../data/czech_words_clean.txt',
        min_length=3
    )
    print(f"Vyčištěno {len(words)} slov")
    print(f"Nejdelší slova: {words[:10]}")
    print(f"Průměrná délka: {sum(len(w) for w in words) / len(words):.1f}")
