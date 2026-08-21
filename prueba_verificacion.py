"""Prueba manual de la verificacion de evidencia. No usa la API."""

from qa_agent.verificacion import verificar

falso = {
    "casos_positivos": [
        {  # cita que SI existe en la plantilla
            "id": "CP-01",
            "evidencia": {
                "documento": "01-circuito-alta.md",
                "cita": "El circuito paso a paso",
            },
        },
        {  # regla plausible pero nunca documentada
            "id": "CP-02",
            "evidencia": {
                "documento": "01-circuito-alta.md",
                "cita": "Si la tarjeta es rechazada se muestra un error",
            },
        },
        {  # documento que no existe
            "id": "CP-03",
            "evidencia": {"documento": "99-inexistente.md", "cita": "cualquier cosa"},
        },
        {  # sin evidencia
            "id": "CP-04",
            "evidencia": {"documento": "", "cita": ""},
        },
    ]
}

conteo = verificar(falso)
for caso in falso["casos_positivos"]:
    print(caso["id"], "->", caso["estado_evidencia"])
print()
print("conteo:", conteo)
