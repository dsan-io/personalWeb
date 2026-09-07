"""
Agente mínimo de code review con tool calling real usando Ollama.

Objetivo pedagógico: mostrar el ciclo completo sin ninguna capa oculta
(sin Cline, sin frameworks de agentes) para entender exactamente qué
pasa "por debajo" cuando una herramienta como Cline dice que el modelo
"lee tus archivos".

Requisitos:
    pip install requests
    Ollama corriendo localmente (ollama serve) con el modelo descargado:
    ollama pull qwen3-coder:30b

Uso:
    python agente_code_review.py
"""

import json
import os
from typing import Optional

import requests

OLLAMA_URL = "http://192.168.1.207:11434/api/chat"
MODEL = "qwen3-coder:30b"

# -----------------------------------------------------------------
# Raíz de seguridad: el agente NUNCA puede leer ni listar nada
# fuera de esta carpeta, sin importar qué le pida el modelo.
# Por defecto es la carpeta donde vive este script; cámbiala si
# quieres apuntar a un proyecto en otra ubicación.
# -----------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def _resolver_ruta_segura(path_relativo: str) -> Optional[str]:
    """
    Convierte un path relativo pedido por el modelo en un path absoluto,
    y verifica que siga estando DENTRO de PROJECT_ROOT.

    Esto bloquea trucos como '../../etc/passwd' o rutas absolutas que
    intenten escapar de la carpeta del proyecto. Si el path es inválido
    o intenta escapar, devuelve None.
    """
    ruta_absoluta = os.path.abspath(os.path.join(PROJECT_ROOT, path_relativo))

    # os.path.commonpath detecta si ruta_absoluta realmente vive
    # dentro de PROJECT_ROOT, incluso después de resolver '..' etc.
    try:
        raiz_comun = os.path.commonpath([PROJECT_ROOT, ruta_absoluta])
    except ValueError:
        # Pasa en Windows si están en unidades de disco distintas, por ejemplo.
        return None

    if raiz_comun != PROJECT_ROOT:
        return None

    return ruta_absoluta


# -----------------------------------------------------------------
# 1) La herramienta real. Esto es Python normal y corriente.
#    El modelo JAMÁS ejecuta esto directamente — solo puede "pedir"
#    que se ejecute, y es nuestro código el que decide obedecer o no.
# -----------------------------------------------------------------
def read_file(path: str) -> str:
    """Lee un archivo del disco y devuelve su contenido como texto."""
    ruta_segura = _resolver_ruta_segura(path)
    if ruta_segura is None:
        return (
            f"ERROR: acceso denegado. '{path}' está fuera de la carpeta "
            f"permitida del proyecto ({PROJECT_ROOT})."
        )
    if not os.path.isfile(ruta_segura):
        return f"ERROR: el archivo '{path}' no existe."
    with open(ruta_segura, "r", encoding="utf-8") as f:
        return f.read()


def list_files(directory: str = ".") -> str:
    """
    Lista archivos y subcarpetas dentro de un directorio dado.
    Devuelve rutas relativas para que el modelo las pueda usar
    directamente como argumento de read_file.
    """
    ruta_segura = _resolver_ruta_segura(directory)
    if ruta_segura is None:
        return (
            f"ERROR: acceso denegado. '{directory}' está fuera de la carpeta "
            f"permitida del proyecto ({PROJECT_ROOT})."
        )
    if not os.path.isdir(ruta_segura):
        return f"ERROR: el directorio '{directory}' no existe."

    entradas = []
    for nombre in sorted(os.listdir(ruta_segura)):
        ruta_completa = os.path.join(ruta_segura, nombre)
        # Mostramos la ruta RELATIVA a PROJECT_ROOT, no la absoluta,
        # para que el modelo siga pidiendo rutas relativas y no se
        # confunda con paths del sistema de archivos real.
        ruta_relativa = os.path.relpath(ruta_completa, PROJECT_ROOT)
        tipo = "carpeta" if os.path.isdir(ruta_completa) else "archivo"
        entradas.append(f"{tipo}: {ruta_relativa}")

    if not entradas:
        return f"El directorio '{directory}' está vacío."

    return "\n".join(entradas)


# -----------------------------------------------------------------
# 2) Descripción de la herramienta que le mandamos al modelo.
#    Esto es SOLO metadata — el modelo no recibe el código de
#    read_file, solo sabe que existe una función con este nombre,
#    esta descripción y estos parámetros.
# -----------------------------------------------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Lee el contenido completo de un archivo del proyecto dado su path relativo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta relativa del archivo a leer, ej. 'index.html' o 'style/styles.css'",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": (
                "Lista los archivos y subcarpetas dentro de un directorio del "
                "proyecto. Úsala primero para descubrir qué archivos existen "
                "antes de pedir leerlos con read_file, en vez de asumir nombres "
                "o rutas."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Ruta relativa del directorio a listar, ej. '.' o 'style'",
                    }
                },
                "required": ["directory"],
            },
        },
    },
]

# Mapeo nombre -> función real de Python, para poder ejecutar
# lo que el modelo pida sin usar eval() ni nada peligroso.
AVAILABLE_FUNCTIONS = {
    "read_file": read_file,
    "list_files": list_files,
}


