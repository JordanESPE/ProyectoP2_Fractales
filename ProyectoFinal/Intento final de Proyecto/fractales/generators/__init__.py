"""
Módulo de Generadores de Fractales
Contiene todos los algoritmos de generación consolidados
"""

from .fractal_generators import (
    PaletteGenerator,
    FractalGenerator,
    MandelbrotGenerator,
    JuliaGenerator,
    KochGenerator
)

__all__ = [
    'PaletteGenerator',
    'FractalGenerator', 
    'MandelbrotGenerator',
    'JuliaGenerator',
    'KochGenerator'
]
