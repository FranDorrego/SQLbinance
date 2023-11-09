import threading
import binance
import binance.exceptions
from .transaccion_data import Transaccion_data
from ..entidades.Transaccion import Transaccion
import random


class _SQLBinance():

    instancia = None
    bucle_operaciones = None

    def __new__(cls, APIkey: str | None = None, APIsecret: str | None = None, activate_bucle=True, test = False, *args):
        if _SQLBinance.instancia is None:
            _SQLBinance.instancia = super(_SQLBinance, cls).__new__(cls)
            _SQLBinance.instancia.__init__(APIkey, APIsecret, activate_bucle, test)
        return _SQLBinance.instancia

    def __init__(self, APIkey: str | None = None, APIsecret: str | None = None, activate_bucle=False, test = False, *args):

        if APIkey is None or APIsecret is None:
            raise ValueError("Las claves API no están en el formato correcto. Verifica el constructor de _SQLBinance y sus claves.")

        self.APIkey = APIkey
        self.APIsecret = APIsecret
        self.client = binance.Client(APIkey, APIsecret)
        self.control_bucle = True
        self.test = test
        self.check_permisos()

        if activate_bucle:
            if _SQLBinance.bucle_operaciones is None:
                _SQLBinance.bucle_operaciones = [threading.Thread(target=self.c2c_bucle, name="API Binance")]
                _SQLBinance.bucle_operaciones[0].daemon = True
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

            # Si data esta vacio y estamos en modo test, esto se autorellena
            if self.test:
                historial.append(self.dict_test(conexion))

            for operacion in historial:
                transaccion = Transaccion.dict_a_transaccion(operacion)
                if transaccion.orderStatus == 'COMPLETED':
                    conexion.agrega_c2c(transaccion)

        # Limpio la conexion
        conexion.__del__()

    def dict_test(self, conexion : Transaccion_data) -> dict:
        """ Devuelve un diccionario de demostracion, hace cordinar los numeros para frenar """

        ultima_transaccion = conexion.last_transaccion()
        ultima_transaccion.id += 1 

        self.lado = random.choice(["BUY", "SELL"])
        cantidad = 5000

        return {
                "orderNumber": ultima_transaccion.id ,
                "advNo": "11218246497340924563904",
                "tradeType": self.lado,
                "asset": "BUSD",
                "fiat": "CNY",
                "fiatSymbol": "￥",
                "amount": str(cantidad),
                "totalPrice": "33400.00000000",
                "unitPrice": "6.68",
                "orderStatus": "COMPLETED",
                "createTime": 1619361369000,
                "commission": "0",
                "counterPartNickName": "ab***",
                "advertisementRole": "TAKER"
            }
        


        

