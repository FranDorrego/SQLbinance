import subprocess

def instalar_libreria():
    try:
        import binance
    except ImportError:
        subprocess.call(["pip", "install", "python-binance"])
        
instalar_libreria()


from .classData.comprobante_data import Comprobante_data
from .classData.transaccion_data import Transaccion_data
from .classData._SQLBinance import _SQLBinance
from .classData.informe_data import Informe_data
from .classData.conexion import Conexion
import time

class SQLBinance(_SQLBinance,Informe_data,Transaccion_data,Comprobante_data,Conexion):

    def __init__(self, APIkey: str | None = None, APIsecret: str | None = None, activate_bucle=True, path_db = "./base.db", test = False):
        super().__init__(APIkey, APIsecret, activate_bucle, test)
        Informe_data.__init__(self)
        Transaccion_data.__init__(self)
        Comprobante_data.__init__(self)
        Conexion.__init__(self,path_db)

    def __del__(self):
        super().terminar_hilos()
        Conexion.cerrar_conexion()
        Transaccion_data.__del__()
        super().__del__()
        return 