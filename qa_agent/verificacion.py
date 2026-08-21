"""Verificacion de evidencia.

Tercera capa anti-invencion, y la unica que no depende de que el modelo se
porte bien: para cada caso de prueba se comprueba que el documento citado
exista y que la cita aparezca literalmente en el.

La comparacion normaliza espacios en blanco (saltos de linea, tabs, espacios
repetidos) porque el modelo puede reflowear un parrafo al copiarlo. No
normaliza palabras: si cambio una palabra, la cita no se considera verificada.
"""

from .esquema import SECCIONES_CASOS
from .herramientas import documentos

VERIFICADA = "verificada"
CITA_NO_ENCONTRADA = "cita_no_encontrada"
DOC_INEXISTENTE = "documento_inexistente"
SIN_CITA = "sin_cita"


def _normalizar(texto: str) -> str:
    return " ".join(texto.split()).casefold()


def verificar(resultado: dict) -> dict:
    """Agrega `estado_evidencia` a cada caso y devuelve un resumen del chequeo.

    Muta `resultado` in place y devuelve las estadisticas.
    """
    contenidos = {
        doc.name.casefold(): _normalizar(
            doc.read_text(encoding="utf-8", errors="replace")
        )
        for doc in documentos()
    }

    conteo = {VERIFICADA: 0, CITA_NO_ENCONTRADA: 0, DOC_INEXISTENTE: 0, SIN_CITA: 0}

    for seccion in SECCIONES_CASOS:
        for caso in resultado.get(seccion, []):
            evidencia = caso.get("evidencia") or {}
            nombre = str(evidencia.get("documento", "")).strip()
            cita = str(evidencia.get("cita", "")).strip()

            if not nombre or not cita:
                estado = SIN_CITA
            elif nombre.casefold() not in contenidos:
                estado = DOC_INEXISTENTE
            elif _normalizar(cita) in contenidos[nombre.casefold()]:
                estado = VERIFICADA
            else:
                estado = CITA_NO_ENCONTRADA

            caso["estado_evidencia"] = estado
            conteo[estado] += 1

    total = sum(conteo.values())
    conteo["total"] = total
    conteo["sospechosos"] = total - conteo[VERIFICADA]
    return conteo
