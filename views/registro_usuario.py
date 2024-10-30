from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox,
    QApplication, QMessageBox, QGridLayout
)
import sys
import pymysql
from connector import DBConnector

class RegistroView(QWidget):
    def __init__(self, update_callback=None):
        super().__init__()
        self.update_callback = update_callback
        self.setWindowTitle('Registro de Usuario')
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(800, 600)

        # Widgets de entrada de datos
        self.nombre_label = QLabel('Nombre y Apellidos:')
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText('Ingresa el nombre y apellidos del usuario')

        self.ci_label = QLabel('C.I.:')
        self.ci_input = QLineEdit()
        self.ci_input.setPlaceholderText('Ingresa el C.I. del usuario')

        self.celular_label = QLabel('Celular:')
        self.celular_input = QLineEdit()
        self.celular_input.setPlaceholderText('Ingresa el número de celular del usuario')

        self.direccion_label = QLabel('Dirección:')
        self.direccion_input = QLineEdit()
        self.direccion_input.setPlaceholderText('Ingresa la dirección del usuario')

        self.correo_label = QLabel('Correo:')
        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText('Ingresa el correo del usuario')

        self.password_label = QLabel('Contraseña:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Ingresa una contraseña')

        self.rol_label = QLabel('Rol:')
        self.rol_combo = QComboBox()

        self.registrar_button = QPushButton('Registrar Usuario')
        self.registrar_button.clicked.connect(self.registrar_usuario)

        # Layout
        layout = QGridLayout()
        layout.addWidget(self.nombre_label, 0, 0)
        layout.addWidget(self.nombre_input, 0, 1, 1, 2)
        layout.addWidget(self.ci_label, 1, 0)
        layout.addWidget(self.ci_input, 1, 1, 1, 2)
        layout.addWidget(self.celular_label, 2, 0)
        layout.addWidget(self.celular_input, 2, 1, 1, 2)
        layout.addWidget(self.direccion_label, 3, 0)
        layout.addWidget(self.direccion_input, 3, 1, 1, 2)
        layout.addWidget(self.correo_label, 4, 0)
        layout.addWidget(self.correo_input, 4, 1, 1, 2)
        layout.addWidget(self.password_label, 5, 0)
        layout.addWidget(self.password_input, 5, 1, 1, 2)
        layout.addWidget(self.rol_label, 6, 0)
        layout.addWidget(self.rol_combo, 6, 1, 1, 2)
        layout.addWidget(self.registrar_button, 7, 0, 1, 3)

        self.setLayout(layout)
        self.cargar_roles()

        # Estilos para mantener un diseño coherente
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;  /* Fondo oscuro */
                color: #F0F0F0;  /* Texto blanco */
            }
            QLabel {
                font-size: 14px;
                color: #F0F0F0;  /* Texto blanco para etiquetas */
            }
            QLineEdit, QComboBox {
                padding: 5px;
                font-size: 14px;
                background-color: #3C3C3C;  /* Fondo de entrada */
                color: #F0F0F0;  /* Texto blanco */
                border: 1px solid #555;  /* Borde gris */
                border-radius: 5px;  /* Bordes redondeados */
            }
            QPushButton {
                background-color: #2A9D8F;  /* Color verde */
                color: white;  /* Texto blanco */
                padding: 10px;
                border-radius: 5px;  /* Bordes redondeados */
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #21867A;  /* Verde más oscuro al pasar el ratón */
            }
        """)

    def cargar_roles(self):
        connector = DBConnector()
        connection = connector.conectar()
        if connection:
            try:
                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute("SELECT id, nombre FROM roles")
                    roles = cursor.fetchall()
                    for role in roles:
                        self.rol_combo.addItem(role['nombre'], role['id'])
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar roles: {e}")
            finally:
                connector.cerrar_conexion(connection)

    def registrar_usuario(self):
        nombre = self.nombre_input.text()
        ci = self.ci_input.text()
        celular = self.celular_input.text()
        direccion = self.direccion_input.text()
        correo = self.correo_input.text()
        password = self.password_input.text()
        rol_id = self.rol_combo.currentData()

        if not nombre or not ci or not celular or not correo or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='zzzz',
            database='sistema_ventas',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO usuarios (nombre_apellidos, ci, celular, direccion, correo, password, id_rol)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (nombre, ci, celular, direccion, correo, password, rol_id))
            connection.commit()
            QMessageBox.information(self, "Éxito", "Usuario registrado con éxito.")
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar usuario: {e}")
        finally:
            connection.close()

        if self.update_callback:
            self.update_callback()  # Llama al callback para actualizar la tabla en UserView
        self.close()

    def limpiar_campos(self):
        self.nombre_input.clear()
        self.ci_input.clear()
        self.celular_input.clear()
        self.direccion_input.clear()
        self.correo_input.clear()
        self.password_input.clear()
        self.rol_combo.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_registro = RegistroView()
    ventana_registro.show()
    sys.exit(app.exec())
