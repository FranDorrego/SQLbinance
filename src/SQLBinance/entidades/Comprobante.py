

class Comprobante:
    def __init__(self, id_comprobante=None, path=None, nombre_envia=None, CUIT_envia=None, nombre_recibe=None, CUIT_recibe=None, Cantidad=None, Banco_envia=None, Banco_recibe=None):
        self.id_comprobante = id_comprobante
        self.path = path
        self.nombre_envia = nombre_envia
        self.CUIT_envia = CUIT_envia
        self.nombre_recibe = nombre_recibe
        self.CUIT_recibe = CUIT_recibe
        self.Cantidad = Cantidad
        self.Banco_envia = Banco_envia
        self.Banco_recibe = Banco_recibe

    def __str__(self):
        return f"Comprobante: {self.path}, Envía: {self.nombre_envia} ({self.CUIT_envia}), Recibe: {self.nombre_recibe} ({self.CUIT_recibe}), Cantidad: {self.Cantidad}, Banco Envía: {self.Banco_envia}, Banco Recibe: {self.Banco_recibe}"

    @classmethod
    def dict_a_comprobante(cls, data):
        return cls(
            id=data.get("id"),
            path=data.get("path"),
            nombre_envia=data.get("nombre_envia"),
            CUIT_envia=data.get("CUIT_envia"),
            nombre_recibe=data.get("nombre_recibe"),
            CUIT_recibe=data.get("CUIT_recibe"),
            Cantidad=data.get("Cantidad"),
            Banco_envia=data.get("Banco_envia"),
            Banco_recibe=data.get("Banco_recibe")
        )
    
    @classmethod
    def list_a_comprobante(cls, data):
        return cls(
            id_comprobante=data[0],
            path=data[1],
            nombre_envia=data[2],
            CUIT_envia=data[3],
            nombre_recibe=data[4],
            CUIT_recibe=data[5],
            Cantidad=data[6],
            Banco_envia=data[7],
            Banco_recibe=data[8]
        )