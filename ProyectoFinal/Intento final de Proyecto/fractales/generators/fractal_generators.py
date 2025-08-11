"""
Generadores de Fractales Consolidados
Todos los algoritmos de generación en un solo módulo
Con aceleración CUDA para máximo rendimiento
"""

import numpy as np
import math
import time
import colorsys
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count

try:
    from numba import cuda
    CUDA_AVAILABLE = True
    print("✅ CUDA disponible - Aceleración GPU activada")
except ImportError:
    CUDA_AVAILABLE = False
    print("⚠️ CUDA no disponible - Usando CPU")

# Kernels CUDA para Mandelbrot y Julia
if CUDA_AVAILABLE:
    @cuda.jit
    def mandelbrot_kernel_with_aura(image, width, height, zoom, offset_x, offset_y, max_iter, palette, palette_size, color_mode, aura_intensity, rotation):
        x, y = cuda.grid(2)
        if x >= width or y >= height:
            return

        real = (x - width / 2.0) / zoom + offset_x
        imag = (y - height / 2.0) / zoom + offset_y
        
        # Aplicar rotación
        if rotation != 0.0:
            cos_r = math.cos(rotation)
            sin_r = math.sin(rotation)
            real_rot = real * cos_r - imag * sin_r
            imag_rot = real * sin_r + imag * cos_r
            real, imag = real_rot, imag_rot
        
        c_real, c_imag = real, imag

        z_real, z_imag = 0.0, 0.0
        iter_count = 0
        z_mag_squared = 0.0

        while iter_count < max_iter and (z_real * z_real + z_imag * z_imag) < 4.0:
            temp = z_real * z_real - z_imag * z_imag + c_real
            z_imag = 2.0 * z_real * z_imag + c_imag
            z_real = temp
            iter_count += 1
            z_mag_squared = z_real * z_real + z_imag * z_imag

        if iter_count == max_iter:
            image[y, x, 0] = 0
            image[y, x, 1] = 0
            image[y, x, 2] = 0
            return
            
        smooth_value = iter_count
        if iter_count < max_iter:
            smooth_value = iter_count + 1.0 - min(1.0, z_mag_squared / 4.0)
            
        aura_factor = 0.0
        if z_mag_squared > 0.0:
            edge_proximity = min(1.0, z_mag_squared / 4.0) 
            aura_factor = edge_proximity * aura_intensity
        
        if color_mode == 0:  
            color_index = int(iter_count % palette_size)
            r = palette[color_index][0]
            g = palette[color_index][1]
            b = palette[color_index][2]
            
            r = min(255, int(r + (255 - r) * aura_factor))
            g = min(255, int(g + (255 - g) * aura_factor))
            b = min(255, int(b + (255 - b) * aura_factor))
        else:  
            t = smooth_value / max_iter
            index_float = t * (palette_size - 1)
            index = int(index_float)
            t_interp = index_float - index
            
            if index < palette_size - 1:
                r = int(palette[index][0] * (1.0 - t_interp) + palette[index + 1][0] * t_interp)
                g = int(palette[index][1] * (1.0 - t_interp) + palette[index + 1][1] * t_interp)
                b = int(palette[index][2] * (1.0 - t_interp) + palette[index + 1][2] * t_interp)
            else:
                r = palette[index][0]
                g = palette[index][1]
                b = palette[index][2]
                
            r = min(255, int(r * (1.0 + aura_factor * 0.7)))
            g = min(255, int(g * (1.0 + aura_factor * 0.7)))
            b = min(255, int(b * (1.0 + aura_factor * 0.7)))
        
        image[y, x, 0] = r
        image[y, x, 1] = g
        image[y, x, 2] = b

    @cuda.jit
    def julia_kernel_with_aura(image, width, height, zoom, offset_x, offset_y, max_iter, palette, palette_size, color_mode, aura_intensity, rotation, c_real, c_imag):
        x, y = cuda.grid(2)
        if x >= width or y >= height:
            return

        real = (x - width / 2.0) / zoom + offset_x
        imag = (y - height / 2.0) / zoom + offset_y
        
        # Aplicar rotación
        if rotation != 0.0:
            cos_r = math.cos(rotation)
            sin_r = math.sin(rotation)
            real_rot = real * cos_r - imag * sin_r
            imag_rot = real * sin_r + imag * cos_r
            real, imag = real_rot, imag_rot

        z_real, z_imag = real, imag
        iter_count = 0
        z_mag_squared = 0.0

        while iter_count < max_iter and (z_real * z_real + z_imag * z_imag) < 4.0:
            temp = z_real * z_real - z_imag * z_imag + c_real
            z_imag = 2.0 * z_real * z_imag + c_imag
            z_real = temp
            iter_count += 1
            z_mag_squared = z_real * z_real + z_imag * z_imag

        if iter_count == max_iter:
            image[y, x, 0] = 0
            image[y, x, 1] = 0
            image[y, x, 2] = 0
            return
            
        smooth_value = iter_count
        if iter_count < max_iter:
            smooth_value = iter_count + 1.0 - min(1.0, z_mag_squared / 4.0)
            
        aura_factor = 0.0
        if z_mag_squared > 0.0:
            edge_proximity = min(1.0, z_mag_squared / 4.0) 
            aura_factor = edge_proximity * aura_intensity
        
        if color_mode == 0:  
            color_index = int(iter_count % palette_size)
            r = palette[color_index][0]
            g = palette[color_index][1]
            b = palette[color_index][2]
            
            r = min(255, int(r + (255 - r) * aura_factor))
            g = min(255, int(g + (255 - g) * aura_factor))
            b = min(255, int(b + (255 - b) * aura_factor))
        else:  
            t = smooth_value / max_iter
            index_float = t * (palette_size - 1)
            index = int(index_float)
            t_interp = index_float - index
            
            if index < palette_size - 1:
                r = int(palette[index][0] * (1.0 - t_interp) + palette[index + 1][0] * t_interp)
                g = int(palette[index][1] * (1.0 - t_interp) + palette[index + 1][1] * t_interp)
                b = int(palette[index][2] * (1.0 - t_interp) + palette[index + 1][2] * t_interp)
            else:
                r = palette[index][0]
                g = palette[index][1]
                b = palette[index][2]
                
            r = min(255, int(r * (1.0 + aura_factor * 0.7)))
            g = min(255, int(g * (1.0 + aura_factor * 0.7)))
            b = min(255, int(b * (1.0 + aura_factor * 0.7)))
        
        image[y, x, 0] = r
        image[y, x, 1] = g
        image[y, x, 2] = b


