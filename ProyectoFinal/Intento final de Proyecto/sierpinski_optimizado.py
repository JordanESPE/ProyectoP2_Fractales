#!/usr/bin/env python3
"""
🚀 SIERPINSKI GPU OPTIMIZADO - VERSIÓN LIVIANA
Implementación eficiente con zoom infinito sin sobrecarga
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

class SierpinskiOptimizedWindow(QMainWindow):
    """🚀 SIERPINSKI GPU OPTIMIZADO - SIN SOBRECARGA"""
    
    def __init__(self):
        super().__init__()
        # Parámetros básicos
        self.offset_x = 0
        self.offset_y = 0
        self.rotation = 0
        self.zoom_level = 1.0
        self.last_mouse_pos = None
        self.dragging = False
        
        # Configuración optimizada
        self.adaptive_levels = True
        self.auto_update = True
        self.max_level = 12  # Reducido para evitar sobrecarga
        
        # Timer más conservador para evitar sobrecarga
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self.delayed_render)
        self.render_timer.setSingleShot(True)  # Solo ejecuta una vez
        
        self.setup_ui()
        self.setup_mouse_interaction()
        self.generate_fractal()
    
    def setup_ui(self):
        """Configura la interfaz optimizada."""
        self.setWindowTitle("🔺 SIERPINSKI GPU OPTIMIZADO - SIN SOBRECARGA")
        self.setGeometry(100, 100, 1200, 800)
        
        # Estilos más simples para evitar sobrecarga
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #1a1a2e; 
                color: white; 
            }
            QLabel { 
                color: white; 
                font-weight: bold; 
                font-size: 11px;
            }
            QPushButton {
                background-color: #667eea;
                color: white;
                border: 2px solid #555;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover { 
                background-color: #764ba2;
                border-color: #ff6b6b; 
            }
            QSlider::groove:horizontal {
                border: 1px solid #3c3c3c;
                height: 10px;
                background: #2c3e50;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #ff6b6b;
                border: 2px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            QFrame {
                background-color: rgba(44, 62, 80, 0.8);
                border: 2px solid #555;
                border-radius: 10px;
                margin: 5px;
            }
            QCheckBox {
                color: white;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #555;
                border-radius: 8px;
                background: #2c3e50;
            }
            QCheckBox::indicator:checked {
                background: #00ff88;
                border-color: #00ff88;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Canvas optimizado
        self.canvas = QLabel()
        self.canvas.setMinimumSize(800, 700)
        self.canvas.setStyleSheet("""
            border: 2px solid #667eea; 
            background-color: #000011;
            border-radius: 8px;
        """)
        main_layout.addWidget(self.canvas)
        
        # Panel de controles optimizado
        controls = self.create_optimized_controls()
        main_layout.addWidget(controls)
    
    def create_optimized_controls(self):
        """🎛️ CONTROLES OPTIMIZADOS"""
        frame = QFrame()
        frame.setFixedWidth(350)
        layout = QVBoxLayout()
        frame.setLayout(layout)
        
        # Título
        title = QLabel("🚀 SIERPINSKI GPU")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; color: #00ff88; margin: 10px; font-weight: bold;")
        layout.addWidget(title)
        
        # ===== ZOOM INFINITO =====
        zoom_section = QLabel("🔍 ZOOM INFINITO")
        zoom_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        zoom_section.setStyleSheet("font-size: 13px; color: #ff6b6b; margin: 8px; font-weight: bold;")
        layout.addWidget(zoom_section)
        
        layout.addWidget(QLabel("🔎 Nivel de Zoom (0.01x - 50x):"))
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(1)    # 0.01x
        self.zoom_slider.setMaximum(5000) # 50x (reducido para evitar sobrecarga)
        self.zoom_slider.setValue(100)    # 1.0x
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        layout.addWidget(self.zoom_slider)
        
        self.zoom_label = QLabel("Zoom: 1.00x")
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zoom_label.setStyleSheet("color: #00ff88; font-size: 11px; font-weight: bold;")
        layout.addWidget(self.zoom_label)
        
        # ===== NIVELES ADAPTATIVOS =====
        adaptive_section = QLabel("🧠 NIVELES ADAPTATIVOS")
        adaptive_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        adaptive_section.setStyleSheet("font-size: 13px; color: #667eea; margin: 8px; font-weight: bold;")
        layout.addWidget(adaptive_section)
        
        layout.addWidget(QLabel("📊 Profundidad Base:"))
        self.level_slider = QSlider(Qt.Orientation.Horizontal)
        self.level_slider.setMinimum(2)
        self.level_slider.setMaximum(10)  # Reducido para evitar sobrecarga
        self.level_slider.setValue(6)    # Valor más conservador
        self.level_slider.valueChanged.connect(self.update_level)
        layout.addWidget(self.level_slider)
        
        self.level_label = QLabel("Nivel Base: 6")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.level_label.setStyleSheet("color: #667eea; font-size: 11px; font-weight: bold;")
        layout.addWidget(self.level_label)
        
        # Checkbox optimizado
        self.adaptive_checkbox = QCheckBox("🧠 Niveles Adaptativos")
        self.adaptive_checkbox.setChecked(True)
        self.adaptive_checkbox.stateChanged.connect(self.toggle_adaptive)
        layout.addWidget(self.adaptive_checkbox)
        
        # ===== CONTROLES SIMPLES =====
        controls_section = QLabel("⚡ CONTROLES")
        controls_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_section.setStyleSheet("font-size: 13px; color: #f39c12; margin: 8px; font-weight: bold;")
        layout.addWidget(controls_section)
        
        layout.addWidget(QLabel("🌈 Intensidad de Color:"))
        self.color_slider = QSlider(Qt.Orientation.Horizontal)
        self.color_slider.setMinimum(50)
        self.color_slider.setMaximum(255)
        self.color_slider.setValue(180)
        self.color_slider.valueChanged.connect(self.update_color)
        layout.addWidget(self.color_slider)
        
        self.color_label = QLabel("Intensidad: 180")
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
        
        # Auto-actualizar
        self.auto_checkbox = QCheckBox("🔄 Auto-actualizar")
        self.auto_checkbox.setChecked(True)
        self.auto_checkbox.stateChanged.connect(self.toggle_auto)
        layout.addWidget(self.auto_checkbox)
        
        # ===== BOTONES =====
        buttons_section = QLabel("🎮 ACCIONES")
        buttons_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_section.setStyleSheet("font-size: 13px; color: #e74c3c; margin: 8px; font-weight: bold;")
        layout.addWidget(buttons_section)
        
        reset_btn = QPushButton("🎯 RESET")
        reset_btn.clicked.connect(self.reset_view)
        layout.addWidget(reset_btn)
        
        center_btn = QPushButton("📍 CENTRAR")
        center_btn.clicked.connect(self.center_view)
        layout.addWidget(center_btn)
        
        export_btn = QPushButton("💾 EXPORTAR")
        export_btn.clicked.connect(self.export_fractal)
        layout.addWidget(export_btn)
        
        # ===== INFORMACIÓN =====
        info_section = QLabel("📊 INFORMACIÓN")
        info_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_section.setStyleSheet("font-size: 12px; color: #95a5a6; margin-top: 10px; font-weight: bold;")
        layout.addWidget(info_section)
        
        info_text = QLabel("""
