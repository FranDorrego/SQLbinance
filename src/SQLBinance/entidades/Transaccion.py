from .Comprobante import Comprobante


class Transaccion:

    def __init__(
        self,
        id = 0,
        orderNumber = 0,
        advNo = None,
        tradeType = None,
        asset = None,
        fiat = None,
        fiatSymbol = None,
        amount = None,
        totalPrice = None,
        unitPrice = None,
        orderStatus = None,
        createTime = None,
        commission = None,
        counterPartNickName = None,
        advertisementRole = None,
        id_informe = None,
    ):
        self.id = id
        self.orderNumber = orderNumber
        self.advNo = advNo
        self.tradeType = tradeType
        self.asset = asset
        self.fiat = fiat
        self.fiatSymbol = fiatSymbol
        self.amount = amount
        self.totalPrice = totalPrice
        self.unitPrice = unitPrice
        self.orderStatus = orderStatus
        self.createTime = createTime
        self.commission = commission
        self.counterPartNickName = counterPartNickName
        self.advertisementRole = advertisementRole
        self.comprobante = Comprobante()
        self.id_informe = id_informe


    def dict_a_transaccion(data: dict):
        return Transaccion(
            id=data.get("id"),
            orderNumber=data.get("orderNumber"),
            advNo=data.get("advNo"),
            tradeType=data.get("tradeType"),
            asset=data.get("asset"),
            fiat=data.get("fiat"),
            fiatSymbol=data.get("fiatSymbol"),
            amount=float(data.get("amount")),  # Convertir a float
            totalPrice=float(data.get("totalPrice")),  # Convertir a float
            unitPrice=float(data.get("unitPrice")),  # Convertir a float
            orderStatus=data.get("orderStatus"),
            createTime=int(data.get("createTime")),  # Convertir a entero
            commission=float(data.get("commission")),  # Convertir a float
            counterPartNickName=data.get("counterPartNickName"),
            advertisementRole=data.get("advertisementRole"),
            id_informe=data.get("id_informe")
        )

    def list_a_transaccion(data: list):
        id_informe = None

        if len(data) > 15:
            id_informe=data[15]

        
        return Transaccion(
            id = data[0],
            orderNumber=data[1],
            advNo=data[2],
            tradeType=data[3],
            asset=data[4],
            fiat=data[5],
            fiatSymbol=data[6],
            amount=data[7],
            totalPrice=data[8],
            unitPrice=data[9],
            orderStatus=data[10],
            createTime=data[11],
            commission=data[12],
            counterPartNickName=data[13],
            advertisementRole=data[14],
            id_informe = id_informe
        )
