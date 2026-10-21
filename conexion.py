"""Conexion a MongoDB (capa de persistencia)."""

import os

from mongoengine import connect, disconnect
from pymongo.errors import ServerSelectionTimeoutError

# La URI se lee del entorno para no dejar credenciales en el codigo fuente.
# Si no esta definida, se usa la instancia local de desarrollo.
URI_POR_DEFECTO = "mongodb://localhost:27017/"
NOMBRE_BD = "odm_bda"


def conectar():
    """Abre la conexion con MongoDB y verifica que el servidor responda.

    MongoEngine no contacta al servidor al llamar a connect(): solo registra
    los datos. Por eso se envia un 'ping' explicito, que si viaja por la red y
    permite detectar aqui un servidor caido en lugar de fallar mas adelante.

    Returns:
        True si la conexion quedo establecida, False en caso contrario.
    """
    uri = os.getenv("MONGO_URI", URI_POR_DEFECTO)
    try:
        cliente = connect(db=NOMBRE_BD, host=uri, serverSelectionTimeoutMS=3000)
        cliente.admin.command("ping")
        print(f"Conexion exitosa a MongoDB (base: {NOMBRE_BD})")
        return True
    except ServerSelectionTimeoutError:
        print("ERROR: no se pudo conectar a MongoDB.")
        print("Verifica que el servicio este encendido y escuchando en el puerto 27017.")
        return False


def desconectar():
    """Cierra la conexion con MongoDB."""
    disconnect()
