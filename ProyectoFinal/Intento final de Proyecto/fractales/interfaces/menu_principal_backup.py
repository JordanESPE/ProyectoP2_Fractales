"""
Menú Principal - Selector Simple de Fractales
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QApplication, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SimpleFractalMenu(QMainWindow):
    """Menú simple con solo botones para acceder a cada fractal."""
    
    def __init__(self):
        super().__init__()
        self.mandelbrot_window = None
        self.julia_window = None
        self.koch_window = None
        self.tree_window = None
        self.sierpinski_window = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz simple con solo botones."""
        self.setWindowTitle("Fractales - Seleccionar")
        self.setGeometry(200, 200, 600, 400)
        
        # Fondo simple
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
        """)
        
        # Widget principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)
        central_widget.setLayout(main_layout)
        
        # Título
        title = QLabel("Selecciona un Fractal")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; margin-bottom: 30px;")
        main_layout.addWidget(title)
        
        # Grid de botones
        buttons_widget = QWidget()
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(20)
        buttons_widget.setLayout(buttons_layout)
        
        # Crear botones simples
        self.create_fractal_buttons(buttons_layout)
        
        main_layout.addWidget(buttons_widget)
        main_layout.addStretch()
    
    def create_fractal_buttons(self, layout):
        """Crea los botones simples para cada fractal."""
        
        # Botón Mandelbrot
        mandelbrot_btn = self.create_simple_button("Mandelbrot", "#e74c3c")
        mandelbrot_btn.clicked.connect(self.open_mandelbrot)
        layout.addWidget(mandelbrot_btn, 0, 0)
        
        # Botón Julia
        julia_btn = self.create_simple_button("Julia", "#9b59b6")
        julia_btn.clicked.connect(self.open_julia)
        layout.addWidget(julia_btn, 0, 1)
        
        # Botón Koch
        koch_btn = self.create_simple_button("Koch", "#3498db")
        koch_btn.clicked.connect(self.open_koch)
        layout.addWidget(koch_btn, 0, 2)
        
        # Botón Árbol
        tree_btn = self.create_simple_button("Árbol", "#27ae60")
        tree_btn.clicked.connect(self.open_tree)
        layout.addWidget(tree_btn, 1, 0)
        
        # Botón Sierpinski
        sierpinski_btn = self.create_simple_button("Sierpinski", "#f39c12")
        sierpinski_btn.clicked.connect(self.open_sierpinski)
        layout.addWidget(sierpinski_btn, 1, 1)
    
    def create_simple_button(self, text, color):
        """Crea un botón simple con el nombre del fractal."""
        button = QPushButton(text)
        button.setFixedSize(150, 80)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 0.3)};
            }}
        """)
        return button
    
    def darken_color(self, hex_color, factor=0.2):
        """Oscurece un color hexadecimal."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def open_mandelbrot(self):
        """Abre la ventana del conjunto de Mandelbrot."""
        try:
            if self.mandelbrot_window is None:
                from .ventana_mandelbrot import MandelbrotMainWindow as MWindow
                self.mandelbrot_window = MWindow()
            
            self.mandelbrot_window.show()
            self.mandelbrot_window.raise_()
            self.mandelbrot_window.activateWindow()
        except Exception as e:
            print(f"Error abriendo Mandelbrot: {e}")
    
    def open_julia(self):
        """Abre la ventana del conjunto de Julia."""
        try:
            if self.julia_window is None:
                from .ventanas_fractales import JuliaMainWindow as JWindow
                self.julia_window = JWindow()
            
            self.julia_window.show()
            self.julia_window.raise_()
            self.julia_window.activateWindow()
        except Exception as e:
            print(f"Error abriendo Julia: {e}")
    
    def open_koch(self):
        """Abre la ventana de la Curva de Koch."""
        try:
            if self.koch_window is None:
                from .ventanas_fractales import KochMainWindow as KWindow
                self.koch_window = KWindow()
            
            self.koch_window.show()
            self.koch_window.raise_()
            self.koch_window.activateWindow()
        except Exception as e:
            print(f"Error abriendo Koch: {e}")
    
    def open_tree(self):
        """Abre la ventana del Árbol Fractal."""
        try:
            if self.tree_window is None:
                from .ventanas_fractales import TreeMainWindow as TWindow
                self.tree_window = TWindow()
            
            self.tree_window.show()
            self.tree_window.raise_()
            self.tree_window.activateWindow()
        except Exception as e:
            print(f"Error abriendo Árbol: {e}")
    
    def open_sierpinski(self):
        """Abre la ventana del Triángulo de Sierpinski."""
        try:
            if self.sierpinski_window is None:
                from .ventanas_fractales import SierpinskiMainWindow as SWindow
                self.sierpinski_window = SWindow()
            
            self.sierpinski_window.show()
            self.sierpinski_window.raise_()
            self.sierpinski_window.activateWindow()
        except Exception as e:
            print(f"Error abriendo Sierpinski: {e}")
    
    def closeEvent(self, event):
        """Maneja el cierre de la aplicación."""
        # Cerrar ventanas secundarias si existen
        if self.mandelbrot_window:
            self.mandelbrot_window.close()
        if self.julia_window:
            self.julia_window.close()
        if self.koch_window:
            self.koch_window.close()
        if self.tree_window:
            self.tree_window.close()
        if self.sierpinski_window:
            self.sierpinski_window.close()
        
        event.accept()


class SimpleFractalMenu(QMainWindow):
    """Menú simple con solo botones para acceder a cada fractal."""
    
    def __init__(self):
        super().__init__()
        self.mandelbrot_window = None
        self.julia_window = None
        self.koch_window = None
        self.tree_window = None
        self.sierpinski_window = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz simple con solo botones."""
        self.setWindowTitle("Fractales - Seleccionar")
        self.setGeometry(200, 200, 600, 400)
        
        # Fondo simple
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
        """)
        
        # Widget principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)
        central_widget.setLayout(main_layout)
        
        # Título
        title = QLabel("Selecciona un Fractal")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; margin-bottom: 30px;")
        main_layout.addWidget(title)
        
        # Grid de botones
        buttons_widget = QWidget()
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(20)
        buttons_widget.setLayout(buttons_layout)
        
        # Crear botones simples
        self.create_fractal_buttons(buttons_layout)
        
        main_layout.addWidget(buttons_widget)
        main_layout.addStretch()
    
    def create_fractal_buttons(self, layout):
        """Crea los botones simples para cada fractal."""
        
        # Botón Mandelbrot
        mandelbrot_btn = self.create_simple_button("Mandelbrot", "#e74c3c")
        mandelbrot_btn.clicked.connect(self.open_mandelbrot)
        layout.addWidget(mandelbrot_btn, 0, 0)
        
        # Botón Julia
        julia_btn = self.create_simple_button("Julia", "#9b59b6")
        julia_btn.clicked.connect(self.open_julia)
        layout.addWidget(julia_btn, 0, 1)
        
        # Botón Koch
        koch_btn = self.create_simple_button("Koch", "#3498db")
        koch_btn.clicked.connect(self.open_koch)
        layout.addWidget(koch_btn, 0, 2)
        
        # Botón Árbol
        tree_btn = self.create_simple_button("Árbol", "#27ae60")
        tree_btn.clicked.connect(self.open_tree)
        layout.addWidget(tree_btn, 1, 0)
        
        # Botón Sierpinski
        sierpinski_btn = self.create_simple_button("Sierpinski", "#f39c12")
        sierpinski_btn.clicked.connect(self.open_sierpinski)
        layout.addWidget(sierpinski_btn, 1, 1)
    
    def create_simple_button(self, text, color):
        """Crea un botón simple con el nombre del fractal."""
        button = QPushButton(text)
        button.setFixedSize(150, 80)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 0.3)};
            }}
        """)
        return button
    
    def darken_color(self, hex_color, factor=0.2):
        """Oscurece un color hexadecimal."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def open_mandelbrot(self):
        """Abre la ventana del conjunto de Mandelbrot."""
        try:
            if self.mandelbrot_window is None:
                from .ventana_mandelbrot import MandelbrotMainWindow as MWindow
                self.mandelbrot_window = MWindow()
            
            self.mandelbrot_window.show()
            self.mandelbrot_window.raise_()
            self.mandelbrot_window.activateWindow()
        except Exception as e:
            print(f"Error abriendo Mandelbrot: {e}")
    
    def open_julia(self):
        """Abre la ventana del conjunto de Julia."""
        try:
            if self.julia_window is None:
                from .ventanas_fractales import JuliaMainWindow as JWindow
                self.julia_window = JWindow()
            
            self.julia_window.show()
            self.julia_window.raise_()
            self.julia_window.activateWindow()
        except Exception as e:
            print(f"Error abriendo Julia: {e}")
    
    def open_koch(self):
        """Abre la ventana de la Curva de Koch."""
        try:
            if self.koch_window is None:
                from .ventanas_fractales import KochMainWindow as KWindow
                self.koch_window = KWindow()
            
            self.koch_window.show()
            self.koch_window.raise_()
            self.koch_window.activateWindow()
        except Exception as e:
            print(f"Error abriendo Koch: {e}")
    
    def open_tree(self):
        """Abre la ventana del Árbol Fractal."""
        try:
            if self.tree_window is None:
                from .ventanas_fractales import TreeMainWindow as TWindow
                self.tree_window = TWindow()
            
            self.tree_window.show()
            self.tree_window.raise_()
            self.tree_window.activateWindow()
        except Exception as e:
            print(f"Error abriendo Árbol: {e}")
    
    def open_sierpinski(self):
        """Abre la ventana del Triángulo de Sierpinski."""
        try:
            if self.sierpinski_window is None:
                from .ventanas_fractales import SierpinskiMainWindow as SWindow
                self.sierpinski_window = SWindow()
            
            self.sierpinski_window.show()
            self.sierpinski_window.raise_()
            self.sierpinski_window.activateWindow()
        except Exception as e:
            print(f"Error abriendo Sierpinski: {e}")
    
    def closeEvent(self, event):
        """Maneja el cierre de la aplicación."""
        # Cerrar ventanas secundarias si existen
        if self.mandelbrot_window:
            self.mandelbrot_window.close()
        if self.julia_window:
            self.julia_window.close()
        if self.koch_window:
            self.koch_window.close()
        if self.tree_window:
            self.tree_window.close()
        if self.sierpinski_window:
            self.sierpinski_window.close()
        
        event.accept()
