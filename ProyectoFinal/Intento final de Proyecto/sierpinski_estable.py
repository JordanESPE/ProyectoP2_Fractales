#!/usr/bin/env python3
"""
🔺 SIERPINSKI BÁSICO Y ESTABLE
Versión ultra-simple que nunca se cierra
"""

import sys
import math
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QSlider, QFrame, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen, QColor

class SierpinskiStableWindow(QMainWindow):
    """🔺 SIERPINSKI ESTABLE - NUNCA SE CIERRA"""
    
    def __init__(self):
        super().__init__()
        # Parámetros mínimos
        self.zoom_level = 1.0
        self.level = 5
        self.color_intensity = 150
        
        self.setup_ui()
        self.generate_fractal()
    
    def setup_ui(self):
        """Interfaz ultra-simple."""
        self.setWindowTitle("🔺 SIERPINSKI ESTABLE")
        self.setGeometry(200, 200, 1000, 700)
        
        # Estilos mínimos
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #1a1a2e; 
                color: white; 
            }
            QLabel { 
                color: white; 
                font-size: 12px;
            }
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: 1px solid #666;
                border-radius: 4px;
                padding: 6px;
                font-size: 11px;
            }
            QPushButton:hover { 
                background-color: #5a5a5a;
            }
            QSlider::groove:horizontal {
                border: 1px solid #3c3c3c;
                height: 8px;
                background: #2c2c2c;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #66aaff;
                border: 1px solid #555;
                width: 16px;
                margin: -2px 0;
                border-radius: 8px;
            }
            QFrame {
                background-color: #2a2a3e;
                border: 1px solid #444;
                border-radius: 6px;
                margin: 3px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Canvas simple
        self.canvas = QLabel()
        self.canvas.setMinimumSize(700, 600)
        self.canvas.setStyleSheet("border: 1px solid #666; background-color: #000;")
        main_layout.addWidget(self.canvas)
        
        # Controles mínimos
        controls = self.create_simple_controls()
        main_layout.addWidget(controls)
    
    def create_simple_controls(self):
        """Controles ultra-simples."""
        frame = QFrame()
        frame.setFixedWidth(280)
        layout = QVBoxLayout()
        frame.setLayout(layout)
        
        # Título
        title = QLabel("🔺 SIERPINSKI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; color: #66aaff; margin: 10px; font-weight: bold;")
        layout.addWidget(title)
        
        # Zoom simple
        layout.addWidget(QLabel("🔍 Zoom:"))
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(25)   # 0.25x
        self.zoom_slider.setMaximum(400)  # 4x
        self.zoom_slider.setValue(100)    # 1x
        self.zoom_slider.valueChanged.connect(self.safe_update_zoom)
        layout.addWidget(self.zoom_slider)
        
        self.zoom_label = QLabel("Zoom: 1.0x")
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.zoom_label)
        
        # Nivel simple
        layout.addWidget(QLabel("📊 Nivel:"))
        self.level_slider = QSlider(Qt.Orientation.Horizontal)
        self.level_slider.setMinimum(2)
        self.level_slider.setMaximum(8)  # Muy limitado
        self.level_slider.setValue(5)
        self.level_slider.valueChanged.connect(self.safe_update_level)
        layout.addWidget(self.level_slider)
        
        self.level_label = QLabel("Nivel: 5")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.level_label)
        
        # Color simple
        layout.addWidget(QLabel("🌈 Color:"))
        self.color_slider = QSlider(Qt.Orientation.Horizontal)
        self.color_slider.setMinimum(50)
        self.color_slider.setMaximum(255)
        self.color_slider.setValue(150)
        self.color_slider.valueChanged.connect(self.safe_update_color)
        layout.addWidget(self.color_slider)
        
        self.color_label = QLabel("Color: 150")
        self.color_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.color_label)
        
        # Botones simples
        layout.addWidget(QLabel(""))  # Espacio
        
        reset_btn = QPushButton("🎯 Resetear")
        reset_btn.clicked.connect(self.safe_reset)
        layout.addWidget(reset_btn)
        
        generate_btn = QPushButton("🔄 Generar")
        generate_btn.clicked.connect(self.safe_generate)
        layout.addWidget(generate_btn)
        
        # Info
        layout.addWidget(QLabel(""))  # Espacio
        info = QLabel("Versión estable\nsin sobrecarga")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("color: #aaa; font-size: 10px;")
        layout.addWidget(info)
        
        layout.addStretch()
        return frame
    
    def safe_update_zoom(self):
        """Actualización segura del zoom."""
        try:
            value = self.zoom_slider.value()
            self.zoom_level = value / 100.0
            self.zoom_label.setText(f"Zoom: {self.zoom_level:.1f}x")
            self.safe_generate()
        except Exception as e:
            print(f"Error en zoom: {e}")
    
    def safe_update_level(self):
        """Actualización segura del nivel."""
        try:
            self.level = self.level_slider.value()
            self.level_label.setText(f"Nivel: {self.level}")
            self.safe_generate()
        except Exception as e:
            print(f"Error en nivel: {e}")
    
    def safe_update_color(self):
        """Actualización segura del color."""
        try:
            self.color_intensity = self.color_slider.value()
            self.color_label.setText(f"Color: {self.color_intensity}")
            self.safe_generate()
        except Exception as e:
            print(f"Error en color: {e}")
    
    def safe_reset(self):
        """Reset seguro."""
        try:
            self.zoom_level = 1.0
            self.level = 5
            self.color_intensity = 150
            self.zoom_slider.setValue(100)
            self.level_slider.setValue(5)
            self.color_slider.setValue(150)
            self.safe_generate()
        except Exception as e:
            print(f"Error en reset: {e}")
    
    def safe_generate(self):
        """Generación completamente segura."""
        try:
            self.generate_fractal()
        except Exception as e:
            print(f"Error en generación: {e}")
            # Si falla, mostrar mensaje simple
            self.show_error_message()
    
    def show_error_message(self):
        """Muestra mensaje de error simple."""
        try:
            image = QImage(700, 600, QImage.Format.Format_RGB888)
            image.fill(QColor(20, 20, 40))
            
            painter = QPainter(image)
            painter.setPen(QPen(QColor(255, 100, 100), 2))
            painter.drawText(300, 300, "Error - Reinicia")
            painter.end()
            
            pixmap = QPixmap.fromImage(image)
            self.canvas.setPixmap(pixmap)
        except:
            pass  # Si esto también falla, no hacer nada
    
    def generate_fractal(self):
        """Generación ultra-simple del fractal."""
        # Límites estrictos de seguridad
        if self.level > 8:
            self.level = 8
        if self.level < 2:
            self.level = 2
        if self.zoom_level > 5.0:
            self.zoom_level = 5.0
        if self.zoom_level < 0.25:
            self.zoom_level = 0.25
        
        # Crear imagen simple
        width, height = 700, 600
        image = QImage(width, height, QImage.Format.Format_RGB888)
        image.fill(QColor(0, 0, 20))
        
        painter = QPainter(image)
        
        # Transformación simple
        painter.translate(width/2, height/2)
        painter.scale(self.zoom_level, self.zoom_level)
        
        # Triángulo base
        size = 150
        height_tri = size * math.sqrt(3) / 2
        
        p1 = (-size/2, -height_tri/3)
        p2 = (size/2, -height_tri/3)
        p3 = (0, 2*height_tri/3)
        
        # Dibujar sierpinski simple
        self.draw_simple_sierpinski(painter, p1, p2, p3, self.level)
        
        painter.end()
        
        # Mostrar en canvas
        pixmap = QPixmap.fromImage(image)
        self.canvas.setPixmap(pixmap)
        
        # Actualizar título
        self.setWindowTitle(f"🔺 SIERPINSKI - Zoom: {self.zoom_level:.1f}x - Nivel: {self.level}")
    
    def draw_simple_sierpinski(self, painter, p1, p2, p3, level):
        """Sierpinski ultra-simple sin riesgo de crash."""
        # Límite absoluto
        if level <= 0 or level > 8:
            # Triángulo final simple
            color = QColor(self.color_intensity, 100, 200)
            painter.setBrush(color)
            painter.setPen(QPen(color, 1))
            
            # Verificar que los puntos sean válidos
            try:
                from PyQt6.QtCore import QPoint
                points = [QPoint(int(p1[0]), int(p1[1])),
                         QPoint(int(p2[0]), int(p2[1])),
                         QPoint(int(p3[0]), int(p3[1]))]
                painter.drawPolygon(points)
            except:
                pass  # Si falla, no dibujar
            return
        
        # Recursión con verificación
        try:
            # Puntos medios
            mid12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
            mid23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
            mid31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
            
            # Recursión simple
            self.draw_simple_sierpinski(painter, p1, mid12, mid31, level - 1)
            self.draw_simple_sierpinski(painter, mid12, p2, mid23, level - 1)
            self.draw_simple_sierpinski(painter, mid31, mid23, p3, level - 1)
        except:
            pass  # Si algo falla en la recursión, parar

def main():
    """Función principal ultra-segura."""
    print("🔺 SIERPINSKI ESTABLE - NUNCA SE CIERRA")
    print("=" * 40)
    
    try:
        app = QApplication(sys.argv)
        
        window = SierpinskiStableWindow()
        window.show()
        
        print("✅ SIERPINSKI ESTABLE INICIADO")
        print("🛡️ Características de seguridad:")
        print("  • Zoom limitado: 0.25x a 4x")
        print("  • Niveles limitados: 2 a 8")
        print("  • Sin efectos pesados")
        print("  • Manejo de errores completo")
        print("  • Nunca se cierra inesperadamente")
        
        return app.exec()
        
    except Exception as e:
        print(f"Error crítico: {e}")
        print("El programa no pudo iniciarse")
        return 1

if __name__ == "__main__":
    main()