class PaletteGenerator:
    """Generador de paletas de colores para fractales."""
    
    def __init__(self):
        self.palette_size = 256
        self.palettes = {}
        self._create_all_palettes()
    
    def _create_all_palettes(self):
        """Crea todas las paletas disponibles."""
        self.palettes[0] = self._create_fire_palette()      # Fuego
        self.palettes[1] = self._create_ocean_palette()     # Océano
        self.palettes[2] = self._create_rainbow_palette()   # Arcoíris
        self.palettes[3] = self._create_neon_palette()      # Neón
        self.palettes[4] = self._create_cosmic_palette()    # Cósmico
        self.palettes[5] = self._create_emerald_palette()   # Esmeralda
        self.palettes[6] = self._create_psychedelic_palette() # Psicodélico
    
    def _create_fire_palette(self):
        """Paleta de fuego."""
        colors = []
        for i in range(self.palette_size):
            t = i / (self.palette_size - 1)
            r = int(min(255, t * 3 * 255))
            g = int(min(255, t * t * 255))
            b = int(min(255, t * 0.5 * 100))
            colors.append((r, g, b))
        return colors
    
    def _create_ocean_palette(self):
        """Paleta oceánica."""
        colors = []
        for i in range(self.palette_size):
            t = i / (self.palette_size - 1)
            r = int(t * 0.3 * 100)
            g = int(t * 0.8 * 200)
            b = int(min(255, t * 255))
            colors.append((r, g, b))
        return colors
    
    def _create_rainbow_palette(self):
        """Paleta arcoíris."""
        colors = []
        for i in range(self.palette_size):
            h = i / (self.palette_size - 1)
            r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
            colors.append((int(r * 255), int(g * 255), int(b * 255)))
        return colors
    
    def _create_neon_palette(self):
        """Paleta neón."""
        colors = []
        for i in range(self.palette_size):
            t = i / (self.palette_size - 1)
            h = (t * 0.8 + 0.7) % 1.0
            r, g, b = colorsys.hsv_to_rgb(h, 0.9, 1.0)
            colors.append((int(r * 255), int(g * 255), int(b * 255)))
        return colors
    
    def _create_cosmic_palette(self):
        """Paleta cósmica."""
        colors = []
        for i in range(self.palette_size):
            t = i / (self.palette_size - 1)
            if t < 0.5:
                r = int(t * 2 * 255)
                g = int(t * 100)
                b = int(100 + t * 155)
            else:
                r = int(255)
                g = int(100 + (t - 0.5) * 2 * 155)
                b = int(255)
            colors.append((r, g, b))
        return colors
    
    def _create_emerald_palette(self):
        """Paleta esmeralda."""
        colors = []
        for i in range(self.palette_size):
            t = i / (self.palette_size - 1)
            r = int(t * 200)
            g = int(min(255, t * 2 * 255))
            b = int(t * 150)
            colors.append((r, g, b))
        return colors
    
    def _create_psychedelic_palette(self):
        """Paleta psicodélica."""
        colors = []
        for i in range(self.palette_size):
            t = i / (self.palette_size - 1)
            phase = 6 * t
            
            if phase < 1:
                r, g, b = 10, int(phase * 155), 0
            elif phase < 2:
                r, g, b = int((2 - phase) * 155), 225, 0
            elif phase < 3:
                r, g, b = 0, 255, int((phase - 2) * 225)
            elif phase < 4:
                r, g, b = 0, int((4 - phase) * 155), 225
            elif phase < 5:
                r, g, b = int((phase - 4) * 155), 0, 225
            else:
                r, g, b = 0, 0, int((6 - phase) * 225)
                
            colors.append((r, g, b))
        return colors
    
    def get_palette(self, scheme_index):
        """Obtiene una paleta por índice."""
        return self.palettes.get(scheme_index, self.palettes[0])
    
    def get_palette_names(self):
        """Obtiene los nombres de las paletas disponibles."""
        return [
            "Fuego", "Océano", "Arcoíris", "Neón", 
            "Cósmico", "Esmeralda", "Psicodélico"
        ]
    
    def get_palette_as_array(self, scheme_index):
        """Obtiene una paleta como array NumPy."""
        palette = self.get_palette(scheme_index)
        return np.array(palette, dtype=np.uint8)
    
    def _create_classic_palette(self):
        """Paleta clásica azul-blanco."""
        colors = []
        for i in range(256):
            t = i / 255.0
            r = int(t * 255)
            g = int(t * 255)
            b = 255
            colors.append((r, g, b))
        return colors
    
    def _create_fire_palette(self):
        """Paleta de fuego."""
        colors = []
        for i in range(256):
            t = i / 255.0
            if t < 0.5:
                r = int(255 * (t * 2))
                g = int(128 * (t * 2))
                b = 0
            else:
                r = 255
                g = int(128 + 127 * ((t - 0.5) * 2))
                b = int(255 * ((t - 0.5) * 2))
            colors.append((r, g, b))
        return colors
    
    def _create_rainbow_palette(self):
        """Paleta arcoíris."""
        colors = []
        for i in range(256):
            t = i / 255.0 * 6
            if t < 1:
                r, g, b = 255, int(255 * t), 0
            elif t < 2:
                r, g, b = int(255 * (2 - t)), 255, 0
            elif t < 3:
                r, g, b = 0, 255, int(255 * (t - 2))
            elif t < 4:
                r, g, b = 0, int(255 * (4 - t)), 255
            elif t < 5:
                r, g, b = int(255 * (t - 4)), 0, 255
            else:
                r, g, b = 255, 0, int(255 * (6 - t))
            colors.append((r, g, b))
        return colors
    
    def _create_ocean_palette(self):
        """Paleta océano."""
        colors = []
        for i in range(256):
            t = i / 255.0
            r = int(30 * t)
            g = int(100 + 155 * t)
            b = int(150 + 105 * t)
            colors.append((r, g, b))
        return colors
    
    def _create_forest_palette(self):
        """Paleta bosque."""
        colors = []
        for i in range(256):
            t = i / 255.0
            r = int(34 + 100 * t)
            g = int(139 + 116 * t)
            b = int(34 + 100 * t)
            colors.append((r, g, b))
        return colors
    
    def _create_sunset_palette(self):
        """Paleta atardecer."""
        colors = []
        for i in range(256):
            t = i / 255.0
            r = int(255 * (0.8 + 0.2 * t))
            g = int(140 + 115 * t)
            b = int(60 * (1 - t))
            colors.append((r, g, b))
        return colors
    
    def _create_neon_palette(self):
        """Paleta neón."""
        colors = []
        for i in range(256):
            t = i / 255.0
            r = int(255 * abs(math.sin(t * math.pi * 3)))
            g = int(255 * abs(math.sin(t * math.pi * 3 + math.pi/3)))
            b = int(255 * abs(math.sin(t * math.pi * 3 + 2*math.pi/3)))
            colors.append((r, g, b))
        return colors
    
    def get_palette(self, scheme_index):
        """Obtiene una paleta por índice."""
        return self.palettes.get(scheme_index, self.palettes[0])
    
    def get_palette_as_array(self, scheme_index):
        """Obtiene una paleta como array NumPy."""
        palette = self.get_palette(scheme_index)
        return np.array(palette, dtype=np.uint8)


