from mongoengine import NotUniqueError
from ..modelos import User

#Función para crear un nuevo usuario en la base de datos
def create_user(email, first_name, last_name,created_at): #Usa los parámetros definidos en el modelo User
        new_user= User(
            email=User.email,
            first_name=User.first_name,
            last_name=User.last_name,
            created_at =User.timestamp
        )
        try:
            #Intenta guardar el nuevo usuario en la base de datos
            saved_user=new_user.save()
            return saved_user
        except NotUniqueError:
            print("Ya existe un usuario con este correo electrónico.")
            return None
        except Exception as e:
            print (f"Error al crear el usuario: {e}")
            return None
#Función para leer todos los usuarios de la base de datos
def leer_usuarios():
    try:
        usuarios = User.objects()
        if not usuarios:
            print("No hay usuarios registrados.")
            return
        print("\n--- Lista de Usuarios ---")
        for u in usuarios:
            print(f"Email: {u.email} | Nombre: {u.first_name} {u.last_name}")
    except Exception as e:
        print(f"Error al leer usuarios: {e}")
#Función para actualizar un usuario existente en la base de datos
def actualizar_usuario(email_actual, nuevo_first_name, nuevo_last_name):
    try:
        usuario = User.objects.get(email=email_actual)
        usuario.first_name = nuevo_first_name.strip() if nuevo_first_name.strip() else usuario.first_name
        usuario.last_name = nuevo_last_name.strip() if nuevo_last_name.strip() else usuario.last_name
        return usuario.save()
    except DoesNotExist:
        print("Error: No se encontró ningún usuario con ese email.")
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
    return None
#Función para eliminar un usuario de la base de datos
def eliminar_usuario(email):
    try:
        usuario = User.objects.get(email=email)
        usuario.delete()
        print("Usuario eliminado con éxito.")
    except DoesNotExist:
        print("Error: El usuario no existe.")
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")