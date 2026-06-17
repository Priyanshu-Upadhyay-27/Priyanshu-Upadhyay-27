import os
import random

# --- PIXEL ART BUILDER ---
# Helper function to perfectly center and pad our 53x7 grid
def build_grid(rows):
    grid = ["".ljust(53)] # Row 0 (Empty padding)
    for r in rows:
        grid.append(r.ljust(53)[:53])
    while len(grid) < 7:
        grid.append("".ljust(53))
    return grid

# --- THE 4 DESIGNS ---

DESIGN_P_BUILDS = {
    "type": "single",
    "grid": build_grid([
        "  XXXX          XXXX   X   X  XXX  X     XXX   XXXX",
        "  X   X         X   X  X   X   X   X     X  X  X",
        "  XXXX   XXX    XXXX   X   X   X   X     X  X  XXXX",
        "  X             X   X  X   X   X   X     X  X     X",
        "  X             XXXX    XXX   XXX  XXXX  XXX   XXXX"
    ])
}

DESIGN_MATH = {
    "type": "single",
    "grid": build_grid([
        "  X   X         X   X  X   X        X",
        "  X   X         X   X   X X         X",
        "   X X   XXXX   X X X    X     XX   XXXX",
        "    X           XX XX   X X    XX   X   X",
        "    X           X   X  X   X        X   X",
        "  XXX           X   X  X   X        XXXX"
    ])
}

DESIGN_INFINITY = {
    "type": "single",
    "grid": build_grid([
        "         XXXXX      XXXXX",
        "       XX     XX  XX     XX",
        "      XX        XX        XX",
        "       XX     XX  XX     XX",
        "         XXXXX      XXXXX"
    ])
}

DESIGN_ATTENTION = {
    "type": "multi",
    "phases": [
        build_grid([ # PHASE 1: ATTENTION
            "        X  XXX XXX XXX X  X XXX XXX  XX  X  X",
            "       X X  X   X  X   XX X  X   X  X  X XX X",
            "       XXX  X   X  XX  X XX  X   X  X  X X XX",
            "       X X  X   X  X   X  X  X   X  X  X X  X",
            "       X X  X   X  XXX X  X  X  XXX  XX  X  X"
        ]),
        build_grid([ # PHASE 2: IS ALL
            "                XXX  XX    X  X   X",
            "                 X  X     X X X   X",
            "                 X   X    XXX X   X",
            "                 X    X   X X X   X",
            "                XXX XX    X X XXX XXX"
        ]),
        build_grid([ # PHASE 3: YOU NEED
            "          X X  XX  X  X  X  X XXX XXX XX",
            "          X X X  X X  X  XX X X   X   X X",
            "           X  X  X X  X  X XX XX  XX  X  X",
            "           X  X  X X  X  X  X X   X   X X",
            "           X   XX   XX   X  X XXX XXX XX"
        ])
    ]
}

ROULETTE = [DESIGN_P_BUILDS, DESIGN_MATH, DESIGN_INFINITY, DESIGN_ATTENTION]

def generate_dynamic_svg():
    # 1. Randomly pick today's design
    active_design = random.choice(ROULETTE)
    
    # 2. Setup the SVG canvas and CSS Engine
    svg_parts = [
        '<svg width="820" height="150" xmlns="http://www.w3.org/2000/svg">',
        '<style>',
        '  .bg { fill: #0d1117; }',
        '  .dot { fill: #161b22; rx: 2; ry: 2; }',
        
        # CSS for Single-Phase Sweep
        '  .sweep { fill: #00ff88; rx: 2; ry: 2; opacity: 0; animation: sweepAnim 8s infinite; }',
        '  @keyframes sweepAnim {',
        '    0%, 10% { opacity: 0; }',
        '    15%, 85% { opacity: 1; }',
        '    95%, 100% { opacity: 0; }',
        '  }',
        
        # CSS for Multi-Phase Fade (Attention Is All You Need)
        '  .phase1 { fill: #00ff88; rx: 2; ry: 2; opacity: 0; animation: p1 12s infinite; }',
        '  .phase2 { fill: #00ff88; rx: 2; ry: 2; opacity: 0; animation: p2 12s infinite; }',
        '  .phase3 { fill: #00ff88; rx: 2; ry: 2; opacity: 0; animation: p3 12s infinite; }',
        
        '  @keyframes p1 { 0%, 5%{opacity:0} 10%, 25%{opacity:1} 30%, 100%{opacity:0} }',
        '  @keyframes p2 { 0%, 35%{opacity:0} 40%, 55%{opacity:1} 60%, 100%{opacity:0} }',
        '  @keyframes p3 { 0%, 65%{opacity:0} 70%, 85%{opacity:1} 90%, 100%{opacity:0} }',
        
        # CSS for Continuous Snake Context
        '  .snake { fill: #00d4ff; rx: 2; ry: 2; animation: slither 6s infinite linear; opacity: 0.6; }',
        '  @keyframes slither {',
        '    0% { transform: translate(0px, 0px); }',
        '    25% { transform: translate(600px, 50px); }',
        '    50% { transform: translate(800px, 10px); }',
        '    75% { transform: translate(200px, 100px); }',
        '    100% { transform: translate(0px, 0px); }',
        '  }',
        '</style>',
        '<rect width="100%" height="100%" class="bg" rx="6"/>'
    ]
    
    # 3. Generate the 53x7 Grid layout
    grid_width = 53
    grid_height = 7
    box_size = 12
    gap = 3
    padding_x = 20
    padding_y = 20
    
    for row in range(grid_height):
        for col in range(grid_width):
            x = padding_x + col * (box_size + gap)
            y = padding_y + row * (box_size + gap)
            
            # Draw standard background dot
            svg_parts.append(f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" class="dot"/>')
            
            # Overlay active glowing dots based on design type
            if active_design["type"] == "single":
                if col < len(active_design["grid"][row]) and active_design["grid"][row][col] == 'X':
                    delay = col * 0.08  # Left to right sweep
                    svg_parts.append(f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" class="sweep" style="animation-delay: {delay}s;"/>')
            
            elif active_design["type"] == "multi":
                if col < len(active_design["phases"][0][row]) and active_design["phases"][0][row][col] == 'X':
                    svg_parts.append(f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" class="phase1"/>')
                if col < len(active_design["phases"][1][row]) and active_design["phases"][1][row][col] == 'X':
                    svg_parts.append(f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" class="phase2"/>')
                if col < len(active_design["phases"][2][row]) and active_design["phases"][2][row][col] == 'X':
                    svg_parts.append(f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" class="phase3"/>')
                
    # 4. Add the slithering context snake
    svg_parts.append('<rect x="20" y="20" width="12" height="12" class="snake"/>')
    svg_parts.append('<rect x="50" y="60" width="12" height="12" class="snake" style="animation-delay: -1s; fill: #00ff88;"/>')
    
    svg_parts.append('</svg>')
    
    # 5. Write to file
    with open("mlops-pipeline.svg", "w") as f:
        f.write("\n".join(svg_parts))

if __name__ == "__main__":
    generate_dynamic_svg()
    print("Multi-Phase Roulette SVG Generated Successfully!")
