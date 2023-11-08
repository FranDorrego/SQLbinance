from .Comprobante import Comprobante


class Transaccion:

    def __init__(
        self,
        orderNumber,
        advNo,
        tradeType,
        asset,
        fiat,
        fiatSymbol,
        amount,
        totalPrice,
        unitPrice,
        orderStatus,
        createTime,
        commission,
        counterPartNickName,
        advertisementRole,
        id_informe
    ):
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
        try: id_informe=data[15]
        except: pass
        
        return Transaccion(
            orderNumber=data[0],
            advNo=data[1],
            tradeType=data[2],
            asset=data[3],
            fiat=data[4],
            fiatSymbol=data[5],
            amount=data[6],
            totalPrice=data[7],
            unitPrice=data[8],
            orderStatus=data[9],
            createTime=data[10],
            commission=data[11],
            counterPartNickName=data[12],
            advertisementRole=data[13],
            id_informe = id_informe
        )
