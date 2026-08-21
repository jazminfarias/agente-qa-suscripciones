"""Loop del agente: razonar, llamar herramientas, leer resultados, generar.

Se usa el loop manual (no el tool runner del SDK, que es beta) porque en un
trabajo practico sobre agentes conviene que el ciclo este a la vista.
"""

import json
from typing import Tuple

import anthropic

from .config import MAX_ITERACIONES, MAX_TOKENS, MODELO, leer_credencial
from .esquema import ESQUEMA_SALIDA
from .herramientas import DEFINICIONES, ejecutar
from .prompt import SYSTEM

PEDIDO_POR_DEFECTO = (
    "Analiza la documentacion disponible del circuito de alta de suscripciones y "
    "genera casos de prueba funcionales."
)


def generar(pedido: str = PEDIDO_POR_DEFECTO, *, verbose: bool = True) -> Tuple[dict, list]:
    """Ejecuta el agente. Devuelve (resultado, traza de herramientas)."""
    cliente = anthropic.Anthropic(api_key=leer_credencial())

    mensajes: list = [{"role": "user", "content": pedido}]
    traza: list[dict] = []

    for vuelta in range(1, MAX_ITERACIONES + 1):
        # Streaming: con MAX_TOKENS grande una peticion comun puede superar el
        # timeout HTTP. get_final_message() espera el mensaje completo, asi que
        # el resto del loop no cambia.
        with cliente.messages.stream(
            model=MODELO,
            max_tokens=MAX_TOKENS,
            system=SYSTEM,
            tools=DEFINICIONES,
            output_config={"format": ESQUEMA_SALIDA},
            messages=mensajes,
        ) as flujo:
            respuesta = flujo.get_final_message()

        if respuesta.stop_reason == "refusal":
            detalle = getattr(respuesta, "stop_details", None)
            motivo = getattr(detalle, "explanation", None) or "sin detalle"
            raise RuntimeError(f"El modelo rechazo la solicitud: {motivo}")

        if respuesta.stop_reason == "max_tokens":
            raise RuntimeError(
                "La respuesta se corto por max_tokens. Subi MAX_TOKENS en "
                "qa_agent/config.py o pedi un alcance mas acotado."
            )

        llamadas = [b for b in respuesta.content if b.type == "tool_use"]

        # Sin llamadas a herramientas: el agente termino y devolvio el JSON.
        if not llamadas:
            texto = next((b.text for b in respuesta.content if b.type == "text"), "")
            if not texto.strip():
                raise RuntimeError("El modelo no devolvio contenido.")
            return json.loads(texto), traza

        mensajes.append({"role": "assistant", "content": respuesta.content})

        resultados = []
        for llamada in llamadas:
            salida, es_error = ejecutar(llamada.name, dict(llamada.input))
            if verbose:
                argumentos = ", ".join(
                    f"{k}={v!r}" for k, v in dict(llamada.input).items()
                )
                marca = "ERROR" if es_error else "ok"
                print(
                    f"  [{vuelta}] {llamada.name}({argumentos}) -> "
                    f"{marca}, {len(salida)} caracteres"
                )
            traza.append(
                {
                    "vuelta": vuelta,
                    "herramienta": llamada.name,
                    "entrada": dict(llamada.input),
                    "es_error": es_error,
                    "caracteres_devueltos": len(salida),
                }
            )
            resultados.append(
                {
                    "type": "tool_result",
                    "tool_use_id": llamada.id,
                    "content": salida,
                    "is_error": es_error,
                }
            )

        mensajes.append({"role": "user", "content": resultados})

    raise RuntimeError(
        f"El agente no termino en {MAX_ITERACIONES} vueltas. "
        "Revisa MAX_ITERACIONES en qa_agent/config.py."
    )
