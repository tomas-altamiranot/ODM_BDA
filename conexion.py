from mongoengine import connect
from pymongo.errors import ServerSelectionTimeoutError


try:
    cliente = connect (
        'mi_blog_db', 
        host = 'localhost', 
        port = 27017,
        serverSelectionTimeoutMS = 3000
    )
    cliente.admin.command("ping")
    print("Conexión exitosa a MongoDB")

except ServerSelectionTimeoutError as e:
    print(f"Error al conectar a MongoDB, error: {e}")
