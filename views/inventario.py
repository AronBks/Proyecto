import sys
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox, QFormLayout, QLineEdit, QApplication
)
from PySide6.QtCore import Qt

# Asegúrate de que el sistema pueda encontrar el módulo 'controllers'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importaciones desde el directorio 'views'
from connector import DBConnector
from registro_producto import RegistroProductoView
from editar_producto import EditarProductoView
from controllers.producto_controller import ProductoController

class InventarioView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gestión de Productos')
        self.setGeometry(300, 100, 900, 600)
        self.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF;")

        # Inicializar el conector
        self.connector = DBConnector()
        self.product_controller = ProductoController(self.connector)

        # Layout principal (Horizontal para dividir lista de productos y detalles)
        self.main_layout = QHBoxLayout()

        # Layout de la lista de productos
        self.product_list_layout = QVBoxLayout()

        # Etiqueta de título
        self.title_label = QLabel('Gestión de Productos')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        self.product_list_layout.addWidget(self.title_label)

        # Barra de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Buscar producto...')
        self.search_input.setFixedHeight(40)
        self.search_input.setStyleSheet("font-size: 16px; padding: 10px; background-color: #2E2E2E; color: #FFFFFF; border-radius: 5px;")
        self.search_input.textChanged.connect(self.filtrar_productos)
        self.product_list_layout.addWidget(self.search_input)

        # Lista de productos
        self.product_list_widget = QListWidget()
        self.product_list_widget.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF; border: none; padding: 5px;")
        self.product_list_widget.itemClicked.connect(self.mostrar_detalles_producto)
        self.product_list_layout.addWidget(self.product_list_widget)

        # Layout para botones
        self.button_layout = QHBoxLayout()
        
        # Botón para agregar producto
        self.add_product_button = QPushButton('Añadir Producto')
        self.add_product_button.setStyleSheet("background-color: #2A9D8F; color: #FFFFFF; padding: 12px; border-radius: 5px; font-size: 16px;")
        self.add_product_button.clicked.connect(self.abrir_registro_producto)
        self.button_layout.addWidget(self.add_product_button)

        # Botón para editar producto
        self.edit_product_button = QPushButton('Editar Producto')
        self.edit_product_button.setStyleSheet("background-color: #FFA500; color: #FFFFFF; padding: 12px; border-radius: 5px; font-size: 16px;")
        self.edit_product_button.clicked.connect(self.editar_producto)
        self.button_layout.addWidget(self.edit_product_button)

        # Botón para eliminar producto
        self.delete_product_button = QPushButton('Eliminar Producto')
        self.delete_product_button.setStyleSheet("background-color: #FF4C4C; color: #FFFFFF; padding: 12px; border-radius: 5px; font-size: 16px;")
        self.delete_product_button.clicked.connect(self.eliminar_producto)
        self.button_layout.addWidget(self.delete_product_button)

        self.product_list_layout.addLayout(self.button_layout)
        self.main_layout.addLayout(self.product_list_layout, 1)

        # Layout de detalles de producto
        self.details_layout = QFormLayout()
        self.details_layout.setLabelAlignment(Qt.AlignLeft)

        self.details_label = QLabel('Detalles del Producto')
        self.details_label.setAlignment(Qt.AlignCenter)
        self.details_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; padding: 5px;")
        self.details_layout.addRow(self.details_label)

        # Campos de detalle del producto con diseño mejorado
        fields = {
            'Nombre:': 'nombre_input',
            'Descripción:': 'descripcion_input',
            'Precio:': 'precio_input',
            'Stock:': 'stock_input',
            'Código de Barras:': 'codigo_barras_input'
        }

        for label_text, attr_name in fields.items():
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px;")
            field = QLineEdit()
            field.setReadOnly(True)
            field.setStyleSheet("font-size: 16px; padding: 8px; border-radius: 5px; background-color: #333; color: #FFFFFF;")
            field.setFixedWidth(300)
            self.details_layout.addRow(label, field)
            setattr(self, attr_name, field)

        self.main_layout.addLayout(self.details_layout, 2)

        # Cargar productos al iniciar
        self.load_products()

        # Conectar el evento de escaneo de código de barras
        self.search_input.returnPressed.connect(self.detectar_codigo_barras)

        # Configurar el layout principal
        self.setLayout(self.main_layout)

    def load_products(self):
        self.product_list_widget.clear()
        productos = self.get_productos()

        if not productos:
            self.product_list_widget.addItem("No hay productos registrados.")
        else:
            for producto in productos:
                self.product_list_widget.addItem(producto)

    def get_productos(self):
        connection = self.connector.conectar()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT nombre FROM productos"
                cursor.execute(sql)
                resultados = cursor.fetchall()
                return [producto[0] for producto in resultados]
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            self.connector.cerrar_conexion(connection)

    def mostrar_detalles_producto(self, item):
        nombre_producto = item.text()
        connection = self.connector.conectar()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT nombre, descripcion, precio, stock, codigo_barras FROM productos WHERE nombre = %s"
                cursor.execute(sql, (nombre_producto,))
                resultado = cursor.fetchone()

                if resultado:
                    # Mostrar los detalles en los campos
                    self.nombre_input.setText(resultado[0])
                    self.descripcion_input.setText(resultado[1])
                    self.precio_input.setText(str(resultado[2]))
                    self.stock_input.setText(str(resultado[3]))
                    self.codigo_barras_input.setText(resultado[4])
                else:
                    QMessageBox.warning(self, "Advertencia", "No se encontraron detalles para el producto seleccionado.")
        except Exception as e:
            print(f"Error al obtener detalles del producto: {e}")
        finally:
            self.connector.cerrar_conexion(connection)

    def filtrar_productos(self):
        filtro = self.search_input.text().lower()
        for i in range(self.product_list_widget.count()):
            item = self.product_list_widget.item(i)
            item.setHidden(filtro not in item.text().lower())

    def abrir_registro_producto(self):
        self.registro_view = RegistroProductoView()
        self.registro_view.producto_registrado.connect(self.load_products)
        self.registro_view.show()

    def editar_producto(self):
        selected_item = self.product_list_widget.currentItem()
        if selected_item:
            nombre_producto = selected_item.text()
            producto = self.obtener_datos_producto(nombre_producto)
            if producto:
                self.editar_view = EditarProductoView(producto)
                self.editar_view.producto_editado.connect(self.load_products)
                self.editar_view.show()
            else:
                QMessageBox.warning(self, "Advertencia", "No se pudo encontrar el producto para editar.")
        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona un producto para editar.")

    def obtener_datos_producto(self, nombre_producto):
        connection = self.connector.conectar()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT nombre, descripcion, precio, stock, codigo_barras FROM productos WHERE nombre = %s"
                cursor.execute(sql, (nombre_producto,))
                resultado = cursor.fetchone()
                return resultado
        except Exception as e:
            print(f"Error al obtener datos del producto: {e}")
            return None
        finally:
            self.connector.cerrar_conexion(connection)

    def eliminar_producto(self):
        selected_item = self.product_list_widget.currentItem()
        if selected_item:
            nombre_producto = selected_item.text()
            confirmar = QMessageBox.question(self, "Confirmar Eliminación", f"¿Estás seguro de eliminar {nombre_producto}?",
                                             QMessageBox.Yes | QMessageBox.No)
            if confirmar == QMessageBox.Yes:
                connection = self.connector.conectar()
                try:
                    with connection.cursor() as cursor:
                        sql = "DELETE FROM productos WHERE nombre = %s"
                        cursor.execute(sql, (nombre_producto,))
                        connection.commit()
                        self.load_products()
                        QMessageBox.information(self, "Éxito", "Producto eliminado exitosamente.")
                except Exception as e:
                    print(f"Error al eliminar producto: {e}")
                    QMessageBox.critical(self, "Error", "No se pudo eliminar el producto.")
                finally:
                    self.connector.cerrar_conexion(connection)
        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona un producto para eliminar.")

    def detectar_codigo_barras(self):
      codigo_barras = self.search_input.text().strip()
      if codigo_barras:
        # Lógica para buscar el producto por código de barras.
        connection = self.connector.conectar()
        try:
            with connection.cursor() as cursor:
                # Buscar el nombre del producto basado en el código de barras.
                sql = "SELECT nombre FROM productos WHERE codigo_barras = %s"
                cursor.execute(sql, (codigo_barras,))
                resultado = cursor.fetchone()

                if resultado:
                    nombre_producto = resultado[0]
                    # Verificar si el producto está en la lista
                    item = self.product_list_widget.findItems(nombre_producto, Qt.MatchExactly)
                    if item:
                        self.product_list_widget.setCurrentItem(item[0])
                        self.mostrar_detalles_producto(item[0])  # Mostrar detalles del producto
                    else:
                        QMessageBox.warning(self, "Advertencia", "El producto no se encuentra en la lista.")
                else:
                    QMessageBox.warning(self, "Advertencia", "No se encontró el producto por código de barras.")
        except Exception as e:
            print(f"Error al buscar producto por código de barras: {e}")
        finally:
            self.connector.cerrar_conexion(connection)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventarioView()
    window.show()
    sys.exit(app.exec())
