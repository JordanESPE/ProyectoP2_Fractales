"""
Módulo Principal de Fractales
Aplicación completa de generación y visualización de fractales
"""

from .generators import (
    PaletteGenerator,
    FractalGenerator, 
    MandelbrotGenerator,
    JuliaGenerator,
    KochGenerator
)

from .interfaces import (
    SimpleFractalMenu
)

from .utils import (
    config,
    performance_monitor,
    setup_project_path,
    ensure_directories
)

# Configurar el entorno al importar
setup_project_path()
ensure_directories()

__all__ = [
    # Generadores
    'PaletteGenerator',
    'FractalGenerator',
    'MandelbrotGenerator', 
    'JuliaGenerator',
    'KochGenerator',
    # Interfaces
    'SimpleFractalMenu',
    # Utilidades
    'config',
    'performance_monitor',
    'setup_project_path',
    'ensure_directories'
]

__version__ = "1.0.0"
__author__ = "Fractales Infinitos"
__description__ = "Aplicación completa de generación y visualización de fractales"
