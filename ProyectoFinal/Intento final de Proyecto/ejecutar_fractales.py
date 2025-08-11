"""
Lanzador del Programa de Fractales
Script directo para ejecutar la aplicación con Sierpinski Ultra-Fluido integrado
"""

import sys
import os
from PyQt6.QtWidgets import QApplication

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Lanza la aplicación de fractales."""
    print("🎯 FRACTALES - Aplicación con Sierpinski Ultra-Fluido")
    print("🔺 Sierpinski integrado con zoom infinito y navegación ultra-fluida")
    print("✨ Haz clic en 'Sierpinski' para acceder al fractal optimizado")
    
    try:
        from fractales.interfaces.menu_principal import SimpleFractalMenu
        
        app = QApplication(sys.argv)
        app.setApplicationName("Fractales - Sierpinski Ultra-Fluido")
        app.setStyle('Fusion')
        
        # Crear y mostrar el menú principal
        menu = SimpleFractalMenu()
        menu.show()
        
        # Ejecutar la aplicación
        return app.exec()
        
    except Exception as e:
        print(f"❌ Error al lanzar la aplicación: {e}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")
        sys.exit(0)
