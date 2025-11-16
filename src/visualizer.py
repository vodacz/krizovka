#!/usr/bin/env python3
"""
Vizualizace křížovky.
"""

from typing import List
from grid import Grid, Direction

def visualize_ascii(grid: Grid, show_letters: bool = True) -> str:
    """
    Vytvoří ASCII reprezentaci křížovky.

    Args:
        grid: Mřížka křížovky
        show_letters: Zda zobrazit písmena (True) nebo prázdná pole (False)

    Returns:
        ASCII string
    """
    if not grid.words:
        return "Prázdná mřížka"

    trimmed = grid.get_trimmed_grid()
    min_row, max_row, min_col, max_col = grid.get_bounds()

    lines = []

    # Horní okraj
    lines.append("┌" + "─" * (len(trimmed[0]) * 2 - 1) + "┐")

    # Řádky mřížky - v české klasické křížovce nejsou černá pole
    for i, row in enumerate(trimmed):
        abs_row = min_row + i
        line_parts = ["│"]

        for j, cell in enumerate(row):
            abs_col = min_col + j

            # Zobraz písmeno nebo prázdné pole
            if cell != ' ':
                char = cell.upper() if show_letters else ' '
            else:
                char = '·'  # Prázdné pole (mezera mezi slovy)

            # Přidej znak
            if j > 0:
                # Kontrola, zda mezi buňkami je hranice slova (tučná linka)
                if (abs_row, abs_col) in grid.word_boundaries_h:
                    line_parts.append("│")  # Tučná linka
                else:
                    line_parts.append(" ")  # Normální mezera

            line_parts.append(char)

        line_parts.append("│")
        lines.append("".join(line_parts))

    # Spodní okraj
    lines.append("└" + "─" * (len(trimmed[0]) * 2 - 1) + "┘")

    return "\n".join(lines)

def visualize_html(grid: Grid, show_letters: bool = True, title: str = "Křížovka") -> str:
    """
    Vytvoří HTML reprezentaci křížovky.

    Args:
        grid: Mřížka křížovky
        show_letters: Zda zobrazit písmena (True) nebo prázdná pole (False)
        title: Nadpis křížovky

    Returns:
        HTML string
    """
    if not grid.words:
        return "<p>Prázdná mřížka</p>"

    trimmed = grid.get_trimmed_grid()
    min_row, max_row, min_col, max_col = grid.get_bounds()

    html = [f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            text-align: center;
            color: #333;
        }}
        .container {{
            display: flex;
            gap: 30px;
            margin-top: 30px;
        }}
        .grid-container {{
            flex: 1;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .crossword {{
            display: inline-grid;
            grid-template-columns: repeat({len(trimmed[0])}, 35px);
            border: 2px solid #000;
        }}
        .cell {{
            width: 35px;
            height: 35px;
            background-color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 16px;
            text-transform: uppercase;
            border-right: 1px solid #ccc;
            border-bottom: 1px solid #ccc;
            box-sizing: border-box;
        }}
        .cell.empty {{
            background-color: #f0f0f0;
        }}
        .cell.border-left {{
            border-left: 3px solid #000;
        }}
        .cell.border-right {{
            border-right: 3px solid #000;
        }}
        .cell.border-top {{
            border-top: 3px solid #000;
        }}
        .cell.border-bottom {{
            border-bottom: 3px solid #000;
        }}
        .words-container {{
            flex: 1;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .word-list {{
            margin-bottom: 20px;
        }}
        .word-list h2 {{
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .word-item {{
            padding: 8px;
            margin: 5px 0;
            background: #f9f9f9;
            border-left: 3px solid #4CAF50;
            font-family: monospace;
        }}
        .stats {{
            margin-top: 20px;
            padding: 15px;
            background: #e3f2fd;
            border-radius: 4px;
        }}
        .stats h3 {{
            margin-top: 0;
            color: #1976d2;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>

    <div class="container">
        <div class="grid-container">
            <div class="crossword">
"""]

    # Generuj buňky mřížky
    for i, row in enumerate(trimmed):
        abs_row = min_row + i

        for j, cell in enumerate(row):
            abs_col = min_col + j

            # Určení CSS tříd pro tučné bordery
            css_classes = ["cell"]

            # Kontrola hranic slov
            if (abs_row, abs_col) in grid.word_boundaries_h:
                css_classes.append("border-left")
            if (abs_row, abs_col + 1) in grid.word_boundaries_h:
                css_classes.append("border-right")
            if (abs_row, abs_col) in grid.word_boundaries_v:
                css_classes.append("border-top")
            if (abs_row + 1, abs_col) in grid.word_boundaries_v:
                css_classes.append("border-bottom")

            # Obsah buňky
            if cell == ' ':
                css_classes.append("empty")
                content = ''
            else:
                content = cell.upper() if show_letters else ''

            class_str = ' '.join(css_classes)
            html.append(f'                <div class="{class_str}">{content}</div>')

    html.append("""            </div>
        </div>

        <div class="words-container">
            <div class="word-list">
                <h2>Slova v křížovce</h2>
""")

    # Seznam slov
    horizontal_words = [w for w in grid.words if w.direction == Direction.HORIZONTAL]
    vertical_words = [w for w in grid.words if w.direction == Direction.VERTICAL]

    if horizontal_words:
        html.append("                <h3>Vodorovně →</h3>")
        for word in horizontal_words:
            html.append(f'                <div class="word-item">{word.text}</div>')

    if vertical_words:
        html.append("                <h3>Svisle ↓</h3>")
        for word in vertical_words:
            html.append(f'                <div class="word-item">{word.text}</div>')

    # Statistiky
    html.append(f"""            </div>

            <div class="stats">
                <h3>Statistiky</h3>
                <p><strong>Celkem slov:</strong> {len(grid.words)}</p>
                <p><strong>Vodorovně:</strong> {len(horizontal_words)}</p>
                <p><strong>Svisle:</strong> {len(vertical_words)}</p>
                <p><strong>Velikost mřížky:</strong> {len(trimmed[0])} × {len(trimmed)}</p>
            </div>
        </div>
    </div>
</body>
</html>""")

    return "\n".join(html)

def save_html(grid: Grid, filename: str, show_letters: bool = True, title: str = "Křížovka"):
    """Uloží křížovku do HTML souboru."""
    html = visualize_html(grid, show_letters, title)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Křížovka uložena do: {filename}")
