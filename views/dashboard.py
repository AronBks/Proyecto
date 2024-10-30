import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QToolBar, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget
)
from PySide6.QtCore import Qt
from views.connector import DBConnector

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema de Ventas')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF;")  # Fondo oscuro para el dashboard

        # Inicializar el conector
        self.connector = DBConnector()  # No es necesario pasar argumentos aquí

        # Configurar la barra de herramientas
        self.toolbar = QToolBar('Toolbar', self)
        self.toolbar.setStyleSheet("background-color: #2E2E2E;")  # Color de fondo para la barra
        self.addToolBar(self.toolbar)

        # Botón para abrir la ventana de registro de productos
        self.register_product_button = QPushButton('Registrar Producto', self)
        self.register_product_button.setStyleSheet("""
            background-color: #FF6F61;  /* Color de fondo del botón */
            color: #FFFFFF;              /* Color del texto del botón */
            padding: 10px 20px;          /* Espaciado interno del botón */
            border: none;                /* Sin borde */
            border-radius: 5px;         /* Bordes redondeados */
        """)
        self.register_product_button.clicked.connect(self.open_register_product_view)
        self.toolbar.addWidget(self.register_product_button)

        # Área central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        
        # Mensaje de bienvenida
        self.welcome_label = QLabel('Bienvenido al Sistema de Ventas')
        self.welcome_label.setAlignment(Qt.AlignCenter)  # Centrar el texto
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")  # Estilo del texto
        self.layout.addWidget(self.welcome_label)

        # Lista de productos
        self.product_list_widget = QListWidget()
        self.product_list_widget.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF; border: none;")
        self.layout.addWidget(self.product_list_widget)

        # Cargar productos
        self.load_products()

        # Añadir un espacio entre el título y los botones
        self.layout.addStretch()

        self.central_widget.setLayout(self.layout)

    def load_products(self):
        # Simulación de carga de productos, en un sistema real cargarías de la base de datos
        productos = self.get_productos()  # Método para obtener productos

        if not productos:
            self.product_list_widget.addItem("No hay productos registrados.")
        else:
            for producto in productos:
                self.product_list_widget.addItem(producto)

    def get_productos(self):
        # Aquí iría la lógica para obtener los productos desde la base de datos
        # Por ahora, simplemente devolvemos una lista de ejemplo
        return ["Producto A", "Producto B", "Producto C"]  # Ejemplo de productos

    def open_register_product_view(self):
        from registro_producto import RegistroProductoView  # Importación local para evitar circularidad
        self.register_product_view = RegistroProductoView()
        self.register_product_view.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())
