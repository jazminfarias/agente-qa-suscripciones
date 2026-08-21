"""Configuracion central del agente de QA."""

import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_DOCS = RAIZ / "docs"
DIR_SALIDAS = RAIZ / "salidas"

MODELO = "claude-opus-5"

# Presupuesto de salida por vuelta. Tiene que cubrir el razonamiento interno del
# modelo mas el JSON completo con todos los casos. Con 16000 la respuesta se
# cortaba a mitad de camino. Para presupuestos de este tamano hay que usar
# streaming (ver agente.py), si no la peticion corre riesgo de timeout HTTP.
MAX_TOKENS = 64000

# Tope de vueltas del loop de herramientas. Evita que el agente quede dando
# vueltas leyendo documentos para siempre.
MAX_ITERACIONES = 12

# Extensiones que el agente considera documentacion funcional.
EXTENSIONES = {".md", ".txt"}

# Archivos dentro de docs/ que NO son documentacion del circuito.
# Tambien se ignora cualquier archivo que empiece con "_".
IGNORADOS = {"README.md"}

# Cuantas coincidencias devuelve como maximo buscar_en_documentos.
MAX_COINCIDENCIAS = 40


def cargar_env() -> None:
    """Carga pares CLAVE=valor desde un archivo .env en la raiz del proyecto.

    Implementado a mano para no depender de python-dotenv. Las variables que ya
    existen en el entorno tienen prioridad y no se sobreescriben.
    """
    archivo = RAIZ / ".env"
    if not archivo.is_file():
        return
    # utf-8-sig descarta el BOM que agregan Notepad y Out-File en Windows. Sin
    # esto, la primera clave del archivo llega como "﻿ANTHROPIC_API_KEY" y
    # no coincide con nada.
    for linea in archivo.read_text(encoding="utf-8-sig").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        clave = clave.strip()
        valor = valor.strip().strip('"').strip("'")
        if clave and clave not in os.environ:
            os.environ[clave] = valor


def leer_credencial() -> str:
    """Devuelve la API key, o lanza un error con instrucciones claras."""
    cargar_env()
    clave = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not clave:
        archivo = RAIZ / ".env"
        estado = "existe pero no tiene la clave" if archivo.is_file() else "no existe"
        raise SystemExit(
            "Falta la credencial de la API.\n\n"
            f"Busque en: {archivo}  ({estado})\n"
            "y en la variable de entorno ANTHROPIC_API_KEY (ausente).\n\n"
            "Para arreglarlo, ese archivo tiene que tener una linea asi:\n"
            "    ANTHROPIC_API_KEY=sk-ant-...\n"
        )
    return clave
