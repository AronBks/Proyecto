import pymysql

class VentaDAO:
    def __init__(self, connector):
        self.connector = connector

    def registrar_venta(self, id_cliente, id_usuario, id_producto, cantidad, total, estado, descripcion, generar_factura):
        connection = self.connector.conectar()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Registrar venta
                    cursor.execute(
                        "INSERT INTO ventas (id_cliente, id_usuario, total, estado, fecha) VALUES (%s, %s, %s, %s, NOW())",
                        (id_cliente, id_usuario, total, estado)
                    )
                    id_venta = cursor.lastrowid

                    # Registrar detalle de venta
                    cursor.execute(
                        "INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                        (id_venta, id_producto, cantidad, total / cantidad)  # Suponiendo que el total es la suma de todos los productos
                    )

                    # Confirmar cambios
                    connection.commit()
                    return True
            except pymysql.MySQLError as e:
                print(f"Error al registrar venta: {e}")
                connection.rollback()
                return False
            finally:
                self.connector.cerrar_conexion(connection)
        return False
