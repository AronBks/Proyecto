from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QGridLayout, QVBoxLayout, QHBoxLayout)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from connector import DBConnector  # Ajusta la ruta según tu estructura de carpetas
import pymysql

class RegistroWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Registro')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: white;")

        # Fuente para los títulos y subtítulos
        title_font = QFont("Montserrat", 18, QFont.Bold)
        subtitle_font = QFont("Montserrat", 14, QFont.Bold)

        # Layout principal
        main_layout = QGridLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Título "Información"
        lbl_info = QLabel("Información:")
        lbl_info.setFont(title_font)
        lbl_info.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(lbl_info, 0, 0, 1, 2)

        # Campos de entrada (nombre, CI, celular, dirección, correo, clave)
        lbl_name = QLabel("Nombres y Apellidos")
        lbl_name.setFont(subtitle_font)
        lbl_name.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(lbl_name, 1, 0)

        self.txt_name = QLineEdit()
        self.txt_name.setStyleSheet("background-color: #e1e2e2; color: black; border-radius: 10px; padding: 5px;")
        main_layout.addWidget(self.txt_name, 2, 0, 1, 2)

        lbl_ci = QLabel("C.I.")
        lbl_ci.setFont(subtitle_font)
        lbl_ci.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(lbl_ci, 3, 0)

        self.txt_ci = QLineEdit()
        self.txt_ci.setStyleSheet("background-color: #e1e2e2; color: black; border-radius: 10px; padding: 5px;")
        main_layout.addWidget(self.txt_ci, 4, 0)

        lbl_phone = QLabel("N° Celular")
        lbl_phone.setFont(subtitle_font)
        lbl_phone.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(lbl_phone, 3, 1)

        self.txt_phone = QLineEdit()
        self.txt_phone.setStyleSheet("background-color: #e1e2e2; color: black; border-radius: 10px; padding: 5px;")
        main_layout.addWidget(self.txt_phone, 4, 1)

        lbl_address = QLabel("Dirección")
        lbl_address.setFont(subtitle_font)
        lbl_address.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(lbl_address, 5, 0)

        self.txt_address = QLineEdit()
        self.txt_address.setStyleSheet("background-color: #e1e2e2; color: black; border-radius: 10px; padding: 5px;")
        main_layout.addWidget(self.txt_address, 6, 0, 1, 2)

        lbl_email = QLabel("Correo")
        lbl_email.setFont(subtitle_font)
        lbl_email.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(lbl_email, 7, 0)

        self.txt_email = QLineEdit()
        self.txt_email.setStyleSheet("background-color: #e1e2e2; color: black; border-radius: 10px; padding: 5px;")
        main_layout.addWidget(self.txt_email, 8, 0)

        lbl_password = QLabel("Clave")
        lbl_password.setFont(subtitle_font)
        lbl_password.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(lbl_password, 7, 1)

        password_layout = QHBoxLayout()
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setStyleSheet("background-color: #e1e2e2; color: black; border-radius: 10px; padding: 5px;")

        btn_show_password = QPushButton()
        btn_show_password.setIcon(QIcon('assets/icons/eye_icon.png'))
        btn_show_password.setFixedSize(24, 24)
        btn_show_password.setStyleSheet("background-color: transparent;")
        btn_show_password.setMouseTracking(True)
        btn_show_password.mousePressEvent = self.show_password
        btn_show_password.mouseReleaseEvent = self.hide_password

        password_layout.addWidget(self.txt_password)
        password_layout.addWidget(btn_show_password)
        main_layout.addLayout(password_layout, 8, 1)

        # Campo "Cargo"
        lbl_cargo = QLabel("Cargo")
        lbl_cargo.setFont(subtitle_font)
        lbl_cargo.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(lbl_cargo, 9, 0)

        self.combo_cargo = QComboBox()
        self.combo_cargo.addItems(["Administrador", "Empleado"])
        self.combo_cargo.setStyleSheet("""
            QComboBox {
                background-color: #ffca28;
                color: black;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
                border: none;
                padding-right: 20px; /* Espacio adicional para ocultar la flecha */
            }
            QComboBox::drop-down {
                border: none; /* Quita la flecha */
            }
            QComboBox QAbstractItemView {
                background-color: #ffca28;
                color: black;
            }
        """)
        main_layout.addWidget(self.combo_cargo, 10, 0)

        # Texto y botón Continuar
        lbl_info_text = QLabel("Completa toda tu información, esta\nservirá para ingresar al sistema y\npara mostrar en los reportes de ventas.")
        lbl_info_text.setFont(QFont("Montserrat", 12))
        lbl_info_text.setStyleSheet("color: #2C3E50;")
        lbl_info_text.setWordWrap(True)

        user_icon_layout = QVBoxLayout()
        user_icon_layout.addWidget(lbl_info_text, alignment=Qt.AlignTop)

        lbl_user_icon = QLabel()
        lbl_user_icon.setPixmap(QIcon('assets/icons/user_icon.png').pixmap(200, 200))
        user_icon_layout.addWidget(lbl_user_icon, alignment=Qt.AlignCenter)

        main_layout.addLayout(user_icon_layout, 4, 2, 4, 1, alignment=Qt.AlignRight | Qt.AlignTop)

        btn_continue = QPushButton("Finalizar")
        btn_continue.setStyleSheet("background-color: #ffca28; color: black; font-size: 16px; border-radius: 10px; padding: 10px;")
        btn_continue.clicked.connect(self.save_user_data)  # Conectar el botón al método de guardar
        main_layout.addWidget(btn_continue, 10, 2, alignment=Qt.AlignBottom | Qt.AlignRight)

    def show_password(self, event):
        self.txt_password.setEchoMode(QLineEdit.Normal)

    def hide_password(self, event):
        self.txt_password.setEchoMode(QLineEdit.Password)

    def save_user_data(self):
        nombre_apellidos = self.txt_name.text()
        ci = self.txt_ci.text()
        celular = self.txt_phone.text()
        direccion = self.txt_address.text()
        correo = self.txt_email.text()
        password = self.txt_password.text()
        id_rol = 1 if self.combo_cargo.currentText() == "Administrador" else 2

        db_connector = DBConnector()
        connection = db_connector.conectar()
        
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = """
                    INSERT INTO usuarios (nombre_apellidos, ci, celular, direccion, correo, password, id_rol)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (nombre_apellidos, ci, celular, direccion, correo, password, id_rol))
                    connection.commit()
                    print("Usuario registrado exitosamente.")
            except pymysql.MySQLError as e:
                print(f"Error al registrar el usuario: {e}")
            finally:
                db_connector.cerrar_conexion(connection)

if __name__ == "__main__":
    app = QApplication([])
    window = RegistroWindow()
    window.show()
    app.exec()
