# Taller de agentes con Gemini y MCP

Práctica en Python para conectar Gemini, mediante una clave de Google AI Studio, con herramientas locales que se comunican por Model Context Protocol (MCP). El chat conserva el historial durante la sesión para interpretar referencias como «ese archivo».

El primer servidor trabaja con archivos de texto. El reto agrega un segundo servidor para crear y editar libros de Excel y combina ambos en el mismo chat. La prueba final crea tres archivos de texto con datos distintos y convierte su contenido en una tabla de Excel.

## Instalación

Necesitas Python 3.11 o superior. Abre una terminal en la carpeta `taller-gemini-mcp`, donde está `requirements.txt`.

### macOS

```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
if [ ! -f .env ]; then cp .env.example .env; fi
```

### Windows (PowerShell)

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Si el comando `py` no está disponible, usa `python` para comprobar la versión y crear el entorno virtual.

### Configurar la clave de Gemini

Obtén una clave en Google AI Studio, abre el archivo `.env` con tu editor y pega la clave después de `GEMINI_API_KEY=`. Puedes ajustar `GEMINI_MODEL` si tu cuenta usa otro modelo compatible con llamadas a herramientas. [Obtener una clave en Google AI Studio](https://aistudio.google.com/apikey)

## Iniciar el chat

Ejecuta los comandos de tu sistema desde la carpeta del proyecto. Cada comando abre un chat. Escribe `salir` para cerrarlo antes de iniciar el otro.

**macOS**

```bash
# Chat con archivos de texto
.venv/bin/python chat_ia.py

# Chat con archivos de texto y Excel
.venv/bin/python chat_dos_servidores.py
```

**Windows (PowerShell)**

```powershell
# Chat con archivos de texto
.\.venv\Scripts\python.exe chat_ia.py

# Chat con archivos de texto y Excel
.\.venv\Scripts\python.exe chat_dos_servidores.py
```

## Chat con archivos de texto

`mi_servidor_mcp.py` puede listar carpetas, navegar por ellas, resolver rutas y crear, leer o ampliar archivos `.txt`. Prueba estos mensajes en la misma sesión:

1. Crea un archivo y escribe algo en él.
2. Agrégale otra línea a ese archivo.
3. Muéstrame qué archivos hay en la carpeta y lee el que acabamos de crear.
4. ¿En qué carpeta estás y cuál es la ruta de ese archivo?

## Reto con dos servidores

El chat abre una conexión MCP por servidor mediante entrada y salida estándar y registra las dos sesiones en Gemini. `servidor_excel_mcp.py` usa openpyxl para crear libros `.xlsx`, listar hojas, leer filas, escribir celdas y agregar filas.

1. Crea tres archivos de texto. En cada uno pon el nombre, la edad y la ciudad de una persona ficticia distinta.
2. Lee los tres archivos que acabas de crear. Organiza sus datos en un libro nuevo de Excel con los encabezados Nombre, Edad y Ciudad.
3. Abre el libro y verifica que tenga los encabezados y una fila por persona.

Los servidores trabajan dentro de `archivos_prueba/`. Los libros y archivos generados quedan en esa carpeta y Git los ignora, igual que `.env`. Usa datos ficticios en el taller porque Gemini recibe los resultados de las herramientas como parte de la conversación. El historial dura hasta cerrar el chat. Escribe `salir` para terminar.
