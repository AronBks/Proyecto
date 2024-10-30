from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                               QFileDialog, QLineEdit, QCheckBox, QComboBox, 
                               QVBoxLayout, QHBoxLayout, QGridLayout, QWidget)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from views.connector import DBConnector
from views.config_backup import ExportImportDatabase
import sys
import os
import pymysql
# Asegúrate de que el sistema pueda encontrar el módulo 'controllers'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
class ConfigInicial(QMainWindow):
    def __init__(self):  
        super().__init__()  
        self.setWindowTitle("Configuración Inicial")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        # Fondo blanco general
        self.setStyleSheet("background-color: white;")

        # Sección de logo y botón para cambiar logo
        logo_layout = QVBoxLayout()
        self.logo_label = QLabel("Tu logo aquí")
        self.logo_label.setFixedSize(200, 200)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setStyleSheet("""  
            QLabel {
                border: 2px solid #2C3E50;
                border-radius: 100px;  /* Hacer el logo circular */
                background-color: #E0E0E0;
                font-size: 16px;
                font-weight: bold;
                color: #2C3E50;
                padding: 0;
                qproperty-alignment: AlignCenter;
            }
        """)

        logo_btn = QPushButton("Cambiar")
        logo_btn.setFixedSize(120, 40)  # Ajusta el tamaño para hacerlo más amplio
        logo_btn.setStyleSheet("""  
            QPushButton {
                background-color: #FEC007;
                color: black;
                border-radius: 20px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FEC042;
            }
        """)
        logo_btn.clicked.connect(self.change_logo)

        logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        logo_layout.addWidget(logo_btn, alignment=Qt.AlignCenter)
        layout.addLayout(logo_layout, 0, 3, 2, 1)

        # Título Nombre de la Empresa
        titulo_nombre_empresa = QLabel("Nombre de tu Empresa")
        titulo_nombre_empresa.setStyleSheet("font-weight: bold; font-size: 18px; color: #2C3E50;")
        layout.addWidget(titulo_nombre_empresa, 0, 0, 1, 2, Qt.AlignLeft | Qt.AlignBottom)  

        # Campo para Nombre de la Empresa
        self.nombre_empresa = QLineEdit()
        self.nombre_empresa.setPlaceholderText("Nombre de tu Empresa")
        self.nombre_empresa.setFixedSize(400, 45)
        self.nombre_empresa.setStyleSheet("""  
            QLineEdit {
                background-color: #E0E0E0;
                border: none;
                border-radius: 20px;
                padding: 10px;
                font-size: 16px;
                color: #2C3E50;
            }
        """)
        layout.addWidget(self.nombre_empresa, 1, 0, 1, 2, Qt.AlignLeft | Qt.AlignTop)

        # País y Moneda
        # Etiqueta País
        label_pais = QLabel("País")
        label_pais.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(label_pais, 2, 0, Qt.AlignTop)

        # Campo de texto para País
        self.combo_pais = QLineEdit("Bolivia")
        self.combo_pais.setFixedSize(150, 40)
        self.combo_pais.setStyleSheet("""  
            QLineEdit {
                background-color: #E0E0E0;
                border-radius: 20px;
                padding: 10px;
                font-size: 16px;
                color: #2C3E50;
            }
        """)
        layout.addWidget(self.combo_pais, 3, 0, 1, 1, Qt.AlignLeft)

        # Etiqueta Moneda
        label_moneda = QLabel("Moneda")
        label_moneda.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(label_moneda, 2, 1)

        # Campo de texto para Moneda
        self.combo_moneda = QLineEdit("Bs.")
        self.combo_moneda.setFixedSize(150, 40)
        self.combo_moneda.setStyleSheet("""  
            QLineEdit { 
                background-color: #E0E0E0;
                border-radius: 20px;
                padding: 10px;
                font-size: 16px;
                color: #2C3E50;
            }
        """)
        layout.addWidget(self.combo_moneda, 3, 1, 1, 1, Qt.AlignLeft)

        # Impuestos y Porcentaje
        label_impuestos = QLabel("Impuestos")
        label_impuestos.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(label_impuestos, 4, 0, 1, 1)

        # Campo de selección para impuestos
        self.combo_impuestos = QComboBox()
        self.combo_impuestos.addItems(["IVA", "IT", "IUE"])
        self.combo_impuestos.setFixedHeight(40)
        self.combo_impuestos.setFixedWidth(150)
        self.combo_impuestos.setStyleSheet("""  
            QComboBox {
                background-color: #E0E0E0; 
                border: 1px solid #BDC3C7;   
                border-radius: 20px;
                padding: 5px;
                font-size: 16px;
                color: #2C3E50;
            }
            QComboBox::drop-down {
                border: none;                
                width: 0px;                 
            }
            QComboBox QAbstractItemView {
                background-color: #E0E0E0;  
                color: #2C3E50;             
            }
            QComboBox QAbstractItemView::item {
                padding: 10px;              
            }
        """)
        layout.addWidget(self.combo_impuestos, 5, 0, 1, 1, Qt.AlignTop)

        # Campo de texto para porcentaje (editable, sin flecha)
        self.porcentaje = QLineEdit("0%")
        self.porcentaje.setFixedHeight(40)
        self.porcentaje.setFixedWidth(150)
        self.porcentaje.setStyleSheet("""  
            QLineEdit {
                background-color: #E0E0E0;
                border-radius: 20px;
                padding: 5px;
                font-size: 16px;
                color: #2C3E50;
            }
        """)
        layout.addWidget(self.porcentaje, 5, 1, 1, 1, Qt.AlignLeft)

        # Mensaje adicional en dos líneas como el diseño original
        mensaje_impuestos = QLabel("(Si no manejas impuestos\ncoloca el % en 0)")
        mensaje_impuestos.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        mensaje_impuestos.setWordWrap(True)
        layout.addWidget(mensaje_impuestos, 5, 2, 2, Qt.AlignRight)

        # Preferencias de búsqueda de productos
        preferencia_label = QLabel("¿Cómo buscarás con frecuencia tus productos?")
        preferencia_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(preferencia_label, 7, 0, 1, 2)

        self.checkbox_lector = QCheckBox("Con una Lectora de Barras")
        self.checkbox_lector.setStyleSheet("font-size: 16px; color: #2C3E50;")
        self.checkbox_teclado = QCheckBox("Escribiendo con mi Teclado")
        self.checkbox_teclado.setStyleSheet("font-size: 16px; color: #2C3E50;")
        layout.addWidget(self.checkbox_lector, 8, 0, 1, 2)
        layout.addWidget(self.checkbox_teclado, 9, 0, 1, 2)

        # Carpeta para Copias de Seguridad
        carpeta_label = QLabel("Carpetas para Copias de Seguridad")
        carpeta_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(carpeta_label, 10, 0, 1, 2)

        backup_layout = QHBoxLayout()
        self.label_backup_icon = QLabel()
        self.label_backup_icon.setPixmap(QPixmap("assets/icons/carpeta_icon.png").scaled(50, 50, Qt.KeepAspectRatio))

        # Texto "Seleccionar Ruta"
        self.seleccionar_ruta_label = QLabel("Seleccione una Ruta:")
        self.seleccionar_ruta_label.setStyleSheet("font-size: 16px; color: #2C3E50;")
        self.seleccionar_ruta_label.setAlignment(Qt.AlignCenter)
        backup_layout.addWidget(self.seleccionar_ruta_label)
        backup_layout.addWidget(self.label_backup_icon)

        layout.addLayout(backup_layout, 11, 0, 1, 2)

        # Conectar el clic en el ícono de la carpeta a la función de selección de ruta
        self.label_backup_icon.mousePressEvent = self.open_folder_dialog

        # Botón Continuar
        continue_btn = QPushButton("Continuar")
        continue_btn.setFixedSize(150, 50)
        continue_btn.setStyleSheet("""  
            QPushButton {
                background-color: #FEC007;
                color: black;
                border-radius: 20px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #FEC042;
            }
        """)
        continue_btn.clicked.connect(self.save_config)  # Conectar el botón a la función de guardar
        layout.addWidget(continue_btn, 12, 3)

        # Aplicar layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.logo_path = None  # Variable para almacenar la ruta del logo

    def change_logo(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", 
                                                     "Images (.png *.jpg *.jpeg);;All Files ()", options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
            self.logo_label.setStyleSheet("border: none;")
            self.logo_path = file_name  # Guardar la ruta del logo

    def open_folder_dialog(self, event):
        folder_name = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder_name:
            self.seleccionar_ruta_label.setText(folder_name)

    def save_config(self):
      # Obtener los datos del formulario
      nombre_empresa = self.nombre_empresa.text()
      pais = self.combo_pais.text()
      moneda = self.combo_moneda.text()
      impuesto = self.combo_impuestos.currentText()
      porcentaje = float(self.porcentaje.text().replace('%', ''))  # Quitar el símbolo de porcentaje

      if self.logo_path:
        with open(self.logo_path, 'rb') as logo_file:
            logo_data = logo_file.read()

        # Guardar en la base de datos
        db = DBConnector()  # Asegúrate de tener una clase DBConnector para manejar la conexión
        connection = db.conectar()  # Cambiar aquí para usar el método conectar()
        
        try:
            if connection:  # Verificar si la conexión fue exitosa
                with connection.cursor() as cursor:
                    sql = """INSERT INTO configuracion (nombre_empresa, pais, moneda, impuesto, porcentaje, logo) 
                             VALUES (%s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (nombre_empresa, pais, moneda, impuesto, porcentaje, logo_data))
                connection.commit()
                print("Configuración guardada exitosamente.")
            else:
                print("No se pudo establecer la conexión con la base de datos.")
        except Exception as e:
            print(f"Error al guardar la configuración: {e}")
        finally:
            db.cerrar_conexion(connection)  # Usar el método cerrar_conexion
        # Abrir la ventana de configuración de backup
        self.backup_window = ExportImportDatabase()
        self.backup_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfigInicial()
    window.show()
    sys.exit(app.exec())  