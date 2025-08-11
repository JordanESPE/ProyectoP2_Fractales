"""
Ventana principal para el fractal de Mandelbrot con aceleración CUDA.
Incluye navegación fluida, zoom y rotación usando la GPU.
"""

import sys
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QSlider, QPushButton, QComboBox,
                             QFrame, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor
from fractales.generators.fractal_generators import MandelbrotGenerator, PaletteGenerator


class MandelbrotMainWindow(QMainWindow):
    """Ventana principal para el conjunto de Mandelbrot con aceleración CUDA."""
    
    def __init__(self):
        super().__init__()
        self.generator = MandelbrotGenerator()
        self.palette_gen = PaletteGenerator()
        
        # Parámetros de vista
        self.xmin = -2.5
        self.xmax = 1.5
        self.ymin = -2.0
        self.ymax = 2.0
        self.max_iter = 100
        self.palette_name = "Fire"
        
        # Estado de navegación
        self.drag_start = None
        self.current_image = None
        self.zoom_factor = 1.1
        
        self.setup_ui()
        self.generate_fractal()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        self.setWindowTitle("🔥 Mandelbrot CUDA - Navegación Fluida")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 8px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                border-color: #6666ff;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
            QSlider::groove:horizontal {
                border: 1px solid #3c3c3c;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2b2b2b, stop:1 #1e1e1e);
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a9eff, stop:1 #1e7cff);
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            QComboBox {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 6px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)
        
        # Widget principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Canvas del fractal
        self.canvas_label = QLabel()
        self.canvas_label.setMinimumSize(800, 600)
        self.canvas_label.setStyleSheet("""
            QLabel {
                border: 2px solid #444444;
                background-color: #000000;
            }
        """)
        self.canvas_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.canvas_label.setText("🔄 Generando fractal...")
        
        # Habilitar eventos del mouse
        self.canvas_label.mousePressEvent = self.mouse_press_event
        self.canvas_label.mouseMoveEvent = self.mouse_move_event
        self.canvas_label.mouseReleaseEvent = self.mouse_release_event
        self.canvas_label.wheelEvent = self.wheel_event
        
        main_layout.addWidget(self.canvas_label, 4)
        
        # Panel de controles
        controls_widget = self.create_controls_panel()
        main_layout.addWidget(controls_widget)
    
    def create_controls_panel(self):
        """Crea el panel de controles."""
        controls_frame = QFrame()
        controls_frame.setFixedWidth(280)
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border: 2px solid #3c3c3c;
                border-radius: 10px;
                margin: 5px;
            }
        """)
        
        layout = QVBoxLayout()
        controls_frame.setLayout(layout)
        
        # Título
        title = QLabel("🎛️ CONTROLES MANDELBROT")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px; color: #6666ff;")
        layout.addWidget(title)
        
        # Control de iteraciones
        layout.addWidget(QLabel("🔄 Iteraciones:"))
        self.iter_slider = QSlider(Qt.Orientation.Horizontal)
        self.iter_slider.setRange(50, 500)
        self.iter_slider.setValue(self.max_iter)
        self.iter_slider.valueChanged.connect(self.update_iterations)
        layout.addWidget(self.iter_slider)
        
        self.iter_label = QLabel(str(self.max_iter))
        self.iter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.iter_label)
        
        # Selector de paleta
        layout.addWidget(QLabel("🎨 Paleta de colores:"))
        self.palette_combo = QComboBox()
        self.palette_combo.addItems(["Fire", "Ocean", "Rainbow", "Neon", "Cosmic", "Emerald", "Psychedelic"])
        self.palette_combo.setCurrentText(self.palette_name)
        self.palette_combo.currentTextChanged.connect(self.update_palette)
        layout.addWidget(self.palette_combo)
        
        # Botones de navegación
        nav_label = QLabel("🧭 NAVEGACIÓN")
        nav_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_label.setStyleSheet("font-size: 12px; font-weight: bold; margin-top: 15px; color: #66ff66;")
        layout.addWidget(nav_label)
        
        # Botones de zoom
        zoom_layout = QHBoxLayout()
        
        zoom_in_btn = QPushButton("🔍+")
        zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_layout.addWidget(zoom_in_btn)
        
        zoom_out_btn = QPushButton("🔍-")
        zoom_out_btn.clicked.connect(self.zoom_out)
        zoom_layout.addWidget(zoom_out_btn)
        
        layout.addLayout(zoom_layout)
        
        # Botón de reset
        reset_btn = QPushButton("🏠 Reset Vista")
        reset_btn.clicked.connect(self.reset_view)
        layout.addWidget(reset_btn)
        
        # Botón de exportar
        export_btn = QPushButton("💾 Exportar PNG")
        export_btn.clicked.connect(self.export_image)
        layout.addWidget(export_btn)
        
        # Información de navegación
        info_label = QLabel("ℹ️ NAVEGACIÓN")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("font-size: 12px; font-weight: bold; margin-top: 15px; color: #ffff66;")
        layout.addWidget(info_label)
        
        help_text = QLabel("""
