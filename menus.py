"""Capa de interfaz: menus de consola y lectura de datos del usuario.

Este modulo no sabe nada de MongoDB. Solo pregunta, muestra y delega en los
modulos de logica de negocio.
"""

from CRUD_art import crud_art
from CRUD_user import crud_usuario

SEPARADOR = "=" * 55


def _leer_texto(mensaje):
    """Lee una linea de texto. Devuelve cadena vacia si se corta la entrada."""
    try:
        return input(mensaje).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return ""


def _leer_opcion(mensaje, validas):
    """Pide una opcion hasta que sea una de las validas.

    Args:
        mensaje: texto del prompt.
        validas: coleccion de cadenas aceptadas, por ejemplo {"1", "2", "0"}.

    Returns:
        La opcion elegida. Devuelve "0" si la entrada se agota, para que el
        menu cierre ordenadamente en lugar de entrar en un bucle infinito.
    """
    while True:
        try:
            opcion = input(mensaje).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return "0"
        if opcion in validas:
            return opcion
        print(f">> Opcion no valida. Elige una de: {', '.join(sorted(validas))}")


def _mostrar(titulo, lineas):
    """Imprime un bloque con titulo y una lista de lineas."""
    print(f"\n--- {titulo} ---")
    if not lineas:
        print("(no hay registros)")
        return
    for linea in lineas:
        print(f"  {linea}")


# =====================================================================
# MODULO DE USUARIOS
# =====================================================================
def _alta_usuario():
    print("\n= Registrar usuario =")
    email = _leer_texto("Email          : ")
    nombre = _leer_texto("Nombre         : ")
    apellido = _leer_texto("Apellido       : ")

    ok, resultado = crud_usuario.crear_usuario(email, nombre, apellido)
    if ok:
        print(f">> Usuario registrado: {resultado}")
    else:
        print(f">> No se pudo registrar. {resultado}")


def _consultar_usuarios():
    print("\n= Consultar usuarios =")
    print("  1. Listar todos")
    print("  2. Buscar por email")
    opcion = _leer_opcion("Opcion: ", {"1", "2"})

    if opcion == "1":
        usuarios = crud_usuario.listar_usuarios()
        _mostrar(f"Usuarios registrados: {len(usuarios)}", [str(u) for u in usuarios])
    else:
        email = _leer_texto("Email a buscar : ")
        usuario = crud_usuario.buscar_usuario(email)
        if usuario is None:
            print(f">> No existe ningun usuario con el email '{email}'.")
        else:
            print(f">> Encontrado: {usuario}")
            print(f"   Registrado el: {usuario.fecha_creado}")


def _modificar_usuario():
    print("\n= Modificar usuario =")
    email = _leer_texto("Email del usuario : ")
    usuario = crud_usuario.buscar_usuario(email)
    if usuario is None:
        print(f">> No existe ningun usuario con el email '{email}'.")
        return

    print(f"Actual: {usuario}")
    print("(deja en blanco lo que no quieras cambiar)")
    nombre = _leer_texto("Nuevo nombre      : ")
    apellido = _leer_texto("Nuevo apellido    : ")

    ok, resultado = crud_usuario.actualizar_usuario(email, nombre, apellido)
    print(f">> Actualizado: {resultado}" if ok else f">> No se pudo actualizar. {resultado}")


def _baja_usuario():
    print("\n= Eliminar usuario =")
    email = _leer_texto("Email del usuario : ")
    ok, mensaje = crud_usuario.eliminar_usuario(email)
    print(f">> {mensaje}")


def menu_usuarios():
    """Submenu con las cuatro operaciones CRUD sobre usuarios."""
    while True:
        print("\n--- USUARIOS ---")
        print("  1. Registrar   2. Consultar   3. Modificar   4. Eliminar   0. Volver")
        opcion = _leer_opcion("Opcion: ", {"1", "2", "3", "4", "0"})

        if opcion == "1":
            _alta_usuario()
        elif opcion == "2":
            _consultar_usuarios()
        elif opcion == "3":
            _modificar_usuario()
        elif opcion == "4":
            _baja_usuario()
        else:
            return


