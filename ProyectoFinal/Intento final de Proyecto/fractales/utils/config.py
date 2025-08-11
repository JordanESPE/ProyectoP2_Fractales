"""
Utilidades y Configuraciones para Fractales
Módulo consolidado de configuraciones y utilidades comunes
"""

import os
import sys
from pathlib import Path

# Configuraciones por defecto
DEFAULT_ZOOM = 1.0
DEFAULT_OFFSET_X = 0.0
DEFAULT_OFFSET_Y = 0.0
DEFAULT_MAX_ITER = 100
DEFAULT_AURA_INTENSITY = 1.0
THREADS_PER_BLOCK = (16, 16)

# Configuraciones de ventana
DEFAULT_WINDOW_WIDTH = 800
DEFAULT_WINDOW_HEIGHT = 600
DEFAULT_CANVAS_WIDTH = 600
DEFAULT_CANVAS_HEIGHT = 400

# Configuraciones de renderizado
MAX_POINTS = 500000
GENERATION_TIMEOUT = 20.0
MAX_CALCULATION_TIME = 15.0

# Colores por defecto
DEFAULT_BACKGROUND = (0, 0, 0)
DEFAULT_FOREGROUND = (255, 255, 255)

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).parent.parent.parent
CACHE_DIR = PROJECT_ROOT / "cache"
EXPORTS_DIR = PROJECT_ROOT / "exports"

def ensure_directories():
    """Asegura que existan los directorios necesarios."""
    CACHE_DIR.mkdir(exist_ok=True)
    EXPORTS_DIR.mkdir(exist_ok=True)

def get_project_root():
    """Obtiene la ruta raíz del proyecto."""
    return PROJECT_ROOT

def setup_project_path():
    """Configura el path del proyecto para importaciones."""
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

class FractalConfig:
    """Configuración centralizada para fractales."""
    
    def __init__(self):
        self.zoom = DEFAULT_ZOOM
        self.offset_x = DEFAULT_OFFSET_X
        self.offset_y = DEFAULT_OFFSET_Y
        self.max_iter = DEFAULT_MAX_ITER
        self.aura_intensity = DEFAULT_AURA_INTENSITY
        self.color_scheme = 2
        self.background_color = DEFAULT_BACKGROUND
        
        # Asegurar directorios
        ensure_directories()
    
    def reset_to_defaults(self):
        """Resetea la configuración a valores por defecto."""
        self.__init__()
    
    def get_window_geometry(self):
        """Obtiene la geometría por defecto de ventana."""
        return (100, 100, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
    
    def get_canvas_size(self):
        """Obtiene el tamaño por defecto del canvas."""
        return (DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT)

class PerformanceMonitor:
    """Monitor de rendimiento para fractales."""
    
    def __init__(self):
        self.generation_times = []
        self.point_counts = []
        self.error_counts = 0
    
    def record_generation(self, time_taken, point_count):
        """Registra una generación."""
        self.generation_times.append(time_taken)
        self.point_counts.append(point_count)
        
        # Mantener solo las últimas 100 generaciones
        if len(self.generation_times) > 100:
            self.generation_times.pop(0)
            self.point_counts.pop(0)
    
    def record_error(self):
        """Registra un error."""
        self.error_counts += 1
    
    def get_average_time(self):
        """Obtiene el tiempo promedio de generación."""
        if not self.generation_times:
            return 0.0
        return sum(self.generation_times) / len(self.generation_times)
    
    def get_performance_stats(self):
        """Obtiene estadísticas de rendimiento."""
        return {
            'avg_time': self.get_average_time(),
            'total_generations': len(self.generation_times),
            'error_count': self.error_counts,
            'last_point_count': self.point_counts[-1] if self.point_counts else 0
        }

# Instancia global de configuración
config = FractalConfig()
performance_monitor = PerformanceMonitor()

# Funciones de utilidad globales
def clamp(value, min_val, max_val):
    """Limita un valor entre un mínimo y máximo."""
    return max(min_val, min(max_val, value))

def safe_divide(a, b, default=0.0):
    """División segura que evita división por cero."""
    try:
        return a / b if b != 0 else default
    except (ZeroDivisionError, TypeError):
        return default

def validate_numeric_input(value, min_val=None, max_val=None, default=0.0):
    """Valida entrada numérica con límites opcionales."""
    try:
        num_value = float(value)
        if min_val is not None and num_value < min_val:
            return min_val
        if max_val is not None and num_value > max_val:
            return max_val
        return num_value
    except (ValueError, TypeError):
        return default

def format_time(seconds):
    """Formatea tiempo en segundos a formato legible."""
    if seconds < 1:
        return f"{seconds*1000:.1f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes}m {seconds:.1f}s"

def format_number(number):
    """Formatea números grandes con separadores."""
    if isinstance(number, (int, float)):
        if number >= 1_000_000:
            return f"{number/1_000_000:.1f}M"
        elif number >= 1_000:
            return f"{number/1_000:.1f}K"
        else:
            return str(int(number))
    return str(number)