class FractalGenerator:
    """Generador base para todos los fractales."""
    
    def __init__(self):
        # Parámetros comunes
        self.zoom = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.rotation = 0.0
        self.iterations = 4
        self.line_width = 1.0
        
        # Sistema de colores
        self.color_scheme = 2
        self.gradient_mode = True
        self.background_color = (0, 0, 0)
        self.palette_generator = PaletteGenerator()
        self.current_palette = None
        self._update_palette()
        
        # Sistema de rendimiento
        self._max_calculation_time = 15.0
        self._start_time = None
        self._point_count = 0
        self._max_points = 500000
        self._generation_timeout = 20.0
        
        # Pool de hilos
        max_workers = max(8, cpu_count() * 2)
        self._thread_pool = ThreadPoolExecutor(max_workers=max_workers)
    
    def _update_palette(self):
        """Actualiza la paleta actual."""
        self.current_palette = self.palette_generator.get_palette(self.color_scheme)
    
    def set_zoom(self, zoom):
        """Establece el zoom."""
        self.zoom = max(0.01, min(1000000, zoom))
    
    def set_offset(self, offset_x, offset_y):
        """Establece el desplazamiento."""
        max_offset = 10.0
        self.offset_x = max(-max_offset, min(max_offset, offset_x))
        self.offset_y = max(-max_offset, min(max_offset, offset_y))
    
    def set_iterations(self, iterations):
        """Establece las iteraciones."""
        self.iterations = max(0, min(20, iterations))
    
    def set_color_scheme(self, scheme_index):
        """Cambia el esquema de colores."""
        if scheme_index != self.color_scheme:
            self.color_scheme = scheme_index
            self._update_palette()
    
    def zoom_in(self, factor=1.5):
        """Aumenta el zoom."""
        self.zoom *= factor
    
    def zoom_out(self, factor=1.5):
        """Disminuye el zoom."""
        self.zoom /= factor
    
    def move(self, delta_x, delta_y):
        """Mueve la vista."""
        self.offset_x += delta_x
        self.offset_y += delta_y


