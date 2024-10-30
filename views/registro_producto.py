from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QDoubleSpinBox, QSpinBox, QApplication, QMessageBox
)
from PySide6.QtCore import Qt, Signal
import sys
import pymysql
from connector import DBConnector


class ProductoDAO:
    def __init__(self, connector):
        self.connector = connector

    def registrar_producto(self, nombre, descripcion, precio, stock, codigo_barras):
        connection = self.connector.conectar()
        try:
            with connection.cursor() as cursor:
                # Verificar si el código de barras ya existe
                sql_check = "SELECT COUNT(*) FROM productos WHERE codigo_barras = %s"
                cursor.execute(sql_check, (codigo_barras,))
                result = cursor.fetchone()
                
                if result[0] > 0:
                    return "El código de barras ya está registrado."

                # Insertar el producto
                sql = "INSERT INTO productos (nombre, descripcion, precio, stock, codigo_barras) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (nombre, descripcion, precio, stock, codigo_barras))
                connection.commit()
                return "Producto registrado con éxito."
        except pymysql.MySQLError as e:
            return f"Error al registrar el producto: {e}"
        finally:
            self.connector.cerrar_conexion(connection)


class RegistroProductoView(QWidget):
    producto_registrado = Signal()  # Definir la señal aquí

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Registro de Productos')
        self.setGeometry(300, 100, 400, 450)

        # Crear el conector y DAO
        self.connector = DBConnector()
        self.producto_dao = ProductoDAO(self.connector)

        # Crear los widgets
        self.nombre_label = QLabel('Nombre del Producto:')
        self.nombre_input = QLineEdit()
        self.nombre_input.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF; border: 1px solid #CCCCCC; padding: 5px;")

        self.precio_label = QLabel('Precio:')
        self.precio_input = QDoubleSpinBox()
        self.precio_input.setRange(0.0, 10000.0)
        self.precio_input.setDecimals(2)
        self.precio_input.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF; border: 1px solid #CCCCCC; padding: 5px;")

        self.cantidad_label = QLabel('Stock:')
        self.cantidad_input = QSpinBox()
        self.cantidad_input.setRange(0, 1000)
        self.cantidad_input.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF; border: 1px solid #CCCCCC; padding: 5px;")
        self.cantidad_input.setValue(0)

        self.descripcion_label = QLabel('Descripción:')
        self.descripcion_input = QLineEdit()
        self.descripcion_input.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF; border: 1px solid #CCCCCC; padding: 5px;")

        self.codigo_barras_label = QLabel('Código de Barras:')
        self.codigo_barras_input = QLineEdit()
        self.codigo_barras_input.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF; border: 1px solid #CCCCCC; padding: 5px;")

        self.registrar_button = QPushButton('Registrar Producto')
        self.registrar_button.setStyleSheet("""background-color: #FF6F61; color: #FFFFFF; padding: 10px 20px; border: none; border-radius: 5px;""")
        self.registrar_button.clicked.connect(self.registrar_producto)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.nombre_label)
        layout.addWidget(self.nombre_input)
        layout.addWidget(self.precio_label)
        layout.addWidget(self.precio_input)
        layout.addWidget(self.cantidad_label)
        layout.addWidget(self.cantidad_input)
        layout.addWidget(self.descripcion_label)
        layout.addWidget(self.descripcion_input)
        layout.addWidget(self.codigo_barras_label)
        layout.addWidget(self.codigo_barras_input)
        layout.addWidget(self.registrar_button)

        self.setLayout(layout)

    def registrar_producto(self):
        nombre = self.nombre_input.text()
        precio = self.precio_input.value()
        cantidad = self.cantidad_input.value()
        descripcion = self.descripcion_input.text()
        codigo_barras = self.codigo_barras_input.text()

        # Validar campos vacíos
        if not nombre or not codigo_barras or not descripcion:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return
        
        if precio <= 0:
            QMessageBox.warning(self, "Error", "El precio debe ser mayor a 0.")
            return

        # Registrar el producto
        resultado = self.producto_dao.registrar_producto(nombre, descripcion, precio, cantidad, codigo_barras)

        if "éxito" in resultado:
            QMessageBox.information(self, "Éxito", resultado)
            self.limpiar_campos()  # Limpiar los campos tras el registro exitoso
            self.producto_registrado.emit()  # Emitir señal de registro exitoso
            self.close()  # Cerrar la ventana después de registrar exitosamente
        else:
            QMessageBox.warning(self, "Error", resultado)

    def limpiar_campos(self):
        self.nombre_input.clear()
        self.precio_input.setValue(0)
        self.cantidad_input.setValue(0)
        self.descripcion_input.clear()
        self.codigo_barras_input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_registro_producto = RegistroProductoView()
    ventana_registro_producto.show()
    sys.exit(app.exec())