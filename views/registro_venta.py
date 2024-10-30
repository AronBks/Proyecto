from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, 
    QTableWidget, QTableWidgetItem, QHBoxLayout, QSpinBox, 
    QMessageBox, QApplication, QHeaderView
)
from PySide6.QtCore import Qt
import sys
from connector import DBConnector
from productoDao import ProductoDAO

class RegistroVentaView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Registro de Ventas')
        self.setGeometry(300, 100, 800, 600)
        self.setStyleSheet(self.style_sheet())

        # Crear el conector y el DAO
        self.connector = DBConnector()
        self.producto_dao = ProductoDAO(self.connector)

        # Propiedades adicionales
        self.productos_seleccionados = []
        self.total = 0.0

        # Inicializar la interfaz de usuario
        self.init_ui()

    def style_sheet(self):
        return """
            QWidget {
                font-family: Arial;
                background-color: #2e2e2e;
                color: #e0e0e0;
            }
            QLabel {
                font-size: 14px;
                color: #e0e0e0;
            }
            QTableWidget, QPushButton, QSpinBox {
                font-size: 14px;
                padding: 8px;
                margin-bottom: 15px;
                color: #e0e0e0;
                background-color: #424242;
            }
            QPushButton {
                background-color: #1a1a1a;
                border: 1px solid #ff0000;
                color: #ff0000;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff0000;
                color: #ffffff;
            }
        """

    def init_ui(self):
        # Layout principal
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        # Tabla de productos disponibles
        self.producto_table = QTableWidget()
        self.producto_table.setColumnCount(4)
        self.producto_table.setHorizontalHeaderLabels(["ID", "Nombre", "Precio", "Stock"])
        self.producto_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Ajustar el tamaño de las columnas para que ocupen todo el espacio
        header = self.producto_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.producto_table)

        # Cargar productos en la tabla
        self.cargar_productos()

        # SpinBox para cantidad
        cantidad_layout = QHBoxLayout()
        self.cantidad_spinbox = QSpinBox()
        self.cantidad_spinbox.setRange(1, 100)
        cantidad_label = QLabel("Cantidad:")
        cantidad_layout.addWidget(cantidad_label)
        cantidad_layout.addWidget(self.cantidad_spinbox)
        layout.addLayout(cantidad_layout)

        # Botón para agregar al carrito
        self.agregar_button = QPushButton("Agregar al Carrito")
        self.agregar_button.clicked.connect(self.agregar_al_carrito)
        layout.addWidget(self.agregar_button)

        # Tabla de carrito
        self.carrito_table = QTableWidget()
        self.carrito_table.setColumnCount(4)
        self.carrito_table.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "Total"])

        # Ajustar el tamaño de las columnas para que ocupen todo el espacio
        carrito_header = self.carrito_table.horizontalHeader()
        carrito_header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.carrito_table)

        # Mostrar el total
        self.total_label = QLabel("Total: $0.00")
        layout.addWidget(self.total_label)

        # Botón para finalizar compra
        self.finalizar_button = QPushButton("Finalizar Compra")
        self.finalizar_button.clicked.connect(self.finalizar_compra)
        layout.addWidget(self.finalizar_button)

    def cargar_productos(self):
        try:
            productos = self.producto_dao.obtener_productos()
            self.producto_table.setRowCount(len(productos))
            self.productos = productos  # Guardamos los productos
            for row, producto in enumerate(productos):
                self.producto_table.setItem(row, 0, QTableWidgetItem(str(producto['id'])))
                self.producto_table.setItem(row, 1, QTableWidgetItem(producto['nombre']))
                self.producto_table.setItem(row, 2, QTableWidgetItem(f"${producto['precio']}"))
                self.producto_table.setItem(row, 3, QTableWidgetItem(str(producto['stock'])))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar productos: {str(e)}")

    def agregar_al_carrito(self):
        selected_row = self.producto_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Selecciona un producto de la lista.")
            return

        try:
            producto_id = int(self.producto_table.item(selected_row, 0).text())
            nombre = self.producto_table.item(selected_row, 1).text()
            precio = float(self.producto_table.item(selected_row, 2).text().replace("$", ""))
            stock = int(self.producto_table.item(selected_row, 3).text())
            cantidad = self.cantidad_spinbox.value()

            if cantidad > stock:
                QMessageBox.warning(self, "Error", f"No hay suficiente stock para {nombre}. Disponible: {stock}")
                return

            # Reducir el stock en la tabla de productos
            nuevo_stock = stock - cantidad
            self.producto_table.setItem(selected_row, 3, QTableWidgetItem(str(nuevo_stock)))

            # Alerta de poco stock
            if nuevo_stock < 5:
                QMessageBox.warning(self, "Advertencia", f"Queda poco stock de {nombre}. Stock actual: {nuevo_stock}")

            # Calcular total y agregar producto al carrito
            total = precio * cantidad
            row_count = self.carrito_table.rowCount()
            self.carrito_table.insertRow(row_count)
            self.carrito_table.setItem(row_count, 0, QTableWidgetItem(str(producto_id)))
            self.carrito_table.setItem(row_count, 1, QTableWidgetItem(nombre))
            self.carrito_table.setItem(row_count, 2, QTableWidgetItem(str(cantidad)))
            self.carrito_table.setItem(row_count, 3, QTableWidgetItem(f"${total:.2f}"))

            # Actualizar total
            self.total += total
            self.total_label.setText(f"Total: ${self.total:.2f}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar al carrito: {str(e)}")

    def finalizar_compra(self):
        if self.carrito_table.rowCount() == 0:
            QMessageBox.warning(self, "Carrito vacío", "No hay productos en el carrito.")
            return

        # Paso 1: Registrar la venta
        total_compra = self.total
        id_cliente = 1  # Cliente predeterminado, asegurarte de que existe en la base de datos
        id_usuario = 2  # Usuario predeterminado, asegurarte de que existe en la base de datos

        print(f"Intentando registrar venta: Cliente ID: {id_cliente}, Usuario ID: {id_usuario}, Total: {total_compra}")

        try:
            query_venta = """
                INSERT INTO ventas (id_cliente, id_usuario, total)
                VALUES (%s, %s, %s)
            """
            self.producto_dao.connector.ejecutar_modificacion(query_venta, (id_cliente, id_usuario, total_compra))

            # Obtener el ID de la venta recién creada
            query_ultima_venta = "SELECT LAST_INSERT_ID() as id_venta"
            resultado = self.producto_dao.connector.ejecutar_query(query_ultima_venta)
            id_venta = resultado[0]['id_venta'] if resultado else None

            if not id_venta:
                QMessageBox.critical(self, "Error", "No se pudo registrar la venta.")
                return

            # Paso 2: Registrar los detalles de la venta (productos vendidos) y actualizar stock
            for row in range(self.carrito_table.rowCount()):
                producto_id = int(self.carrito_table.item(row, 0).text())
                cantidad = int(self.carrito_table.item(row, 2).text())
                precio_unitario = float(self.carrito_table.item(row, 3).text().replace("$", "")) / cantidad
                descuento = 0  # Puedes implementar lógica para aplicar descuentos si es necesario

                # Registrar el detalle de la venta
                query_detalle_venta = """
                    INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, descuento)
                    VALUES (%s, %s, %s, %s, %s)
                """
                self.producto_dao.connector.ejecutar_modificacion(query_detalle_venta, (id_venta, producto_id, cantidad, precio_unitario, descuento))

                # Actualizar el stock del producto en la base de datos
                producto = self.producto_dao.obtener_producto_por_id(producto_id)
                nuevo_stock = producto['stock'] - cantidad
                query_actualizar_stock = "UPDATE productos SET stock = %s WHERE id = %s"
                self.producto_dao.connector.ejecutar_modificacion(query_actualizar_stock, (nuevo_stock, producto_id))

            # Paso 3: Limpiar el carrito y resetear el total
            QMessageBox.information(self, "Compra finalizada", "La compra se ha realizado con éxito.")
            self.carrito_table.setRowCount(0)
            self.total = 0.0
            self.total_label.setText("Total: $0.00")
            self.cargar_productos()  # Recargar la tabla de productos
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al finalizar la compra: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = RegistroVentaView()
    ventana.show()
    sys.exit(app.exec())