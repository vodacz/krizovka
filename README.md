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

Používá seznam 1000 nejčastějších českých slov ze serveru GitHub.
Po vyčištění obsahuje 887 validních slov délky 3-15 znaků.

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
│   ├── czech_words.txt        # Původní seznam českých slov
│   └── czech_words_clean.txt  # Vyčištěný seznam (887 slov)
├── src/
│   ├── generator.py           # Hlavní generátor křížovky
│   ├── generate_html.py       # Generátor HTML výstupu
│   ├── grid.py                # Třída pro mřížku
│   ├── prepare_words.py       # Příprava a čištění slov
│   └── visualizer.py          # Vizualizace výstupu
├── output/
│   ├── krizovka_reseni.html   # HTML s řešením
│   └── krizovka_zadani.html   # HTML prázdné zadání
└── README.md
```

## Algoritmus

1. Vyber slova z databáze
2. Začni s prvním slovem (nejdelší)
3. Postupně přidávej další slova, která se mohou křížit
4. Kontroluj validitu křížení (písmena musí pasovat)
5. Pokud nejde umístit, zkus jiné slovo nebo pozici
6. Opakuj dokud není mřížka naplněna nebo nejsou další slova
