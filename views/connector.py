import pymysql
from pymysql.cursors import DictCursor

class DBConnector:
    def __init__(self):
        # Parámetros de conexión
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'zzzz'
        self.database = 'sistema_ventas'

    def conectar(self):
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=DictCursor  # Establece DictCursor aquí
            )
            return connection
        except pymysql.MySQLError as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def cerrar_conexion(self, connection):
        if connection:
            connection.close()

    def ejecutar_query(self, query, params=None):
        """
        Ejecuta una consulta SQL que no modifica la base de datos (como SELECT).
        """
        connection = self.conectar()
        if connection:
            try:
                with connection.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    return cursor.fetchall()  # Retorna los resultados como lista de diccionarios
            except pymysql.MySQLError as e:
                print(f"Error al ejecutar la consulta: {e}")
                print(f"Consulta: {query}, Parámetros: {params}")  # Agrega esta línea
                return []
            finally:
                self.cerrar_conexion(connection)
        return []

    def ejecutar_modificacion(self, query, params=None):
        """
        Ejecuta una consulta SQL que modifica la base de datos (como INSERT, UPDATE, DELETE).
        """
        connection = self.conectar()
        if connection:
            try:
                with connection.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                connection.commit()  # Confirma los cambios
                return True
            except pymysql.MySQLError as e:
                print(f"Error al modificar la base de datos: {e}")
                connection.rollback()  # Revertir cambios en caso de error
                return False
            finally:
                self.cerrar_conexion(connection)
        return False

    def get_config_data(self):
        """
        Método para obtener datos de configuración (nombre de la empresa y logo).
        """
        connection = self.conectar()
        if connection:
            try:
                with connection.cursor() as cursor:
                    query = "SELECT nombre_empresa, logo FROM configuracion LIMIT 1"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    if result:
                        return {"nombre_empresa": result["nombre_empresa"], "logo": result["logo"]}
                    else:
                        return {"nombre_empresa": "Nombre de la Empresa", "logo": None}
            finally:
                self.cerrar_conexion(connection)
        return {"nombre_empresa": "Nombre de la Empresa", "logo": None}