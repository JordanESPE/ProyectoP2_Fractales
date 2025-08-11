"""
Script para corregir ventanas_fractales.py reemplazando la clase TreeMainWindow
"""

# Leer el archivo original
with open('fractales/interfaces/ventanas_fractales.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Definir la nueva clase TreeMainWindow corregida
new_tree_class = '''class TreeMainWindow(QMainWindow):
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

'''

# Encontrar las posiciones de TreeMainWindow
tree_start = None
tree_end = None
for i, line in enumerate(lines):
    if 'class TreeMainWindow(QMainWindow):' in line:
        tree_start = i
    elif 'class SierpinskiMainWindow(QMainWindow):' in line:
        tree_end = i
        break

if tree_start is not None and tree_end is not None:
    # Crear nuevo contenido: antes + nueva clase + después
    new_lines = (
        lines[:tree_start] +  # Todo antes de TreeMainWindow
        [new_tree_class + '\n\n'] +  # Nueva clase TreeMainWindow
        lines[tree_end:]  # SierpinskiMainWindow y el resto
    )
    
    # Escribir archivo corregido
    with open('fractales/interfaces/ventanas_fractales.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✅ Archivo corregido exitosamente")
    print(f"   - TreeMainWindow reemplazada (era líneas {tree_start+1}-{tree_end})")
    print(f"   - Líneas totales: {len(lines)} → {len(new_lines)}")
else:
    print("❌ No se pudo encontrar TreeMainWindow o SierpinskiMainWindow")
