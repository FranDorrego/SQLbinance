import sqlite3
from ..entidades.Comprobante import Comprobante
from ..entidades.Transaccion import Transaccion
from .conexion import Conexion

class Comprobante_data():

    def __init__(self,*agrs) -> None:
        self.conexion = Conexion()
        pass

    def __del__(self):
        # Cierra la conexion abierta aquí.
        self.conexion.__del__()
        
    def actualiza_comprobante(self, transaccion : Comprobante | Transaccion):
        """
        Actualiza los datos del comprobante en la tabla "comprobante" con base en el ID proporcionado.
        """
        # Saco el comprobante de la transaccion
        if isinstance(transaccion, Transaccion):
            transaccion = transaccion.comprobante

        try:
            conn, cursor = self.conexion.verifica_conn()

            # Actualiza los datos del comprobante en la tabla "comprobante"
            consulta = """
            UPDATE comprobante
            SET path = ?,
                nombre_envia = ?,
                CUIT_envia = ?,
                nombre_recibe = ?,
                CUIT_recibe = ?,
                Cantidad = ?,
                Banco_envia = ?,
                Banco_recibe = ?
            WHERE id = ?
            """
            cursor.execute(consulta, (
                transaccion.comprobante.path,
                transaccion.comprobante.nombre_envia,
                transaccion.comprobante.CUIT_envia,
                transaccion.comprobante.nombre_recibe,
                transaccion.comprobante.CUIT_recibe,
                transaccion.comprobante.Cantidad,
                transaccion.comprobante.Banco_envia,
                transaccion.comprobante.Banco_recibe,
                transaccion.id_comprobante
            ))
            conn.commit()

        except sqlite3.Error as e:
            print(f"Error al actualizar el comprobante en la base de datos: {str(e)}")