# Generátor křížovek

Automatický generátor českých klasických křížovek.

## Funkce

- Generování mřížky křížovky z databáze slov
- Česká klasická křížovka (slova oddělená tučnými linkami, ne černými poli)
- Automatické umisťování slov s kontrolou křížení
- Slova mohou být těsně vedle sebe (vizuálně oddělená linkami)
- Vizualizace v ASCII a HTML formátu
- Export do HTML (s řešením i prázdné zadání)

## Databáze slov

**Malá databáze:** 887 slov (pro rychlé testování)
**Velká databáze:** 23,113 slov (všechny tvary)
**Nominativní databáze:** 22,833 slov (pouze nominativ sg/pl)

Zdroje:
- Malá: 1000 nejčastějších českých slov
- Velká: word-o-mat seznam z titulků (Creative Commons BY-SA 3.0)
- Nominativní: automaticky filtrováno pomocí morfologických pravidel

## Použití

### Generování křížovky s ASCII výstupem:

```bash
cd src
python generator.py
```

### Generování křížovky do HTML souborů:

```bash
cd src
python generate_html.py
```

Vytvoří dva HTML soubory v adresáři `output/`:
- `krizovka_reseni.html` - křížovka s vyplněným řešením
- `krizovka_zadani.html` - prázdná křížovka k vyplnění

### Generování husté křížovky (98% vyplněnost):

```bash
cd src
python generate_dense_html.py
```

Vytvoří hustou křížovku, kde téměř každé políčko je součástí slova:
- `krizovka_husta_reseni.html` - hustá křížovka s řešením
- `krizovka_husta_zadani.html` - hustá křížovka k vyplnění

Používá velkou databázi 23,113 slov a vygeneruje 80-120 slov s vyplněností 95-99%.

**Varování:** Hustá křížovka může obsahovat nevalidní sekvence písmen.

### Generování validní křížovky (DOPORUČENO):

```bash
cd src
python generate_valid_html.py
```

Vytvoří **validní křížovku**, kde:
- **Všechna slova (vodorovně i svisle) jsou z databáze**
- **Žádné duplicity** - každé slovo použito max 1x
- Vygeneruje typicky 20-40 slov
- Mřížka je menší, ale 100% validní

Soubory:
- `krizovka_validni_reseni.html` - validní křížovka s řešením
- `krizovka_validni_zadani.html` - validní křížovka k vyplnění

### První spuštění:

```bash
# Vyčištění seznamu slov (už provedeno)
cd src
python prepare_words.py
```

## Struktura projektu

```
krizovka/
├── data/
│   ├── czech_words.txt                 # Původní malý seznam (1000 slov)
│   ├── czech_words_clean.txt           # Vyčištěný malý seznam (887 slov)
│   ├── czech_words_large.txt           # Velký seznam (23,371 slov)
│   ├── czech_words_large_clean.txt     # Vyčištěný velký seznam (23,113 slov)
│   └── czech_words_large_nominative.txt # Pouze nominativy (22,833 slov)
├── src/
│   ├── generator.py            # Základní generátor křížovky
│   ├── dense_generator.py      # Generátor hustých křížovek
│   ├── valid_generator.py      # Generátor validních křížovek ⭐
│   ├── generate_html.py        # HTML výstup (základní)
│   ├── generate_dense_html.py  # HTML výstup (hustá křížovka)
│   ├── generate_valid_html.py  # HTML výstup (validní křížovka) ⭐
│   ├── grid.py                 # Třída pro mřížku
│   ├── prepare_words.py        # Příprava a čištění slov
│   ├── nominative_filter_v2.py # Filtr pro nominativní tvary
│   └── visualizer.py           # Vizualizace výstupu
├── output/
│   ├── krizovka_reseni.html         # Základní křížovka - řešení
│   ├── krizovka_zadani.html         # Základní křížovka - zadání
│   ├── krizovka_husta_reseni.html   # Hustá křížovka - řešení
│   ├── krizovka_husta_zadani.html   # Hustá křížovka - zadání
│   ├── krizovka_validni_reseni.html # Validní křížovka - řešení ⭐
│   └── krizovka_validni_zadani.html # Validní křížovka - zadání ⭐
└── README.md
```

## Algoritmus

1. Vyber slova z databáze
2. Začni s prvním slovem (nejdelší)
3. Postupně přidávej další slova, která se mohou křížit
4. Kontroluj validitu křížení (písmena musí pasovat)
5. Pokud nejde umístit, zkus jiné slovo nebo pozici
6. Opakuj dokud není mřížka naplněna nebo nejsou další slova
