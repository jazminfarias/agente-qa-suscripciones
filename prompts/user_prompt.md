# User prompt del agente

> Igual que `system_prompt.md`, este archivo tiene que reflejar lo que el
> código realmente envía como primer mensaje del usuario. La fuente de
> verdad es `PEDIDO_POR_DEFECTO` en `qa_agent/agente.py` y el argumento
> `pedido` de `main.py`.

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
*qué* se le pide analizar en una corrida en particular. Mantenerlos
separados es lo que te permite, en `corridas/`, documentar el mismo
contrato corriendo sobre pedidos distintos sin reescribir el system prompt
cada vez.
