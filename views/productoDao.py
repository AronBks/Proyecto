# productoDao.py
import pymysql

class ProductoDAO:
    def __init__(self, connector):
        self.connector = connector

    def registrar_producto(self, nombre, descripcion, precio, stock):
        connection = self.connector.conectar()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (nombre, descripcion, precio, stock))
                connection.commit()
                print("Producto registrado con éxito.")
        except pymysql.MySQLError as e:
            print(f"Error al registrar el producto: {e}")
        finally:
            self.connector.cerrar_conexion(connection)

    def cargar_productos(self):
        connection = self.connector.conectar()
        productos = []
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id, nombre, descripcion, precio, stock FROM productos"
                cursor.execute(sql)
                resultados = cursor.fetchall()
                for producto in resultados:
                    productos.append({
                        'id': producto[0],
                        'nombre': producto[1],
                        'descripcion': producto[2],
                        'precio': producto[3],
                        'stock': producto[4],
                    })
        except pymysql.MySQLError as e:
            print(f"Error al cargar productos: {e}")
        finally:
            self.connector.cerrar_conexion(connection)

        return productos
