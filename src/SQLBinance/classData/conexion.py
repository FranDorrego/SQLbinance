import sqlite3
import threading

import os

class Conexion():

    hilos = {}

    def __init__(self, path: str | None = "./base.db", *agrs) -> None:

        self.path = path

        if not os.path.exists(path):
            self.crea_base()

    def __del__(self):
        try:
            # Cierra la conexion abierta aquí.
            conn, cursor = self.get_conexion()
            conn.close()
        except:
            pass

    def crea_base(self):
        try:
            conn = sqlite3.connect(self.path)

            with conn:
                # Ejecuta las consultas SQL
                conn.execute('''Drop table IF EXISTS comprobante;''')
                conn.execute('''CREATE TABLE comprobante ( id INTEGER PRIMARY KEY, path TEXT, nombre_envia TEXT, CUIT_envia TEXT, nombre_recibe TEXT, CUIT_recibe TEXT, Cantidad REAL, Banco_envia TEXT, Banco_recibe TEXT );''')

                conn.execute('''DROP TABLE IF EXISTS Informe;''')
                conn.execute('''CREATE TABLE Informe ( id INTEGER PRIMARY KEY, fecha DATE DEFAULT CURRENT_DATE, punto_equilibrio REAL DEFAULT 0, total_compra_fiat REAL DEFAULT 0, total_venta_fiat REAL DEFAULT 0, tipo_fiat TEXT DEFAULT '', total_compra_cripto REAL DEFAULT 0, total_venta_cripto REAL DEFAULT 0, tipo_cripto TEXT DEFAULT '' );''')

                conn.execute('''Drop table IF EXISTS transacciones;''')
                conn.execute('''CREATE TABLE Transacciones ( id INTEGER PRIMARY KEY AUTOINCREMENT, orderNumber TEXT, advNo TEXT, tradeType TEXT, asset TEXT, fiat TEXT, fiatSymbol TEXT, amount REAL, totalPrice REAL, unitPrice REAL, orderStatus TEXT, createTime INTEGER, commission REAL, counterPartNickName TEXT, advertisementRole TEXT, id_comprobante INTEGER DEFAULT(NULL), id_informe INTEGER DEFAULT(NULL), FOREIGN KEY (id_comprobante) REFERENCES Comprobante(id), FOREIGN KEY (id_informe) REFERENCES Informe(id) );''')

                conn.execute('''Drop TRIGGER IF EXISTS crea_comprobante;''')
                conn.execute('''CREATE TRIGGER crea_comprobante AFTER INSERT ON Transacciones BEGIN -- Inserta un registro en la tabla Comprobante INSERT INTO Comprobante (path) VALUES (''); -- Actualiza la columna id_comprobante en la tabla Transacciones UPDATE Transacciones SET id_comprobante = (SELECT last_insert_rowid() FROM Comprobante) WHERE id = new.id; END;''')

        except Exception as e:
            print(f"Ocurrio un error al crear la Base de datos: {e}")


    def get_conexion(self) -> [sqlite3.Connection, sqlite3.Cursor]:
        """
        Devuelve una conexión a la base de datos con la que se creó la instancia.

        Este método se utiliza para administrar múltiples conexiones con diferentes hilos y garantizar la consistencia de la base de datos.

        Returns:
            (sqlite3.Connection, sqlite3.Cursor): Una tupla que contiene una conexión a la base de datos y un cursor para consultas.
        """

        if Conexion.hilos.get(threading.get_ident(), False):
            conn, cursor = Conexion.hilos.get(threading.get_ident())

            try: conn.execute("SELECT * FROM sqlite_sequence")
            except sqlite3.ProgrammingError:
                conn = sqlite3.connect(self.path)
                Conexion.hilos[threading.get_ident()] = [conn, conn.cursor()]

            return Conexion.hilos[threading.get_ident()]

        # Si no existe una conexión previa, crea una nueva y la almacena para su reutilización
        conn = sqlite3.connect(self.path)
        Conexion.hilos[threading.get_ident()] = [conn, conn.cursor()]
        return Conexion.hilos[threading.get_ident()]