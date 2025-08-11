"""
Ventanas de Fractales - Versión corregida
Interfaces fluidas y minimalistas para todos los fractales
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QSlider, QSpinBox, QComboBox,
                             QFrame, QApplication, QFileDialog, QMessageBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QPoint
from PyQt6.QtGui import QPixmap, QImage, QPainter, QFont, QPen, QColor

import numpy as np
import math
from ..generators.fractal_generators import JuliaGenerator


class JuliaMainWindow(QMainWindow):
    """Ventana principal optimizada para Julia con CUDA."""
    
    def __init__(self):
        super().__init__()
        self.generator = JuliaGenerator()
        self.setup_ui()
        self.setup_mouse_interaction()
        self.setup_presets()
        self.update_fractal()
    
    def setup_ui(self):
        """Configura la interfaz minimalista y fluida."""
        self.setWindowTitle("🌀 Conjunto de Julia - Acelerado por GPU")
        self.setGeometry(100, 100, 900, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Canvas principal
        self.canvas = QLabel()
        self.canvas.setGeometry(0, 0, 900, 700)
        self.canvas.setStyleSheet("border: 2px solid #333; background-color: black;")
        main_layout.addWidget(self.canvas)
        
        # Panel de controles superior
        controls_frame1 = QFrame()
        controls_frame1.setFixedHeight(50)
        controls_frame1.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #FF6B35;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E55A2B;
            }
            QSpinBox, QComboBox, QSlider, QDoubleSpinBox {
                background-color: #3b3b3b;
                color: white;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        
        controls_layout1 = QHBoxLayout()
        controls_frame1.setLayout(controls_layout1)
        
        # Presets de Julia
        controls_layout1.addWidget(QLabel("Preset:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "Clásico", "Dragón", "Espiral", "Hoja", "Rayo", 
            "Coral", "Tormenta", "Galaxia", "Personalizado"
        ])
        self.preset_combo.currentIndexChanged.connect(self.change_preset)
        controls_layout1.addWidget(self.preset_combo)
        
        # Parámetros C real e imaginario
        controls_layout1.addWidget(QLabel("C Real:"))
        self.c_real_spin = QDoubleSpinBox()
        self.c_real_spin.setRange(-2.0, 2.0)
        self.c_real_spin.setSingleStep(0.01)
        self.c_real_spin.setDecimals(3)
        self.c_real_spin.setValue(-0.7)
        self.c_real_spin.valueChanged.connect(self.update_julia_constant)
        controls_layout1.addWidget(self.c_real_spin)
        
        controls_layout1.addWidget(QLabel("C Imag:"))
        self.c_imag_spin = QDoubleSpinBox()
        self.c_imag_spin.setRange(-2.0, 2.0)
        self.c_imag_spin.setSingleStep(0.01)
        self.c_imag_spin.setDecimals(3)
        self.c_imag_spin.setValue(0.27015)
        self.c_imag_spin.valueChanged.connect(self.update_julia_constant)
        controls_layout1.addWidget(self.c_imag_spin)
        
        controls_layout1.addStretch()
        main_layout.addWidget(controls_frame1)
        
        # Panel de controles inferior
        controls_frame2 = QFrame()
        controls_frame2.setFixedHeight(50)
        controls_frame2.setStyleSheet(controls_frame1.styleSheet())
        
        controls_layout2 = QHBoxLayout()
        controls_frame2.setLayout(controls_layout2)
        
        # Iteraciones
        controls_layout2.addWidget(QLabel("Iter:"))
        self.iterations_spinbox = QSpinBox()
        self.iterations_spinbox.setRange(1, 5000)
        self.iterations_spinbox.setValue(200)
        self.iterations_spinbox.valueChanged.connect(self.update_iterations)
        controls_layout2.addWidget(self.iterations_spinbox)
        
        # Zoom
        zoom_in_btn = QPushButton("🔍+")
        zoom_in_btn.clicked.connect(self.zoom_in)
        controls_layout2.addWidget(zoom_in_btn)
        
        zoom_out_btn = QPushButton("🔍-")
        zoom_out_btn.clicked.connect(self.zoom_out)
        controls_layout2.addWidget(zoom_out_btn)
        
        # Paletas de colores
        controls_layout2.addWidget(QLabel("Color:"))
        self.color_combo = QComboBox()
        palette_names = self.generator.palette_generator.get_palette_names()
        self.color_combo.addItems(palette_names)
        self.color_combo.currentIndexChanged.connect(self.change_color_scheme)
        controls_layout2.addWidget(self.color_combo)
        
        # Modo de color
        controls_layout2.addWidget(QLabel("Modo:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Paleta Simple", "Interpolación Suave"])
        self.mode_combo.setCurrentIndex(1)
        self.mode_combo.currentIndexChanged.connect(self.change_color_mode)
        controls_layout2.addWidget(self.mode_combo)
        
        # Aura
        controls_layout2.addWidget(QLabel("Aura:"))
        self.aura_slider = QSlider(Qt.Orientation.Horizontal)
        self.aura_slider.setRange(0, 100)
        self.aura_slider.setValue(50)
        self.aura_slider.setFixedWidth(80)
        self.aura_slider.valueChanged.connect(self.change_aura_intensity)
        controls_layout2.addWidget(self.aura_slider)
        
        # Exportar
        export_btn = QPushButton("💾 Exportar")
        export_btn.clicked.connect(self.export_high_res)
        controls_layout2.addWidget(export_btn)
        
        # Reset
        reset_btn = QPushButton("🏠 Reset")
        reset_btn.clicked.connect(self.reset_view)
        controls_layout2.addWidget(reset_btn)
        
        controls_layout2.addStretch()
        main_layout.addWidget(controls_frame2)
    
    def setup_mouse_interaction(self):
        """Configura la interacción con mouse para navegación fluida."""
        self.is_dragging = False
        self.last_mouse_pos = QPoint()
        
        # Habilitar tracking del mouse
        self.canvas.setMouseTracking(True)
        self.setMouseTracking(True)
    
    def setup_presets(self):
        """Configura los presets de Julia."""
        self.julia_presets = {
            0: (-0.7, 0.27015),    # Clásico
            1: (-0.835, -0.2321),  # Dragón
            2: (-0.8, 0.156),      # Espiral
            3: (-0.75, 0.11),      # Hoja
            4: (-0.4, 0.6),        # Rayo
            5: (0.285, 0.01),      # Coral
            6: (-0.123, 0.745),    # Tormenta
            7: (-0.194, 0.6557),   # Galaxia
            8: (-0.7, 0.27015)     # Personalizado (valor inicial)
        }
    
    def change_preset(self, index):
        """Cambia el preset de Julia."""
        if index < len(self.julia_presets):
            real, imag = self.julia_presets[index]
            self.c_real_spin.setValue(real)
            self.c_imag_spin.setValue(imag)
            self.generator.set_julia_constant(real, imag)
            self.update_fractal()
    
    def update_julia_constant(self):
        """Actualiza la constante de Julia."""
        real = self.c_real_spin.value()
        imag = self.c_imag_spin.value()
        self.generator.set_julia_constant(real, imag)
        # Cambiar a preset personalizado
        self.preset_combo.setCurrentIndex(8)
        self.update_fractal()
    
    def update_iterations(self):
        """Actualiza el número de iteraciones."""
        self.generator.set_max_iterations(self.iterations_spinbox.value())
        self.update_fractal()
    
    def change_aura_intensity(self):
        """Actualiza la intensidad del aura."""
        intensity = self.aura_slider.value() / 50.0
        self.generator.set_aura_intensity(intensity)
        self.update_fractal()
    
    def zoom_in(self):
        """Aumenta el zoom."""
        self.generator.zoom_in(1.5)
        self.update_fractal()
    
    def zoom_out(self):
        """Disminuye el zoom."""
        self.generator.zoom_out(1.5)
        self.update_fractal()
    
    def change_color_scheme(self, index):
        """Cambia el esquema de color."""
        self.generator.set_color_scheme(index)
        self.update_fractal()
    
    def change_color_mode(self, index):
        """Cambia el modo de coloración."""
        self.generator.set_color_mode(index)
        self.update_fractal()
    
    def reset_view(self):
        """Resetea la vista a la posición inicial."""
        self.generator.set_zoom(300.0)
        self.generator.set_offset(0.0, 0.0)
        self.generator.set_rotation(0.0)
        self.update_fractal()
    
    def mousePressEvent(self, event):
        """Detecta cuando se presiona el mouse."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.last_mouse_pos = event.position()
        elif event.button() == Qt.MouseButton.RightButton:
            # Click derecho para zoom out
            self.generator.zoom_out(1.3)
            self.update_fractal()
    
    def mouseMoveEvent(self, event):
        """Detecta el movimiento del mouse para arrastrar."""
        if self.is_dragging and (event.buttons() & Qt.MouseButton.LeftButton):
            delta = event.position() - self.last_mouse_pos
            self.last_mouse_pos = event.position()
            
            # Ajustar la sensibilidad del movimiento
            sensitivity = 0.5
            self.generator.move(delta.x() * sensitivity, delta.y() * sensitivity)
            
            # Actualizar fractal con un pequeño delay para fluidez
            QTimer.singleShot(10, self.update_fractal)
    
    def mouseReleaseEvent(self, event):
        """Detecta cuando se suelta el mouse."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
    
    def wheelEvent(self, event):
        """Detecta la rueda del mouse para zoom centrado."""
        # Obtener posición del mouse en coordenadas del canvas
        mouse_pos = event.position()
        canvas_rect = self.canvas.geometry()
        
        # Verificar si el mouse está sobre el canvas
        if canvas_rect.contains(mouse_pos.toPoint()):
            delta = event.angleDelta().y()
            
            # Zoom más suave
            zoom_factor = 1.1 if delta > 0 else 1.0/1.1
            
            if delta > 0:
                self.generator.zoom_in(zoom_factor)
            else:
                self.generator.zoom_out(zoom_factor)
            
            self.update_fractal()
    
    def update_fractal(self):
        """Actualiza el fractal en tiempo real."""
        try:
            width, height = 900, 700
            fractal_array = self.generator.generate_fractal(width, height)
            
            # Convertir a QImage
            q_image = QImage(fractal_array.data, width, height, 
                           3 * width, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.canvas.setPixmap(pixmap)
            
        except Exception as e:
            print(f"Error generando fractal: {e}")
    
    def export_high_res(self):
        """Exporta el fractal en alta resolución."""
        try:
            export_width = 4000
            export_height = 4000
            
            print(f"Generando Julia en resolución {export_width}x{export_height}...")
            
            # Generar imagen de alta resolución
            high_res_image = self.generator.generate_fractal(export_width, export_height)
            
            # Convertir a QImage
            qimage = QImage(high_res_image.data, export_width, export_height, 
                          3 * export_width, QImage.Format.Format_RGB888)
            
            # Diálogo para guardar
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Julia", "julia.png", 
                "PNG Files (*.png);;JPG Files (*.jpg);;All Files (*)"
            )
            
            if file_path:
                qimage.save(file_path)
                QMessageBox.information(self, "Éxito", 
                                      f"Fractal exportado correctamente:\n{file_path}")
                print(f"Imagen guardada en: {file_path}")
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al exportar: {str(e)}")
            print(f"Error en exportación: {e}")


# Clases básicas para los otros fractales (implementación simplificada)
class KochMainWindow(QMainWindow):
    """Ventana principal para la Curva de Koch."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.generate_fractal()
    
    def setup_ui(self):
        """Configura la interfaz."""
        self.setWindowTitle("❄️ Curva de Koch")
        self.setGeometry(100, 100, 900, 700)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.canvas = QLabel()
        self.canvas.setMinimumSize(800, 600)
        self.canvas.setStyleSheet("border: 2px solid #444; background-color: black;")
        layout.addWidget(self.canvas)
        
        info = QLabel("❄️ Curva de Koch - Implementación básica")
        info.setStyleSheet("color: white; font-size: 14px; padding: 10px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
    
    def generate_fractal(self):
        """Genera la curva de Koch básica."""
        image = QImage(800, 600, QImage.Format.Format_RGB888)
        image.fill(QColor(0, 0, 0))
        
        painter = QPainter(image)
        painter.setPen(QPen(QColor(0, 255, 255), 3))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dibujar un copo de nieve básico
        center_x, center_y = 400, 300
        radius = 200
        
        for i in range(6):
            angle = i * 60 * math.pi / 180
            x1 = center_x + radius * math.cos(angle)
            y1 = center_y + radius * math.sin(angle)
            x2 = center_x + radius * 0.7 * math.cos(angle)
            y2 = center_y + radius * 0.7 * math.sin(angle)
            painter.drawLine(int(x2), int(y2), int(x1), int(y1))
        
        painter.end()
        pixmap = QPixmap.fromImage(image)
        self.canvas.setPixmap(pixmap)


class TreeMainWindow(QMainWindow):
    """Ventana principal para el Árbol Fractal."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.generate_fractal()
    
    def setup_ui(self):
        """Configura la interfaz."""
        self.setWindowTitle("🌳 Árbol Fractal")
        self.setGeometry(100, 100, 900, 700)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.canvas = QLabel()
        self.canvas.setMinimumSize(800, 600)
        self.canvas.setStyleSheet("border: 2px solid #444; background-color: #001122;")
        layout.addWidget(self.canvas)
        
        info = QLabel("🌳 Árbol Fractal - Implementación básica")
        info.setStyleSheet("color: white; font-size: 14px; padding: 10px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
    
    def generate_fractal(self):
        """Genera el árbol fractal básico."""
        image = QImage(800, 600, QImage.Format.Format_RGB888)
        image.fill(QColor(0, 10, 20))
        
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dibujar un árbol básico
        self.draw_branch(painter, 400, 550, 100, -90, 5)
        
        painter.end()
        pixmap = QPixmap.fromImage(image)
        self.canvas.setPixmap(pixmap)
    
    def draw_branch(self, painter, x, y, length, angle, level):
        """Dibuja una rama recursivamente."""
        if level <= 0 or length < 2:
            return
        
        # Color que cambia con el nivel
        if level > 3:
            painter.setPen(QPen(QColor(139, 69, 19), max(1, level)))  # Marrón
        else:
            painter.setPen(QPen(QColor(0, 255, 0), max(1, level)))   # Verde
        
        # Calcular punto final
        end_x = x + length * math.cos(math.radians(angle))
        end_y = y + length * math.sin(math.radians(angle))
        
        # Dibujar rama
        painter.drawLine(int(x), int(y), int(end_x), int(end_y))
        
        # Dibujar ramas hijas
        new_length = length * 0.7
        self.draw_branch(painter, end_x, end_y, new_length, angle - 25, level - 1)
        self.draw_branch(painter, end_x, end_y, new_length, angle + 25, level - 1)


class SierpinskiMainWindow(QMainWindow):
    """Ventana principal para el Triángulo de Sierpinski."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.generate_fractal()
    
    def setup_ui(self):
        """Configura la interfaz."""
        self.setWindowTitle("🔺 Triángulo de Sierpinski")
        self.setGeometry(100, 100, 900, 700)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.canvas = QLabel()
        self.canvas.setMinimumSize(800, 600)
        self.canvas.setStyleSheet("border: 2px solid #444; background-color: black;")
        layout.addWidget(self.canvas)
        
        info = QLabel("🔺 Triángulo de Sierpinski - Implementación básica")
        info.setStyleSheet("color: white; font-size: 14px; padding: 10px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
    
    def generate_fractal(self):
        """Genera el triángulo de Sierpinski básico."""
        image = QImage(800, 600, QImage.Format.Format_RGB888)
        image.fill(QColor(0, 0, 0))
        
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Triángulo principal
        size = 300
        height = size * math.sqrt(3) / 2
        center_x, center_y = 400, 320
        
        p1 = (center_x, center_y - height / 2)
        p2 = (center_x - size / 2, center_y + height / 2)
        p3 = (center_x + size / 2, center_y + height / 2)
        
        # Dibujar sierpinski básico
        self.draw_sierpinski(painter, p1, p2, p3, 4)
        
        painter.end()
        pixmap = QPixmap.fromImage(image)
        self.canvas.setPixmap(pixmap)
    
    def draw_sierpinski(self, painter, p1, p2, p3, level):
        """Dibuja sierpinski recursivamente."""
        if level <= 0:
            # Triángulo sólido
            color = QColor(255, int(100 + level * 30), 0)
            painter.setBrush(color)
            painter.setPen(QPen(color, 1))
            
            points = [QPoint(int(p1[0]), int(p1[1])), 
                     QPoint(int(p2[0]), int(p2[1])), 
                     QPoint(int(p3[0]), int(p3[1]))]
            painter.drawPolygon(points)
            return
        
        # Puntos medios
        mid12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        mid23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
        mid31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
        
        # Recursión
        self.draw_sierpinski(painter, p1, mid12, mid31, level - 1)
        self.draw_sierpinski(painter, mid12, p2, mid23, level - 1)
        self.draw_sierpinski(painter, mid31, mid23, p3, level - 1)
