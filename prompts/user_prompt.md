# User prompt del agente

Este archivo refleja el primer mensaje que el código envía como usuario, definido en PEDIDO_POR_DEFECTO (qa_agent/agente.py) y parametrizable con el argumento pedido de main.py.

## Pedido por defecto

Es el mensaje que se envía cuando corrés `python main.py` sin argumentos:

```
Analiza la documentacion disponible del circuito de alta de suscripciones y
genera casos de prueba funcionales.
```

Le pide al agente cubrir todo lo que encuentre en `docs/`, sin acotar a un
subtema. Es el que usaste en la corrida de referencia (25 casos generados).

## Pedido acotado (opcional)

`main.py` acepta reemplazar el pedido por uno más específico, por ejemplo:

```
python main.py "alta de suscripcion pagando con tarjeta de credito"
```

Esto le pide al agente enfocarse solo en ese subcircuito en vez de generar
casos para todo el flujo. Sirve para corridas más chicas o para probar una
sección puntual después de agregar documentación nueva.

## Por qué importa esta distinción

El `system_prompt.md` define *cómo* tiene que comportarse el agente siempre
(no inventar, citar evidencia, formato JSON). El `user_prompt.md` define
*qué* se le pide analizar en una corrida en particular. Mantenerlos separados es lo que permite, en corridas/, comparar el mismo pedido corriendo sobre distintos motores sin tocar el system prompt entre una corrida y otra.