# =====================================================================
# MODULO DE ARTICULOS
# =====================================================================
def _alta_articulo():
    print("\n= Registrar articulo =")
    nombre = _leer_texto("Nombre            : ")
    descripcion = _leer_texto("Descripcion       : ")
    marca = _leer_texto("Marca             : ")
    email = _leer_texto("Email responsable : ")

    ok, resultado = crud_art.crear_articulo(nombre, descripcion, marca, email)
    if ok:
        print(f">> Articulo registrado: {resultado}")
    else:
        print(f">> No se pudo registrar. {resultado}")


def _consultar_articulos():
    print("\n= Consultar articulos =")
    print("  1. Listar todos")
    print("  2. Buscar por ID")
    print("  3. Listar por usuario que modifico")
    opcion = _leer_opcion("Opcion: ", {"1", "2", "3"})

    if opcion == "1":
        articulos = crud_art.listar_articulos()
        _mostrar(f"Articulos registrados: {len(articulos)}", [str(a) for a in articulos])

    elif opcion == "2":
        id_articulo = _leer_texto("ID del articulo : ")
        articulo = crud_art.buscar_articulo_por_id(id_articulo)
        if articulo is None:
            print(f">> No existe ningun articulo con el id '{id_articulo}'.")
        else:
            print()
            print(articulo.detalle())

    else:
        email = _leer_texto("Email del usuario : ")
        ok, resultado = crud_art.buscar_articulos_por_usuario(email)
        if not ok:
            print(f">> {resultado}")
        else:
            _mostrar(
                f"Articulos modificados por {email}: {len(resultado)}",
                [str(a) for a in resultado],
            )


def _modificar_articulo():
    print("\n= Modificar articulo =")
    id_articulo = _leer_texto("ID del articulo : ")
    articulo = crud_art.buscar_articulo_por_id(id_articulo)
    if articulo is None:
        print(f">> No existe ningun articulo con el id '{id_articulo}'.")
        return

    print()
    print(articulo.detalle())
    print("\n(deja en blanco lo que no quieras cambiar)")
    nombre = _leer_texto("Nuevo nombre      : ")
    descripcion = _leer_texto("Nueva descripcion : ")
    marca = _leer_texto("Nueva marca       : ")
    email = _leer_texto("Nuevo responsable : ")

    ok, resultado = crud_art.actualizar_articulo(
        id_articulo, nombre, descripcion, marca, email
    )
    print(f">> Actualizado: {resultado}" if ok else f">> No se pudo actualizar. {resultado}")


def _baja_articulo():
    print("\n= Eliminar articulo =")
    id_articulo = _leer_texto("ID del articulo : ")
    ok, mensaje = crud_art.eliminar_articulo(id_articulo)
    print(f">> {mensaje}")


def menu_articulos():
    """Submenu con las cuatro operaciones CRUD sobre articulos."""
    while True:
        print("\n--- ARTICULOS ---")
        print("  1. Registrar   2. Consultar   3. Modificar   4. Eliminar   0. Volver")
        opcion = _leer_opcion("Opcion: ", {"1", "2", "3", "4", "0"})

        if opcion == "1":
            _alta_articulo()
        elif opcion == "2":
            _consultar_articulos()
        elif opcion == "3":
            _modificar_articulo()
        elif opcion == "4":
            _baja_articulo()
        else:
            return


# =====================================================================
# MENU PRINCIPAL
# =====================================================================
def menu_principal():
    """Bucle principal de la aplicacion."""
    while True:
        print(f"\n{SEPARADOR}")
        print("   SISTEMA DE INVENTARIO Y AUDITORIA DE ARTICULOS")
        print(SEPARADOR)
        print("  1. Usuarios")
        print("  2. Articulos")
        print("  0. Salir")
        print("-" * 55)

        opcion = _leer_opcion("Opcion: ", {"1", "2", "0"})

        if opcion == "1":
            menu_usuarios()
        elif opcion == "2":
            menu_articulos()
        else:
            print("\nHasta luego.")
            return
