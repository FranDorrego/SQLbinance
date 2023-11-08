import threading
import binance
import binance.exceptions
from .transaccion_data import Transaccion_data
from ..entidades.Transaccion import Transaccion

class _SQLBinance():

    instancia = None
    bucle_operaciones = None

    def __new__(cls, APIkey: str | None = None, APIsecret: str | None = None, activate_bucle=True, *args):
        if _SQLBinance.instancia is None:
            _SQLBinance.instancia = super(_SQLBinance, cls).__new__(cls)
            _SQLBinance.instancia.__init__(APIkey, APIsecret, activate_bucle)
        return _SQLBinance.instancia

    def __init__(self, APIkey: str | None = None, APIsecret: str | None = None, activate_bucle=False):

        if APIkey is None or APIsecret is None:
            raise ValueError("Las claves API no están en el formato correcto. Verifica el constructor de _SQLBinance y sus claves.")

        self.APIkey = APIkey
        self.APIsecret = APIsecret
        self.client = binance.Client(APIkey, APIsecret)
        self.check_permisos()
        self.control_bucle = True

        if activate_bucle:
            if _SQLBinance.bucle_operaciones is None:
                _SQLBinance.bucle_operaciones = [threading.Thread(target=self.c2c_bucle, name="API Binance")]
                _SQLBinance.bucle_operaciones[0].start()

    def terminar_hilos(self):
        for hilo in _SQLBinance.bucle_operaciones:
            self.control_bucle = False
            hilo.join()

    def check_permisos(self):
        """ Chequea que tenga perimisos de lectura """
        try:
            self.client.get_account()
        except binance.exceptions.BinanceAPIException as e:
            if "Read-only API Key" in str(e):
                raise PermissionError("Las claves de API no tienen permisos de lectura.")
            else:
                raise e 

    def c2c_bucle(self):
        """ Es el que pide la informacion a binance """
        # Creo una nueva conexion
        conexion = Transaccion_data()

        while self.control_bucle:

            historial = self.client.get_c2c_trade_history()
            historial = historial.get("data")
            historial.append({
                "orderNumber": "20219644646554779678948",
                "advNo": "11218246497340924563904",
                "tradeType": "BULL",
                "asset": "BUSD",
                "fiat": "CNY",
                "fiatSymbol": "￥",
                "amount": "5000.00000000",
                "totalPrice": "33400.00000000",
                "unitPrice": "6.68",
                "orderStatus": "COMPLETED",
                "createTime": 1619361369000,
                "commission": "0",
                "counterPartNickName": "ab***",
                "advertisementRole": "TAKER"
            })

            for operacion in historial:
                transaccion = Transaccion.dict_a_transaccion(operacion)
                if transaccion.orderStatus == 'COMPLETED':
                    conexion.agrega_c2c(transaccion)

        # Limpio la conexion
        conexion.__del__()


