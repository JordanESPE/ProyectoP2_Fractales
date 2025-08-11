#!/usr/bin/env python3
"""
Script para encontrar definiciones de SierpinskiMainWindow
"""

def find_sierpinski_classes():
    """Busca todas las definiciones de SierpinskiMainWindow"""
    
    file_path = r"c:\Users\Jordan Guaman\OneDrive\Desktop\Intento final de Proyecto\fractales\interfaces\ventanas_fractales.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    sierpinski_lines = []
    
    for i, line in enumerate(lines):
        if 'class SierpinskiMainWindow' in line:
            sierpinski_lines.append((i+1, line.strip()))
            # Mostrar contexto alrededor
            start = max(0, i-3)
            end = min(len(lines), i+10)
            
            print(f"\n=== ENCONTRADA EN LÍNEA {i+1} ===")
            for j in range(start, end):
                marker = ">>> " if j == i else "    "
                print(f"{marker}{j+1:4d}: {lines[j].rstrip()}")
    
    print(f"\nTotal de definiciones encontradas: {len(sierpinski_lines)}")
    return sierpinski_lines

if __name__ == "__main__":
    find_sierpinski_classes()
