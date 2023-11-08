from entidades.Transaccion import Transaccion

class Informe:

    def __init__(
        self,
        id,
        fecha,
        punto_equilibrio,
        total_compra_fiat,
        total_venta_fiat,
        tipo_fiat,
        total_compra_cripto,
        total_venta_cripto,
        tipo_cripto
    ):
        self.id = id
        self.fecha = fecha
        self.punto_equilibrio = punto_equilibrio
        self.total_compra_fiat = total_compra_fiat
        self.total_venta_fiat = total_venta_fiat
        self.tipo_fiat = tipo_fiat
        self.total_compra_cripto = total_compra_cripto
        self.total_venta_cripto = total_venta_cripto
        self.tipo_cripto = tipo_cripto
        self.transacciones = list()

    def __str__(self):
        return f"Informe ID: {self.id}, Fecha: {self.fecha}, Punto Equilibrio: {self.punto_equilibrio}, Total Compra Fiat: {self.total_compra_fiat}, Total Venta Fiat: {self.total_venta_fiat}, Tipo Fiat: {self.tipo_fiat}, Total Compra Cripto: {self.total_compra_cripto}, Total Venta Cripto: {self.total_venta_cripto}, Tipo Cripto: {self.tipo_cripto}"

    def agrega_transaccion(self, transaccion : Transaccion):
        """ Agrega un objeto transaccion a la lista """
        self.transacciones.append(transaccion)
        
    @classmethod
    def list_a_informe(cls, data : list):
        return cls(
            id=data[0],
            fecha=data[1],
            punto_equilibrio=data[2],
            total_compra_fiat=data[3],
            total_venta_fiat=data[4],
            tipo_fiat=data[5],
            total_compra_cripto=data[6],
            total_venta_cripto=data[7],
            tipo_cripto=data[8]
        )


    @classmethod
    def dict_a_informe(cls, data : dict):
        return cls(
            id=data.get("id"),
            fecha=data.get("fecha"),
            punto_equilibrio=data.get("punto_equilibrio"),
            total_compra_fiat=data.get("total_compra_fiat"),
            total_venta_fiat=data.get("total_venta_fiat"),
            tipo_fiat=data.get("tipo_fiat"),
            total_compra_cripto=data.get("total_compra_cripto"),
            total_venta_cripto=data.get("total_venta_cripto"),
            tipo_cripto=data.get("tipo_cripto")
        )