• Arrastrar: Mover vista
• Rueda: Zoom in/out
• Click derecho: Zoom out
• CUDA: Aceleración GPU""")
        help_text.setStyleSheet("font-size: 10px; color: #cccccc; margin: 5px;")
        help_text.setWordWrap(True)
        layout.addWidget(help_text)
        
        layout.addStretch()
        
        return controls_frame
    
    def generate_fractal(self):
        """Genera el fractal de Mandelbrot usando CUDA."""
        width = max(800, self.canvas_label.width())
        height = max(600, self.canvas_label.height())
        
        # Usar CUDA para generar el fractal
        fractal_data = self.generator.generate_cuda(
            width, height, self.xmin, self.xmax, 
            self.ymin, self.ymax, self.max_iter
        )
        
        # Aplicar paleta de colores
        colored_image = self.palette_gen.apply_palette(fractal_data, self.palette_name)
        
        # Convertir a QImage
        height, width, channel = colored_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(colored_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Actualizar la imagen
        self.current_image = q_image
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(
            self.canvas_label.size(), 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        self.canvas_label.setPixmap(scaled_pixmap)
    
    def mouse_press_event(self, event):
        """Maneja clicks del mouse."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start = event.position()
        elif event.button() == Qt.MouseButton.RightButton:
            # Click derecho para zoom out
            self.zoom_out()
    
    def mouse_move_event(self, event):
        """Maneja arrastre del mouse para navegación fluida."""
        if self.drag_start and (event.buttons() & Qt.MouseButton.LeftButton):
            # Calcular desplazamiento
            current_pos = event.position()
            dx = (current_pos.x() - self.drag_start.x()) / self.canvas_label.width()
            dy = (current_pos.y() - self.drag_start.y()) / self.canvas_label.height()
            
            # Aplicar desplazamiento al rango de coordenadas
            x_range = self.xmax - self.xmin
            y_range = self.ymax - self.ymin
            
            self.xmin -= dx * x_range
            self.xmax -= dx * x_range
            self.ymin += dy * y_range  # Invertir Y
            self.ymax += dy * y_range
            
            self.drag_start = current_pos
            
            # Regenerar fractal con navegación fluida
            QTimer.singleShot(10, self.generate_fractal)
    
    def mouse_release_event(self, event):
        """Maneja liberación del mouse."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start = None
    
    def wheel_event(self, event):
        """Maneja zoom con rueda del mouse."""
        # Obtener posición del mouse en coordenadas del canvas
        mouse_x = event.position().x() / self.canvas_label.width()
        mouse_y = event.position().y() / self.canvas_label.height()
        
        # Convertir a coordenadas del fractal
        fractal_x = self.xmin + mouse_x * (self.xmax - self.xmin)
        fractal_y = self.ymin + mouse_y * (self.ymax - self.ymin)
        
        # Determinar factor de zoom
        if event.angleDelta().y() > 0:
            # Zoom in
            factor = 1.0 / self.zoom_factor
        else:
            # Zoom out
            factor = self.zoom_factor
        
        # Aplicar zoom centrado en la posición del mouse
        x_range = (self.xmax - self.xmin) * factor
        y_range = (self.ymax - self.ymin) * factor
        
        self.xmin = fractal_x - x_range * mouse_x
        self.xmax = fractal_x + x_range * (1 - mouse_x)
        self.ymin = fractal_y - y_range * mouse_y
        self.ymax = fractal_y + y_range * (1 - mouse_y)
        
        # Regenerar fractal
        self.generate_fractal()
    
    def zoom_in(self):
        """Zoom in centrado."""
        center_x = (self.xmin + self.xmax) / 2
        center_y = (self.ymin + self.ymax) / 2
        
        x_range = (self.xmax - self.xmin) / self.zoom_factor
        y_range = (self.ymax - self.ymin) / self.zoom_factor
        
        self.xmin = center_x - x_range / 2
        self.xmax = center_x + x_range / 2
        self.ymin = center_y - y_range / 2
        self.ymax = center_y + y_range / 2
        
        self.generate_fractal()
    
    def zoom_out(self):
        """Zoom out centrado."""
        center_x = (self.xmin + self.xmax) / 2
        center_y = (self.ymin + self.ymax) / 2
        
        x_range = (self.xmax - self.xmin) * self.zoom_factor
        y_range = (self.ymax - self.ymin) * self.zoom_factor
        
        self.xmin = center_x - x_range / 2
        self.xmax = center_x + x_range / 2
        self.ymin = center_y - y_range / 2
        self.ymax = center_y + y_range / 2
        
        self.generate_fractal()
    
    def reset_view(self):
        """Reinicia la vista a los valores por defecto."""
        self.xmin = -2.5
        self.xmax = 1.5
        self.ymin = -2.0
        self.ymax = 2.0
        self.generate_fractal()
    
    def update_iterations(self, value):
        """Actualiza el número de iteraciones."""
        self.max_iter = value
        self.iter_label.setText(str(value))
        self.generate_fractal()
    
    def update_palette(self, palette_name):
        """Actualiza la paleta de colores."""
        self.palette_name = palette_name
        self.generate_fractal()
    
    def export_image(self):
        """Exporta la imagen actual en alta resolución."""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Guardar Fractal", "mandelbrot_hd.png", "PNG Files (*.png)"
            )
            
            if file_path:
                # Generar en alta resolución
                width, height = 4000, 4000
                fractal_data = self.generator.generate_cuda(
                    width, height, self.xmin, self.xmax, 
                    self.ymin, self.ymax, self.max_iter
                )
                
                colored_image = self.palette_gen.apply_palette(fractal_data, self.palette_name)
                
                # Convertir y guardar
                height, width, channel = colored_image.shape
                bytes_per_line = 3 * width
                q_image = QImage(colored_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                
                q_image.save(file_path)
                
                QMessageBox.information(self, "Éxito", f"Imagen guardada en:\n{file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar imagen:\n{e}")
    
    def resizeEvent(self, event):
        """Maneja el redimensionamiento."""
        super().resizeEvent(event)
        if hasattr(self, 'current_image') and self.current_image:
            QTimer.singleShot(100, self.generate_fractal)


def main():
    """Función principal para ejecutar la aplicación de Mandelbrot."""
    app = QApplication(sys.argv)
    window = MandelbrotMainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
