import pymysql

class Venta:
    def __init__(self, id_cliente, id_usuario, total, estado='completada'):
        self.id_cliente = id_cliente
        self.id_usuario = id_usuario
        self.total = total
        self.estado = estado

    def guardar(self, db_connector):
        connection = db_connector.conectar()
        if connection:
            try:
                with connection.cursor() as cursor:
                    query = """
                    INSERT INTO ventas (id_cliente, id_usuario, total, estado)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, (self.id_cliente, self.id_usuario, self.total, self.estado))
                    connection.commit()
                    return cursor.lastrowid  # Retorna el ID de la venta insertada
            finally:
                db_connector.cerrar_conexion(connection)

class DetalleVenta:
    def __init__(self, id_venta, id_producto, cantidad, precio_unitario, descuento=0):
        self.id_venta = id_venta
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.descuento = descuento

    def guardar(self, db_connector):
        connection = db_connector.conectar()
        if connection:
            try:
                with connection.cursor() as cursor:
                    query = """
                    INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, descuento)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (self.id_venta, self.id_producto, self.cantidad, self.precio_unitario, self.descuento))
                    connection.commit()
            finally:
                db_connector.cerrar_conexion(connection)