class MandelbrotGenerator(FractalGenerator):
    """Generador del conjunto de Mandelbrot con aceleración CUDA."""
    
    def __init__(self):
        super().__init__()
        self.max_iter = 200
        self.aura_intensity = 1.0
        self.color_mode = 1  # 0: Simple, 1: Interpolación suave
        self.zoom = 300.0
        self.offset_x = -0.5
        self.offset_y = 0.0
        self.rotation = 0.0
        self.palette_generator = PaletteGenerator()
        self.current_palette = self.palette_generator.get_palette(0)
        self.current_palette_index = 0
    
    def set_max_iterations(self, max_iter):
        """Establece las iteraciones máximas."""
        self.max_iter = max(1, min(5000, max_iter))
    
    def set_aura_intensity(self, intensity):
        """Establece la intensidad del aura."""
        self.aura_intensity = max(0.0, min(5.0, intensity))
    
    def set_color_scheme(self, scheme_index):
        """Cambia el esquema de colores."""
        self.current_palette_index = scheme_index
        self.current_palette = self.palette_generator.get_palette(scheme_index)
    
    def set_color_mode(self, mode):
        """Establece el modo de color."""
        self.color_mode = mode
    
    def set_zoom(self, zoom):
        """Establece el zoom."""
        self.zoom = max(1.0, zoom)
    
    def set_offset(self, offset_x, offset_y):
        """Establece el offset."""
        self.offset_x = offset_x
        self.offset_y = offset_y
    
    def set_rotation(self, rotation):
        """Establece la rotación."""
        self.rotation = rotation
    
    def zoom_in(self, factor=1.5):
        """Aumenta el zoom."""
        self.zoom *= factor
    
    def zoom_out(self, factor=1.5):
        """Disminuye el zoom."""
        self.zoom /= factor
    
    def move(self, delta_x, delta_y):
        """Mueve la vista."""
        self.offset_x -= delta_x / self.zoom
        self.offset_y -= delta_y / self.zoom
    
    def generate_fractal(self, width, height, zoom=None, offset_x=None, offset_y=None):
        """Genera el fractal de Mandelbrot usando CUDA si está disponible."""
        if zoom is None:
            zoom = self.zoom
        if offset_x is None:
            offset_x = self.offset_x
        if offset_y is None:
            offset_y = self.offset_y

        if CUDA_AVAILABLE:
            return self._generate_with_cuda(width, height, zoom, offset_x, offset_y)
        else:
            return self._generate_with_cpu(width, height, zoom, offset_x, offset_y)
    
    def _generate_with_cuda(self, width, height, zoom, offset_x, offset_y):
        """Genera usando CUDA."""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        d_image = cuda.to_device(image)
        
        palette_array = np.array(self.current_palette, dtype=np.uint8)
        d_palette = cuda.to_device(palette_array)

        threads_per_block = (16, 16)
        blocks_per_grid_x = (width + threads_per_block[0] - 1) // threads_per_block[0]
        blocks_per_grid_y = (height + threads_per_block[1] - 1) // threads_per_block[1]
        blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

        mandelbrot_kernel_with_aura[blocks_per_grid, threads_per_block](
            d_image, width, height, zoom, offset_x, offset_y, self.max_iter, 
            d_palette, len(self.current_palette), self.color_mode, 
            self.aura_intensity, self.rotation
        )

        image = d_image.copy_to_host()
        return image
    
    def _generate_with_cpu(self, width, height, zoom, offset_x, offset_y):
        """Genera usando CPU como fallback."""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        for py in range(height):
            for px in range(width):
                real = (px - width / 2.0) / zoom + offset_x
                imag = (py - height / 2.0) / zoom + offset_y
                
                # Aplicar rotación
                if self.rotation != 0.0:
                    cos_r = math.cos(self.rotation)
                    sin_r = math.sin(self.rotation)
                    real_rot = real * cos_r - imag * sin_r
                    imag_rot = real * sin_r + imag * cos_r
                    real, imag = real_rot, imag_rot
                
                c = complex(real, imag)
                z = 0
                iterations = 0
                
                while abs(z) <= 2 and iterations < self.max_iter:
                    z = z * z + c
                    iterations += 1
                
                if iterations == self.max_iter:
                    color = (0, 0, 0)
                else:
                    # Usar paleta
                    if self.color_mode == 0:  # Simple
                        color_index = iterations % len(self.current_palette)
                        color = self.current_palette[color_index]
                    else:  # Interpolación suave
                        t = iterations / self.max_iter
                        index = int(t * (len(self.current_palette) - 1))
                        color = self.current_palette[min(index, len(self.current_palette) - 1)]
                
                image[py, px] = color
        
        return image
    
    def generate(self, width, height, xmin, xmax, ymin, ymax, max_iter):
        """Método de compatibilidad para generar con parámetros específicos."""
        # Configurar temporalmente los parámetros
        old_max_iter = self.max_iter
        old_zoom = self.zoom
        old_offset_x = self.offset_x
        old_offset_y = self.offset_y
        
        self.max_iter = max_iter
        # Calcular zoom y offset basado en los límites
        center_x = (xmin + xmax) / 2
        center_y = (ymin + ymax) / 2
        range_x = xmax - xmin
        range_y = ymax - ymin
        
        self.offset_x = center_x
        self.offset_y = center_y
        self.zoom = min(width / range_x, height / range_y)
        
        # Generar
        result = self.generate_fractal(width, height)
        
        # Restaurar parámetros
        self.max_iter = old_max_iter
        self.zoom = old_zoom
        self.offset_x = old_offset_x
        self.offset_y = old_offset_y
        
        return result


