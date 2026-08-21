"""Herramientas que el agente usa para consultar la documentacion local.

Son tres, deliberadamente pocas:

    listar_documentos()        que documentacion existe
    leer_documento(nombre)     el texto completo de un documento
    buscar_en_documentos(texto) donde aparece un termino

El agente arranca sin la documentacion en contexto: tiene que ir a buscarla.
"""

from pathlib import Path
from typing import Tuple

from .config import DIR_DOCS, EXTENSIONES, IGNORADOS, MAX_COINCIDENCIAS


def documentos() -> list[Path]:
    """Documentos funcionales disponibles, en orden alfabetico."""
    if not DIR_DOCS.is_dir():
        return []
    return sorted(
        p
        for p in DIR_DOCS.iterdir()
        if p.is_file()
        and p.suffix.lower() in EXTENSIONES
        and p.name not in IGNORADOS
        and not p.name.startswith("_")
    )


def _resolver(nombre: str) -> Path | None:
    """Busca un documento por nombre. Solo acepta nombres de la lista blanca,
    asi que no hay forma de leer archivos fuera de docs/."""
    pedido = Path(nombre).name.casefold()
    for doc in documentos():
        if doc.name.casefold() == pedido or doc.stem.casefold() == pedido:
            return doc
    return None


def _titulo(texto: str) -> str:
    """Primer encabezado markdown del documento; si no hay, la primera linea
    con contenido que no sea un comentario HTML."""
    candidata = ""
    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("<!--") or linea.startswith("-->"):
            continue
        if linea.startswith("#"):
            return linea.lstrip("# ").strip()
        candidata = candidata or linea
    return candidata or "(sin titulo)"


# --------------------------------------------------------------------------
# Implementaciones
# --------------------------------------------------------------------------

def listar_documentos() -> str:
    docs = documentos()
    if not docs:
        return (
            "No hay documentacion disponible en la carpeta docs/. "
            "No se puede generar ningun caso de prueba."
        )
    lineas = [f"Documentos disponibles ({len(docs)}):", ""]
    for doc in docs:
        texto = doc.read_text(encoding="utf-8", errors="replace")
        titulo = _titulo(texto)
        palabras = len(texto.split())
        lineas.append(f"- {doc.name} | {titulo} | ~{palabras} palabras")
    return "\n".join(lineas)


def leer_documento(nombre: str) -> Tuple[str, bool]:
    doc = _resolver(nombre)
    if doc is None:
        disponibles = ", ".join(d.name for d in documentos()) or "(ninguno)"
        return (
            f"No existe el documento '{nombre}'. Documentos disponibles: {disponibles}",
            True,
        )
    texto = doc.read_text(encoding="utf-8", errors="replace")
    return f"=== {doc.name} ===\n\n{texto}", False


def buscar_en_documentos(texto: str) -> str:
    aguja = texto.strip().casefold()
    if not aguja:
        return "La busqueda esta vacia."

    coincidencias: list[str] = []
    for doc in documentos():
        for nro, linea in enumerate(
            doc.read_text(encoding="utf-8", errors="replace").splitlines(), start=1
        ):
            if aguja in linea.casefold():
                coincidencias.append(f"{doc.name}:{nro}: {linea.strip()}")
                if len(coincidencias) >= MAX_COINCIDENCIAS:
                    break
        if len(coincidencias) >= MAX_COINCIDENCIAS:
            break

    if not coincidencias:
        return (
            f"Sin coincidencias para '{texto}'. "
            "Ese termino no aparece en la documentacion disponible."
        )
    return f"{len(coincidencias)} coincidencia(s) para '{texto}':\n\n" + "\n".join(
        coincidencias
    )


# --------------------------------------------------------------------------
# Definiciones para la API
# --------------------------------------------------------------------------

DEFINICIONES = [
    {
        "name": "listar_documentos",
        "description": (
            "Lista la documentacion funcional disponible sobre el circuito, con "
            "titulo y tamano aproximado. Usala primero, antes de cualquier otra cosa."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
    {
        "name": "leer_documento",
        "description": (
            "Devuelve el texto completo de un documento. Usa exactamente el nombre "
            "de archivo que devolvio listar_documentos."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre": {
                    "type": "string",
                    "description": "Nombre del archivo, por ejemplo '01-circuito-alta.md'.",
                }
            },
            "required": ["nombre"],
            "additionalProperties": False,
        },
    },
    {
        "name": "buscar_en_documentos",
        "description": (
            "Busca un texto literal en todos los documentos y devuelve las lineas "
            "donde aparece. Sirve para confirmar si un termino esta documentado o no "
            "antes de asumir nada sobre el."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "texto": {
                    "type": "string",
                    "description": "Termino o frase a buscar.",
                }
            },
            "required": ["texto"],
            "additionalProperties": False,
        },
    },
]


def ejecutar(nombre: str, entrada: dict) -> Tuple[str, bool]:
    """Ejecuta una herramienta. Devuelve (resultado, es_error)."""
    if nombre == "listar_documentos":
        return listar_documentos(), False
    if nombre == "leer_documento":
        return leer_documento(str(entrada.get("nombre", "")))
    if nombre == "buscar_en_documentos":
        return buscar_en_documentos(str(entrada.get("texto", ""))), False
    return f"Herramienta desconocida: {nombre}", True
