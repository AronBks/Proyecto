from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QTableWidget, 
    QTableWidgetItem, QComboBox, QApplication, QMessageBox
)
from PySide6.QtCore import Qt
import sys
import os

# Agrega la ruta del directorio padre para importar los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.user_controller import UserController
from connector import DBConnector  # Importa DBConnector
from views.registro_usuario import RegistroView

class UserView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gestión de Usuarios')
        self.setGeometry(100, 100, 800, 600)  # Tamaño de la ventana
        self.setMinimumSize(800, 600)

        # Crear instancia de DBConnector
        connector = DBConnector()

        # Crear instancia de UserController con el conector
        self.controller = UserController(connector)

        # Widgets de entrada de datos
        self.nombre_label = QLabel('Nombre y Apellidos:')
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText('Ingresa el nombre del usuario')

        self.ci_label = QLabel('C.I.:')
        self.ci_input = QLineEdit()
        self.ci_input.setPlaceholderText('Ingresa la C.I. del usuario')

        self.celular_label = QLabel('Celular:')
        self.celular_input = QLineEdit()
        self.celular_input.setPlaceholderText('Ingresa el número de celular')

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

        self.estado_label = QLabel('Estado:')
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(['activo', 'inactivo'])

        self.id_rol_label = QLabel('Rol:')
        self.id_rol_input = QComboBox()
        self.id_rol_input.addItems(['1', '2', '3'])  

        # Botones
        self.registrar_button = QPushButton('Registrar Usuario')
        self.registrar_button.clicked.connect(self.abrir_registro_usuario)

        self.actualizar_button = QPushButton('Actualizar Usuario')
        self.actualizar_button.clicked.connect(self.actualizar_usuario)
        self.actualizar_button.setEnabled(False)  # Deshabilitado al inicio

        self.eliminar_button = QPushButton('Eliminar Usuario')
        self.eliminar_button.clicked.connect(self.eliminar_usuario)
        self.eliminar_button.setEnabled(False)  # Deshabilitado al inicio

        # Tabla de usuarios
        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(8)  # Ajustado para incluir el id_rol
        self.tabla_usuarios.setHorizontalHeaderLabels(['ID', 'Nombre y Apellidos', 'C.I.', 'Celular', 'Dirección', 'Correo', 'Estado', 'Rol'])
        self.tabla_usuarios.setStyleSheet("QTableWidget { gridline-color: lightgray; }")
        self.tabla_usuarios.horizontalHeader().setStretchLastSection(True)
        self.tabla_usuarios.itemSelectionChanged.connect(self.seleccionar_usuario)

        # Cargar usuarios
        self.cargar_usuarios()

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
        layout.addWidget(self.estado_label, 6, 0)
        layout.addWidget(self.estado_combo, 6, 1, 1, 2)
        layout.addWidget(self.id_rol_label, 7, 0)
        layout.addWidget(self.id_rol_input, 7, 1, 1, 2) 

        layout.addWidget(self.registrar_button, 7, 0, 1, 1)
        layout.addWidget(self.actualizar_button, 7, 1, 1, 1)
        layout.addWidget(self.eliminar_button, 7, 2, 1, 1)

        layout.addWidget(self.tabla_usuarios, 8, 0, 1, 3)

        self.setLayout(layout)

        # Estilos adicionales para un tema oscuro
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #F0F0F0;
            }
            QLabel {
                font-size: 14px;
                color: #F0F0F0;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                font-size: 14px;
                background-color: #3C3C3C;
                color: #F0F0F0;
                border: 1px solid #555;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #2A9D8F;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #21867A;
            }
            QTableWidget {
                background-color: #3C3C3C;
                color: #F0F0F0;
                gridline-color: #555;
            }
            QHeaderView::section {
                background-color: #555555;
                color: #F0F0F0;
                padding: 5px;
                border: 1px solid #444;
            }
        """)

    def abrir_registro_usuario(self):
        self.ventana_registro = RegistroView()
        self.ventana_registro.update_callback = self.cargar_usuarios  # Actualiza la tabla después de registrar
        self.ventana_registro.show()

    def actualizar_usuario(self):
        if not self.tabla_usuarios.selectedItems():
            QMessageBox.warning(self, "Error", "Por favor, selecciona un usuario para actualizar.")
            return

        row = self.tabla_usuarios.currentRow()
        usuario_id = self.tabla_usuarios.item(row, 0).text()
        nombre = self.nombre_input.text()
        ci = self.ci_input.text()
        celular = self.celular_input.text()
        direccion = self.direccion_input.text()
        correo = self.correo_input.text()
        password = self.password_input.text()
        estado = self.estado_combo.currentText()
        id_rol = self.id_rol_input.currentText()

        if not nombre or not ci or not celular or not direccion or not correo or not password:
            QMessageBox.warning(self, "Error", "Por favor, rellena todos los campos.")
            return

        try:
            self.controller.actualizar_usuario(usuario_id, nombre, ci, celular, direccion, correo, password, estado, id_rol)
            self.cargar_usuarios()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar usuario: {e}")

    def eliminar_usuario(self):
        if not self.tabla_usuarios.selectedItems():
            return

        row = self.tabla_usuarios.currentRow()
        usuario_id = self.tabla_usuarios.item(row, 0).text()

        confirm = QMessageBox.question(self, "Confirmar", "¿Seguro que deseas eliminar este usuario?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.controller.eliminar_usuario(usuario_id)
            self.cargar_usuarios()
            self.limpiar_campos()

    def cargar_usuarios(self):
        usuarios = self.controller.listar_usuarios()
        self.tabla_usuarios.setRowCount(0)  # Limpiar la tabla
        for usuario in usuarios:
            row_position = self.tabla_usuarios.rowCount()
            self.tabla_usuarios.insertRow(row_position)
            self.tabla_usuarios.setItem(row_position, 0, QTableWidgetItem(str(usuario[0])))  # ID
            self.tabla_usuarios.setItem(row_position, 1, QTableWidgetItem(usuario[1]))      # Nombre
            self.tabla_usuarios.setItem(row_position, 2, QTableWidgetItem(usuario[2]))      # C.I.
            self.tabla_usuarios.setItem(row_position, 3, QTableWidgetItem(usuario[3]))      # Celular
            self.tabla_usuarios.setItem(row_position, 4, QTableWidgetItem(usuario[4]))      # Dirección
            self.tabla_usuarios.setItem(row_position, 5, QTableWidgetItem(usuario[5]))      # Correo
            self.tabla_usuarios.setItem(row_position, 6, QTableWidgetItem(usuario[6]))      # Estado
            self.tabla_usuarios.setItem(row_position, 7, QTableWidgetItem(str(usuario[7])))  # Rol (id_rol)

    def seleccionar_usuario(self):
        selected_items = self.tabla_usuarios.selectedItems()
        if not selected_items:
            return

        row = self.tabla_usuarios.currentRow()
        self.nombre_input.setText(self.tabla_usuarios.item(row, 1).text())
        self.ci_input.setText(self.tabla_usuarios.item(row, 2).text())
        self.celular_input.setText(self.tabla_usuarios.item(row, 3).text())
        self.direccion_input.setText(self.tabla_usuarios.item(row, 4).text())
        self.correo_input.setText(self.tabla_usuarios.item(row, 5).text())
        self.estado_combo.setCurrentText(self.tabla_usuarios.item(row, 6).text())
        self.id_rol_input.setCurrentText(self.tabla_usuarios.item(row, 7).text())

        self.actualizar_button.setEnabled(True)
        self.eliminar_button.setEnabled(True)

    def limpiar_campos(self):
        self.nombre_input.clear()
        self.ci_input.clear()
        self.celular_input.clear()
        self.direccion_input.clear()
        self.correo_input.clear()
        self.password_input.clear()
        self.estado_combo.setCurrentIndex(0)
        self.id_rol_input.setCurrentIndex(0)
        self.actualizar_button.setEnabled(False)
        self.eliminar_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserView()
    window.show()
    sys.exit(app.exec())