class JuliaGenerator(FractalGenerator):
    """Generador del conjunto de Julia con aceleración CUDA."""
    
    def __init__(self):
        super().__init__()
        self.max_iter = 200
        self.aura_intensity = 1.0
        self.color_mode = 1  # 0: Simple, 1: Interpolación suave
        self.zoom = 300.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.rotation = 0.0
        self.c_real = -0.7
        self.c_imag = 0.27015
        self.palette_generator = PaletteGenerator()
        self.current_palette = self.palette_generator.get_palette(0)
        self.current_palette_index = 0
    
    def set_julia_constant(self, real, imag):
        """Establece la constante de Julia."""
        self.c_real = real
        self.c_imag = imag
    
    def set_max_iterations(self, max_iter):
        """Establece las iteraciones máximas."""
        self.max_iter = max(1, min(5000, max_iter))
    
    def set_aura_intensity(self, intensity):
        """Establece la intensidad del aura."""
        self.aura_intensity = max(0.0, min(5.0, intensity))
    
    def set_color_scheme(self, scheme_index):
        """Cambia el esquema de colores."""
        self.current_palette_index = scheme_index
        self.current_palette = self.palette_generator.get_palette(scheme_index)
    
    def set_color_mode(self, mode):
        """Establece el modo de color."""
        self.color_mode = mode
    
    def set_zoom(self, zoom):
        """Establece el zoom."""
        self.zoom = max(1.0, zoom)
    
    def set_offset(self, offset_x, offset_y):
        """Establece el offset."""
        self.offset_x = offset_x
        self.offset_y = offset_y
    
    def set_rotation(self, rotation):
        """Establece la rotación."""
        self.rotation = rotation
    
    def zoom_in(self, factor=1.5):
        """Aumenta el zoom."""
        self.zoom *= factor
    
    def zoom_out(self, factor=1.5):
        """Disminuye el zoom."""
        self.zoom /= factor
    
    def move(self, delta_x, delta_y):
        """Mueve la vista."""
        self.offset_x -= delta_x / self.zoom
        self.offset_y -= delta_y / self.zoom
    
    def generate_fractal(self, width, height, zoom=None, offset_x=None, offset_y=None):
        """Genera el fractal de Julia usando CUDA si está disponible."""
        if zoom is None:
            zoom = self.zoom
        if offset_x is None:
            offset_x = self.offset_x
        if offset_y is None:
            offset_y = self.offset_y

        if CUDA_AVAILABLE:
            return self._generate_with_cuda(width, height, zoom, offset_x, offset_y)
        else:
            return self._generate_with_cpu(width, height, zoom, offset_x, offset_y)
    
    def _generate_with_cuda(self, width, height, zoom, offset_x, offset_y):
        """Genera usando CUDA."""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        d_image = cuda.to_device(image)
        
        palette_array = np.array(self.current_palette, dtype=np.uint8)
        d_palette = cuda.to_device(palette_array)

        threads_per_block = (16, 16)
        blocks_per_grid_x = (width + threads_per_block[0] - 1) // threads_per_block[0]
        blocks_per_grid_y = (height + threads_per_block[1] - 1) // threads_per_block[1]
        blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

        julia_kernel_with_aura[blocks_per_grid, threads_per_block](
            d_image, width, height, zoom, offset_x, offset_y, self.max_iter, 
            d_palette, len(self.current_palette), self.color_mode, 
            self.aura_intensity, self.rotation, self.c_real, self.c_imag
        )

        image = d_image.copy_to_host()
        return image
    
    def _generate_with_cpu(self, width, height, zoom, offset_x, offset_y):
        """Genera usando CPU como fallback."""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        c = complex(self.c_real, self.c_imag)
        
        for py in range(height):
            for px in range(width):
                real = (px - width / 2.0) / zoom + offset_x
                imag = (py - height / 2.0) / zoom + offset_y
                
                # Aplicar rotación
                if self.rotation != 0.0:
                    cos_r = math.cos(self.rotation)
                    sin_r = math.sin(self.rotation)
                    real_rot = real * cos_r - imag * sin_r
                    imag_rot = real * sin_r + imag * cos_r
                    real, imag = real_rot, imag_rot
                
                z = complex(real, imag)
                iterations = 0
                
                while abs(z) <= 2 and iterations < self.max_iter:
                    z = z * z + c
                    iterations += 1
                
                if iterations == self.max_iter:
                    color = (0, 0, 0)
                else:
                    # Usar paleta
                    if self.color_mode == 0:  # Simple
                        color_index = iterations % len(self.current_palette)
                        color = self.current_palette[color_index]
                    else:  # Interpolación suave
                        t = iterations / self.max_iter
                        index = int(t * (len(self.current_palette) - 1))
                        color = self.current_palette[min(index, len(self.current_palette) - 1)]
                
                image[py, px] = color
        
        return image
    
    def generate_julia(self, width, height, xmin, xmax, ymin, ymax, max_iter, c_real, c_imag):
        """Método de compatibilidad para generar Julia con parámetros específicos."""
        # Configurar temporalmente los parámetros
        old_max_iter = self.max_iter
        old_zoom = self.zoom
        old_offset_x = self.offset_x
        old_offset_y = self.offset_y
        old_c_real = self.c_real
        old_c_imag = self.c_imag
        
        self.max_iter = max_iter
        self.c_real = c_real
        self.c_imag = c_imag
        
        # Calcular zoom y offset basado en los límites
        center_x = (xmin + xmax) / 2
        center_y = (ymin + ymax) / 2
        range_x = xmax - xmin
        range_y = ymax - ymin
        
        self.offset_x = center_x
        self.offset_y = center_y
        self.zoom = min(width / range_x, height / range_y)
        
        # Generar
        result = self.generate_fractal(width, height)
        
        # Restaurar parámetros
        self.max_iter = old_max_iter
        self.zoom = old_zoom
        self.offset_x = old_offset_x
        self.offset_y = old_offset_y
        self.c_real = old_c_real
        self.c_imag = old_c_imag
        
        return result


