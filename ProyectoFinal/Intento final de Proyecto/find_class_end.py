#!/usr/bin/env python3
"""
Script para encontrar dónde termina la clase SierpinskiMainWindow básica
"""

def find_class_end():
    """Busca dónde termina la clase SierpinskiMainWindow"""
    
    file_path = r"c:\Users\Jordan Guaman\OneDrive\Desktop\Intento final de Proyecto\fractales\interfaces\ventanas_fractales.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    sierpinski_start = None
    sierpinski_end = None
    
    for i, line in enumerate(lines):
        if 'class SierpinskiMainWindow' in line:
            sierpinski_start = i
            print(f"Inicio de SierpinskiMainWindow: línea {i+1}")
        elif sierpinski_start is not None and line.strip() and not line.startswith(' ') and not line.startswith('\t'):
            # Nueva definición al nivel de clase
            if line.strip().startswith('class ') or line.strip().startswith('def ') or line.strip().startswith('import '):
                sierpinski_end = i
                print(f"Final de SierpinskiMainWindow: línea {i}")
                break
    
    if sierpinski_start is not None:
        if sierpinski_end is None:
            sierpinski_end = len(lines)
            print(f"Final de SierpinskiMainWindow: final del archivo (línea {len(lines)})")
        
        print(f"\nLa clase SierpinskiMainWindow va desde la línea {sierpinski_start+1} hasta la línea {sierpinski_end}")
        
        # Mostrar las últimas líneas de la clase
        print("\nÚltimas líneas de la clase:")
        start_show = max(sierpinski_end-10, sierpinski_start)
        for i in range(start_show, sierpinski_end):
            print(f"{i+1:4d}: {lines[i].rstrip()}")
    
    return sierpinski_start, sierpinski_end

if __name__ == "__main__":
    find_class_end()
