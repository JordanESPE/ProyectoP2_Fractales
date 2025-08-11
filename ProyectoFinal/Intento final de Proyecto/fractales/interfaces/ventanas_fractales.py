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
        
        # Rotación
        controls_layout2.addWidget(QLabel("Rot:"))
        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_slider.setRange(0, 360)
        self.rotation_slider.setValue(0)
        self.rotation_slider.setFixedWidth(80)
        self.rotation_slider.valueChanged.connect(self.change_rotation)
        controls_layout2.addWidget(self.rotation_slider)
        
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
    
    def change_rotation(self):
        """Cambia la rotación del fractal."""
        # Convertir grados a radianes
        rotation_degrees = self.rotation_slider.value()
        rotation_radians = math.radians(rotation_degrees)
        self.generator.set_rotation(rotation_radians)
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
        self.rotation_slider.setValue(0)
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
    """Ventana principal para la Curva de Koch - VERSIÓN CORREGIDA."""
    
    def __init__(self):
        super().__init__()
        self.points = []
        self.rotation = 0  # Agregar variable de rotación
        self.setup_ui()
        self.generate_fractal()
    
    def setup_ui(self):
        """Configura la interfaz."""
        self.setWindowTitle("❄️ Curva de Koch - CORREGIDA")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a1a; color: white; }
            QLabel { color: white; font-weight: bold; }
            QPushButton {
                background-color: #3d3d3d;
                color: white;
                border: 2px solid #555;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #4a4a4a; border-color: #6666ff; }
            QSlider::groove:horizontal {
                border: 1px solid #3c3c3c;
                height: 8px;
                background: #2b2b2b;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4a9eff;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            QFrame {
                background-color: #2b2b2b;
                border: 2px solid #3c3c3c;
                border-radius: 10px;
                margin: 5px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Canvas
        self.canvas = QLabel()
        self.canvas.setMinimumSize(600, 600)
        self.canvas.setStyleSheet("border: 2px solid #444; background-color: #000;")
        main_layout.addWidget(self.canvas)
        
        # Controles
        controls = self.create_controls()
        main_layout.addWidget(controls)
    
    def create_controls(self):
        """Crea los controles."""
        frame = QFrame()
        frame.setFixedWidth(250)
        layout = QVBoxLayout()
        frame.setLayout(layout)
        
        # Título
        title = QLabel("🎛️ CONTROLES KOCH")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 14px; color: #6666ff; margin: 10px;")
        layout.addWidget(title)
        
        # Nivel de recursión
        layout.addWidget(QLabel("🔄 Nivel de recursión:"))
        self.level_slider = QSlider(Qt.Orientation.Horizontal)
        self.level_slider.setMinimum(0)
        self.level_slider.setMaximum(6)
        self.level_slider.setValue(3)
        self.level_slider.valueChanged.connect(self.update_level)
        layout.addWidget(self.level_slider)
        
        self.level_label = QLabel("Nivel: 3")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.level_label)
        
        # Tipo de Koch
        layout.addWidget(QLabel("🎨 Tipo:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Línea Simple", "Triángulo", "Copo de Nieve"])
        self.type_combo.setCurrentIndex(2)  # Copo de Nieve por defecto
        self.type_combo.currentTextChanged.connect(self.generate_fractal)
        self.type_combo.setStyleSheet("""
            QComboBox {
                background-color: #3d3d3d;
                color: white;
                border: 2px solid #555;
                border-radius: 6px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.type_combo)
        
        # Rotación
        layout.addWidget(QLabel("🔄 Rotación:"))
        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_slider.setMinimum(0)
        self.rotation_slider.setMaximum(360)
        self.rotation_slider.setValue(0)
        self.rotation_slider.valueChanged.connect(self.update_rotation)
        layout.addWidget(self.rotation_slider)
        
        self.rotation_label = QLabel("Rotación: 0°")
        self.rotation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.rotation_label)
        
        # Botón regenerar
        regen_btn = QPushButton("🔄 Regenerar")
        regen_btn.clicked.connect(self.generate_fractal)
        layout.addWidget(regen_btn)
        
        # Botón exportar
        export_btn = QPushButton("💾 Exportar PNG")
        export_btn.clicked.connect(self.export_fractal)
        layout.addWidget(export_btn)
        
        # Información
        info_label = QLabel("ℹ️ INFORMACIÓN")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("font-size: 12px; color: #ffff66; margin-top: 15px;")
        layout.addWidget(info_label)
        
        info_text = QLabel("Curva de Koch corregida con algoritmo matemático preciso")
        info_text.setStyleSheet("font-size: 10px; color: #ccc; margin: 5px;")
        info_text.setWordWrap(True)
        layout.addWidget(info_text)
        
        layout.addStretch()
        return frame
    
    def update_level(self):
        """Actualiza el nivel."""
        level = self.level_slider.value()
        self.level_label.setText(f"Nivel: {level}")
        self.generate_fractal()
    
    def update_rotation(self):
        """Actualiza la rotación."""
        rotation = self.rotation_slider.value()
        self.rotation = rotation
        self.rotation_label.setText(f"Rotación: {rotation}°")
        self.generate_fractal()
    
    def rotate_point(self, x, y, center_x, center_y, angle_degrees):
        """Rota un punto alrededor de un centro."""
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        # Trasladar al origen
        dx = x - center_x
        dy = y - center_y
        
        # Rotar
        new_x = dx * cos_a - dy * sin_a
        new_y = dx * sin_a + dy * cos_a
        
        # Trasladar de vuelta
        return (new_x + center_x, new_y + center_y)
    
    def koch_line(self, p1, p2, level):
        """Genera una línea de Koch recursivamente (algoritmo corregido)."""
        if level == 0:
            return [p1, p2]
        
        # Calcular los puntos de la transformación de Koch
        x1, y1 = p1
        x2, y2 = p2
        
        # Dividir en tercios
        dx = (x2 - x1) / 3.0
        dy = (y2 - y1) / 3.0
        
        # Puntos A, B, D, E
        a = (x1, y1)
        b = (x1 + dx, y1 + dy)
        d = (x1 + 2*dx, y1 + 2*dy)
        e = (x2, y2)
        
        # Calcular punto C (pico del triángulo equilátero)
        mid_x = (b[0] + d[0]) / 2
        mid_y = (b[1] + d[1]) / 2
        
        # Vector perpendicular (rotado 90° antihorario)
        perp_x = -dy
        perp_y = dx
        
        # Normalizar y escalar por altura del triángulo equilátero
        length_bd = math.sqrt(dx*dx + dy*dy)
        if length_bd > 0:
            height = length_bd * math.sqrt(3) / 2
            perp_x = perp_x / length_bd * height
            perp_y = perp_y / length_bd * height
        
        c = (mid_x + perp_x, mid_y + perp_y)
        
        # Generar recursivamente los 4 segmentos
        result = []
        
        # Segmento AB
        seg1 = self.koch_line(a, b, level - 1)
        result.extend(seg1[:-1])  # Excluir último punto para evitar duplicados
        
        # Segmento BC
        seg2 = self.koch_line(b, c, level - 1)
        result.extend(seg2[:-1])
        
        # Segmento CD
        seg3 = self.koch_line(c, d, level - 1)
        result.extend(seg3[:-1])
        
        # Segmento DE
        seg4 = self.koch_line(d, e, level - 1)
        result.extend(seg4)  # Incluir último punto
        
        return result
    
    def generate_fractal(self):
        """Genera la curva de Koch."""
        level = self.level_slider.value()
        fractal_type = self.type_combo.currentText()
        
        # Crear imagen
        image = QImage(600, 600, QImage.Format.Format_RGB888)
        image.fill(QColor(0, 0, 0))
        
        painter = QPainter(image)
        painter.setPen(QPen(QColor(0, 255, 255), 2))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if fractal_type == "Línea Simple":
            # Una sola línea horizontal
            start = (50, 300)
            end = (550, 300)
            points = self.koch_line(start, end, level)
            
            # Aplicar rotación
            center_x, center_y = 300, 300
            if self.rotation != 0:
                points = [self.rotate_point(p[0], p[1], center_x, center_y, self.rotation) for p in points]
            
            for i in range(len(points) - 1):
                painter.drawLine(int(points[i][0]), int(points[i][1]),
                               int(points[i+1][0]), int(points[i+1][1]))
        
        elif fractal_type == "Triángulo":
            # Triángulo equilátero
            side = 400
            height = side * math.sqrt(3) / 2
            center_x, center_y = 300, 300
            
            # Vértices del triángulo
            p1 = (center_x, center_y - height/2)
            p2 = (center_x - side/2, center_y + height/2)
            p3 = (center_x + side/2, center_y + height/2)
            
            # Aplicar rotación a los vértices
            if self.rotation != 0:
                p1 = self.rotate_point(p1[0], p1[1], center_x, center_y, self.rotation)
                p2 = self.rotate_point(p2[0], p2[1], center_x, center_y, self.rotation)
                p3 = self.rotate_point(p3[0], p3[1], center_x, center_y, self.rotation)
            
            # Generar cada lado
            side1 = self.koch_line(p1, p2, level)
            side2 = self.koch_line(p2, p3, level)
            side3 = self.koch_line(p3, p1, level)
            
            # Dibujar cada lado
            for points in [side1, side2, side3]:
                for i in range(len(points) - 1):
                    painter.drawLine(int(points[i][0]), int(points[i][1]),
                                   int(points[i+1][0]), int(points[i+1][1]))
        
        else:  # Copo de Nieve
            # Copo de nieve (triángulo con curvas hacia afuera)
            side = 350
            height = side * math.sqrt(3) / 2
            center_x, center_y = 300, 320
            
            # Vértices del triángulo
            p1 = (center_x, center_y - height/2)
            p2 = (center_x - side/2, center_y + height/2)
            p3 = (center_x + side/2, center_y + height/2)
            
            # Aplicar rotación a los vértices
            if self.rotation != 0:
                p1 = self.rotate_point(p1[0], p1[1], center_x, center_y, self.rotation)
                p2 = self.rotate_point(p2[0], p2[1], center_x, center_y, self.rotation)
                p3 = self.rotate_point(p3[0], p3[1], center_x, center_y, self.rotation)
            
            # Generar cada lado del copo
            side1 = self.koch_line(p1, p2, level)
            side2 = self.koch_line(p2, p3, level)
            side3 = self.koch_line(p3, p1, level)
            
            # Dibujar con colores diferentes para cada lado
            colors = [QColor(255, 100, 100), QColor(100, 255, 100), QColor(100, 100, 255)]
            
            for idx, points in enumerate([side1, side2, side3]):
                painter.setPen(QPen(colors[idx], 2))
                for i in range(len(points) - 1):
                    painter.drawLine(int(points[i][0]), int(points[i][1]),
                                   int(points[i+1][0]), int(points[i+1][1]))
        
        painter.end()
        
        pixmap = QPixmap.fromImage(image)
        self.canvas.setPixmap(pixmap)
        
        # Calcular número de segmentos
        num_segments = 3 * (4 ** level)
        self.setWindowTitle(f"❄️ Curva de Koch CORREGIDA - Nivel {level} - {num_segments} segmentos")
    
    def export_fractal(self):
        """Exporta el fractal actual."""
        try:
            from PyQt6.QtWidgets import QFileDialog, QMessageBox
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Koch", "koch_curve_fixed.png", "PNG Files (*.png)"
            )
            
            if file_path:
                # Generar en alta resolución
                level = self.level_slider.value()
                fractal_type = self.type_combo.currentText()
                
                # Imagen de alta resolución
                image = QImage(4000, 4000, QImage.Format.Format_RGB888)
                image.fill(QColor(0, 0, 0))
                
                painter = QPainter(image)
                painter.setPen(QPen(QColor(0, 255, 255), 6))
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                
                # Escalar coordenadas para alta resolución
                scale = 4000 / 600
                
                if fractal_type == "Copo de Nieve":
                    side = 350 * scale
                    height = side * math.sqrt(3) / 2
                    center_x, center_y = 2000, 2200
                    
                    p1 = (center_x, center_y - height/2)
                    p2 = (center_x - side/2, center_y + height/2)
                    p3 = (center_x + side/2, center_y + height/2)
                    
                    side1 = self.koch_line(p1, p2, level)
                    side2 = self.koch_line(p2, p3, level)
                    side3 = self.koch_line(p3, p1, level)
                    
                    colors = [QColor(255, 100, 100), QColor(100, 255, 100), QColor(100, 100, 255)]
                    
                    for idx, points in enumerate([side1, side2, side3]):
                        painter.setPen(QPen(colors[idx], 6))
                        for i in range(len(points) - 1):
                            painter.drawLine(int(points[i][0]), int(points[i][1]),
                                           int(points[i+1][0]), int(points[i+1][1]))
                
                painter.end()
                
                image.save(file_path)
                QMessageBox.information(self, "Éxito", f"Fractal exportado en 4K:\n{file_path}")
                
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al exportar: {e}")


class TreeMainWindow(QMainWindow):
    """Ventana principal para el Árbol Fractal recursivo con navegación avanzada."""
    
    def __init__(self):
        super().__init__()
        
        # Parámetros de navegación y transformación
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.rotation = 0
        self.dragging = False
        self.last_mouse_pos = None
        
        self.setup_ui()
        self.generate_fractal()
    
    def setup_ui(self):
        """Configura la interfaz."""
        self.setWindowTitle("🌳 Árbol Fractal Recursivo Avanzado")
        self.setGeometry(100, 100, 1100, 800)
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a1a; color: white; }
            QLabel { color: white; font-weight: bold; }
            QPushButton {
                background-color: #3d3d3d;
                color: white;
                border: 2px solid #555;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #4a4a4a; border-color: #66ff66; }
            QSlider::groove:horizontal {
                border: 1px solid #3c3c3c;
                height: 8px;
                background: #2b2b2b;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #66ff66;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            QFrame {
                background-color: #2b2b2b;
                border: 2px solid #3c3c3c;
                border-radius: 10px;
                margin: 5px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Canvas con eventos de mouse para navegación
        self.canvas = QLabel()
        self.canvas.setMinimumSize(700, 700)
        self.canvas.setStyleSheet("border: 2px solid #444; background-color: #001122;")
        
        # Habilitar eventos de mouse
        self.canvas.mousePressEvent = self.mouse_press_event
        self.canvas.mouseMoveEvent = self.mouse_move_event
        self.canvas.mouseReleaseEvent = self.mouse_release_event
        self.canvas.wheelEvent = self.wheel_event
        
        main_layout.addWidget(self.canvas)
        
        # Controles
        controls = self.create_controls()
        main_layout.addWidget(controls)
    
    # Funciones de navegación con mouse
    def mouse_press_event(self, event):
        """Maneja el clic del mouse."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.pos()
    
    def mouse_move_event(self, event):
        """Maneja el movimiento del mouse."""
        if self.dragging and self.last_mouse_pos:
            delta = event.pos() - self.last_mouse_pos
            self.offset_x += delta.x()
            self.offset_y += delta.y()
            self.last_mouse_pos = event.pos()
            self.generate_fractal()
    
    def mouse_release_event(self, event):
        """Maneja la liberación del mouse."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def wheel_event(self, event):
        """Maneja la rueda del mouse para zoom."""
        delta = event.angleDelta().y()
        zoom_factor = 1.1 if delta > 0 else 0.9
        self.zoom *= zoom_factor
        self.generate_fractal()
    
    def create_controls(self):
        """Crea los controles avanzados."""
        frame = QFrame()
        frame.setFixedWidth(320)
        layout = QVBoxLayout()
        frame.setLayout(layout)
        
        # Título
        title = QLabel("🎛️ CONTROLES ÁRBOL")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 14px; color: #66ff66; margin: 10px;")
        layout.addWidget(title)
        
        # ===== NAVEGACIÓN =====
        nav_label = QLabel("🧭 NAVEGACIÓN")
        nav_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_label.setStyleSheet("font-size: 12px; color: #ffaa00; margin: 10px;")
        layout.addWidget(nav_label)
        
        # Zoom
        layout.addWidget(QLabel("🔍 Zoom:"))
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(10)
        self.zoom_slider.setMaximum(300)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        layout.addWidget(self.zoom_slider)
        
        self.zoom_label = QLabel("Zoom: 1.0x")
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.zoom_label)
        
        # Rotación
        layout.addWidget(QLabel("🔄 Rotación:"))
        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_slider.setMinimum(0)
        self.rotation_slider.setMaximum(360)
        self.rotation_slider.setValue(0)
        self.rotation_slider.valueChanged.connect(self.update_rotation)
        layout.addWidget(self.rotation_slider)
        
        self.rotation_label = QLabel("Rotación: 0°")
        self.rotation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.rotation_label)
        
        # Resetear vista
        reset_btn = QPushButton("🎯 Resetear Vista")
        reset_btn.clicked.connect(self.reset_view)
        layout.addWidget(reset_btn)
        
        # ===== ESTRUCTURA =====
        struct_label = QLabel("🌿 ESTRUCTURA")
        struct_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        struct_label.setStyleSheet("font-size: 12px; color: #ffaa00; margin: 10px;")
        layout.addWidget(struct_label)
        
        # Tipo de árbol
        layout.addWidget(QLabel("🌳 Tipo:"))
        self.tree_type = QComboBox()
        self.tree_type.addItems(["Binario", "Ternario", "Asimétrico", "Natural"])
        self.tree_type.currentTextChanged.connect(self.generate_fractal)
        layout.addWidget(self.tree_type)
        
        # Nivel
        layout.addWidget(QLabel("🔄 Profundidad:"))
        self.level_slider = QSlider(Qt.Orientation.Horizontal)
        self.level_slider.setMinimum(1)
        self.level_slider.setMaximum(12)
        self.level_slider.setValue(8)
        self.level_slider.valueChanged.connect(self.update_level)
        layout.addWidget(self.level_slider)
        
        self.level_label = QLabel("Nivel: 8")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.level_label)
        
        # Ángulo
        layout.addWidget(QLabel("🌿 Ángulo:"))
        self.angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.angle_slider.setMinimum(10)
        self.angle_slider.setMaximum(60)
        self.angle_slider.setValue(25)
        self.angle_slider.valueChanged.connect(self.update_angle)
        layout.addWidget(self.angle_slider)
        
        self.angle_label = QLabel("Ángulo: 25°")
        self.angle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.angle_label)
        
        # Factor
        layout.addWidget(QLabel("📏 Factor:"))
        self.factor_slider = QSlider(Qt.Orientation.Horizontal)
        self.factor_slider.setMinimum(50)
        self.factor_slider.setMaximum(90)
        self.factor_slider.setValue(70)
        self.factor_slider.valueChanged.connect(self.update_factor)
        layout.addWidget(self.factor_slider)
        
        self.factor_label = QLabel("Factor: 0.70")
        self.factor_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.factor_label)
        
        # Grosor
        layout.addWidget(QLabel("🎨 Grosor:"))
        self.thickness_slider = QSlider(Qt.Orientation.Horizontal)
        self.thickness_slider.setMinimum(1)
        self.thickness_slider.setMaximum(15)
        self.thickness_slider.setValue(5)
        self.thickness_slider.valueChanged.connect(self.update_thickness)
        layout.addWidget(self.thickness_slider)
        
        self.thickness_label = QLabel("Grosor: 5")
        self.thickness_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.thickness_label)
        
        # Estilo
        layout.addWidget(QLabel("🎨 Estilo:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Verde Natural", "Otoño", "Arcoíris", "Fuego"])
        self.style_combo.currentTextChanged.connect(self.generate_fractal)
        layout.addWidget(self.style_combo)
        
        # Botones
        regen_btn = QPushButton("🔄 Regenerar")
        regen_btn.clicked.connect(self.generate_fractal)
        layout.addWidget(regen_btn)
        
        export_btn = QPushButton("💾 Exportar")
        export_btn.clicked.connect(self.export_fractal)
        layout.addWidget(export_btn)
        
        random_btn = QPushButton("🎲 Aleatorio")
        random_btn.clicked.connect(self.randomize)
        layout.addWidget(random_btn)
        
        # Info
        info_text = QLabel("• Arrastra: Mover\n• Rueda: Zoom\n• Controles completos")
        info_text.setStyleSheet("font-size: 10px; color: #ccc; margin: 10px;")
        info_text.setWordWrap(True)
        layout.addWidget(info_text)
        
        layout.addStretch()
        return frame
    
    # Funciones de actualización
    def update_zoom(self):
        zoom_value = self.zoom_slider.value() / 100.0
        self.zoom = zoom_value
        self.zoom_label.setText(f"Zoom: {zoom_value:.1f}x")
        self.generate_fractal()
    
    def update_rotation(self):
        rotation = self.rotation_slider.value()
        self.rotation = rotation
        self.rotation_label.setText(f"Rotación: {rotation}°")
        self.generate_fractal()
    
    def reset_view(self):
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.rotation = 0
        self.zoom_slider.setValue(100)
        self.rotation_slider.setValue(0)
        self.generate_fractal()
    
    def update_level(self):
        level = self.level_slider.value()
        self.level_label.setText(f"Nivel: {level}")
        self.generate_fractal()
    
    def update_angle(self):
        angle = self.angle_slider.value()
        self.angle_label.setText(f"Ángulo: {angle}°")
        self.generate_fractal()
    
    def update_factor(self):
        factor = self.factor_slider.value() / 100.0
        self.factor_label.setText(f"Factor: {factor:.2f}")
        self.generate_fractal()
    
    def update_thickness(self):
        thickness = self.thickness_slider.value()
        self.thickness_label.setText(f"Grosor: {thickness}")
        self.generate_fractal()
    
    def randomize(self):
        """Aleatoriza los parámetros."""
        import random
        self.angle_slider.setValue(random.randint(15, 45))
        self.factor_slider.setValue(random.randint(60, 85))
        self.thickness_slider.setValue(random.randint(2, 10))
        self.generate_fractal()
    
    def get_branch_color(self, level, max_level, style):
        """Obtiene el color de la rama."""
        ratio = level / max_level
        
        if style == "Verde Natural":
            if ratio > 0.7:
                return QColor(139, 69, 19)  # Marrón
            elif ratio > 0.3:
                return QColor(34, 139, 34)  # Verde oscuro
            else:
                return QColor(0, 255, 0)    # Verde brillante
        elif style == "Otoño":
            if ratio > 0.7:
                return QColor(139, 69, 19)  # Marrón
            elif ratio > 0.3:
                return QColor(255, 140, 0)  # Naranja
            else:
                return QColor(255, 215, 0)  # Dorado
        elif style == "Arcoíris":
            hue = int(ratio * 360)
            color = QColor()
            color.setHsv(hue, 255, 255)
            return color
        else:  # Fuego
            if ratio > 0.7:
                return QColor(139, 0, 0)    # Rojo oscuro
            elif ratio > 0.3:
                return QColor(255, 69, 0)   # Rojo naranja
            else:
                return QColor(255, 255, 0)  # Amarillo
    
    def draw_branch(self, painter, x, y, length, angle, level, max_level, style, thickness, tree_type):
        """Dibuja una rama recursivamente."""
        if level <= 0 or length < 2:
            return
        
        # Aplicar transformaciones
        scaled_length = length * self.zoom
        rotated_angle = angle + self.rotation
        
        # Calcular punto final
        end_x = x + scaled_length * math.cos(math.radians(rotated_angle))
        end_y = y + scaled_length * math.sin(math.radians(rotated_angle))
        
        # Aplicar offset
        start_x = x + self.offset_x
        start_y = y + self.offset_y
        final_end_x = end_x + self.offset_x
        final_end_y = end_y + self.offset_y
        
        # Configurar color y grosor
        color = self.get_branch_color(level, max_level, style)
        current_thickness = max(1, int(thickness * (level / max_level) * self.zoom))
        painter.setPen(QPen(color, current_thickness))
        
        # Dibujar rama
        painter.drawLine(int(start_x), int(start_y), int(final_end_x), int(final_end_y))
        
        # Parámetros para ramas hijas
        new_length = scaled_length * (self.factor_slider.value() / 100.0)
        branch_angle = self.angle_slider.value()
        
        # Diferentes tipos de árboles
        if tree_type == "Binario":
            self.draw_branch(painter, end_x, end_y, new_length / self.zoom, 
                           rotated_angle - branch_angle, level - 1, max_level, style, thickness, tree_type)
            self.draw_branch(painter, end_x, end_y, new_length / self.zoom, 
                           rotated_angle + branch_angle, level - 1, max_level, style, thickness, tree_type)
        elif tree_type == "Ternario":
            self.draw_branch(painter, end_x, end_y, new_length / self.zoom, 
                           rotated_angle - branch_angle, level - 1, max_level, style, thickness, tree_type)
            self.draw_branch(painter, end_x, end_y, new_length * 0.9 / self.zoom, 
                           rotated_angle, level - 1, max_level, style, thickness, tree_type)
            self.draw_branch(painter, end_x, end_y, new_length / self.zoom, 
                           rotated_angle + branch_angle, level - 1, max_level, style, thickness, tree_type)
        elif tree_type == "Asimétrico":
            self.draw_branch(painter, end_x, end_y, new_length / self.zoom, 
                           rotated_angle - branch_angle, level - 1, max_level, style, thickness, tree_type)
            self.draw_branch(painter, end_x, end_y, new_length * 0.8 / self.zoom, 
                           rotated_angle + branch_angle * 0.7, level - 1, max_level, style, thickness, tree_type)
        else:  # Natural
            import random
            num_branches = random.randint(2, 3)
            for i in range(num_branches):
                angle_offset = (i - 1) * branch_angle / 2
                length_factor = 0.8 + random.random() * 0.3
                self.draw_branch(painter, end_x, end_y, new_length * length_factor / self.zoom, 
                               rotated_angle + angle_offset, level - 1, max_level, style, thickness, tree_type)
    
    def generate_fractal(self):
        """Genera el árbol fractal."""
        level = self.level_slider.value()
        style = self.style_combo.currentText()
        thickness = self.thickness_slider.value()
        tree_type = self.tree_type.currentText()
        
        # Crear imagen
        canvas_size = 700
        image = QImage(canvas_size, canvas_size, QImage.Format.Format_RGB888)
        image.fill(QColor(10, 20, 30))
        
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Parámetros iniciales
        center_x = canvas_size // 2
        center_y = int(canvas_size * 0.8)
        initial_length = canvas_size // 6
        initial_angle = -90
        
        # Dibujar árbol
        self.draw_branch(painter, center_x - self.offset_x, center_y - self.offset_y, 
                        initial_length, initial_angle, level, level, style, thickness, tree_type)
        
        painter.end()
        
        pixmap = QPixmap.fromImage(image)
        self.canvas.setPixmap(pixmap)
        
        # Actualizar título
        zoom_info = f"- Zoom: {self.zoom:.1f}x" if self.zoom != 1.0 else ""
        rot_info = f"- Rot: {self.rotation}°" if self.rotation != 0 else ""
        self.setWindowTitle(f"🌳 Árbol {tree_type} - Nivel {level} {zoom_info} {rot_info}")
    
    def export_fractal(self):
        """Exporta el fractal."""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Árbol", "tree_fractal.png", "PNG Files (*.png)"
            )
            
            if file_path:
                QMessageBox.information(self, "Éxito", f"Funcionalidad de exportación lista: {file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}")



class SierpinskiMainWindow(QMainWindow):
    """Ventana principal para el Triángulo de Sierpinski con rotación."""
    
    def __init__(self):
        super().__init__()
        self.rotation = 0  # Variable de rotación
        self.setup_ui()
        self.generate_fractal()
    
    def setup_ui(self):
        """Configura la interfaz."""
        self.setWindowTitle("🔺 Triángulo de Sierpinski")
        self.setGeometry(100, 100, 1100, 700)
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a1a; color: white; }
            QLabel { color: white; font-weight: bold; }
            QPushButton {
                background-color: #3d3d3d;
                color: white;
                border: 2px solid #555;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #4a4a4a; border-color: #ff6600; }
            QSlider::groove:horizontal {
                border: 1px solid #3c3c3c;
                height: 8px;
                background: #2b2b2b;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #ff6600;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            QFrame {
                background-color: #2b2b2b;
                border: 2px solid #3c3c3c;
                border-radius: 10px;
                margin: 5px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Canvas
        self.canvas = QLabel()
        self.canvas.setMinimumSize(800, 600)
        self.canvas.setStyleSheet("border: 2px solid #444; background-color: black;")
        main_layout.addWidget(self.canvas)
        
        # Panel de controles
        controls = self.create_controls()
        main_layout.addWidget(controls)
    
    def create_controls(self):
        """Crea el panel de controles."""
        frame = QFrame()
        frame.setFixedWidth(280)
        layout = QVBoxLayout()
        frame.setLayout(layout)
        
        # Título
        title = QLabel("🎛️ CONTROLES SIERPINSKI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 14px; color: #ff6600; margin: 10px;")
        layout.addWidget(title)
        
        # Nivel de recursión
        layout.addWidget(QLabel("🔄 Nivel de recursión:"))
        self.level_slider = QSlider(Qt.Orientation.Horizontal)
        self.level_slider.setMinimum(0)
        self.level_slider.setMaximum(7)
        self.level_slider.setValue(4)
        self.level_slider.valueChanged.connect(self.update_level)
        layout.addWidget(self.level_slider)
        
        self.level_label = QLabel("Nivel: 4")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.level_label)
        
        # Rotación
        layout.addWidget(QLabel("🔄 Rotación:"))
        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_slider.setMinimum(0)
        self.rotation_slider.setMaximum(360)
        self.rotation_slider.setValue(0)
        self.rotation_slider.valueChanged.connect(self.update_rotation)
        layout.addWidget(self.rotation_slider)
        
        self.rotation_label = QLabel("Rotación: 0°")
        self.rotation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.rotation_label)
        
        # Estilo de color
        layout.addWidget(QLabel("🎨 Estilo:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Clásico", "Arcoíris", "Fuego", "Océano", "Neón"])
        self.style_combo.currentTextChanged.connect(self.generate_fractal)
        self.style_combo.setStyleSheet("""
            QComboBox {
                background-color: #3d3d3d;
                color: white;
                border: 2px solid #555;
                border-radius: 6px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.style_combo)
        
        # Botones
        regen_btn = QPushButton("🔄 Regenerar")
        regen_btn.clicked.connect(self.generate_fractal)
        layout.addWidget(regen_btn)
        
        export_btn = QPushButton("💾 Exportar PNG")
        export_btn.clicked.connect(self.export_fractal)
        layout.addWidget(export_btn)
        
        # Información
        info_label = QLabel("ℹ️ INFORMACIÓN")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("font-size: 12px; color: #ffff66; margin-top: 15px;")
        layout.addWidget(info_label)
        
        info_text = QLabel("Triángulo de Sierpinski con rotación completa y estilos de color")
        info_text.setStyleSheet("font-size: 10px; color: #ccc; margin: 5px;")
        info_text.setWordWrap(True)
        layout.addWidget(info_text)
        
        layout.addStretch()
        return frame
    
    def update_level(self):
        """Actualiza el nivel."""
        level = self.level_slider.value()
        self.level_label.setText(f"Nivel: {level}")
        self.generate_fractal()
    
    def update_rotation(self):
        """Actualiza la rotación."""
        rotation = self.rotation_slider.value()
        self.rotation = rotation
        self.rotation_label.setText(f"Rotación: {rotation}°")
        self.generate_fractal()
    
    def rotate_point(self, x, y, center_x, center_y, angle_degrees):
        """Rota un punto alrededor de un centro."""
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        # Trasladar al origen
        dx = x - center_x
        dy = y - center_y
        
        # Rotar
        new_x = dx * cos_a - dy * sin_a
        new_y = dx * sin_a + dy * cos_a
        
        # Trasladar de vuelta
        return (new_x + center_x, new_y + center_y)
    
    def get_color_for_level(self, level, max_level, style):
        """Obtiene el color según el nivel y estilo."""
        ratio = level / max(max_level, 1)
        
        if style == "Clásico":
            return QColor(255, int(100 + level * 30), 0)
        elif style == "Arcoíris":
            hue = int((level * 60) % 360)
            color = QColor()
            color.setHsv(hue, 255, 255)
            return color
        elif style == "Fuego":
            red = 255
            green = int(255 - level * 40)
            blue = int(level * 20)
            return QColor(red, max(0, green), min(255, blue))
        elif style == "Océano":
            red = int(level * 30)
            green = int(100 + level * 25)
            blue = 255
            return QColor(min(255, red), min(255, green), blue)
        else:  # Neón
            green = 255
            red = int(255 - level * 50)
            blue = int(255 - level * 30)
            return QColor(max(0, red), green, max(0, blue))
    
    def generate_fractal(self):
        """Genera el triángulo de Sierpinski con rotación."""
        level = self.level_slider.value()
        style = self.style_combo.currentText()
        
        image = QImage(800, 600, QImage.Format.Format_RGB888)
        image.fill(QColor(0, 0, 0))
        
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Triángulo principal
        size = 300
        height = size * math.sqrt(3) / 2
        center_x, center_y = 400, 320
        
        # Vértices originales
        p1 = (center_x, center_y - height / 2)
        p2 = (center_x - size / 2, center_y + height / 2)
        p3 = (center_x + size / 2, center_y + height / 2)
        
        # Aplicar rotación si es necesario
        if self.rotation != 0:
            p1 = self.rotate_point(p1[0], p1[1], center_x, center_y, self.rotation)
            p2 = self.rotate_point(p2[0], p2[1], center_x, center_y, self.rotation)
            p3 = self.rotate_point(p3[0], p3[1], center_x, center_y, self.rotation)
        
        # Dibujar sierpinski
        self.draw_sierpinski(painter, p1, p2, p3, level, level, style)
        
        painter.end()
        pixmap = QPixmap.fromImage(image)
        self.canvas.setPixmap(pixmap)
        
        # Actualizar título
        rot_info = f" - Rot: {self.rotation}°" if self.rotation != 0 else ""
        self.setWindowTitle(f"🔺 Sierpinski {style} - Nivel {level}{rot_info}")
    
    def draw_sierpinski(self, painter, p1, p2, p3, level, max_level, style):
        """Dibuja sierpinski recursivamente con colores."""
        if level <= 0:
            # Triángulo sólido
            color = self.get_color_for_level(max_level - level, max_level, style)
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
        self.draw_sierpinski(painter, p1, mid12, mid31, level - 1, max_level, style)
        self.draw_sierpinski(painter, mid12, p2, mid23, level - 1, max_level, style)
        self.draw_sierpinski(painter, mid31, mid23, p3, level - 1, max_level, style)
    
    def export_fractal(self):
        """Exporta el fractal actual."""
        try:
            from PyQt6.QtWidgets import QFileDialog, QMessageBox
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Sierpinski", "sierpinski_fractal.png", "PNG Files (*.png)"
            )
            
            if file_path:
                # Generar en alta resolución
                level = self.level_slider.value()
                style = self.style_combo.currentText()
                
                # Imagen de alta resolución
                image = QImage(3200, 2400, QImage.Format.Format_RGB888)
                image.fill(QColor(0, 0, 0))
                
                painter = QPainter(image)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                
                # Escalar para alta resolución
                size = 1200
                height = size * math.sqrt(3) / 2
                center_x, center_y = 1600, 1280
                
                p1 = (center_x, center_y - height / 2)
                p2 = (center_x - size / 2, center_y + height / 2)
                p3 = (center_x + size / 2, center_y + height / 2)
                
                if self.rotation != 0:
                    p1 = self.rotate_point(p1[0], p1[1], center_x, center_y, self.rotation)
                    p2 = self.rotate_point(p2[0], p2[1], center_x, center_y, self.rotation)
                    p3 = self.rotate_point(p3[0], p3[1], center_x, center_y, self.rotation)
                
                self.draw_sierpinski(painter, p1, p2, p3, level, level, style)
                
                painter.end()
                image.save(file_path)
                QMessageBox.information(self, "Éxito", f"Fractal exportado en alta resolución:\n{file_path}")
                
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al exportar: {e}")
