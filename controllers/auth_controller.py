from views.connector import DBConnector

class AuthController:
    def __init__(self):
        self.db = DBConnector()

    def validar_credenciales(self, email, password):
        connection = self.db.conectar()
        if not connection:
            return None, "Error al conectar a la base de datos."

        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM usuarios WHERE correo = %s AND password = %s"
                cursor.execute(query, (email, password))
                usuario = cursor.fetchone()

                if usuario:
                    return usuario, None
                else:
                    return None, "Correo o contraseña incorrectos."
        except Exception as e:
            return None, f"Error durante la autenticación: {e}"
        finally:
            self.db.cerrar_conexion(connection)
