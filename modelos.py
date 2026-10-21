"""Modelos de datos (capa de persistencia).

Define las dos entidades del sistema como documentos de MongoDB usando
MongoEngine. Los nombres de los campos siguen la especificacion de la
actividad.
"""

import datetime

import mongoengine as me


def _ahora_utc():
    """Devuelve la fecha y hora actual en UTC.

    Se pasa como callable a DateTimeField (no como valor ya calculado) para
    que MongoEngine la evalue en el momento de crear cada documento. Si se
    pasara el resultado de la llamada, todos los documentos compartirian la
    misma marca de tiempo: la del arranque del programa.
    """
    return datetime.datetime.now(datetime.timezone.utc)


class User(me.Document):
    """Usuario del sistema. El email es su identificador de negocio."""

    meta = {"collection": "usuarios"}

    email = me.EmailField(required=True, unique=True)
    nombre = me.StringField(max_length=50)
    apellido = me.StringField(max_length=50)
    fecha_creado = me.DateTimeField(default=_ahora_utc)

    def __str__(self):
        return f"[{self.email}] {self.nombre} {self.apellido}"


class Articulo(me.Document):
    """Articulo del inventario.

    usuario_modifico guarda una referencia (el _id) al User responsable de la
    ultima modificacion. La regla DENY impide borrar un usuario mientras tenga
    articulos asociados: el historial de auditoria se preserva.
    """

    meta = {"collection": "articulos"}

    nombre = me.StringField(required=True, max_length=100)
    descripcion = me.StringField(max_length=300)
    marca = me.StringField(max_length=50)
    usuario_modifico = me.ReferenceField(User, reverse_delete_rule=me.DENY)

    def __str__(self):
        responsable = self.usuario_modifico.email if self.usuario_modifico else "sin asignar"
        return (
            f"[{self.id}] {self.nombre} | marca: {self.marca or '-'} "
            f"| modifico: {responsable}"
        )

    def detalle(self):
        """Version extendida para la opcion de consulta individual."""
        responsable = self.usuario_modifico.email if self.usuario_modifico else "sin asignar"
        return (
            f"ID          : {self.id}\n"
            f"Nombre      : {self.nombre}\n"
            f"Descripcion : {self.descripcion or '-'}\n"
            f"Marca       : {self.marca or '-'}\n"
            f"Modifico    : {responsable}"
        )
