"""
Módulo de Interfaces de Usuario para Fractales
Contiene todas las ventanas y controles de la aplicación
"""

# Solo importar el menú principal para evitar importaciones circulares
from .menu_principal import SimpleFractalMenu

__all__ = [
    'SimpleFractalMenu'
]
