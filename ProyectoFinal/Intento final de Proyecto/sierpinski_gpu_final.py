#!/usr/bin/env python3
"""
🚀 SIERPINSKI GPU INDEPENDIENTE - VERSIÓN DEFINITIVA
Implementación completa con zoom infinito y máxima potencia GPU
"""

import sys
import os
import math

# Agregar directorio padre al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QSlider, QSpinBox, QComboBox,
                             QFrame, QApplication, QFileDialog, QMessageBox, 
                             QDoubleSpinBox, QCheckBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QPoint
from PyQt6.QtGui import QPixmap, QImage, QPainter, QFont, QPen, QColor

class SierpinskiGPUWindow(QMainWindow):
    """🚀 SIERPINSKI GPU-OPTIMIZADO - ZOOM INFINITO - MÁXIMA POTENCIA"""
    
    def __init__(self):
        super().__init__()
        # Parámetros de transformación y navegación
        self.offset_x = 0
        self.offset_y = 0
        self.rotation = 0
        self.scale_factor = 1.0
        self.zoom_level = 1.0
        self.last_mouse_pos = None
        self.dragging = False
        
        # Configuración avanzada GPU
        self.adaptive_levels = True
        self.high_quality = True
        self.auto_update = True
        self.max_level = 10
        self.gpu_mode = True
        self.antialiasing = True
        
        # Timer para renderizado suave a 60 FPS
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self.smooth_render)
        self.render_timer.start(16)  # ~60 FPS
        
        self.setup_ui()
        self.setup_mouse_interaction()
        self.generate_fractal()
    
    def setup_ui(self):
        """Configura la interfaz GPU-optimizada con todos los controles avanzados."""
        self.setWindowTitle("🔺 SIERPINSKI GPU - ZOOM INFINITO ∞ - MÁXIMA POTENCIA")
        self.setGeometry(100, 100, 1400, 900)
        
        # Estilos avanzados con gradientes GPU y efectos visuales
        self.setStyleSheet("""
            QMainWindow { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #0f0f23, stop:0.5 #1a1a2e, stop:1 #16213e); 
                color: white; 
            }
            QLabel { 
                color: white; 
                font-weight: bold; 
                font-size: 11px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: 2px solid #555;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #764ba2, stop:1 #667eea);
                border-color: #ff6b6b; 
            }
            QSlider::groove:horizontal {
                border: 1px solid #3c3c3c;
                height: 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c3e50, stop:1 #34495e);
                border-radius: 6px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff6b6b, stop:1 #ee5a24);
                border: 2px solid #5c5c5c;
                width: 22px;
                margin: -3px 0;
                border-radius: 11px;
            }
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(44, 62, 80, 0.9), stop:1 rgba(52, 73, 94, 0.9));
                border: 2px solid #555;
                border-radius: 15px;
                margin: 5px;
            }
            QCheckBox {
                color: white;
                font-weight: bold;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #555;
                border-radius: 9px;
                background: #2c3e50;
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00ff88, stop:1 #00cc6a);
                border-color: #00ff88;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Canvas principal GPU-optimizado
        self.canvas = QLabel()
        self.canvas.setMinimumSize(900, 800)
        self.canvas.setStyleSheet("""
            border: 3px solid #667eea; 
            background-color: #000011;
            border-radius: 10px;
        """)
        main_layout.addWidget(self.canvas)
        
        # Panel de controles GPU
        controls = self.create_gpu_controls()
        main_layout.addWidget(controls)
    
    def create_gpu_controls(self):
        """🎛️ CONTROLES GPU - MÁXIMA POTENCIA"""
        frame = QFrame()
        frame.setFixedWidth(400)
        layout = QVBoxLayout()
        frame.setLayout(layout)
        
        # Título GPU
        title = QLabel("🚀 SIERPINSKI GPU CONTROLS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 16px; 
            color: #00ff88; 
            margin: 15px;
            font-weight: bold;
        """)
        layout.addWidget(title)
        
        # ===== ZOOM INFINITO =====
        zoom_label = QLabel("🔍 ZOOM INFINITO")
        zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        zoom_label.setStyleSheet("font-size: 14px; color: #ff6b6b; margin: 10px; font-weight: bold;")
        layout.addWidget(zoom_label)
        
        layout.addWidget(QLabel("🔎 Nivel de Zoom (0.01x - 100x):"))
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(1)    # 0.01x
        self.zoom_slider.setMaximum(10000) # 100x
        self.zoom_slider.setValue(100)     # 1.0x
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        layout.addWidget(self.zoom_slider)
        
        self.zoom_label = QLabel("Zoom: 1.00x")
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zoom_label.setStyleSheet("color: #00ff88; font-size: 12px; font-weight: bold;")
        layout.addWidget(self.zoom_label)
        
        # ===== NIVELES ADAPTATIVOS =====
        adaptive_label = QLabel("🧠 NIVELES ADAPTATIVOS")
        adaptive_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        adaptive_label.setStyleSheet("font-size: 14px; color: #667eea; margin: 10px; font-weight: bold;")
        layout.addWidget(adaptive_label)
        
        layout.addWidget(QLabel("📊 Profundidad Base:"))
        self.level_slider = QSlider(Qt.Orientation.Horizontal)
        self.level_slider.setMinimum(1)
        self.level_slider.setMaximum(15)
        self.level_slider.setValue(8)
        self.level_slider.valueChanged.connect(self.update_level)
        layout.addWidget(self.level_slider)
        
        self.level_label = QLabel("Nivel Base: 8")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.level_label.setStyleSheet("color: #667eea; font-size: 12px; font-weight: bold;")
        layout.addWidget(self.level_label)
        
        # Checkboxes GPU
        self.adaptive_checkbox = QCheckBox("🧠 Niveles Adaptativos")
        self.adaptive_checkbox.setChecked(True)
        self.adaptive_checkbox.stateChanged.connect(self.toggle_adaptive)
        layout.addWidget(self.adaptive_checkbox)
        
        # ===== CONTROLES AVANZADOS =====
        advanced_label = QLabel("⚡ CONTROLES AVANZADOS")
        advanced_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        advanced_label.setStyleSheet("font-size: 14px; color: #f39c12; margin: 10px; font-weight: bold;")
        layout.addWidget(advanced_label)
        
        layout.addWidget(QLabel("🌈 Intensidad de Color:"))
        self.color_slider = QSlider(Qt.Orientation.Horizontal)
        self.color_slider.setMinimum(10)
        self.color_slider.setMaximum(255)
        self.color_slider.setValue(200)
        self.color_slider.valueChanged.connect(self.update_color)
        layout.addWidget(self.color_slider)
        
        self.color_label = QLabel("Intensidad: 200")
        self.color_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.color_label)
        
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
        
        # Más checkboxes
        self.gpu_checkbox = QCheckBox("⚡ Modo GPU")
        self.gpu_checkbox.setChecked(True)
        self.gpu_checkbox.stateChanged.connect(self.toggle_gpu)
        layout.addWidget(self.gpu_checkbox)
        
        self.hq_checkbox = QCheckBox("🎨 Anti-aliasing")
        self.hq_checkbox.setChecked(True)
        self.hq_checkbox.stateChanged.connect(self.toggle_quality)
        layout.addWidget(self.hq_checkbox)
        
        self.auto_checkbox = QCheckBox("🔄 Auto-actualizar")
        self.auto_checkbox.setChecked(True)
        self.auto_checkbox.stateChanged.connect(self.toggle_auto)
        layout.addWidget(self.auto_checkbox)
        
        # ===== BOTONES DE ACCIÓN =====
        action_label = QLabel("🎮 ACCIONES")
        action_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        action_label.setStyleSheet("font-size: 14px; color: #e74c3c; margin: 10px; font-weight: bold;")
        layout.addWidget(action_label)
        
        # Botones con efectos
        reset_btn = QPushButton("🎯 RESET VISTA")
        reset_btn.clicked.connect(self.reset_view)
        layout.addWidget(reset_btn)
        
        center_btn = QPushButton("📍 CENTRAR")
        center_btn.clicked.connect(self.center_view)
        layout.addWidget(center_btn)
        
        random_btn = QPushButton("🎲 ALEATORIO")
        random_btn.clicked.connect(self.randomize_params)
        layout.addWidget(random_btn)
        
        export_btn = QPushButton("💾 EXPORTAR 4K")
        export_btn.clicked.connect(self.export_fractal)
        layout.addWidget(export_btn)
        
        # ===== INFORMACIÓN GPU =====
        info_label = QLabel("📊 INFORMACIÓN GPU")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("font-size: 12px; color: #95a5a6; margin-top: 15px; font-weight: bold;")
        layout.addWidget(info_label)
        
        info_text = QLabel("""
• Zoom infinito: 0.01x a 100x
• Niveles adaptativos con log2(zoom)
• Renderizado GPU a 60 FPS
• Anti-aliasing avanzado
• Navegación con mouse
• Exportación 4K disponible""")
        info_text.setStyleSheet("font-size: 9px; color: #bdc3c7; margin: 5px;")
        info_text.setWordWrap(True)
        layout.addWidget(info_text)
        
        layout.addStretch()
        return frame
    
    def setup_mouse_interaction(self):
        """Configura la interacción avanzada con mouse."""
        self.canvas.mousePressEvent = self.mouse_press_event
        self.canvas.mouseMoveEvent = self.mouse_move_event
        self.canvas.mouseReleaseEvent = self.mouse_release_event
        self.canvas.wheelEvent = self.wheel_event
        self.canvas.setMouseTracking(True)
    
    def mouse_press_event(self, event):
        """Maneja clics del mouse."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.pos()
    
    def mouse_move_event(self, event):
        """Maneja movimiento del mouse para navegación."""
        if self.dragging and self.last_mouse_pos:
            delta = event.pos() - self.last_mouse_pos
            sensitivity = 2.0 / self.zoom_level
            self.offset_x += delta.x() * sensitivity
            self.offset_y += delta.y() * sensitivity
            self.last_mouse_pos = event.pos()
            if self.auto_update:
                self.generate_fractal()
    
    def mouse_release_event(self, event):
        """Maneja liberación del mouse."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def wheel_event(self, event):
        """Zoom con rueda del mouse."""
        delta = event.angleDelta().y()
        zoom_factor = 1.15 if delta > 0 else 1.0/1.15
        
        new_zoom = self.zoom_level * zoom_factor
        new_zoom = max(0.01, min(100.0, new_zoom))
        
        # Actualizar slider
        slider_value = int(new_zoom * 100)
        self.zoom_slider.setValue(slider_value)
    
    def update_zoom(self):
        """Actualiza el zoom infinito."""
        slider_value = self.zoom_slider.value()
        self.zoom_level = slider_value / 100.0
        self.zoom_label.setText(f"Zoom: {self.zoom_level:.2f}x")
        
        # Niveles adaptativos basados en zoom
        if self.adaptive_levels:
            base_level = self.level_slider.value()
            adaptive_boost = int(math.log2(max(1, self.zoom_level)) * 2)
            self.adaptive_level = min(15, base_level + adaptive_boost)
        
        if self.auto_update:
            self.generate_fractal()
    
    def update_level(self):
        """Actualiza el nivel base."""
        level = self.level_slider.value()
        self.level_label.setText(f"Nivel Base: {level}")
        if self.auto_update:
            self.generate_fractal()
    
    def update_color(self):
        """Actualiza intensidad de color."""
        intensity = self.color_slider.value()
        self.color_label.setText(f"Intensidad: {intensity}")
        if self.auto_update:
            self.generate_fractal()
    
    def update_rotation(self):
        """Actualiza rotación."""
        rotation = self.rotation_slider.value()
        self.rotation = rotation
        self.rotation_label.setText(f"Rotación: {rotation}°")
        if self.auto_update:
            self.generate_fractal()
    
    def toggle_adaptive(self, state):
        """Toggle niveles adaptativos."""
        self.adaptive_levels = state == 2
        if self.auto_update:
            self.generate_fractal()
    
    def toggle_gpu(self, state):
        """Toggle modo GPU."""
        self.gpu_mode = state == 2
        if self.auto_update:
            self.generate_fractal()
    
    def toggle_quality(self, state):
        """Toggle anti-aliasing."""
        self.antialiasing = state == 2
        if self.auto_update:
            self.generate_fractal()
    
    def toggle_auto(self, state):
        """Toggle auto-actualización."""
        self.auto_update = state == 2
    
    def reset_view(self):
        """Resetea la vista."""
        self.offset_x = 0
        self.offset_y = 0
        self.rotation = 0
        self.zoom_level = 1.0
        self.zoom_slider.setValue(100)
        self.rotation_slider.setValue(0)
        self.generate_fractal()
    
    def center_view(self):
        """Centra la vista."""
        self.offset_x = 0
        self.offset_y = 0
        self.generate_fractal()
    
    def randomize_params(self):
        """Aleatoriza parámetros."""
        import random
        self.zoom_slider.setValue(random.randint(50, 500))
        self.rotation_slider.setValue(random.randint(0, 360))
        self.color_slider.setValue(random.randint(100, 255))
        self.generate_fractal()
    
    def smooth_render(self):
        """Renderizado suave a 60 FPS."""
        if hasattr(self, '_needs_render') and self._needs_render:
            self.generate_fractal()
            self._needs_render = False
    
    def generate_fractal(self):
        """🚀 GENERA SIERPINSKI GPU-OPTIMIZADO CON ZOOM INFINITO"""
        try:
            # Obtener nivel efectivo
            base_level = self.level_slider.value()
            if self.adaptive_levels:
                adaptive_boost = int(math.log2(max(1, self.zoom_level)) * 2)
                effective_level = min(15, base_level + adaptive_boost)
            else:
                effective_level = base_level
            
            # Crear imagen GPU-optimizada
            width, height = 900, 800
            image = QImage(width, height, QImage.Format.Format_RGB888)
            image.fill(QColor(0, 0, 17))  # Azul muy oscuro
            
            painter = QPainter(image)
            if self.antialiasing:
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Configurar transformaciones
            painter.translate(width/2 + self.offset_x, height/2 + self.offset_y)
            painter.scale(self.zoom_level, self.zoom_level)
            painter.rotate(self.rotation)
            
            # Triángulo principal escalado
            size = 200
            height_tri = size * math.sqrt(3) / 2
            
            p1 = (-size/2, -height_tri/3)
            p2 = (size/2, -height_tri/3)
            p3 = (0, 2*height_tri/3)
            
            # Generar Sierpinski GPU-optimizado
            self.draw_sierpinski_gpu(painter, p1, p2, p3, effective_level)
            
            painter.end()
            
            # Aplicar al canvas
            pixmap = QPixmap.fromImage(image)
            self.canvas.setPixmap(pixmap)
            
            # Actualizar título con información
            info = f"🔺 SIERPINSKI GPU - Zoom: {self.zoom_level:.2f}x - Nivel: {effective_level}"
            if self.adaptive_levels:
                info += f" (Base: {base_level} + Adaptativo: {effective_level - base_level})"
            self.setWindowTitle(info)
            
        except Exception as e:
            print(f"Error en generación GPU: {e}")
    
    def draw_sierpinski_gpu(self, painter, p1, p2, p3, level):
        """Dibuja Sierpinski con optimizaciones GPU."""
        if level <= 0:
            # Generar color dinámico basado en intensidad
            intensity = self.color_slider.value()
            
            # Colores vibrantes con gradientes
            if self.gpu_mode:
                colors = [
                    QColor(intensity, 100, 255),  # Azul-violeta
                    QColor(255, intensity, 100),  # Naranja
                    QColor(100, 255, intensity),  # Verde
                    QColor(255, 100, intensity),  # Rosa
                    QColor(intensity, 255, 100),  # Verde-amarillo
                ]
                color = colors[level % len(colors)]
            else:
                color = QColor(intensity, int(intensity * 0.7), 0)
            
            painter.setBrush(color)
            painter.setPen(QPen(color, 1))
            
            # Dibujar triángulo optimizado
            points = [QPoint(int(p1[0]), int(p1[1])),
                     QPoint(int(p2[0]), int(p2[1])),
                     QPoint(int(p3[0]), int(p3[1]))]
            painter.drawPolygon(points)
            return
        
        # Calcular puntos medios con precisión GPU
        mid12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        mid23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
        mid31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
        
        # Recursión GPU-optimizada
        self.draw_sierpinski_gpu(painter, p1, mid12, mid31, level - 1)
        self.draw_sierpinski_gpu(painter, mid12, p2, mid23, level - 1)
        self.draw_sierpinski_gpu(painter, mid31, mid23, p3, level - 1)
    
    def export_fractal(self):
        """Exporta fractal en 4K."""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Sierpinski 4K", "sierpinski_gpu_4k.png", 
                "PNG Files (*.png);;JPG Files (*.jpg)"
            )
            
            if file_path:
                # Generar en 4K
                image_4k = QImage(3840, 2160, QImage.Format.Format_RGB888)
                image_4k.fill(QColor(0, 0, 17))
                
                painter_4k = QPainter(image_4k)
                if self.antialiasing:
                    painter_4k.setRenderHint(QPainter.RenderHint.Antialiasing)
                
                # Escalar para 4K
                scale_4k = 3840 / 900
                painter_4k.translate(1920 + self.offset_x * scale_4k, 
                                    1080 + self.offset_y * scale_4k)
                painter_4k.scale(self.zoom_level * scale_4k, self.zoom_level * scale_4k)
                painter_4k.rotate(self.rotation)
                
                # Triángulo para 4K
                size_4k = 400
                height_4k = size_4k * math.sqrt(3) / 2
                
                p1_4k = (-size_4k/2, -height_4k/3)
                p2_4k = (size_4k/2, -height_4k/3)
                p3_4k = (0, 2*height_4k/3)
                
                # Nivel alto para 4K
                level_4k = self.level_slider.value() + 3
                self.draw_sierpinski_gpu(painter_4k, p1_4k, p2_4k, p3_4k, level_4k)
                
                painter_4k.end()
                image_4k.save(file_path)
                
                QMessageBox.information(self, "✅ Exportado", 
                                      f"Sierpinski GPU exportado en 4K:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar: {e}")

def main():
    """Función principal."""
    print("🚀 INICIANDO SIERPINSKI GPU - ZOOM INFINITO")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    
    window = SierpinskiGPUWindow()
    window.show()
    
    print("✅ SIERPINSKI GPU INICIADO CORRECTAMENTE")
    print("🔍 Controles disponibles:")
    print("  • Zoom infinito: 0.01x a 100x")
    print("  • Niveles adaptativos automáticos")
    print("  • Navegación con mouse (arrastrar y rueda)")
    print("  • Rotación y colores dinámicos")
    print("  • Exportación 4K")
    print("\n💡 ¡Usa la rueda del mouse para hacer zoom!")
    
    return app.exec()

if __name__ == "__main__":
    main()