def run_agent(prompt_inicial: str, max_pasos: int = 15):
    """
    Ciclo principal del agente:
    1. Mandamos el prompt + la lista de herramientas disponibles.
    2. Si el modelo pide ejecutar una herramienta, la ejecutamos
       nosotros y le devolvemos el resultado.
    3. Repetimos hasta que el modelo dé una respuesta final (sin
       más tool calls) o se acabe max_pasos como límite de seguridad.
    """
    messages = [{"role": "user", "content": prompt_inicial}]

    for paso in range(max_pasos):
        print(f"\n--- Paso {paso + 1}: mandando mensaje al modelo ---")

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "tools": TOOLS,
                "stream": False,
                # Ollama por defecto suele usar una ventana de contexto muy
                # chica (2048-4096 tokens). Con varios archivos + resultados
                # de herramientas acumulados, eso se llena rápido y el modelo
                # empieza a "olvidar" mensajes anteriores, incluyendo tus
                # instrucciones originales. La forzamos explícitamente más
                # grande. Si tu máquina tiene poca RAM/VRAM, bájala si ves
                # errores de memoria.
                "options": {
                    "num_ctx": 8192,
                },
            },
        )
        response.raise_for_status()
        data = response.json()
        mensaje_modelo = data["message"]

        # --- DEBUG: quita esto una vez resuelto el diagnóstico ---
        print("--- Respuesta cruda del modelo en este paso ---")
        print(json.dumps(mensaje_modelo, indent=2, ensure_ascii=False))
        print("------------------------------------------------")

        tool_calls = mensaje_modelo.get("tool_calls")

        if not tool_calls:
            # El modelo ya no pidió más herramientas: esta es su respuesta final.
            print("\n=== RESPUESTA FINAL DEL MODELO ===\n")
            print(mensaje_modelo["content"])
            return mensaje_modelo["content"]

        # El modelo pidió usar una o más herramientas.
        messages.append(mensaje_modelo)

        for call in tool_calls:
            nombre_funcion = call["function"]["name"]
            argumentos = call["function"]["arguments"]

            print(f"El modelo pidió ejecutar: {nombre_funcion}({argumentos})")

            funcion = AVAILABLE_FUNCTIONS.get(nombre_funcion)
            if funcion is None:
                resultado = f"ERROR: herramienta '{nombre_funcion}' no existe."
            else:
                resultado = funcion(**argumentos)

            # Le devolvemos el resultado real al modelo como mensaje de tipo "tool".
            messages.append(
                {
                    "role": "tool",
                    "content": resultado,
                }
            )

        # --- Blindaje contra "deriva de instrucciones" ---
        # Si en esta ronda el modelo ya leyó archivos con read_file (no solo
        # exploró con list_files), es probable que ya tenga todo lo que
        # necesita. Le recordamos el formato exacto ANTES de su próxima
        # respuesta, para no depender de que lo recuerde solo desde el
        # primer mensaje, varios turnos atrás.
        llamo_read_file = any(
            call["function"]["name"] == "read_file" for call in tool_calls
        )
        if llamo_read_file:
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "Ya tienes el contenido de los archivos necesarios. "
                        "Si ya leíste TODOS los archivos HTML y CSS relevantes, "
                        "responde ahora siguiendo EXACTAMENTE este formato, "
                        "sin omitir ninguna sección: "
                        "1) Bugs reales (cita el archivo y la línea/fragmento), "
                        "2) Malas prácticas con ejemplo de cómo corregirlas, "
                        "3) Accesibilidad y contraste de colores si aplica, "
                        "4) Qué está bien hecho, "
                        "5) 1-2 preguntas para que el desarrollador piense la "
                        "solución. Si todavía falta leer algún archivo relevante, "
                        "pide leerlo primero antes de responder."
                    ),
                }
            )

    print("\nSe alcanzó el límite de pasos sin respuesta final.")
    return None


if __name__ == "__main__":
    # Cambia esta ruta/prompt según tu proyecto real.
    # Ya no hace falta describir la estructura de carpetas a mano:
    # el modelo tiene list_files para descubrirla por su cuenta.
    prompt = (
        "Actúa como un Senior Developer haciendo code review real. "
        "Primero explora la estructura del proyecto con list_files "
        "(empieza por el directorio '.', y si encuentras subcarpetas "
        "relevantes, list_files sobre ellas también). Después lee con "
        "read_file todos los archivos HTML y CSS que encuentres — "
        "usando la ruta exacta tal como aparece en list_files, incluyendo "
        "la subcarpeta si la tiene. Ten en cuenta que normalize.css, si "
        "existe, es una hoja de reset/normalización estándar de terceros: "
        "no la critiques como si fuera código propio, solo úsala como "
        "contexto para entender qué estilos base ya están definidos antes "
        "de evaluar el resto del CSS. Luego evalúa: 1) bugs reales, "
        "2) malas prácticas, 3) accesibilidad y contraste de colores si "
        "aplica, 4) qué está bien hecho, 5) termina con 1-2 preguntas para "
        "que el desarrollador piense la solución en vez de dársela directa."
    )
    run_agent(prompt)
