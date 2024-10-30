from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QWidget, QFileDialog
from PySide6.QtGui import QFont, QPixmap, QIcon, QCursor
from PySide6.QtCore import Qt, QRect, QSize
from views.impresora import ConfigWindow
import sys

class ExportImportDatabase(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setStyleSheet("background-color: white;")

    def init_ui(self):
        # Window title
        self.setWindowTitle("Exporte e Importe su Base de Datos")
        self.setGeometry(100, 100, 800, 600)
        
        # Fonts and Styles
        font_title = QFont("Montserrat", 14, QFont.Bold)
        font_label = QFont("Montserrat", 13, QFont.Bold)
        font_instruction = QFont("Montserrat", 12)
        label_color = "color: #2C3E50;"
        button_color = "background-color: #FEC007; color: black; border-radius: 20px; padding: 10px;"

        # Title Label (Top Title)
        self.title_label = QLabel("Exporte e Importe su Base de Datos:", self)
        self.title_label.setFont(font_title)
        self.title_label.setStyleSheet(label_color)
        self.title_label.setGeometry(QRect(50, 40, 700, 50))  # Adjusted width to fit the title

        # Subtitle (Adjusted "Ruta Exportar Backup" Position with bold font)
        self.path_label = QLabel("Ruta Exportar Backup:", self)
        self.path_label.setFont(font_label)
        self.path_label.setStyleSheet(label_color)
        self.path_label.setGeometry(QRect(325, 120, 410, 60))  # Aligned more to the left

        # Path Input and Folder Icon (Adjusted for more left alignment and longer width)
        self.path_input = QLineEdit(self)
        self.path_input.setGeometry(QRect(200, 180, 450, 35))  # Longer and more to the left
        self.path_input.setStyleSheet("background-color: #E0E0E0; border: none; border-radius: 15px; padding: 10px; font-size: 16px; color: #2C3E50;")
        self.path_input.setReadOnly(True)  # Set read-only to prevent manual input

        # Button to open folder dialog with enhanced hover effect
        self.folder_button = QPushButton(self)
        self.folder_button.setIcon(QIcon("assets/icons/carpeta_icon.png"))
        self.folder_button.setGeometry(QRect(650, 180, 50, 35))  # Icon aligned with the input field
        self.folder_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        self.folder_button.setIconSize(QSize(40, 40))
        self.folder_button.clicked.connect(self.open_folder_dialog)

        # Simulating hover effects with signals
        self.folder_button.enterEvent = self.on_hover_enter
        self.folder_button.leaveEvent = self.on_hover_leave

        # Instruction Label (Adjusted with smaller font and \n for line breaks)
        self.instruction_label = QLabel("Seleccione las carpetas donde se\n guardarán y desde donde importan sus\n respaldos:", self)
        self.instruction_label.setFont(font_instruction)
        self.instruction_label.setStyleSheet(label_color)
        self.instruction_label.setGeometry(QRect(-80, 300, 500, 60))  # Adjusted for smaller font and line breaks
        self.instruction_label.setAlignment(Qt.AlignCenter)

        # Recycle Bin Icon (Moved more to the left)
        self.recycle_bin_icon = QLabel(self)
        self.recycle_bin_icon.setPixmap(QPixmap("assets/icons/recycle_bin.png").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Corrected size
        self.recycle_bin_icon.setGeometry(QRect(100, 370, 150, 150))  # Moved to the left
        self.recycle_bin_icon.setAlignment(Qt.AlignCenter)
    
        # Continue Button
        self.continue_button = QPushButton("Continuar", self)
        self.continue_button.setFont(QFont("Montserrat", 11, QFont.Normal))
        self.continue_button.setGeometry(QRect(625, 464, 130, 50))  # Adjusted size and position
        self.continue_button.setStyleSheet("""
             background-color: #FEC007;
             color: black;
             border-radius: 25px;
             padding: 10px;
             text-align: center;
        """)
        self.continue_button.clicked.connect(self.open_config_window)
       

    def open_config_window(self):
        # Crea una nueva instancia de ConfigWindow y la muestra
        self.impresora_window = ConfigWindow()
        self.impresora_window.show()
        self.close()

    def on_hover_enter(self, event):
        # Simulating hover effect for the folder button
        self.folder_button.setStyleSheet("""
            QPushButton {
                background-color: #FEC007;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        self.folder_button.setIconSize(QSize(45, 45))  # Slightly enlarge icon
        self.setCursor(QCursor(Qt.PointingHandCursor))  # Change cursor to hand

    def on_hover_leave(self, event):
        # Remove hover effect when the cursor leaves
        self.folder_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
            }
        """)
        self.folder_button.setIconSize(QSize(40, 40))  # Return to original size
        self.setCursor(QCursor(Qt.ArrowCursor))  # Reset cursor to default

    def open_folder_dialog(self):
        # Open a file dialog to select a folder
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccione una carpeta")
        if folder_path:  # If a folder is selected, set the path in the QLineEdit
            self.path_input.setText(folder_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExportImportDatabase()
    window.show()
    sys.exit(app.exec())