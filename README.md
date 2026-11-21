# Taller de agentes con Gemini y MCP

Práctica en Python para conectar Gemini, mediante una clave de Google AI Studio, con herramientas locales que se comunican por Model Context Protocol (MCP). El chat conserva el historial durante la sesión para interpretar referencias como «ese archivo».

El primer servidor trabaja con archivos de texto. El reto agrega un segundo servidor para crear y editar libros de Excel y combina ambos en el mismo chat. La prueba final crea tres archivos de texto con datos distintos y convierte su contenido en una tabla de Excel.

## Instalación

Desde la carpeta del proyecto, con Python 3.11 o superior:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

En PowerShell, usa `.venv\Scripts\Activate.ps1` para activar el entorno y `Copy-Item .env.example .env` para copiar la configuración.

Obtén una clave en [Google AI Studio](https://aistudio.google.com/apikey) y guárdala como `GEMINI_API_KEY` en `.env`. Puedes ajustar `GEMINI_MODEL` si tu cuenta usa otro modelo compatible con llamadas a herramientas.

## Chat con archivos de texto

```bash
python chat_ia.py
```

`mi_servidor_mcp.py` puede listar carpetas, navegar por ellas, resolver rutas y crear, leer o ampliar archivos `.txt`. Prueba estos mensajes en la misma sesión:

1. Crea un archivo y escribe algo en él.
2. Agrégale otra línea a ese archivo.
3. Muéstrame qué archivos hay en la carpeta y lee el que acabamos de crear.
4. ¿En qué carpeta estás y cuál es la ruta de ese archivo?

## Reto con dos servidores

```bash
python chat_dos_servidores.py
```

El chat abre una conexión MCP por servidor mediante entrada y salida estándar y registra las dos sesiones en Gemini. `servidor_excel_mcp.py` usa openpyxl para crear libros `.xlsx`, listar hojas, leer filas, escribir celdas y agregar filas.

1. Crea tres archivos de texto. En cada uno pon el nombre, la edad y la ciudad de una persona ficticia distinta.
2. Lee los tres archivos que acabas de crear. Organiza sus datos en un libro nuevo de Excel con los encabezados Nombre, Edad y Ciudad.
3. Abre el libro y verifica que tenga los encabezados y una fila por persona.

Los servidores trabajan dentro de `archivos_prueba/`. Los libros y archivos generados quedan en esa carpeta y Git los ignora, igual que `.env`. Usa datos ficticios en el taller porque Gemini recibe los resultados de las herramientas como parte de la conversación. El historial dura hasta cerrar el chat. Escribe `salir` para terminar.
