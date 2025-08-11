"""
Script para reemplazar completamente la clase KochMainWindow con la versión corregida
"""

# Leer el archivo original
with open('fractales/interfaces/ventanas_fractales.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Verificar si hay problemas en la clase Koch
print("🔍 Verificando clase KochMainWindow...")

# Buscar la posición de KochMainWindow
koch_start = content.find('class KochMainWindow(QMainWindow):')
if koch_start == -1:
    print("❌ No se encontró KochMainWindow")
    exit()

# Buscar donde termina (siguiente class)
koch_end = content.find('class TreeMainWindow(QMainWindow):', koch_start)
if koch_end == -1:
    print("❌ No se encontró TreeMainWindow después de Koch")
    exit()

print(f"✅ KochMainWindow encontrada: posición {koch_start} a {koch_end}")

# Nueva implementación de KochMainWindow COMPLETA Y CORREGIDA
new_koch_class = '''class KochMainWindow(QMainWindow):
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
                QMessageBox.information(self, "Éxito", f"Fractal exportado en 4K:\\n{file_path}")
                
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al exportar: {e}")


'''

# Reemplazar la clase completa
new_content = content[:koch_start] + new_koch_class + content[koch_end:]

# Guardar el archivo corregido
with open('fractales/interfaces/ventanas_fractales.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ KochMainWindow reemplazada completamente con la versión corregida")
print("🔄 Ahora debería mostrar el copo de nieve perfecto")
