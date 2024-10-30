from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.auth_controller import AuthController  # Importamos el controlador de autenticación


class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Iniciar Sesión')
        self.setFixedSize(600, 300)

        # Inicializar AuthController
        self.auth_controller = AuthController()

        # Estilo personalizado mejorado
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
            }
            QLabel {
                font-size: 14px;
                color: #ecf0f1;
            }
            QLineEdit {
                font-size: 14px;
                padding: 10px;
                border: 2px solid #34495e;
                border-radius: 5px;
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #FF6F61;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)

        # Crear el logo
        logo_label = QLabel(self)
        pixmap = QPixmap('assets/icons/logo.png')  # Asegúrate de tener la ruta correcta del logo
        logo_label.setPixmap(pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)

        # Crear etiquetas y campos de entrada
        self.email_label = QLabel('Correo:')
        self.email_input = QLineEdit()

        self.password_label = QLabel('Contraseña:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        # Mensaje de estado para mostrar éxito o fallo
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)

        # Botón para iniciar sesión
        self.login_button = QPushButton('Iniciar Sesión')
        self.login_button.clicked.connect(self.iniciar_sesion)

        # Layout del formulario
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_button)
        form_layout.addWidget(self.status_label)

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.addWidget(logo_label)  # Logo a la izquierda
        main_layout.addLayout(form_layout)  # Formulario a la derecha
        main_layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(main_layout)

    def iniciar_sesion(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            self.status_label.setText("Debe ingresar un correo y una contraseña")
            return

        usuario, error = self.auth_controller.validar_credenciales(email, password)

        if usuario:
            self.status_label.setText(f"Bienvenido, {usuario['nombre']}")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText(error)
            self.status_label.setStyleSheet("color: red;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginView()
    window.show()
    sys.exit(app.exec())
