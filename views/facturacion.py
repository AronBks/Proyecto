from PySide6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QWidget, QScrollArea, 
                               QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, 
                               QFrame, QLineEdit)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PIL import Image, ImageQt
import pymysql
import io
from views.connector import DBConnector
from register_user import RegistroWindow

class FacturacionWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Facturación")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        inner_widget = QWidget()
        inner_layout = QVBoxLayout(inner_widget)
        inner_widget.setFixedSize(400, 800)

        self.add_encabezado(inner_layout)
        self.add_detalle_ticket(inner_layout)
        self.add_pie(inner_layout)

        scroll.setWidget(inner_widget)
        main_layout.addWidget(scroll)

        right_layout = QVBoxLayout()
        right_layout.addStretch()
        self.add_personaliza_ticket(right_layout)

        continuar_btn = QPushButton("Continuar")
        continuar_btn.setStyleSheet(""" 
            background-color: #ffca28; 
            padding: 10px; 
            font-size: 14px; 
            color: black;
            border: none;
            border-radius: 15px;
        """)
        continuar_btn.setFixedSize(150, 50)
        continuar_btn.clicked.connect(self.generate_invoice)
        continuar_btn.clicked.connect(self.continue_to_register) 
        right_layout.addWidget(continuar_btn, alignment=Qt.AlignHCenter | Qt.AlignBottom)

        main_layout.addLayout(right_layout)
        self.setStyleSheet("background-color: white;")

    def add_encabezado(self, layout):
        config_data = DBConnector().get_config_data()

        logo_label = QLabel()
        logo_data = config_data["logo"]
        if logo_data:
            image = Image.open(io.BytesIO(logo_data))
            pixmap = QPixmap.fromImage(ImageQt.ImageQt(image))
        else:
            pixmap = QPixmap("assets/icons/logo.png")

        logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)

        empresa_title_label = QLabel(config_data["nombre_empresa"])
        empresa_title_label.setAlignment(Qt.AlignCenter)
        empresa_title_label.setStyleSheet("color: black; font-weight: bold; font-size: 18px;")

        encabezado_layout = QVBoxLayout()
        encabezado_layout.addWidget(logo_label)
        encabezado_layout.addWidget(empresa_title_label)

        self.ruc_line_edit = self.add_line_edit_with_background(encabezado_layout, "###########", "ruc")
        self.direccion_line_edit = self.add_line_edit_with_background(encabezado_layout, "Dirección", "direccion")
        self.region_line_edit = self.add_line_edit_with_background(encabezado_layout, "Región-Departamento", "region")
        self.telefono_line_edit = self.add_line_edit_with_background(encabezado_layout, "Teléfono", "telefono")

        layout.addLayout(encabezado_layout)

    def add_detalle_ticket(self, layout):
        layout.addSpacing(20)
        self.add_horizontal_separator(layout)

        self.add_label_pair(layout, "Cajero:", "Nombre del Cajero")
        self.add_label_pair(layout, "Fech. Emisión:", "00/00/24")
        self.add_horizontal_separator(layout)

        header_layout = QHBoxLayout()
        header_labels = ["Cant", "Descripción", "Importe"]
        for label_text in header_labels:
            header_label = QLabel(label_text)
            header_label.setStyleSheet("font-weight: bold; font-size: 12px; color: black;")
            header_label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(header_label)
        layout.addLayout(header_layout)

        self.add_horizontal_separator(layout)

        product_layout = QHBoxLayout()
        product_cant = QLabel("1")
        product_desc = QLabel("Ejemplo de Producto")
        product_importe = QLabel("0,00")

        product_cant.setStyleSheet("font-size: 12px; color: black;")
        product_desc.setStyleSheet("font-size: 12px; color: black;")
        product_importe.setStyleSheet("font-size: 12px; color: black;")

        product_layout.addWidget(product_cant, alignment=Qt.AlignCenter)
        product_layout.addWidget(product_desc, alignment=Qt.AlignCenter)
        product_layout.addWidget(product_importe, alignment=Qt.AlignCenter)
        layout.addLayout(product_layout)

        total_layout = QVBoxLayout()

        subtotal_label = QLabel("Sub. Total:".rjust(30) + " 0,00")
        subtotal_label.setStyleSheet("font-weight: bold; font-size: 12px; color: black;")
        total_layout.addWidget(subtotal_label, alignment=Qt.AlignRight)

        descuento_label = QLabel("Descuento:".rjust(30) + " 0,00")
        descuento_label.setStyleSheet("font-weight: bold; font-size: 12px; color: black;")
        total_layout.addWidget(descuento_label, alignment=Qt.AlignRight)

        total_label = QLabel("Total:".rjust(30) + " 0,00")
        total_label.setStyleSheet("font-weight: bold; font-size: 12px; color: black;")
        total_layout.addWidget(total_label, alignment=Qt.AlignRight)

        layout.addLayout(total_layout)

        self.add_horizontal_separator(layout)
        self.add_label_pair(layout, "Número de Productos", "1")
        self.add_horizontal_separator(layout)

    def add_pie(self, layout):
        gracias_label = QLabel("¡Gracias por elegirnos!")
        gracias_label.setAlignment(Qt.AlignCenter)
        gracias_label.setStyleSheet("background-color: #e1e2e2; color: black; padding: 5px;")
        layout.addWidget(gracias_label)

        vuelve_label = QLabel("Vuelve pronto")
        vuelve_label.setAlignment(Qt.AlignCenter)
        vuelve_label.setStyleSheet("background-color: #e1e2e2; color: black; padding: 5px;")
        layout.addWidget(vuelve_label)

        qr_label = QLabel()
        qr_pixmap = QPixmap("assets/icons/qr_code.png")
        qr_label.setPixmap(qr_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(qr_label)

    def add_personaliza_ticket(self, layout):
        personaliza_layout = QVBoxLayout()
        personaliza_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        personaliza_label = QLabel("Personaliza el Formato de tu\nTicket de Ventas")
        personaliza_label.setAlignment(Qt.AlignCenter)
        personaliza_label.setStyleSheet("color: #004aad; font-size: 16px; font-weight: bold;")

        flecha_label = QLabel()
        flecha_pixmap = QPixmap("assets/icons/flecha_abajo.png")
        flecha_label.setPixmap(flecha_pixmap.scaled(200, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        flecha_label.setAlignment(Qt.AlignCenter)

        personaliza_layout.addWidget(personaliza_label)
        personaliza_layout.addWidget(flecha_label)
        personaliza_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout.addLayout(personaliza_layout)

    def add_horizontal_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #c0c0c0;")
        layout.addWidget(line)

    def add_label_pair(self, layout, label_text1, label_text2):
        label_layout = QHBoxLayout()
        label1 = QLabel(label_text1)
        label2 = QLabel(label_text2)

        label1.setStyleSheet("color: black; font-weight: bold;")
        label2.setStyleSheet("color: black;")
        label_layout.addWidget(label1)
        label_layout.addWidget(label2)
        layout.addLayout(label_layout)

    def add_line_edit_with_background(self, layout, placeholder, object_name):
        line_edit = QLineEdit()
        line_edit.setObjectName(object_name)
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet(""" 
            QLineEdit {
                background-color: #e1e2e2; 
                border: 2px solid #b0b0b0; 
                border-radius: 10px; 
                padding: 5px; 
                font-size: 14px;
                color: black;
            }
        """)
        layout.addWidget(line_edit)
        return line_edit  # Return the line edit for later use

    def generate_invoice(self):
        id_venta = self.register_sale()  # Call the function to register the sale
        self.save_invoice_data()  # Save invoice data (RUC, dirección, región, teléfono)

        if id_venta:
            print("Venta registrada con ID:", id_venta)
        else:
            print("Error al registrar la venta.")

    def register_sale(self):
        # Here you should implement your logic to register the sale and return the sale ID
        # This is a placeholder example:
        return 1  # Example sale ID

    def save_invoice_data(self):
        ruc = self.ruc_line_edit.text()
        direccion = self.direccion_line_edit.text()
        region = self.region_line_edit.text()
        telefono = self.telefono_line_edit.text()

        connection = DBConnector().conectar()
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO datos_facturacion (ruc, direccion, region, telefono) 
                         VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql, (ruc, direccion, region, telefono))
                connection.commit()
        except pymysql.Error as e:
            print("Error al registrar los datos de facturación:", e)
        finally:
            connection.close()
    def continue_to_register(self):
        # Abrir la ventana de registro
        self.register_window = RegistroWindow()
        self.register_window.show()
        self.close()  # Cerrar la ventana actual si se desea
if __name__ == "__main__":
    app = QApplication([])
    widget = FacturacionWidget()
    widget.show()
    app.exec()
