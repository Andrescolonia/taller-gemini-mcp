import re
from contextlib import contextmanager

from mcp.server.fastmcp import FastMCP as MCPServer
from openpyxl import Workbook, load_workbook
from openpyxl.utils.cell import coordinate_to_tuple

from espacio import archivo

mcp = MCPServer("ExcelServer")


@contextmanager
def abrir_libro(ruta: str):
    destino = archivo(ruta, ".xlsx")
    if not destino.is_file():
        raise ValueError(f"No existe el libro de Excel: {ruta}")
    libro = load_workbook(destino)
    try:
        yield libro, destino
    finally:
        libro.close()


def obtener_hoja(libro, hoja: str):
    if hoja not in libro.sheetnames:
        raise ValueError(f"No existe la hoja: {hoja}. Hojas disponibles: {libro.sheetnames}")
    return libro[hoja]


@mcp.tool()
def crear_excel(nombre: str, hoja: str = "Datos") -> str:
    """Crea un libro Excel con una hoja inicial y devuelve su ruta."""
    destino = archivo(nombre, ".xlsx")
    if not hoja.strip() or len(hoja) > 31 or re.search(r"[\\/*?:\[\]]", hoja):
        raise ValueError("El nombre de la hoja debe tener 1 a 31 caracteres válidos.")
    libro = Workbook()
    try:
        libro.active.title = hoja
        with destino.open("xb") as salida:
            libro.save(salida)
    except FileExistsError as error:
        raise ValueError(f"Ya existe el libro de Excel: {nombre}") from error
    finally:
        libro.close()
    return str(destino)


@mcp.tool()
def listar_hojas(ruta: str) -> list[str]:
    """Lista los nombres de las hojas de un libro Excel."""
    with abrir_libro(ruta) as (libro, _):
        return libro.sheetnames


@mcp.tool()
def leer_excel(ruta: str, hoja: str = "Datos") -> list[list[str]]:
    """Lee las filas de una hoja y devuelve los valores como texto."""
    with abrir_libro(ruta) as (libro, _):
        return [
            ["" if valor is None else str(valor) for valor in fila]
            for fila in obtener_hoja(libro, hoja).values
        ]


@mcp.tool()
def escribir_celda(ruta: str, hoja: str, celda: str, valor: str) -> str:
    """Escribe texto en una celda individual, como B2, y guarda el libro."""
    celda = celda.strip().upper()
    if not re.fullmatch(r"[A-Z]{1,3}[1-9][0-9]{0,6}", celda):
        raise ValueError(f"Celda inválida: {celda}. Usa una referencia como B2.")
    fila, columna = coordinate_to_tuple(celda)
    if fila > 1048576 or columna > 16384:
        raise ValueError(f"Celda fuera del rango de Excel: {celda}.")
    with abrir_libro(ruta) as (libro, destino):
        entrada = obtener_hoja(libro, hoja)[celda]
        entrada.value = valor
        entrada.data_type = "s"
        libro.save(destino)
    return f"Celda {celda} guardada en la hoja {hoja}."


@mcp.tool()
def agregar_filas(ruta: str, hoja: str, filas: list[list[str]]) -> str:
    """Agrega filas de texto al final de una hoja. Incluye encabezados al crear una tabla."""
    with abrir_libro(ruta) as (libro, destino):
        pagina = obtener_hoja(libro, hoja)
        for fila in filas:
            pagina.append(fila)
            for celda in pagina[pagina.max_row][:len(fila)]:
                celda.data_type = "s"
        libro.save(destino)
    return f"Filas agregadas en {hoja}: {len(filas)}."


if __name__ == "__main__":
    mcp.run(transport="stdio")
