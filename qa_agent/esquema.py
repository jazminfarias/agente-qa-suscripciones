"""Esquema JSON de la salida del agente.

Segunda capa anti-invencion: `evidencia` es obligatoria en cada caso de prueba,
asi que el modelo no puede producir un caso sin declarar de donde lo saco.

El esquema es estricto (`additionalProperties: false` y todos los campos en
`required`), que es lo que exige la API para structured outputs.
"""

_EVIDENCIA = {
    "type": "object",
    "description": "De donde sale este caso. Sin esto, el caso no existe.",
    "properties": {
        "documento": {
            "type": "string",
            "description": "Nombre del archivo de docs/ que respalda el caso.",
        },
        "cita": {
            "type": "string",
            "description": (
                "Fragmento copiado textualmente del documento, caracter por "
                "caracter. Se verifica automaticamente contra el archivo."
            ),
        },
    },
    "required": ["documento", "cita"],
    "additionalProperties": False,
}


def _caso(prefijo: str, descripcion: str) -> dict:
    return {
        "type": "array",
        "description": descripcion,
        "items": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": f"Identificador correlativo, formato {prefijo}-01.",
                },
                "titulo": {"type": "string"},
                "precondiciones": {"type": "array", "items": {"type": "string"}},
                "pasos": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Pasos concretos y ejecutables, en orden.",
                },
                "resultado_esperado": {
                    "type": "string",
                    "description": "Que tiene que pasar, segun la documentacion.",
                },
                "evidencia": _EVIDENCIA,
            },
            "required": [
                "id",
                "titulo",
                "precondiciones",
                "pasos",
                "resultado_esperado",
                "evidencia",
            ],
            "additionalProperties": False,
        },
    }


ESQUEMA_SALIDA = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {
            "resumen": {
                "type": "string",
                "description": (
                    "Dos o tres oraciones sobre que cubre la documentacion leida "
                    "y que tan completa esta."
                ),
            },
            "documentos_consultados": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Nombres de los archivos que efectivamente leiste.",
            },
            "casos_positivos": _caso(
                "CP", "Casos donde el circuito funciona segun lo documentado."
            ),
            "casos_negativos": _caso(
                "CN", "Casos invalidos cuyo rechazo esta documentado."
            ),
            "casos_borde": _caso(
                "CB", "Limites y estados poco frecuentes que esten documentados."
            ),
            "informacion_faltante": {
                "type": "array",
                "description": "Huecos de la documentacion que impiden probar.",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "Formato IF-01."},
                        "tema": {
                            "type": "string",
                            "description": "Que aspecto del circuito no esta documentado.",
                        },
                        "por_que_bloquea": {
                            "type": "string",
                            "description": "Que caso de prueba no se puede escribir por esto.",
                        },
                        "donde_deberia_estar": {
                            "type": "string",
                            "description": (
                                "Documento donde corresponderia documentarlo, o "
                                "'no hay documento para este tema'."
                            ),
                        },
                    },
                    "required": ["id", "tema", "por_que_bloquea", "donde_deberia_estar"],
                    "additionalProperties": False,
                },
            },
            "preguntas_analista": {
                "type": "array",
                "description": "Preguntas cerradas y accionables para el analista funcional.",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "Formato PR-01."},
                        "pregunta": {"type": "string"},
                        "relacionada_con": {
                            "type": "string",
                            "description": "Id de informacion_faltante que resuelve, por ejemplo IF-02.",
                        },
                    },
                    "required": ["id", "pregunta", "relacionada_con"],
                    "additionalProperties": False,
                },
            },
        },
        "required": [
            "resumen",
            "documentos_consultados",
            "casos_positivos",
            "casos_negativos",
            "casos_borde",
            "informacion_faltante",
            "preguntas_analista",
        ],
        "additionalProperties": False,
    },
}

# Secciones que contienen casos de prueba con evidencia verificable.
SECCIONES_CASOS = ("casos_positivos", "casos_negativos", "casos_borde")
