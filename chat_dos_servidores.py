import asyncio

from chat_ia import INSTRUCCIONES, conversar

INSTRUCCIONES_EXCEL = (
    INSTRUCCIONES
    + " Dispones de herramientas para archivos de texto y libros de Excel. "
    "Cuando te pidan trasladar información, lee los archivos de texto con sus herramientas "
    "y usa las de Excel para organizar los datos en filas con encabezados."
)


if __name__ == "__main__":
    asyncio.run(conversar(
        ("mi_servidor_mcp.py", "servidor_excel_mcp.py"), INSTRUCCIONES_EXCEL
    ))
