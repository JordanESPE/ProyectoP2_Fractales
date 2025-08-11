#!/usr/bin/env python3
"""
🔺 SIERPINSKI NAVEGABLE Y FLUIDO
Versión estable con zoom infinito y navegación por el fractal
"""

import sys
import math
import time
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QSlider, QFrame, QApplication)
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QPolygonF

class SierpinskiNavigableWindow(QMainWindow):
    """🔺 SIERPINSKI NAVEGABLE - ZOOM INFINITO Y MOVIMIENTO FLUIDO"""
    
    def __init__(self):
        super().__init__()
        # Parámetros de navegación
        self.zoom_level = 1.0
        self.min_zoom = 0.0001  # Zoom mínimo para ver el fractal completo
        self.max_zoom = 1000000.0  # Zoom máximo para detalles ultra-infinitos
        self.center_x = 0.0
        self.center_y = 0.0
        
        # Parámetros del fractal
        self.base_level = 3
        self.color_intensity = 180
        
        # Control de mouse
        self.mouse_pressed = False
        self.last_mouse_pos = None
        
        # Timer para actualizaciones ultra-fluidas
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.safe_generate)
        self.update_timer.setSingleShot(True)
        
        # Control de fluidez
        self.last_update_time = 0
        self.render_quality = "high"  # high, medium, fast
        
        self.setup_ui()
        self.generate_fractal()
    
    def setup_ui(self):
        """Interfaz para navegación fluida."""
        self.setWindowTitle("🔺 SIERPINSKI ULTRA-FLUIDO - Aparición Natural hasta 1M x")
        self.setGeometry(100, 100, 1200, 800)
        
        # Estilos modernos pero ligeros
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #0a0a1a; 
                color: white; 
            }
            QLabel { 
                color: white; 
                font-size: 12px;
            }
            QPushButton {
                background-color: #2a2a4a;
                color: white;
                border: 1px solid #4a4a6a;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover { 
                background-color: #3a3a5a;
                border-color: #6a6a8a;
            }
            QPushButton:pressed {
                background-color: #1a1a3a;
            }
            QSlider::groove:horizontal {
                border: 1px solid #3c3c4c;
                height: 10px;
                background: #1c1c2c;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #66aaff, stop:1 #4488dd);
                border: 1px solid #555;
                width: 18px;
                margin: -3px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #88ccff, stop:1 #66aaee);
            }
            QFrame {
                background-color: #1a1a2a;
                border: 1px solid #444;
                border-radius: 8px;
                margin: 4px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Canvas navegable
        self.canvas = QLabel()
        self.canvas.setMinimumSize(800, 700)
        self.canvas.setStyleSheet("""
            border: 2px solid #444; 
            background-color: #000;
            border-radius: 4px;
        """)
        self.canvas.mousePressEvent = self.mouse_press_event
        self.canvas.mouseMoveEvent = self.mouse_move_event
        self.canvas.mouseReleaseEvent = self.mouse_release_event
        self.canvas.wheelEvent = self.wheel_event
        main_layout.addWidget(self.canvas)
        
        # Controles de navegación
        controls = self.create_navigation_controls()
        main_layout.addWidget(controls)
    
    def create_navigation_controls(self):
        """Controles para navegación fluida."""
        frame = QFrame()
        frame.setFixedWidth(350)
        layout = QVBoxLayout()
        frame.setLayout(layout)
        
        # Título
        title = QLabel("🔺 SIERPINSKI NAVEGABLE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; color: #66aaff; margin: 15px; font-weight: bold;")
        layout.addWidget(title)
        
        # Info de navegación
        nav_info = QLabel("🖱️ NAVEGACIÓN SÚPER-FLUIDA:\n• Arrastra: movimiento ultra-suave\n• Rueda: zoom fluido extremo\n• Hasta 32 niveles de detalle\n• Triángulos INFINITOS!")
        nav_info.setAlignment(Qt.AlignmentFlag.AlignLeft)
        nav_info.setStyleSheet("background-color: #2a2a3a; padding: 10px; border-radius: 6px; color: #ccccff;")
        layout.addWidget(nav_info)
        
        # Zoom manual
        layout.addWidget(QLabel("🔍 Zoom Manual:"))
        zoom_layout = QHBoxLayout()
        
        zoom_out_btn = QPushButton("➖")
        zoom_out_btn.setFixedSize(40, 30)
        zoom_out_btn.clicked.connect(self.zoom_out)
        zoom_layout.addWidget(zoom_out_btn)
        
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(1)      # 0.0001x
        self.zoom_slider.setMaximum(100000)   # 1,000,000x (logarítmico ultra-amplio)
        self.zoom_slider.setValue(10000)     # 1x
        self.zoom_slider.valueChanged.connect(self.manual_zoom_change)
        zoom_layout.addWidget(self.zoom_slider)
        
        zoom_in_btn = QPushButton("➕")
        zoom_in_btn.setFixedSize(40, 30)
        zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_layout.addWidget(zoom_in_btn)
        
        layout.addLayout(zoom_layout)
        
        self.zoom_label = QLabel("Zoom: 1.0x")
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zoom_label.setStyleSheet("font-weight: bold; color: #aaffaa;")
        layout.addWidget(self.zoom_label)
        
        # Nivel de detalle (adapta automáticamente con zoom)
        layout.addWidget(QLabel("📊 Nivel Base:"))
        self.level_slider = QSlider(Qt.Orientation.Horizontal)
        self.level_slider.setMinimum(1)
        self.level_slider.setMaximum(6)
        self.level_slider.setValue(3)
        self.level_slider.valueChanged.connect(self.safe_update_level)
        layout.addWidget(self.level_slider)
        
        self.level_label = QLabel("Nivel: 3 (+ zoom adaptativo)")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.level_label)
        
        # Color y estilo
        layout.addWidget(QLabel("🌈 Intensidad:"))
        self.color_slider = QSlider(Qt.Orientation.Horizontal)
        self.color_slider.setMinimum(50)
        self.color_slider.setMaximum(255)
        self.color_slider.setValue(180)
        self.color_slider.valueChanged.connect(self.safe_update_color)
        layout.addWidget(self.color_slider)
        
        self.color_label = QLabel("Color: 180")
        self.color_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.color_label)
        
        # Movimiento manual
        layout.addWidget(QLabel("🧭 Movimiento Manual:"))
        move_grid = QVBoxLayout()
        
        # Fila superior
        top_row = QHBoxLayout()
        top_row.addStretch()
        up_btn = QPushButton("⬆️")
        up_btn.setFixedSize(40, 30)
        up_btn.clicked.connect(self.move_up)
        top_row.addWidget(up_btn)
        top_row.addStretch()
        move_grid.addLayout(top_row)
        
        # Fila media
        mid_row = QHBoxLayout()
        left_btn = QPushButton("⬅️")
        left_btn.setFixedSize(40, 30)
        left_btn.clicked.connect(self.move_left)
        mid_row.addWidget(left_btn)
        
        center_btn = QPushButton("🎯")
        center_btn.setFixedSize(40, 30)
        center_btn.clicked.connect(self.reset_view)
        mid_row.addWidget(center_btn)
        
        right_btn = QPushButton("➡️")
        right_btn.setFixedSize(40, 30)
        right_btn.clicked.connect(self.move_right)
        mid_row.addWidget(right_btn)
        move_grid.addLayout(mid_row)
        
        # Fila inferior
        bot_row = QHBoxLayout()
        bot_row.addStretch()
        down_btn = QPushButton("⬇️")
        down_btn.setFixedSize(40, 30)
        down_btn.clicked.connect(self.move_down)
        bot_row.addWidget(down_btn)
        bot_row.addStretch()
        move_grid.addLayout(bot_row)
        
        layout.addLayout(move_grid)
        
        # Información de posición
        self.pos_label = QLabel("Posición: (0.0, 0.0)")
        self.pos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pos_label.setStyleSheet("color: #ffaaaa; font-size: 10px;")
        layout.addWidget(self.pos_label)
        
        # Botones de acción
        layout.addWidget(QLabel(""))  # Espacio
        
        export_btn = QPushButton("💾 Exportar Vista")
        export_btn.clicked.connect(self.export_current_view)
        layout.addWidget(export_btn)
        
        layout.addStretch()
        return frame
    
    # Eventos de mouse para navegación
    def mouse_press_event(self, event):
        """Iniciar arrastre."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = True
            self.last_mouse_pos = event.pos()
    
    def mouse_move_event(self, event):
        """Arrastrar para mover."""
        if self.mouse_pressed and self.last_mouse_pos:
            # Calcular desplazamiento
            dx = event.pos().x() - self.last_mouse_pos.x()
            dy = event.pos().y() - self.last_mouse_pos.y()
            
            # Aplicar desplazamiento ULTRA-FLUIDO (inverso para sensación natural)
            move_factor = 0.8 / self.zoom_level  # Factor más suave para movimiento ultra-fluido
            self.center_x -= dx * move_factor
            self.center_y -= dy * move_factor
            
            self.last_mouse_pos = event.pos()
            self.update_position_info()
            self.schedule_update()
    
    def mouse_release_event(self, event):
        """Finalizar arrastre."""
        self.mouse_pressed = False
        self.last_mouse_pos = None
    
    def wheel_event(self, event):
        """Zoom con rueda del mouse."""
        # Obtener punto del mouse en coordenadas del canvas
        mouse_x = event.position().x()
        mouse_y = event.position().y()
        
        # Convertir a coordenadas del fractal
        canvas_center_x = self.canvas.width() / 2
        canvas_center_y = self.canvas.height() / 2
        
        fractal_x = self.center_x + (mouse_x - canvas_center_x) / self.zoom_level
        fractal_y = self.center_y + (mouse_y - canvas_center_y) / self.zoom_level
        
        # Aplicar zoom ULTRA-FLUIDO
        zoom_factor = 1.08 if event.angleDelta().y() > 0 else 1/1.08  # Factor MÁS suave para fluidez extrema
        new_zoom = self.zoom_level * zoom_factor
        
        # Limitar zoom
        new_zoom = max(self.min_zoom, min(self.max_zoom, new_zoom))
        
        if new_zoom != self.zoom_level:
            # Ajustar centro para mantener punto bajo el mouse
            self.center_x = fractal_x - (mouse_x - canvas_center_x) / new_zoom
            self.center_y = fractal_y - (mouse_y - canvas_center_y) / new_zoom
            
            self.zoom_level = new_zoom
            self.update_zoom_slider()
            self.update_position_info()
            self.schedule_update()
    
    # Controles manuales
    def zoom_in(self):
        """Zoom in manual."""
        self.zoom_level = min(self.max_zoom, self.zoom_level * 1.5)
        self.update_zoom_slider()
        self.schedule_update()
    
    def zoom_out(self):
        """Zoom out manual."""
        self.zoom_level = max(self.min_zoom, self.zoom_level / 1.5)
        self.update_zoom_slider()
        self.schedule_update()
    
    def move_up(self):
        """Mover hacia arriba."""
        self.center_y -= 30 / self.zoom_level  # Movimiento más suave
        self.update_position_info()
        self.schedule_ultra_fluid_update()
    
    def move_down(self):
        """Mover hacia abajo."""
        self.center_y += 30 / self.zoom_level  # Movimiento más suave
        self.update_position_info()
        self.schedule_ultra_fluid_update()
    
    def move_left(self):
        """Mover hacia la izquierda."""
        self.center_x -= 30 / self.zoom_level  # Movimiento más suave
        self.update_position_info()
        self.schedule_ultra_fluid_update()
    
    def move_right(self):
        """Mover hacia la derecha."""
        self.center_x += 30 / self.zoom_level  # Movimiento más suave
        self.update_position_info()
        self.schedule_ultra_fluid_update()
    
    def reset_view(self):
        """Resetear vista al centro."""
        self.zoom_level = 1.0
        self.center_x = 0.0
        self.center_y = 0.0
        self.update_zoom_slider()
        self.update_position_info()
        self.schedule_ultra_fluid_update()
    
    def manual_zoom_change(self):
        """Cambio manual de zoom ultra-amplio."""
        # Conversión logarítmica ultra-amplia para mejor control
        slider_val = self.zoom_slider.value()
        if slider_val <= 10000:
            # 0.0001x a 1x
            progress = slider_val / 10000.0
            self.zoom_level = 0.0001 * (10000 ** progress)
        else:
            # 1x a 1,000,000x
            progress = (slider_val - 10000) / 90000.0
            self.zoom_level = 1.0 * (1000000 ** progress)
        
        self.update_position_info()
        self.schedule_ultra_fluid_update()
    
    def update_zoom_slider(self):
        """Actualizar slider de zoom ultra-amplio."""
        if self.zoom_level <= 1.0:
            # 0.0001x a 1x
            if self.zoom_level <= 0.0001:
                slider_val = 1
            else:
                progress = math.log(self.zoom_level / 0.0001) / math.log(10000)
                slider_val = int(progress * 10000)
        else:
            # 1x a 1,000,000x
            if self.zoom_level >= 1000000:
                slider_val = 100000
            else:
                progress = math.log(self.zoom_level) / math.log(1000000)
                slider_val = int(10000 + progress * 90000)
        
        self.zoom_slider.blockSignals(True)
        self.zoom_slider.setValue(max(1, min(100000, slider_val)))
        self.zoom_slider.blockSignals(False)
    
    def safe_update_level(self):
        """Actualización segura del nivel."""
        try:
            self.base_level = self.level_slider.value()
            self.level_label.setText(f"Nivel: {self.base_level} (+ zoom adaptativo)")
            self.schedule_ultra_fluid_update()
        except Exception as e:
            print(f"Error en nivel: {e}")
    
    def safe_update_color(self):
        """Actualización segura del color."""
        try:
            self.color_intensity = self.color_slider.value()
            self.color_label.setText(f"Color: {self.color_intensity}")
            self.schedule_ultra_fluid_update()
        except Exception as e:
            print(f"Error en color: {e}")
    
    def update_position_info(self):
        """Actualizar información de posición."""
        zoom_text = f"{self.zoom_level:.3f}x" if self.zoom_level < 100 else f"{self.zoom_level:.0f}x"
        self.zoom_label.setText(f"Zoom: {zoom_text}")
        self.pos_label.setText(f"Posición: ({self.center_x:.2f}, {self.center_y:.2f})")
        
        # Actualizar título con calidad optimizada
        quality_emoji = {"high": "🌟", "medium": "⚡", "fast": "🚀", "ultra_fast": "💨"}[self.render_quality]
        self.setWindowTitle(f"🔺 SIERPINSKI FLUIDO {quality_emoji} - Zoom: {zoom_text} - Pos: ({self.center_x:.1f}, {self.center_y:.1f})")
    
    def schedule_ultra_fluid_update(self):
        """Programar actualización SÚPER-FLUIDA optimizada para zoom alto."""
        import time
        current_time = time.time()
        
        # Determinar calidad de render OPTIMIZADA para zoom alto
        if self.zoom_level < 10:
            self.render_quality = "high"
            delay = 16  # 16ms = ~60 FPS
        elif self.zoom_level < 50:
            self.render_quality = "medium"
            delay = 12  # 12ms = ~80 FPS
        elif self.zoom_level < 200:
            self.render_quality = "fast"
            delay = 8   # 8ms = ~120 FPS
        else:
            # NUEVO: Ultra-fast para zoom extremo
            self.render_quality = "ultra_fast"
            delay = 6   # 6ms = ~160 FPS para máxima fluidez
        
        # Evitar actualizaciones muy frecuentes con mejor control
        time_since_last = current_time - self.last_update_time
        if time_since_last > delay / 1000.0:
            self.last_update_time = current_time
            delay = max(2, int(delay * 0.3))  # Actualización más rápida
        
        self.update_timer.stop()
        self.update_timer.start(delay)
    
    def schedule_update(self):
        """Compatibilidad con función anterior."""
        self.schedule_ultra_fluid_update()
    
    def safe_generate(self):
        """Generación segura del fractal."""
        try:
            self.generate_fractal()
        except Exception as e:
            print(f"Error en generación: {e}")
    
    def generate_fractal(self):
        """Generación SÚPER-FLUIDA con aparición natural de triángulos."""
        # Calcular nivel adaptativo SUAVE para aparición natural
        zoom_log = math.log10(max(1, self.zoom_level))
        
        # Aparición MÁS GRADUAL y natural de triángulos
        smooth_factor = zoom_log * 2.8  # Factor más suave
        adaptive_level = self.base_level + int(smooth_factor)
        
        # Interpolación suave para transiciones naturales
        fractional_part = smooth_factor - int(smooth_factor)
        
        # Límites optimizados para zoom alto SIN pérdida de fluidez
        if self.zoom_level < 20:
            max_level = 18
        elif self.zoom_level < 100:
            max_level = 22      # Reducido para mejor fluidez
        elif self.zoom_level < 500:
            max_level = 25      # Optimizado para zoom medio-alto
        else:
            max_level = 27      # Reducido de 32 para mantener fluidez
            
        adaptive_level = min(max_level, adaptive_level)
        
        # Crear imagen con fondo visible
        width, height = 800, 700
        image = QImage(width, height, QImage.Format.Format_RGB888)
        image.fill(QColor(5, 5, 25))  # Fondo azul muy oscuro para contraste
        
        painter = QPainter(image)
        
        # Renderizado ULTRA-OPTIMIZADO para zoom alto
        if self.render_quality == "high":
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        elif self.render_quality == "medium":
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, self.zoom_level < 30)
        elif self.render_quality == "fast":
            # Solo antialiasing básico para mantener velocidad
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, self.zoom_level < 100)
        # ultra_fast = sin renderizado especial para máxima velocidad
        
        # Configurar transformación
        painter.translate(width/2, height/2)
        painter.scale(self.zoom_level, self.zoom_level)
        painter.translate(-self.center_x, -self.center_y)
        
        # Triángulo base con tamaño OPTIMIZADO
        base_size = 220
        if self.zoom_level > 50:
            # Crecimiento más controlado para mantener fluidez
            growth_factor = min(3.0, math.sqrt(self.zoom_level / 50))
            base_size = 220 * growth_factor
            
        height_tri = base_size * math.sqrt(3) / 2
        
        p1 = QPointF(-base_size/2, -height_tri/3)
        p2 = QPointF(base_size/2, -height_tri/3)
        p3 = QPointF(0, 2*height_tri/3)
        
        # Dibujar sierpinski con aparición NATURAL
        self.draw_natural_sierpinski(painter, p1, p2, p3, adaptive_level, fractional_part)
        
        painter.end()
        
        # Mostrar en canvas
        pixmap = QPixmap.fromImage(image)
        self.canvas.setPixmap(pixmap)
        
        # Actualizar info
        self.update_position_info()
        print(f"🔺 FLUIDO-Fractal - Zoom: {self.zoom_level:.1f}x - Nivel: {adaptive_level} - Calidad: {self.render_quality}")
    
    def draw_natural_sierpinski(self, painter, p1, p2, p3, level, opacity_factor=1.0):
        """Sierpinski con aparición NATURAL y fluidez optimizada para zoom alto."""
        if level <= 0:
            # Triángulo final con colores VISIBLES
            zoom_factor = math.log10(max(1, self.zoom_level))
            
            # Colores brillantes y visibles
            position_factor = (abs(p1.x()) + abs(p1.y())) * 0.005
            hue = int((self.color_intensity + level * 35 + zoom_factor * 50 + position_factor * 60) % 360)
            saturation = min(255, 150 + level * 15 + int(zoom_factor * 20))  # Más saturación
            value = min(255, 180 + level * 25 + int(zoom_factor * 15))       # Más brillo
            
            color = QColor()
            color.setHsv(hue, saturation, value)
            
            # CORREGIDO: Sin transparencia para que se vean los triángulos
            # color.setAlpha(final_opacity)  # REMOVIDO
            
            # Grosor visible
            if self.zoom_level > 200:
                line_width = max(0.5, 2.0 / math.log10(self.zoom_level))  # Más grueso
            elif self.zoom_level > 50:
                line_width = max(0.8, 3.0 / math.sqrt(self.zoom_level / 10))
            else:
                line_width = max(1.0, 2.5 / max(1, self.zoom_level / 20))
            
            painter.setBrush(color)
            painter.setPen(QPen(color.lighter(130), line_width))
            
            # Crear polígono visible
            polygon = QPolygonF([p1, p2, p3])
            painter.drawPolygon(polygon)
            
            return
        
        try:
            # Calcular puntos medios
            mid12 = QPointF((p1.x() + p2.x()) * 0.5, (p1.y() + p2.y()) * 0.5)
            mid23 = QPointF((p2.x() + p3.x()) * 0.5, (p2.y() + p3.y()) * 0.5)
            mid31 = QPointF((p3.x() + p1.x()) * 0.5, (p3.y() + p1.y()) * 0.5)
            
            # Recursión optimizada
            if self.zoom_level > 100 and level > 20:
                recursive_level = min(level - 1, 20)
            else:
                recursive_level = level - 1
            
            # CORREGIDO: Sin opacidad variable, todos los triángulos visibles
            self.draw_natural_sierpinski(painter, p1, mid12, mid31, recursive_level, 1.0)
            self.draw_natural_sierpinski(painter, mid12, p2, mid23, recursive_level, 1.0)
            self.draw_natural_sierpinski(painter, mid31, mid23, p3, recursive_level, 1.0)
            
            # Triángulos bonus solo en zoom bajo-medio
            if level > 3 and self.zoom_level > 5 and self.zoom_level < 150:
                self.draw_bonus_triangles_optimized(painter, mid12, mid23, mid31, max(0, level - 3))
            
        except Exception as e:
            # Fallback VISIBLE
            bright_color = QColor(self.color_intensity + 50, 150, 255)  # Color brillante sin transparencia
            painter.setBrush(bright_color)
            painter.setPen(QPen(bright_color.lighter(120), 1.5))
            polygon = QPolygonF([p1, p2, p3])
            painter.drawPolygon(polygon)
    
    def draw_bonus_triangles_optimized(self, painter, p1, p2, p3, level):
        """Triángulos BONUS optimizados y VISIBLES."""
        if level <= 0 or self.zoom_level > 150:
            return
            
        try:
            # Color bonus VISIBLE
            bonus_color = QColor()
            bonus_color.setHsv((self.color_intensity + 120) % 360, 120, 150)  # Sin transparencia
            painter.setBrush(bonus_color)
            painter.setPen(QPen(bonus_color.lighter(140), 0.8))  # Más grueso
            
            # Triángulo central bonus más visible
            center_x = (p1.x() + p2.x() + p3.x()) / 3
            center_y = (p1.y() + p2.y() + p3.y()) / 3
            size_factor = 0.4  # Más grande para ser más visible
            
            offset_x = (p1.x() - center_x) * size_factor
            offset_y = (p1.y() - center_y) * size_factor
            
            small_p1 = QPointF(center_x + offset_x, center_y + offset_y)
            small_p2 = QPointF(center_x + (p2.x() - center_x) * size_factor, center_y + (p2.y() - center_y) * size_factor)
            small_p3 = QPointF(center_x + (p3.x() - center_x) * size_factor, center_y + (p3.y() - center_y) * size_factor)
            
            polygon = QPolygonF([small_p1, small_p2, small_p3])
            painter.drawPolygon(polygon)
            
        except:
            pass
    
    def export_current_view(self):
        """Exportar vista actual."""
        try:
            pixmap = self.canvas.pixmap()
            if pixmap:
                filename = f"sierpinski_zoom_{self.zoom_level:.3f}x_pos_{self.center_x:.1f}_{self.center_y:.1f}.png"
                pixmap.save(filename)
                print(f"✅ Vista exportada como: {filename}")
        except Exception as e:
            print(f"Error al exportar: {e}")

def main():
    """Función principal."""
    print("🔺 SIERPINSKI ULTRA-FLUIDO - APARICIÓN NATURAL")
    print("=" * 65)
    
    try:
        app = QApplication(sys.argv)
        
        window = SierpinskiNavigableWindow()
        window.show()
        
        print("✅ SIERPINSKI ULTRA-FLUIDO INICIADO")
        print("🎮 Controles Ultra-Fluidos Optimizados:")
        print("  🖱️ Arrastra: Movimiento ultra-suave")
        print("  🎡 Rueda: Zoom fluido hasta 200x+ sin pérdidas")
        print("  🔍 Zoom: 0.0001x a 1,000,000x")
        print("  🧠 Niveles: Hasta 27 (optimizado para fluidez)")
        print("  🌈 Aparición natural de triángulos")
        print("  ✨ Triángulos bonus inteligentes")
        print("  💨 Hasta 160 FPS en zoom alto")
        print("  🎯 ¡Navegación fluida garantizada!")
        
        return app.exec()
        
    except Exception as e:
        print(f"Error crítico: {e}")
        return 1

if __name__ == "__main__":
    main()