class KochGenerator(FractalGenerator):
    """Generador de curvas de Koch y fractales geométricos."""
    
    def __init__(self):
        super().__init__()
        self.koch_type = 0  # 0: Snowflake, 1: Line, 2: Square, 3: Triangle, 4: Dragon, 5: Tree, 6: Sierpinski
        self.angle_variation = 60.0
    
    def set_koch_type(self, koch_type):
        """Establece el tipo de curva de Koch."""
        self.koch_type = koch_type
    
    def get_koch_types(self):
        """Obtiene los tipos disponibles."""
        return [
            "Copo de Nieve",
            "Línea de Koch", 
            "Líneas Paralelas",
            "Triángulo de Koch",
            "Curva Dragón",
            "Árbol Fractal Recursivo",
            "Triángulo de Sierpinski"
        ]
    
    def generate_koch_curve(self, level):
        """Genera los puntos de la curva de Koch."""
        # Puntos iniciales (línea horizontal)
        points = [(0, 0), (300, 0)]
        
        for _ in range(level):
            new_points = []
            
            for i in range(len(points) - 1):
                p1 = points[i]
                p2 = points[i + 1]
                
                # Dividir la línea en tres partes
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                
                # Primer tercio
                a = (p1[0] + dx/3, p1[1] + dy/3)
                # Segundo tercio
                b = (p1[0] + 2*dx/3, p1[1] + 2*dy/3)
                
                # Punto del triángulo
                cx = (a[0] + b[0]) / 2 - (b[1] - a[1]) * math.sqrt(3) / 6
                cy = (a[1] + b[1]) / 2 + (b[0] - a[0]) * math.sqrt(3) / 6
                c = (cx, cy)
                
                # Agregar los nuevos puntos
                new_points.append(p1)
                new_points.append(a)
                new_points.append(c)
                new_points.append(b)
            
            new_points.append(points[-1])  # Último punto
            points = new_points
        
        return points
    
    def generate_fractal(self, width, height):
        """Genera el fractal según el tipo seleccionado."""
        image = np.full((height, width, 3), self.background_color, dtype=np.uint8)
        
        center_x = width // 2 + self.offset_x * width
        center_y = height // 2 + self.offset_y * height
        scale = min(width, height) * 0.3 * self.zoom
        
        try:
            if self.koch_type == 0:  # Copo de Nieve
                points = self._generate_snowflake((center_x, center_y), scale, self.iterations)
                if points:
                    self._draw_polygon(image, points, width, height)
            
            elif self.koch_type == 6:  # Sierpinski
                triangles = self._generate_sierpinski_triangle((center_x, center_y), scale, self.iterations)
                if triangles:
                    self._draw_sierpinski_triangles(image, triangles, width, height)
            
            # Agregar otros tipos según sea necesario...
            
        except Exception:
            # En caso de error, dibujar punto central
            if 0 <= center_x < width and 0 <= center_y < height:
                image[int(center_y), int(center_x)] = (255, 255, 255)
        
        return image
    
    def _generate_snowflake(self, center, radius, iterations):
        """Genera un copo de nieve de Koch."""
        # Implementación simplificada
        angles = [math.pi/2, math.pi/2 + 2*math.pi/3, math.pi/2 + 4*math.pi/3]
        vertices = []
        
        for angle in angles:
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            vertices.append((x, y))
        
        return vertices + [vertices[0]]  # Cerrar la figura
    
    def _generate_sierpinski_triangle(self, center, size, iterations):
        """Genera el Triángulo de Sierpinski."""
        if iterations <= 0:
            vertices = self._create_triangle_vertices(center, size)
            return [vertices + [vertices[0]]]
        
        def sierpinski_recursive(vertices, depth):
            if depth <= 0:
                return [vertices + [vertices[0]]]
            
            triangles = []
            p1, p2, p3 = vertices
            
            # Calcular puntos medios
            mid1 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
            mid2 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
            mid3 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
            
            # Generar 3 triángulos externos
            triangles.extend(sierpinski_recursive([p1, mid1, mid3], depth - 1))
            triangles.extend(sierpinski_recursive([mid1, p2, mid2], depth - 1))
            triangles.extend(sierpinski_recursive([mid3, mid2, p3], depth - 1))
            
            return triangles
        
        initial_vertices = self._create_triangle_vertices(center, size)
        return sierpinski_recursive(initial_vertices, iterations)
    
    def _create_triangle_vertices(self, center, size):
        """Crea vértices de triángulo equilátero."""
        angles = [math.pi/2, math.pi/2 + 2*math.pi/3, math.pi/2 + 4*math.pi/3]
        vertices = []
        
        for angle in angles:
            x = center[0] + size * math.cos(angle)
            y = center[1] + size * math.sin(angle)
            vertices.append((x, y))
        
        return vertices
    
    def _draw_polygon(self, image, points, width, height):
        """Dibuja un polígono."""
        if len(points) < 2:
            return
        
        for i in range(len(points) - 1):
            self._draw_line(image, points[i], points[i + 1], width, height)
    
    def _draw_sierpinski_triangles(self, image, triangles, width, height):
        """Dibuja triángulos de Sierpinski."""
        for triangle in triangles:
            self._draw_polygon(image, triangle, width, height)
    
    def _draw_line(self, image, p1, p2, width, height):
        """Dibuja una línea usando algoritmo de Bresenham."""
        try:
            x1, y1 = int(p1[0]), int(p1[1])
            x2, y2 = int(p2[0]), int(p2[1])
            
            # Verificar límites
            if not self._line_intersects_screen(x1, y1, x2, y2, width, height):
                return
            
            # Algoritmo de Bresenham
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            
            if dx == 0 and dy == 0:
                if 0 <= x1 < width and 0 <= y1 < height:
                    image[y1, x1] = self._get_line_color()
                return
            
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy
            
            x, y = x1, y1
            
            while True:
                if 0 <= x < width and 0 <= y < height:
                    image[y, x] = self._get_line_color()
                
                if x == x2 and y == y2:
                    break
                
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x += sx
                if e2 < dx:
                    err += dx
                    y += sy
        
        except (TypeError, ValueError, IndexError):
            pass
    
    def _line_intersects_screen(self, x1, y1, x2, y2, width, height):
        """Verifica si una línea intersecta la pantalla."""
        return not ((x1 < 0 and x2 < 0) or (x1 >= width and x2 >= width) or
                   (y1 < 0 and y2 < 0) or (y1 >= height and y2 >= height))
    
    def _get_line_color(self):
        """Obtiene el color para las líneas."""
        if self.current_palette and len(self.current_palette) > 0:
            return self.current_palette[len(self.current_palette) // 2]
        return (255, 255, 255)
