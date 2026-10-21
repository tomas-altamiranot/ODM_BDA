"""Punto de entrada de la aplicacion.

Conecta con MongoDB, lanza el menu principal y cierra la conexion al salir,
pase lo que pase.
"""

from conexion import conectar, desconectar
from menus import menu_principal


def main():
    if not conectar():
        print("La aplicacion no puede continuar sin conexion a la base de datos.")
        return

    try:
        menu_principal()
    finally:
        desconectar()
        print("Conexion cerrada.")


if __name__ == "__main__":
    main()
