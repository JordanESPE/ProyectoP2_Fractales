"""
Fractales - Aplicación Principal
Launcher principal de la aplicación modular de fractales
"""

import sys
from PyQt6.QtWidgets import QApplication

# Importar desde la estructura modular
from fractales import SimpleFractalMenu, setup_project_path
from fractales.utils import config


def main():
    """Función principal de la aplicación."""
    # Configurar el entorno
    setup_project_path()
    
    print("🎯 FRACTALES - Aplicación Modular")
    print("Estructura organizada y optimizada")
    print("Selecciona el fractal que quieras explorar...")
    
    # Crear la aplicación
    app = QApplication(sys.argv)
    
    # Configurar aplicación
    app.setApplicationName("Fractales")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Fractales Infinitos")
    app.setStyle('Fusion')
    
    # Crear y mostrar el menú principal
    menu = SimpleFractalMenu()
    
    # Aplicar geometría por defecto
    geometry = config.get_window_geometry()
    menu.setGeometry(*geometry)
    
    menu.show()
    
    # Ejecutar la aplicación
    return app.exec()


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"Error crítico: {e}")
        sys.exit(1)
