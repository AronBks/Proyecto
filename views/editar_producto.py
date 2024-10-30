from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from connector import DBConnector

class EditarProductoView(QWidget):
    producto_editado = Signal()

    def __init__(self, producto):
        super().__init__()
        self.setWindowTitle('Editar Producto')
        self.setGeometry(400, 150, 300, 400)
        self.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF;")

        # Inicializar conector de base de datos
        self.connector = DBConnector()

        # Guardar datos del producto actual
        self.producto = producto

        # Layout principal
        self.layout = QVBoxLayout()

        # Etiqueta de título
        self.title_label = QLabel(f'Editar Producto: {self.producto[0]}')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Campo para nombre (con etiqueta)
        self.nombre_label = QLabel('Nombre')
        self.nombre_input = QLineEdit(self)
        self.nombre_input.setText(self.producto[0])  # Cargar nombre actual
        self.layout.addWidget(self.nombre_label)
        self.layout.addWidget(self.nombre_input)

        # Campo para descripción (con etiqueta)
        self.descripcion_label = QLabel('Descripción')
        self.descripcion_input = QLineEdit(self)
        self.descripcion_input.setText(self.producto[1])  # Cargar descripción actual
        self.layout.addWidget(self.descripcion_label)
        self.layout.addWidget(self.descripcion_input)

        # Campo para precio (con etiqueta)
        self.precio_label = QLabel('Precio')
        self.precio_input = QLineEdit(self)
        self.precio_input.setText(str(self.producto[2]))  # Cargar precio actual
        self.layout.addWidget(self.precio_label)
        self.layout.addWidget(self.precio_input)

        # Campo para stock (con etiqueta)
        self.stock_label = QLabel('Stock')
        self.stock_input = QLineEdit(self)
        self.stock_input.setText(str(self.producto[3]))  # Cargar stock actual
        self.layout.addWidget(self.stock_label)
        self.layout.addWidget(self.stock_input)

        # Campo para código de barras (con etiqueta)
        self.codigo_barras_label = QLabel('Código de Barras')
        self.codigo_barras_input = QLineEdit(self)
        self.codigo_barras_input.setText(self.producto[4])  # Cargar código de barras actual
        self.codigo_barras_input.setReadOnly(True)  # No permitir edición
        self.codigo_barras_input.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF; padding: 8px;")
        self.layout.addWidget(self.codigo_barras_label)
        self.layout.addWidget(self.codigo_barras_input)

        # Botones para guardar o cancelar
        button_layout = QHBoxLayout()

        self.save_button = QPushButton('Guardar')
        self.save_button.setStyleSheet("""background-color: #28A745; color: #FFFFFF; padding: 10px; border: none; border-radius: 5px;""")
        self.save_button.clicked.connect(self.guardar_cambios)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton('Cancelar')
        self.cancel_button.setStyleSheet("""background-color: #FF4C4C; color: #FFFFFF; padding: 10px; border: none; border-radius: 5px;""")
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def guardar_cambios(self):
        # Obtener los valores actualizados de los campos
        nuevo_nombre = self.nombre_input.text().strip()
        nueva_descripcion = self.descripcion_input.text().strip()
        
        # Manejo de entradas numéricas
        try:
            nuevo_precio = float(self.precio_input.text().strip())
            nuevo_stock = int(self.stock_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Por favor, ingrese valores válidos para el precio y stock.')
            return

        # Actualizar en la base de datos
        connection = self.connector.conectar()
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE productos 
                    SET nombre = %s, descripcion = %s, precio = %s, stock = %s
                    WHERE codigo_barras = %s
                """
                cursor.execute(sql, (nuevo_nombre, nueva_descripcion, nuevo_precio, nuevo_stock, self.producto[4]))
                connection.commit()

                QMessageBox.information(self, 'Éxito', 'Producto actualizado con éxito.')
                self.close()  # Cerrar ventana después de guardar
                self.producto_editado.emit()  # Emitir señal para actualizar la lista
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error al actualizar el producto: {str(e)}')
        finally:
            self.connector.cerrar_conexion(connection)