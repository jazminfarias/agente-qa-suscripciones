"""Render del resultado a un reporte Markdown legible."""

from datetime import datetime

from .verificacion import CITA_NO_ENCONTRADA, DOC_INEXISTENTE, SIN_CITA, VERIFICADA

_MARCAS = {
    VERIFICADA: "OK evidencia verificada",
    CITA_NO_ENCONTRADA: "ALERTA la cita no aparece literalmente en el documento",
    DOC_INEXISTENTE: "ALERTA el documento citado no existe",
    SIN_CITA: "ALERTA el caso no declara evidencia",
}

_TITULOS = {
    "casos_positivos": "Casos positivos",
    "casos_negativos": "Casos negativos",
    "casos_borde": "Casos borde",
}


def _caso_md(caso: dict) -> list[str]:
    evidencia = caso.get("evidencia") or {}
    estado = caso.get("estado_evidencia", SIN_CITA)
    lineas = [
        f"#### {caso.get('id', '?')} - {caso.get('titulo', '(sin titulo)')}",
        "",
    ]

    precondiciones = caso.get("precondiciones") or []
    if precondiciones:
        lineas.append("**Precondiciones**")
        lineas += [f"- {p}" for p in precondiciones]
        lineas.append("")

    lineas.append("**Pasos**")
    lineas += [f"{i}. {p}" for i, p in enumerate(caso.get("pasos") or [], start=1)]
    lineas.append("")
    lineas.append(f"**Resultado esperado:** {caso.get('resultado_esperado', '-')}")
    lineas.append("")
    lineas.append(
        f"**Evidencia** ({_MARCAS.get(estado, estado)}) - "
        f"`{evidencia.get('documento', '-')}`"
    )
    cita = (evidencia.get("cita") or "").strip()
    if cita:
        lineas.append("")
        lineas += [f"> {l}" for l in cita.splitlines() or [""]]
    lineas.append("")
    return lineas


def render(resultado: dict, traza: list, conteo: dict, pedido: str) -> str:
    md: list[str] = [
        "# Casos de prueba - circuito de alta de suscripciones",
        "",
        f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Pedido: {pedido}",
        "",
        "## Resumen",
        "",
        resultado.get("resumen", "-"),
        "",
        "**Documentos consultados:** "
        + (", ".join(f"`{d}`" for d in resultado.get("documentos_consultados") or []) or "ninguno"),
        "",
        "## Verificacion de evidencia",
        "",
        f"- Casos de prueba generados: {conteo.get('total', 0)}",
        f"- Con cita verificada en la documentacion: {conteo.get(VERIFICADA, 0)}",
        f"- Con evidencia sospechosa: {conteo.get('sospechosos', 0)}",
        "",
    ]

    if conteo.get("sospechosos"):
        md += [
            "> Hay casos cuya cita no se pudo encontrar literalmente en la "
            "documentacion. Revisalos antes de usarlos: pueden apoyarse en una "
            "regla que no esta documentada.",
            "",
        ]

    for seccion, titulo in _TITULOS.items():
        casos = resultado.get(seccion) or []
        md += [f"## {titulo} ({len(casos)})", ""]
        if not casos:
            md += ["Ninguno derivable de la documentacion disponible.", ""]
        for caso in casos:
            md += _caso_md(caso)

    faltante = resultado.get("informacion_faltante") or []
    md += [f"## Informacion faltante ({len(faltante)})", ""]
    if not faltante:
        md += ["Nada registrado.", ""]
    for item in faltante:
        md += [
            f"### {item.get('id', '?')} - {item.get('tema', '-')}",
            "",
            f"- **Por que bloquea:** {item.get('por_que_bloquea', '-')}",
            f"- **Donde deberia estar documentado:** {item.get('donde_deberia_estar', '-')}",
            "",
        ]

    preguntas = resultado.get("preguntas_analista") or []
    md += [f"## Preguntas para el analista funcional ({len(preguntas)})", ""]
    if not preguntas:
        md += ["Ninguna.", ""]
    else:
        md += ["| Id | Pregunta | Relacionada con |", "| --- | --- | --- |"]
        for p in preguntas:
            pregunta = str(p.get("pregunta", "-")).replace("|", "\\|")
            md.append(
                f"| {p.get('id', '?')} | {pregunta} | {p.get('relacionada_con', '-')} |"
            )
        md.append("")

    md += [f"## Traza de herramientas ({len(traza)} llamadas)", ""]
    if traza:
        md += ["| # | Herramienta | Entrada |", "| --- | --- | --- |"]
        for i, paso in enumerate(traza, start=1):
            entrada = str(paso.get("entrada") or {}).replace("|", "\\|")
            md.append(f"| {i} | `{paso['herramienta']}` | `{entrada}` |")
        md.append("")

    return "\n".join(md)
