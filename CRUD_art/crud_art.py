"""Logica de negocio para la coleccion de articulos.

Incluye la validacion de integridad referencial: MongoDB no tiene llaves
foraneas, asi que la existencia del usuario responsable se comprueba aqui,
en codigo, antes de guardar.
"""

from mongoengine.errors import DoesNotExist, ValidationError

from CRUD_user.crud_usuario import buscar_usuario
from modelos import Articulo


def _nombre_valido(nombre):
    """Un nombre es valido si tiene al menos un caracter que no sea espacio."""
    return bool((nombre or "").strip())


def crear_articulo(nombre, descripcion, marca, email_usuario):
    """Registra un articulo nuevo asociado a un usuario existente.

    Args:
        nombre: nombre del articulo, obligatorio y no vacio.
        descripcion: texto libre.
        marca: texto libre.
        email_usuario: email del usuario responsable. Debe existir.

    Returns:
        (True, articulo) si se creo; (False, mensaje de error) si no.
    """
    nombre = (nombre or "").strip()
    descripcion = (descripcion or "").strip()
    marca = (marca or "").strip()

    if not _nombre_valido(nombre):
        return False, "El nombre del articulo no puede estar vacio ni ser solo espacios."

    # Integridad referencial a mano: MongoDB aceptaria una referencia a un
    # usuario inexistente sin avisar, dejando un dato roto en la coleccion.
    usuario = buscar_usuario(email_usuario)
    if usuario is None:
        return False, (
            f"No existe ningun usuario con el email '{email_usuario}'. "
            "Registra primero al usuario responsable."
        )

    try:
        articulo = Articulo(
            nombre=nombre,
            descripcion=descripcion,
            marca=marca,
            usuario_modifico=usuario,
        )
        articulo.save()
        return True, articulo
    except ValidationError as e:
        return False, f"Datos invalidos: {e}"


def listar_articulos():
    """Devuelve todos los articulos ordenados por nombre."""
    return list(Articulo.objects.order_by("nombre"))


def buscar_articulo_por_id(id_articulo):
    """Busca un articulo por su _id de MongoDB.

    Returns:
        El documento Articulo, o None si no existe o el id es invalido.
    """
    id_articulo = (id_articulo or "").strip()
    if not id_articulo:
        return None
    try:
        return Articulo.objects.get(id=id_articulo)
    except (DoesNotExist, ValidationError):
        # ValidationError cubre el caso de un id con formato incorrecto.
        return None


def buscar_articulos_por_usuario(email_usuario):
    """Devuelve los articulos modificados por un usuario.

    Returns:
        (True, lista) si el usuario existe; (False, mensaje) si no.
    """
    usuario = buscar_usuario(email_usuario)
    if usuario is None:
        return False, f"No existe ningun usuario con el email '{email_usuario}'."
    return True, list(Articulo.objects(usuario_modifico=usuario).order_by("nombre"))


def actualizar_articulo(id_articulo, nombre=None, descripcion=None,
                        marca=None, email_usuario=None):
    """Modifica un articulo existente.

    Los campos que lleguen vacios conservan su valor actual. Si se indica un
    email, se valida que el usuario exista antes de reasignar la referencia.

    Returns:
        (True, articulo) si se actualizo; (False, mensaje) si no.
    """
    articulo = buscar_articulo_por_id(id_articulo)
    if articulo is None:
        return False, f"No existe ningun articulo con el id '{id_articulo}'."

    nombre = (nombre or "").strip()
    descripcion = (descripcion or "").strip()
    marca = (marca or "").strip()
    email_usuario = (email_usuario or "").strip()

    # Solo se valida el nombre si el usuario escribio algo: dejarlo en blanco
    # significa "no lo cambies", no "ponlo vacio".
    if nombre:
        articulo.nombre = nombre
    if descripcion:
        articulo.descripcion = descripcion
    if marca:
        articulo.marca = marca

    if email_usuario:
        usuario = buscar_usuario(email_usuario)
        if usuario is None:
            return False, (
                f"No existe ningun usuario con el email '{email_usuario}'. "
                "No se aplico ningun cambio."
            )
        articulo.usuario_modifico = usuario

    if not _nombre_valido(articulo.nombre):
        return False, "El nombre del articulo no puede quedar vacio."

    try:
        articulo.save()
        return True, articulo
    except ValidationError as e:
        return False, f"Datos invalidos: {e}"


def eliminar_articulo(id_articulo):
    """Elimina un articulo por su id.

    Returns:
        (True, mensaje) si se elimino; (False, mensaje) si no.
    """
    articulo = buscar_articulo_por_id(id_articulo)
    if articulo is None:
        return False, f"No existe ningun articulo con el id '{id_articulo}'."

    nombre = articulo.nombre
    articulo.delete()
    return True, f"Articulo '{nombre}' eliminado correctamente."
