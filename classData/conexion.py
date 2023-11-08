import sqlite3
import threading


class Conexion():

    hilos = {}

    def __init__(self, path: str | None = "./base.db", *agrs) -> None:
        self.path = path

    def __del__(self):
        try:
            # Cierra la conexion abierta aquí.
            conn, cursor = self.get_conexion()
            conn.close()
        except:
            pass

    def get_conexion(self) -> [sqlite3.Connection, sqlite3.Cursor]:
        """
        Devuelve una conexión a la base de datos con la que se creó la instancia.

        Este método se utiliza para administrar múltiples conexiones con diferentes hilos y garantizar la consistencia de la base de datos.

        Returns:
            (sqlite3.Connection, sqlite3.Cursor): Una tupla que contiene una conexión a la base de datos y un cursor para consultas.
        """
        if Conexion.hilos.get(threading.get_ident(), False):
            conn, cursor = Conexion.hilos.get(threading.get_ident())

            try:
                conn.execute("SELECT * FROM sqlite_sequence")
            except sqlite3.ProgrammingError:
                conn = sqlite3.connect(self.path)
                Conexion.hilos[threading.get_ident()] = [conn, conn.cursor()]

            return Conexion.hilos[threading.get_ident()]

        # Si no existe una conexión previa, crea una nueva y la almacena para su reutilización
        conn = sqlite3.connect(self.path)
        Conexion.hilos[threading.get_ident()] = [conn, conn.cursor()]
        return Conexion.hilos[threading.get_ident()]