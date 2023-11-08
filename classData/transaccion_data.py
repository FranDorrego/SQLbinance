import sqlite3
from entidades.Transaccion import Transaccion
from entidades.Comprobante import Comprobante
from classData.conexion import Conexion
from classData.comprobante_data import Comprobante_data
from classData.informe_data import Informe_data

class Transaccion_data():

    def __init__(self, *args) -> None:
        self.conexion = Conexion()
        self.comprobante_data = Comprobante_data()
        self._informe_data = Informe_data()

    def __del__(self):
        # Cierra la conexion abierta aquí.
        self.conexion.__del__()

    def all_transacciones(self) -> [Transaccion]:
        """
        Imprime todas las filas de una tabla en la base de datos.

        Args:
            table_name (str): El nombre de la tabla que se desea consultar.

        Returns:
            Lista de Transacciones [Transacciones,]
        """
        try:
            conn, cursor = self.conexion.get_conexion()
            # Ejecutar una consulta SQL para seleccionar todas las filas de la tabla
            cursor.execute(f"SELECT * FROM Transacciones")
            
            # Obtener todas las filas y mostrarlas
            rows = cursor.fetchall()
            lista_transacciones = list()

            for row in rows:
                print(row)
                lista_transacciones.append(Transaccion.list_a_transaccion(row))

            return lista_transacciones
        
        except sqlite3.Error as e:
            print(f"Error al realizar la consulta: {str(e)}")

    def all_transacciones_idInforme(self,id_informe : int) -> [Transaccion]:
        """
        Devuelve un infomre completo segun el ID que le pases

        Args:
            id_informe = int que es el id en la base de datos.

        Returns:
            Lista de Transacciones [Transacciones,]
        """
        try:
            conn, cursor = self.conexion.get_conexion()
            # Ejecutar una consulta SQL para seleccionar todas las filas de la tabla
            cursor.execute(f"SELECT * FROM Transacciones JOIN comprobante ON Transacciones.id_comprobante = comprobante.id WHERE Transacciones.id_informe = {id_informe}")
            
            # Obtener todas las filas y mostrarlas
            rows = cursor.fetchall()
            lista_transacciones = list()

            for row in rows:
                print(row)
                obj_transaccion = Transaccion.list_a_transaccion(row[:16])
                obj_comprobante = Comprobante.list_a_comprobante(row[17:])
                obj_transaccion.comprobante = obj_comprobante

                lista_transacciones.append(obj_transaccion)

            return lista_transacciones
        
        except sqlite3.Error as e:
            print(f"Error al realizar la consulta: {str(e)}")

    def last_transaccion(self) -> Transaccion:
        """
        Busca la ultima operacion registrada en la Base de datos

        Args:
            None

        Returns:
            Un objeto Transaccion
        """

        try:
            conn, cursor = self.conexion.get_conexion()
            # Ejecutar una consulta SQL para seleccionar todas las filas de la tabla
            cursor.execute(f"SELECT * FROM Transacciones JOIN comprobante ON Transacciones.id_comprobante = comprobante.id WHERE Transacciones.id = (SELECT MAX(id) FROM Transacciones)")
            
            # Obtener todas las filas y mostrarlas
            rows = cursor.fetchall()

            for row in rows:
                obj_transaccion = Transaccion.list_a_transaccion(row[:15])
                obj_comprobante = Comprobante.list_a_comprobante(row[16:])
                obj_transaccion.comprobante = obj_comprobante

            return obj_transaccion
        
        except sqlite3.Error as e:
            print(f"Error al realizar la consulta: {str(e)}")

    def __if_exist(self, id, tabla, columna) -> bool:
        """
        Verifica si un registro con el ID especificado existe en la tabla de la base de datos.

        Args:
            id: El ID del registro que se busca en la base de datos.
            tabla: El nombre de la tabla en la que se realizará la búsqueda.
            columna: El nombre de la columna en la que se buscará el ID.

        Returns:
            bool: True si el registro existe, False si no existe.
        """
        conn, cursor = self.conexion.get_conexion()
        consulta = f"SELECT * FROM {tabla} WHERE {columna} = ?"
        cursor.execute(consulta, (id,))
        resultado = cursor.fetchall()
        return len(resultado) > 0
    
    def agrega_c2c(self, transaccion : Transaccion):
        """
        Agrega una nueva transacción a la base de datos.

        Args:
            transaccion: Instancia de la clase Transaccion con los datos de la transacción a agregar.

        Returns:
            None
        """
        if self.__if_exist(transaccion.orderNumber, "Transacciones", "orderNumber"):
            return self.trae_datos_base(transaccion)

        conn, cursor = self.conexion.get_conexion()
        id_informe = self._informe_data.informe_vijente(transaccion.fiat, transaccion.asset)

        consulta = "INSERT INTO Transacciones ( \
            orderNumber, advNo, tradeType, asset, fiat, fiatSymbol, \
            amount, totalPrice, unitPrice, orderStatus, createTime, commission, \
            counterPartNickName, advertisementRole, id_informe) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        
        try:
            cursor.execute(consulta, (
                transaccion.orderNumber,
                transaccion.advNo,
                transaccion.tradeType,
                transaccion.asset,
                transaccion.fiat,
                transaccion.fiatSymbol,
                transaccion.amount,
                transaccion.totalPrice,
                transaccion.unitPrice,
                transaccion.orderStatus,
                transaccion.createTime,
                transaccion.commission,
                transaccion.counterPartNickName,
                transaccion.advertisementRole,
                id_informe                
            ))
            
            conn.commit()

            # Imprime los datos recién insertados
            cursor.execute("SELECT * FROM Transacciones WHERE orderNumber=?", (transaccion.orderNumber,))
            row = cursor.fetchone()
            if row:
                transaccion.comprobante.id_comprobante = row[15]
                transaccion.id_informe = row[16]
            
            # Actualizo el informe con los datos
            self._informe_data.actualiza_informe(id_informe)

        except sqlite3.Error as e:
            print(f"Error al insertar datos en la base de datos: {str(e)}")

    def trae_datos_base(self, transaccion : Transaccion) -> Transaccion:
            
        try:
            conn, cursor = self.conexion.get_conexion()
            cursor.execute("SELECT * FROM Transacciones WHERE orderNumber=?", (transaccion.orderNumber,))
            row = cursor.fetchone()

            if row:
                transaccion = Transaccion.list_a_transaccion(row)

        except sqlite3.Error as e:
            print(f"Error al insertar datos en la base de datos: {str(e)}")
            
    def actualiza_c2c(self, transaccion: Transaccion):
        """
        Actualiza una transacción existente en la base de datos.

        Args:
            transaccion (Transaccion): Instancia de la clase Transaccion con los datos de la transacción actualizada.

        Returns:
            None
        """
         
        if not self.__if_exist(transaccion.orderNumber, "Transacciones", "orderNumber"):
            return

        conn, cursor = self.conexion.get_conexion()
        consulta = "UPDATE Transacciones SET \
            advNo=?, tradeType=?, asset=?, fiat=?, fiatSymbol=?, \
            amount=?, totalPrice=?, unitPrice=?, orderStatus=?, createTime=?, commission=?, \
            counterPartNickName=?, advertisementRole=? WHERE orderNumber=?"

        try:
            cursor.execute(consulta, (
                transaccion.advNo,
                transaccion.tradeType,
                transaccion.asset,
                transaccion.fiat,
                transaccion.fiatSymbol,
                transaccion.amount,
                transaccion.totalPrice,
                transaccion.unitPrice,
                transaccion.orderStatus,
                transaccion.createTime,
                transaccion.commission,
                transaccion.counterPartNickName,
                transaccion.advertisementRole,
                transaccion.orderNumber
            ))
            conn.commit()

            # Actualizo el comprobante
            self.comprobante_data.actualiza_comprobante(transaccion)
            
            # Actualizo el informe con los datos
            self._informe_data.actualiza_informe(transaccion.id_informe)

        except sqlite3.Error as e:
            print(f"Error al actualizar datos en la base de datos: {str(e)}")

    
    
