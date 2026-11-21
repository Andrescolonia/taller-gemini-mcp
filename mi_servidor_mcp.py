from mcp.server.fastmcp import FastMCP as MCPServer

from espacio import RAIZ, archivo, resolver

mcp = MCPServer("FileServer")
directorio = RAIZ


@mcp.tool()
def listar_archivos(ruta: str = ".") -> list[str]:
    """Lista archivos y carpetas visibles en la ruta indicada."""
    carpeta = resolver(ruta, directorio)
    if not carpeta.is_dir():
        raise ValueError(f"No existe la carpeta: {ruta}")
    return sorted(entrada.name for entrada in carpeta.iterdir()
                  if not entrada.name.startswith("."))


@mcp.tool()
def leer_archivo(ruta: str) -> str:
    """Lee el contenido UTF-8 de un archivo de texto."""
    destino = archivo(ruta, ".txt", directorio)
    if not destino.is_file():
        raise ValueError(f"No existe el archivo de texto: {ruta}")
    return destino.read_text(encoding="utf-8")


@mcp.tool()
def crear_archivo_txt(nombre: str, contenido: str = "") -> str:
    """Crea un archivo de texto, con contenido inicial opcional."""
    destino = archivo(nombre, ".txt", directorio)
    try:
        with destino.open("x", encoding="utf-8") as salida:
            salida.write(contenido)
    except FileExistsError as error:
        raise ValueError(f"Ya existe el archivo de texto: {nombre}") from error
    return str(destino)


@mcp.tool()
def agregar_contenido(ruta: str, contenido: str) -> str:
    """Agrega contenido a un archivo de texto existente, en una línea nueva."""
    destino = archivo(ruta, ".txt", directorio)
    if not destino.is_file():
        raise ValueError(f"No existe el archivo de texto: {ruta}")
    with destino.open("r+", encoding="utf-8") as salida:
        previo = salida.read()
        if previo and not previo.endswith("\n"):
            salida.write("\n")
        salida.write(contenido)
    return f"Contenido agregado en {destino}"


@mcp.tool()
def directorio_actual() -> str:
    """Devuelve la ruta absoluta de la carpeta actual del servidor de texto."""
    return str(directorio)


@mcp.tool()
def obtener_ruta(ruta: str) -> str:
    """Devuelve la ruta absoluta de un archivo o carpeta de la práctica."""
    return str(resolver(ruta, directorio))


@mcp.tool()
def cambiar_directorio(ruta: str) -> str:
    """Cambia a una subcarpeta existente de la práctica."""
    global directorio
    destino = resolver(ruta, directorio)
    if not destino.is_dir():
        raise ValueError(f"No existe la carpeta: {ruta}")
    directorio = destino
    return str(directorio)


if __name__ == "__main__":
    mcp.run(transport="stdio")