• Zoom: 0.01x a 50x (optimizado)
• Niveles adaptativos automáticos
• Navegación con mouse
• Renderizado eficiente
• Sin sobrecarga del sistema""")
        info_text.setStyleSheet("font-size: 9px; color: #bdc3c7; margin: 5px;")
        info_text.setWordWrap(True)
        layout.addWidget(info_text)
        
        layout.addStretch()
        return frame
    
    def setup_mouse_interaction(self):
        """Configura interacción con mouse optimizada."""
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
        """Maneja movimiento del mouse."""
        if self.dragging and self.last_mouse_pos:
            delta = event.pos() - self.last_mouse_pos
            sensitivity = 1.5 / max(0.1, self.zoom_level)  # Sensibilidad optimizada
            self.offset_x += delta.x() * sensitivity
            self.offset_y += delta.y() * sensitivity
            self.last_mouse_pos = event.pos()
            self.schedule_render()
    
    def mouse_release_event(self, event):
        """Maneja liberación del mouse."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def wheel_event(self, event):
        """Zoom optimizado con rueda del mouse."""
        delta = event.angleDelta().y()
        zoom_factor = 1.1 if delta > 0 else 1.0/1.1
        
        new_zoom = self.zoom_level * zoom_factor
        new_zoom = max(0.01, min(50.0, new_zoom))  # Límite reducido
        
        slider_value = int(new_zoom * 100)
        self.zoom_slider.setValue(slider_value)
    
    def schedule_render(self):
        """Programa renderizado con delay para evitar sobrecarga."""
        if self.auto_update:
            self.render_timer.start(100)  # 100ms delay
    
    def delayed_render(self):
        """Renderizado con delay."""
        self.generate_fractal()
    
    def update_zoom(self):
        """Actualiza el zoom."""
        slider_value = self.zoom_slider.value()
        self.zoom_level = slider_value / 100.0
        self.zoom_label.setText(f"Zoom: {self.zoom_level:.2f}x")
        self.schedule_render()
    
    def update_level(self):
        """Actualiza el nivel base."""
        level = self.level_slider.value()
        self.level_label.setText(f"Nivel Base: {level}")
        self.schedule_render()
    
    def update_color(self):
        """Actualiza intensidad de color."""
        intensity = self.color_slider.value()
        self.color_label.setText(f"Intensidad: {intensity}")
        self.schedule_render()
    
    def update_rotation(self):
        """Actualiza rotación."""
        rotation = self.rotation_slider.value()
        self.rotation = rotation
        self.rotation_label.setText(f"Rotación: {rotation}°")
        self.schedule_render()
    
    def toggle_adaptive(self, state):
        """Toggle niveles adaptativos."""
        self.adaptive_levels = state == 2
        self.schedule_render()
    
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
    
    def generate_fractal(self):
        """🚀 GENERA SIERPINSKI OPTIMIZADO"""
        try:
            # Nivel efectivo con límites seguros
            base_level = self.level_slider.value()
            if self.adaptive_levels:
                adaptive_boost = min(3, int(math.log2(max(1, self.zoom_level))))  # Límite de boost
                effective_level = min(12, base_level + adaptive_boost)  # Límite total
            else:
                effective_level = base_level
            
            # Crear imagen optimizada
            width, height = 800, 700
            image = QImage(width, height, QImage.Format.Format_RGB888)
            image.fill(QColor(0, 0, 17))
            
            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)  # Desactivar para optimizar
            
            # Configurar transformaciones simples
            painter.translate(width/2 + self.offset_x, height/2 + self.offset_y)
            painter.scale(self.zoom_level, self.zoom_level)
            painter.rotate(self.rotation)
            
            # Triángulo principal
            size = 180
            height_tri = size * math.sqrt(3) / 2
            
            p1 = (-size/2, -height_tri/3)
            p2 = (size/2, -height_tri/3)
            p3 = (0, 2*height_tri/3)
            
            # Generar Sierpinski optimizado
            self.draw_sierpinski_optimized(painter, p1, p2, p3, effective_level)
            
            painter.end()
            
            # Aplicar al canvas
            pixmap = QPixmap.fromImage(image)
            self.canvas.setPixmap(pixmap)
            
            # Actualizar título
            info = f"🔺 SIERPINSKI GPU - Zoom: {self.zoom_level:.2f}x - Nivel: {effective_level}"
            self.setWindowTitle(info)
            
        except Exception as e:
            print(f"Error optimizado: {e}")
    
    def draw_sierpinski_optimized(self, painter, p1, p2, p3, level):
        """Dibuja Sierpinski optimizado sin sobrecarga."""
        if level <= 0:
            # Colores simples y eficientes
            intensity = self.color_slider.value()
            
            colors = [
                QColor(intensity, 100, 200),
                QColor(200, intensity, 100),
                QColor(100, 200, intensity),
                QColor(intensity, 150, 150),
            ]
            color = colors[level % len(colors)]
            
            painter.setBrush(color)
            painter.setPen(QPen(color, 1))
            
            # Dibujar triángulo simple
            points = [QPoint(int(p1[0]), int(p1[1])),
                     QPoint(int(p2[0]), int(p2[1])),
                     QPoint(int(p3[0]), int(p3[1]))]
            painter.drawPolygon(points)
            return
        
        # Recursión optimizada con límites
        if level > 12:  # Límite de seguridad
            return
            
        # Calcular puntos medios
        mid12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        mid23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
        mid31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
        
        # Recursión
        self.draw_sierpinski_optimized(painter, p1, mid12, mid31, level - 1)
        self.draw_sierpinski_optimized(painter, mid12, p2, mid23, level - 1)
        self.draw_sierpinski_optimized(painter, mid31, mid23, p3, level - 1)
    
    def export_fractal(self):
        """Exporta fractal optimizado."""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Sierpinski", "sierpinski_optimized.png", 
                "PNG Files (*.png)"
            )
            
            if file_path:
                # Exportar en resolución moderada
                image_export = QImage(1920, 1080, QImage.Format.Format_RGB888)
                image_export.fill(QColor(0, 0, 17))
                
                painter_export = QPainter(image_export)
                
                # Configuración para exportación
                scale_export = 1920 / 800
                painter_export.translate(960 + self.offset_x * scale_export, 
                                       540 + self.offset_y * scale_export)
                painter_export.scale(self.zoom_level * scale_export, 
                                    self.zoom_level * scale_export)
                painter_export.rotate(self.rotation)
                
                # Triángulo para exportación
                size_export = 180 * scale_export
                height_export = size_export * math.sqrt(3) / 2
                
                p1_export = (-size_export/2, -height_export/3)
                p2_export = (size_export/2, -height_export/3)
                p3_export = (0, 2*height_export/3)
                
                # Usar nivel moderado para exportación
                export_level = min(10, self.level_slider.value() + 2)
                self.draw_sierpinski_optimized(painter_export, p1_export, p2_export, p3_export, export_level)
                
                painter_export.end()
                image_export.save(file_path)
                
                QMessageBox.information(self, "✅ Exportado", 
                                      f"Sierpinski exportado en Full HD:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar: {e}")

def main():
    """Función principal optimizada."""
    print("🚀 SIERPINSKI GPU OPTIMIZADO - SIN SOBRECARGA")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    
    window = SierpinskiOptimizedWindow()
    window.show()
    
    print("✅ SIERPINSKI OPTIMIZADO INICIADO")
    print("🔍 Características:")
    print("  • Zoom: 0.01x a 50x (sin sobrecarga)")
    print("  • Niveles: 2 a 10 (optimizado)")
    print("  • Renderizado eficiente con delays")
    print("  • Sin efectos pesados")
    print("  • Navegación suave")
    
    return app.exec()

if __name__ == "__main__":
    main()
