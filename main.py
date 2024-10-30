# main.py

import sys
from PySide6.QtWidgets import QApplication
from views.config_inicial import ConfigInicial


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Crear y mostrar la ventana de configuración inicial
    ventana_config = ConfigInicial()
    ventana_config.show()

    # Ejecutar el bucle de eventos de la aplicación
    sys.exit(app.exec())
    