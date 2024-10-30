import sys
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QSizePolicy,
    QSpacerItem
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from views.facturacion import FacturacionWidget


class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.setWindowTitle("Configuración de Impresora")
        self.setGeometry(100, 100, 800, 600)  # Tamaño de ventana ajustado

        # Establecer el fondo blanco
        self.setStyleSheet("background-color: white;")

        # Etiqueta principal
        self.title_label = QLabel("Selecciona Impresora Predeterminada:")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")  # Tamaño de fuente aumentado
        self.title_label.setAlignment(Qt.AlignLeft)

        # Campos de Formato Ticket y Formato A4 usando QComboBox
        self.ticket_combo = QComboBox()
        self.ticket_combo.addItems(["Formato Ticket 1", "Formato Ticket 2", "Formato Ticket 3"])  # Opciones de formato ticket
        self.ticket_combo.setFixedHeight(50)
        self.ticket_combo.setStyleSheet("""
            QComboBox {
                border-radius: 20px; 
                background-color: #FEC92E; 
                padding: 10px;
                font-size: 16px; 
                color: #2C3E50;
            }
            QComboBox::drop-down {
                border: none; 
            }
            QComboBox QAbstractItemView {
                background-color: #FEC92E; 
                color: #2C3E50; 
                font-size: 16px; 
            }
            QComboBox QAbstractItemView::item {
                padding: 10px;
            }
        """)

        self.a4_combo = QComboBox()
        self.a4_combo.addItems(["Formato A4 1", "Formato A4 2", "Formato A4 3"])  # Opciones de formato A4
        self.a4_combo.setFixedHeight(50)
        self.a4_combo.setFixedWidth(250)
        self.a4_combo.setStyleSheet("""
            QComboBox {
                border-radius: 20px; 
                background-color: #FEC92E; 
                padding: 10px;
                font-size: 16px; 
                color: #2C3E50;
            }
            QComboBox::drop-down {
                border: none; 
            }
            QComboBox QAbstractItemView {
                background-color: #FEC92E; 
                color: #2C3E50; 
                font-size: 16px; 
            }
            QComboBox QAbstractItemView::item {
                padding: 10px;
            }
        """)

        # Layout para los campos de Formato Ticket y A4 (a la derecha)
        format_layout = QVBoxLayout()
        format_layout.addWidget(QLabel("Formato Ticket:"))  # Label para Formato Ticket
        format_layout.addWidget(self.ticket_combo)           # ComboBox para Formato Ticket
        format_layout.addWidget(QLabel("Formato A4:"))      # Label para Formato A4
        format_layout.addWidget(self.a4_combo)               # ComboBox para Formato A4

        # Diseño de la parte derecha con formato (alineado con el título)
        right_layout = QHBoxLayout()
        right_layout.addWidget(self.title_label)  # Título principal
        right_layout.addLayout(format_layout)     # Campos de Ticket y A4 a la derecha
        right_layout.addStretch()                  # Espacio para empujar hacia la derecha

        # Etiqueta de instrucciones centrada y más grande
        self.instructions_label = QLabel(
            "Los reportes se imprimen en Formato\n"
            "A4 y los Comprobantes en formato\n"
            "Ticket"
        )
        self.instructions_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")  # Tamaño de letra aumentado
        self.instructions_label.setAlignment(Qt.AlignCenter)

        # Verifica que la imagen de impresora esté disponible
        self.printer_label = QLabel()
        self.printer_pixmap = QPixmap("assets/icons/2.png")  # Ruta del icono de impresora
        if not self.printer_pixmap.isNull():
            self.printer_label.setPixmap(self.printer_pixmap.scaled(240, 240, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Tamaño de imagen aumentado
        else:
            self.printer_label.setText("Icono no encontrado")

        # Verifica que la imagen de ticket esté disponible
        self.ticket_label_icon = QLabel()
        self.ticket_pixmap = QPixmap("assets/icons/3.png")  # Ruta del icono de ticket
        if not self.ticket_pixmap.isNull():
            self.ticket_label_icon.setPixmap(self.ticket_pixmap.scaled(240, 240, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Tamaño de imagen aumentado
        else:
            self.ticket_label_icon.setText("Icono no encontrado")

        # Layout para iconos de impresora y tickets (juntos)
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.printer_label, alignment=Qt.AlignCenter)
        icon_layout.addWidget(self.ticket_label_icon, alignment=Qt.AlignCenter)

        # Botón "Continuar"
        self.continue_button = QPushButton("Continuar")
        self.continue_button.setFixedSize(120, 40)
        self.continue_button.setStyleSheet("border-radius: 20px; background-color: #FEC92E; font-size: 16px;")
        self.continue_button.clicked.connect(self.open_config_window)

        # Diseño del botón en la parte inferior derecha
        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.continue_button, alignment=Qt.AlignRight)

        # Diseño principal de la ventana
        main_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)       # Título y formatos alineados
        main_layout.addStretch(1)                  # Espacio flexible para reducir espacio vacío
        main_layout.addWidget(self.instructions_label)  # Instrucciones centradas
        main_layout.addLayout(icon_layout)        # Iconos de impresora y ticket juntos
        main_layout.addStretch(1)                  # Espacio flexible para reducir espacio vacío
        main_layout.addLayout(button_layout)      # Botón "Continuar"

        self.setLayout(main_layout)
    def open_config_window(self):
        # Crea una nueva instancia de ConfigWindow y la muestra
        self.impresora_window = FacturacionWidget()
        self.impresora_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication([])

    window = ConfigWindow()
    window.show()

    app.exec()