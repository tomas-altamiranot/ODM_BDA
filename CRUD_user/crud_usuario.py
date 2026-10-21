"""Logica de negocio para la coleccion de usuarios.

Cada funcion valida sus datos antes de tocar la base y devuelve un resultado
que la capa de interfaz puede interpretar, en lugar de imprimir directamente.
"""

from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError

from modelos import User


def crear_usuario(email, nombre, apellido):
    """Registra un usuario nuevo.

    Args:
        email: correo del usuario, debe ser unico en la coleccion.
        nombre: nombre de pila.
        apellido: apellido.

    Returns:
        (True, usuario) si se creo; (False, mensaje de error) si no.
    """
    email = (email or "").strip().lower()
    nombre = (nombre or "").strip()
    apellido = (apellido or "").strip()

    if not email:
        return False, "El email no puede estar vacio."
    if not nombre:
        return False, "El nombre no puede estar vacio."

    try:
        usuario = User(email=email, nombre=nombre, apellido=apellido)
        usuario.save()
        return True, usuario
    except NotUniqueError:
        return False, f"Ya existe un usuario registrado con el email '{email}'."
    except ValidationError as e:
        return False, f"Datos invalidos: {e}"


def listar_usuarios():
    """Devuelve todos los usuarios ordenados por email."""
    return list(User.objects.order_by("email"))


def buscar_usuario(email):
    """Busca un usuario por su email.

    Returns:
        El documento User, o None si no existe.
    """
    email = (email or "").strip().lower()
    if not email:
        return None
    try:
        return User.objects.get(email=email)
    except DoesNotExist:
        return None


def existe_usuario(email):
    """Indica si hay un usuario con ese email.

    Lo usa el modulo de articulos para validar la integridad referencial
    antes de guardar una referencia.
    """
    return buscar_usuario(email) is not None


def actualizar_usuario(email, nuevo_nombre=None, nuevo_apellido=None):
    """Modifica nombre y/o apellido de un usuario existente.

    Los campos que lleguen vacios se dejan con su valor actual.

    Returns:
        (True, usuario) si se actualizo; (False, mensaje) si no.
    """
    usuario = buscar_usuario(email)
    if usuario is None:
        return False, f"No existe ningun usuario con el email '{email}'."

    nuevo_nombre = (nuevo_nombre or "").strip()
    nuevo_apellido = (nuevo_apellido or "").strip()

    if nuevo_nombre:
        usuario.nombre = nuevo_nombre
    if nuevo_apellido:
        usuario.apellido = nuevo_apellido

    try:
        usuario.save()
        return True, usuario
    except ValidationError as e:
        return False, f"Datos invalidos: {e}"


def eliminar_usuario(email):
    """Elimina un usuario.

    La regla reverse_delete_rule=DENY del modelo Articulo hace que MongoEngine
    rechace el borrado si el usuario todavia tiene articulos asociados, para
    no dejar referencias rotas.

    Returns:
        (True, mensaje) si se elimino; (False, mensaje) si no.
    """
    from mongoengine.errors import OperationError

    usuario = buscar_usuario(email)
    if usuario is None:
        return False, f"No existe ningun usuario con el email '{email}'."

    try:
        usuario.delete()
        return True, f"Usuario '{email}' eliminado correctamente."
    except OperationError:
        return (
            False,
            f"No se puede eliminar '{email}': tiene articulos asociados. "
            "Reasigna o elimina esos articulos primero.",
        )
