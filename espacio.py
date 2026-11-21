import os
from pathlib import Path

RAIZ = Path(os.environ.get(
    "MCP_ARCHIVOS_DIR", Path(__file__).resolve().parent / "archivos_prueba"
)).resolve()
RAIZ.mkdir(parents=True, exist_ok=True)


def resolver(ruta: str, base: Path = RAIZ) -> Path:
    destino = (base / ruta).resolve()
    if not destino.is_relative_to(RAIZ):
        raise ValueError("La ruta debe estar dentro de la carpeta de práctica.")
    return destino


def archivo(ruta: str, extension: str, base: Path = RAIZ) -> Path:
    if not ruta.strip() or not Path(ruta).name:
        raise ValueError("Indica un nombre de archivo.")
    if not Path(ruta).suffix:
        ruta += extension
    if Path(ruta).suffix.lower() != extension:
        raise ValueError(f"Se requiere un archivo {extension}.")
    destino = resolver(ruta, base)
    if destino.suffix.lower() != extension:
        raise ValueError(f"El destino debe ser un archivo {extension}.")
    return destino
