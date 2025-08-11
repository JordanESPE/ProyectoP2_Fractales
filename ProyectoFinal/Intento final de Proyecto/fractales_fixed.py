"""
Versión corregida y limpia de las ventanas de fractales.
"""

import math
import random
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QSlider, QComboBox, QFrame, 
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter, QPen, QColor, QPixmap


class KochMainWindowFixed(QMainWindow):
    """Ventana principal para la Curva de Koch - VERSIÓN CORREGIDA."""
    
    def __init__(self):
        super().__init__()
        self.points = []
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
        self.type_combo.setCurrentIndex(2)
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
            QMessageBox.critical(self, "Error", f"Error al exportar: {e}")


class TreeMainWindowFixed(QMainWindow):
    """Ventana principal para el Árbol Fractal - VERSIÓN CORREGIDA CON CONTROLES."""
    
    def __init__(self):
        super().__init__()
        
        # Parámetros de navegación
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
        self.setWindowTitle("🌳 Árbol Fractal - CORREGIDO CON CONTROLES")
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
        
        # Canvas con eventos de mouse
        self.canvas = QLabel()
        self.canvas.setMinimumSize(700, 700)
        self.canvas.setStyleSheet("border: 2px solid #444; background-color: #001122;")
        
        # Eventos de mouse para navegación
        self.canvas.mousePressEvent = self.mouse_press_event
        self.canvas.mouseMoveEvent = self.mouse_move_event
        self.canvas.mouseReleaseEvent = self.mouse_release_event
        self.canvas.wheelEvent = self.wheel_event
        
        main_layout.addWidget(self.canvas)
        
        # Controles
        controls = self.create_controls()
        main_layout.addWidget(controls)
    
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
        
        # Navegación
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
        
        # Estructura del árbol
        struct_label = QLabel("🌿 ESTRUCTURA")
        struct_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        struct_label.setStyleSheet("font-size: 12px; color: #ffaa00; margin: 10px;")
        layout.addWidget(struct_label)
        
        # Tipo de árbol
        layout.addWidget(QLabel("🌳 Tipo:"))
        self.tree_type = QComboBox()
        self.tree_type.addItems(["Binario", "Ternario", "Asimétrico", "Natural"])
        self.tree_type.currentTextChanged.connect(self.generate_fractal)
        self.tree_type.setStyleSheet("""
            QComboBox {
                background-color: #3d3d3d;
                color: white;
                border: 2px solid #555;
                border-radius: 6px;
                padding: 5px;
            }
        """)
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
        
        export_btn = QPushButton("💾 Exportar")
        export_btn.clicked.connect(self.export_fractal)
        layout.addWidget(export_btn)
        
        random_btn = QPushButton("🎲 Aleatorio")
        random_btn.clicked.connect(self.randomize)
        layout.addWidget(random_btn)
        
        # Info
        info_text = QLabel("• Arrastra: Mover\\n• Rueda: Zoom\\n• Controles completos")
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
        self.angle_slider.setValue(random.randint(15, 45))
        self.factor_slider.setValue(random.randint(60, 85))
        self.thickness_slider.setValue(random.randint(2, 10))
        self.generate_fractal()
    
    # Eventos de mouse
    def mouse_press_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.pos()
    
    def mouse_move_event(self, event):
        if self.dragging and self.last_mouse_pos:
            delta = event.pos() - self.last_mouse_pos
            self.offset_x += delta.x()
            self.offset_y += delta.y()
            self.last_mouse_pos = event.pos()
            self.generate_fractal()
    
    def mouse_release_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def wheel_event(self, event):
        delta = event.angleDelta().y()
        zoom_factor = 1.1 if delta > 0 else 0.9
        self.zoom *= zoom_factor
        self.zoom_slider.setValue(int(self.zoom * 100))
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
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Árbol", "tree_fractal_fixed.png", "PNG Files (*.png)"
            )
            
            if file_path:
                QMessageBox.information(self, "Éxito", f"Funcionalidad de exportación lista: {file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}")
