
from ..entidades.Informe import Informe
from ..entidades.Transaccion import Transaccion
from .conexion import Conexion
import sqlite3


class Informe_data():
    
    def __init__(self, *agrs) -> None: 
        self.conexion = Conexion()
        self.transaccion_data = None
    
    def crea_informe(self, tipo_fiat = "", tipo_cripto = "") -> int:
        """ Inserta un informe nuevo """
        try:
            conn, cursor = self.conexion.get_conexion()

            consulta = "INSERT INTO Informe(fecha, tipo_fiat, tipo_cripto) VALUES (CURRENT_DATE, ?, ?)"
            cursor.execute(consulta, (tipo_fiat, tipo_cripto))
            conn.commit()
            cursor.execute(f"SELECT MAX(id) FROM Informe")
            resultado = cursor.fetchall()
            if resultado:
                return resultado[0][0]
            else:
                raise sqlite3.Error("Ocurrio un error al insertar el informe")
                
        except sqlite3.Error as e:
            print(f"Error al insertar el informe en la base de datos: {str(e)}")

    def all_informe(self) -> [Informe]:
        """ Trae todos los informes, sin relleno de datos hijas """
        try:
            conn, cursor = self.conexion.get_conexion()

            consulta = "SELECT * FROM Informe"
            cursor.execute(consulta)
            resultado = cursor.fetchall()

            list_informe = []
            for result in resultado:
                obj_infomre = Informe.list_a_informe(result)
                list_informe.append(obj_infomre)
            
            return list_informe
                
        except sqlite3.Error as e:
            print(f"Error al tomar todos los informes en la base de datos: {str(e)}")

    def all_informe_id(self, id) -> Informe:
        """ Trae completo un informe con todos los datos y clases rellenas """

        if self.transaccion_data is None:
            from .transaccion_data import Transaccion_data
            self.transaccion_data = Transaccion_data()

        if id is None:
            return None

        try:
            conn, cursor = self.conexion.get_conexion()

            # Creo el infomorme
            consulta = f"SELECT * FROM Informe WHERE id = {id}"
            cursor.execute(consulta)
            resultado = cursor.fetchall()

            if not resultado:
                return Informe()
            
            obj_infomre = Informe.list_a_informe(resultado[0])

            # Trigo todos las transaciones del infomre
            list_transacciones = self.transaccion_data.all_transacciones_idInforme(obj_infomre.id)

            # agrego todas las transacciones a ese informe 
            for list_tran in list_transacciones:
                obj_infomre.agrega_transaccion(list_tran)
            
            return obj_infomre
                
        except sqlite3.Error as e:
            print(f"Error al tomar el informe en la base de datos: {str(e)}")

    def informe_actual_completo(self) -> Informe:
        """ Devuelve el informe actual que se esta utilizando para todas las operaciones """
        return self.all_informe_id(self.id_informe_vijente())

    def informe_last_completo(self) -> Informe:
        """ Devuelve el informe anterior al acutal que ya esta finalizado """
        id_anterior = self.id_informe_vijente()

        if id_anterior is None:
            id_anterior = 0
        else:
            id_anterior-= 1
            
        return self.all_informe_id(id_anterior)
    
    def id_informe_vijente(self) -> int:
        """ Devuelve el ID con el informe aun vigente  """

        try:
            conn, cursor = self.conexion.get_conexion()

            # Consulto por el ultimo informe
            consulta = f"SELECT MAX(id) FROM Informe WHERE open = 1"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            
            if not resultado:
                return None
            
            return resultado[0][0]
        
        except sqlite3.Error as e:
            print(f"Error al tomar el informe en la base de datos: {str(e)}")

    def actualiza_informe(self, id):
        """ Se pasa el ID y se actualizan todos los datos internos """

        try:
            conn, cursor = self.conexion.get_conexion()

            # tomo la lista con los id marcados, venta
            consulta = f"SELECT tradeType, SUM(totalPrice) AS total_fiat, SUM(amount) AS total_cripto FROM Transacciones WHERE id_informe = {id} GROUP BY tradeType; "
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            resultado = self.tuplas_a_dict(resultado)

            open = True
            if resultado.get("BUY").get("cant_cripto") - resultado.get("SELL").get("cant_cripto") == 0:
                open = False

            consulta = """UPDATE Informe 
                    SET 
                        punto_equilibrio = ?,
                        total_compra_fiat = ?,
                        total_venta_fiat = ?,
                        total_compra_cripto = ?,
                        total_venta_cripto = ?,
                        open = ?
                    WHERE id = ?"""

            valores = (resultado.get("BUY").get("cant_cripto") - resultado.get("SELL").get("cant_cripto"),
                    resultado.get("BUY").get("cant_fiat"),
                    resultado.get("SELL").get("cant_fiat"),
                    resultado.get("BUY").get("cant_cripto"),
                    resultado.get("SELL").get("cant_cripto"),
                    open,
                    id)

            cursor.execute(consulta, valores)

            conn.commit()

        except sqlite3.Error as e:
            print(f"Error al tomar el informe en la base de datos: {str(e)}")
    
    def tuplas_a_dict(self, tuplas) -> {dict}:
        mi_dict = {'SELL': {'cant_fiat': 0.0, 'cant_cripto': 0.0},
                'BUY': {'cant_fiat': 0.0, 'cant_cripto': 0.0}}

        for tupla in tuplas:
            if len(tupla) >= 3:
                clave = tupla[0]
                valores = {'cant_fiat': tupla[1], 'cant_cripto': tupla[2]}
                mi_dict[clave] = valores

        return mi_dict