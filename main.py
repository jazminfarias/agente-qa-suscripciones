"""CLI del agente de QA.

Uso:
    python main.py
    python main.py "alta de suscripcion pagando con tarjeta de credito"
    python main.py --solo-docs        (no llama a la API: lista la documentacion)
"""

import argparse
import json
import sys
from datetime import datetime

from qa_agent.agente import PEDIDO_POR_DEFECTO, generar
from qa_agent.config import DIR_SALIDAS
from qa_agent.herramientas import documentos, listar_documentos
from qa_agent.reporte import render
from qa_agent.verificacion import VERIFICADA, verificar


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera casos de prueba a partir de la documentacion en docs/."
    )
    parser.add_argument(
        "pedido",
        nargs="?",
        default=PEDIDO_POR_DEFECTO,
        help="Que analizar. Por defecto, todo el circuito.",
    )
    parser.add_argument(
        "--solo-docs",
        action="store_true",
        help="Muestra la documentacion que veria el agente y termina. No usa la API.",
    )
    args = parser.parse_args()

    if args.solo_docs:
        print(listar_documentos())
        return 0

    if not documentos():
        print(
            "No hay documentacion en docs/. Escribi al menos un documento antes "
            "de correr el agente.",
            file=sys.stderr,
        )
        return 1

    print(f"Pedido: {args.pedido}")
    print("Consultando documentacion...")
    resultado, traza = generar(args.pedido)

    conteo = verificar(resultado)
    print(
        f"\nCasos generados: {conteo['total']} "
        f"(evidencia verificada: {conteo[VERIFICADA]}, "
        f"sospechosos: {conteo['sospechosos']})"
    )
    print(
        f"Informacion faltante: {len(resultado.get('informacion_faltante') or [])} | "
        f"Preguntas: {len(resultado.get('preguntas_analista') or [])}"
    )

    DIR_SALIDAS.mkdir(exist_ok=True)
    sello = datetime.now().strftime("%Y%m%d-%H%M%S")
    ruta_md = DIR_SALIDAS / f"casos-{sello}.md"
    ruta_json = DIR_SALIDAS / f"casos-{sello}.json"

    ruta_md.write_text(
        render(resultado, traza, conteo, args.pedido), encoding="utf-8"
    )
    ruta_json.write_text(
        json.dumps(
            {
                "pedido": args.pedido,
                "verificacion": conteo,
                "resultado": resultado,
                "traza": traza,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"\nReporte: {ruta_md}")
    print(f"JSON:    {ruta_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
