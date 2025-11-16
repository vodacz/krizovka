#!/usr/bin/env python3
"""
Vizualizace 3D křížovky.
"""

from grid_3d import Grid3D, Direction3D

def visualize_layer(grid: Grid3D, z: int) -> str:
    """Vizualizuje jednu vrstvu (Z-úroveň) 3D křížovky."""
    output = []
    output.append(f"┌─ Vrstva Z={z} " + "─" * 20 + "┐")

    for y in range(grid.size):
        row = "│ "
        for x in range(grid.size):
            char = grid.cells[x][y][z]
            if char == ' ':
                row += "· "
            else:
                row += char + " "
        row += "│"
        output.append(row)

    output.append("└" + "─" * (grid.size * 2 + 2) + "┘")
    return "\n".join(output)

def visualize_all_layers(grid: Grid3D) -> str:
    """Vizualizuje všechny vrstvy 3D křížovky."""
    output = []

    for z in range(grid.size):
        output.append(visualize_layer(grid, z))
        output.append("")  # Mezera mezi vrstvami

    return "\n".join(output)

def visualize_compact(grid: Grid3D) -> str:
    """Kompaktní vizualizace - všechny vrstvy vedle sebe."""
    lines = [[] for _ in range(grid.size + 2)]  # +2 pro rámečky

    for z in range(grid.size):
        # Horní rámeček
        lines[0].append(f"Z={z} ")
        lines[0].append("┌" + "─" * (grid.size * 2) + "┐")

        # Řádky dat
        for y in range(grid.size):
            row = "│"
            for x in range(grid.size):
                char = grid.cells[x][y][z]
                row += char if char != ' ' else '·'
                row += " "
            row += "│"
            lines[y + 1].append(row)

        # Spodní rámeček
        lines[grid.size + 1].append("└" + "─" * (grid.size * 2) + "┘")

        # Mezera mezi vrstvami (kromě poslední)
        if z < grid.size - 1:
            for line_list in lines:
                line_list.append("  ")

    return "\n".join(" ".join(line_parts) for line_parts in lines)

def generate_html_3d(grid: Grid3D, filename: str = None) -> str:
    """Vygeneruje HTML vizualizaci 3D křížovky s interaktivním přepínáním vrstev."""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>3D Křížovka</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: #1a1a1a;
            color: #fff;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: #4af;
        }
        .stats {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .layer-controls {
            text-align: center;
            margin: 20px 0;
        }
        .layer-controls button {
            background: #4af;
            color: #000;
            border: none;
            padding: 10px 20px;
            margin: 0 5px;
            cursor: pointer;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
        }
        .layer-controls button:hover {
            background: #6cf;
        }
        .layer-controls button:disabled {
            background: #555;
            cursor: not-allowed;
        }
        .layer-indicator {
            font-size: 24px;
            margin: 10px 0;
            color: #4af;
        }
        .grid {
            display: inline-block;
            background: #000;
            padding: 10px;
            border-radius: 8px;
            margin: 20px auto;
            display: block;
            text-align: center;
        }
        .grid-row {
            line-height: 1.4;
        }
        .cell {
            display: inline-block;
            width: 30px;
            height: 30px;
            line-height: 30px;
            text-align: center;
            margin: 1px;
            font-size: 18px;
            font-weight: bold;
            border: 1px solid #444;
        }
        .cell.filled {
            background: #2a4a6a;
            color: #fff;
        }
        .cell.empty {
            background: #1a1a1a;
            color: #333;
        }
        .layer {
            display: none;
        }
        .layer.active {
            display: block;
        }
        .words-list {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .direction-group {
            margin: 10px 0;
        }
        .direction-title {
            color: #4af;
            font-size: 18px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 3D Křížovka</h1>

        <div class="stats">
            <strong>Velikost:</strong> """ + f"{grid.size}×{grid.size}×{grid.size}" + f""" ({grid.size**3} buněk)<br>
            <strong>Vyplněno:</strong> {grid.get_fill_percentage():.1f}%<br>
            <strong>Počet slov:</strong> {len(grid.words)}<br>
        </div>

        <div class="layer-controls">
            <button onclick="prevLayer()">◀ Předchozí</button>
            <span class="layer-indicator" id="layerIndicator">Vrstva Z = 0</span>
            <button onclick="nextLayer()">Následující ▶</button>
        </div>

        <div id="gridContainer">
"""

    # Generuj všechny vrstvy
    for z in range(grid.size):
        html += f'        <div class="layer{" active" if z == 0 else ""}" id="layer{z}">\n'
        html += '            <div class="grid">\n'

        for y in range(grid.size):
            html += '                <div class="grid-row">\n'
            for x in range(grid.size):
                char = grid.cells[x][y][z]
                cell_class = "filled" if char != ' ' else "empty"
                display_char = char if char != ' ' else '·'
                html += f'                    <span class="cell {cell_class}">{display_char}</span>\n'
            html += '                </div>\n'

        html += '            </div>\n'
        html += '        </div>\n'

    html += """        </div>

        <div class="words-list">
            <h2>Seznam slov</h2>
"""

    # Seznam slov podle směrů
    for direction in Direction3D:
        dir_words = [w for w in grid.words if w.direction == direction]
        if dir_words:
            dir_symbol = {Direction3D.X: "→", Direction3D.Y: "↓", Direction3D.Z: "⊙"}[direction]
            html += f'            <div class="direction-group">\n'
            html += f'                <div class="direction-title">{dir_symbol} {direction.name} ({len(dir_words)} slov)</div>\n'
            for word in dir_words:
                html += f'                {word.text} @ ({word.x},{word.y},{word.z})<br>\n'
            html += '            </div>\n'

    html += """        </div>
    </div>

    <script>
        let currentLayer = 0;
        const maxLayer = """ + str(grid.size - 1) + """;

        function showLayer(z) {
            document.querySelectorAll('.layer').forEach(layer => {
                layer.classList.remove('active');
            });
            document.getElementById('layer' + z).classList.add('active');
            document.getElementById('layerIndicator').textContent = 'Vrstva Z = ' + z;
            currentLayer = z;
        }

        function nextLayer() {
            if (currentLayer < maxLayer) {
                showLayer(currentLayer + 1);
            }
        }

        function prevLayer() {
            if (currentLayer > 0) {
                showLayer(currentLayer - 1);
            }
        }

        // Klávesnice
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
                nextLayer();
            } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                prevLayer();
            }
        });
    </script>
</body>
</html>
"""

    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

    return html
