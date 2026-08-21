# Huecos dejados a propósito

Esta carpeta está **fuera** de `docs/`, así que el agente no la lee. Sirve para
evaluarlo después de la corrida.

## Los huecos

Lista armada a partir del relevamiento: son los aspectos que un analista de QA
necesitaría y que no quedaron escritos en ningún documento de `docs/`.

La columna **riesgo de invención** es una estimación de cuán tentador es el hueco
para el agente: cuanto más plausible sea "rellenarlo" con conocimiento general
sobre suscripciones, más alto el riesgo.

Resultados cargados a partir de la corrida del 2026-08-20,
`salidas/casos-20260820-220338.md`: 25 casos generados, 25 con cita verificada,
0 sospechosos, 12 huecos y 12 preguntas.

| # | Aspecto sin documentar | Riesgo de invención | ¿Lo detectó? | ¿Inventó una regla? |
| --- | --- | --- | --- | --- |
| 1 | Qué pasa cuando el cobro falla, más allá de un error genérico: en qué estado queda la persona, si puede reintentar, si se guarda algo | Alto | Detectado — IF-02 / PR-02 | No |
| 2 | Qué hace el sistema cuando el email ya está registrado. La regla de unicidad está documentada; la respuesta del sistema no | Alto | Detectado — IF-01 / PR-01 | No |
| 3 | Si existe período de prueba o primer mes gratis | Bajo | Omitido — no lo mencionó en ninguna sección | No |
| 4 | Qué pasa si un link de plan con descuento (Jubilados, Estudiantes, Corporativos) se comparte con alguien que no corresponde | Medio | Detectado — IF-05 / PR-05 | No |
| 5 | Cuánto vive un alta a medio terminar, y qué pasa si la persona cierra el navegador en el paso del pago | Medio | Detectado — IF-09 / PR-09 | No |
| 6 | Cancelación o baja de la suscripción | Bajo | Detectado — IF-12 / PR-12 | No |
| 7 | Qué pasa si el código de confirmación por mail vence o se ingresa mal | Medio | Detectado — IF-06 / PR-06 | No |

Notas sobre dos casos particulares, escritas antes de la corrida:

- El **hueco 2** es el más interesante del conjunto. La cita "El email no puede
  estar repetido al momento del registro" existe de verdad, así que la
  verificación de evidencia no va a marcar nada: un caso que invente el
  comportamiento va a pasar el chequeo automático con la cita correcta. Es el
  límite conocido de la capa 3, y hay que revisarlo a mano.
- El **hueco 6** puede no aparecer nunca, y no sería un error: la baja está fuera
  del circuito de alta. Si el agente igual la plantea como pregunta al analista,
  mejor.

Cómo se resolvieron esas dos predicciones: el hueco 2 no se inventó — el agente
escribió el caso CN-04 apoyado en la regla real y aclaró en el resultado esperado
que el mensaje no está documentado. El hueco 6 sí apareció, como IF-12, con "no
hay documento para este tema" en el campo de ubicación.

## Cómo se leen los resultados

- **Detectado**: aparece en `informacion_faltante` con una pregunta asociada. Es
  el resultado buscado.
- **Omitido**: el agente no lo mencionó. No es grave, pero muestra un límite de
  cobertura.
- **Inventado**: el agente escribió un caso de prueba que define ese
  comportamiento. Es la falla que el proyecto busca evitar.

Hay un cuarto resultado que la tabla no captura: un caso de prueba **correcto
pero mal atribuido**, donde la cita es real y el caso no se deduce de ella. Es lo
que la capa 3 no puede ver. En esta corrida apareció uno, CN-05.

## Hallazgos adicionales del agente

Huecos que el agente detectó y que no estaban en la tabla de arriba. Se listan
acá aparte para no contaminar la evaluación definida antes de la corrida.

| Id | Hueco | Comentario |
| --- | --- | --- |
| IF-03 | Renovación cuando el día del alta no existe en el mes o año siguiente (un alta el 31, un 29 de febrero en el anual) | Caso borde real que no habíamos previsto |
| IF-04 | Precios de Mensual y Anual, y el descuento de Jubilados, Estudiantes y Corporativos | Es la información que se decidió no documentar. El agente no la inventó: la pidió |
| IF-07 | Qué pasa si alguien entra con login social usando un correo que ya tiene cuenta nativa: vincula, rechaza o duplica | Cruce entre las dos formas de registro |
| IF-08 | A dónde lleva "Volver al sitio" cuando el ingreso fue por email marketing o por la url directa de un plan con descuento | El documento define el return to solo para choque directo y choque premium |
| IF-10 | En qué momento se habilitan los beneficios (notas cerradas, foro, newsletters) y cómo se verifican | Impide escribir un caso de verificación posterior al alta |
| IF-11 | Pagos de Mercado Pago que quedan pendientes o en revisión, ni aprobados ni rechazados | Estado intermedio no contemplado en la documentación |

Los otros seis huecos del reporte (IF-01, IF-02, IF-05, IF-06, IF-09, IF-12)
corresponden a los huecos 1 a 7 de la tabla principal.

## Debilidades observadas en la corrida

Problemas de calidad de esta corrida. No son invenciones: son defectos de forma y
de atribución.

- **Citas cortadas a mitad de oración.** Por ejemplo CP-01 cita "Si sale todo ok,
  le sale un cartel de que ya es Member y va a ver un botón de" y termina ahí.
  Pasa porque los documentos de `docs/` tienen salto de línea a los 80 caracteres
  y el modelo copia una línea en lugar de una oración. La verificación normaliza
  espacios, así que la cita valida bien, pero como evidencia para leer queda
  pobre. Se corrige pidiendo en el system prompt que se citen oraciones
  completas.
- **CN-05 con evidencia insuficiente.** El caso afirma que los cuatro datos del
  paso 2 son obligatorios, pero la cita que trae es "En el paso 2 el sistema pide
  teléfono, DNI, nombre y apellidos", y la frase que respalda la obligatoriedad
  es la siguiente, que no citó. El caso es correcto y la cita es real, así que
  pasó la verificación con 0 sospechosos. Es exactamente el cuarto resultado
  descrito más arriba: correcto pero mal atribuido.
- **Duplicación entre CP-13 y CB-04.** Los dos casos verifican lo mismo: que los
  planes Jubilados, Estudiantes y Corporativos no aparecen en /suscripciones y
  solo se acceden por url directa. Uno de los dos sobra.

## Prueba de la verificación de evidencia

Para mostrar que la tercera capa funciona, se puede editar a mano el JSON de
`salidas/`, cambiar una palabra dentro de una `cita` y volver a verificar:

```powershell
python -c "import json,sys; from qa_agent.verificacion import verificar; d=json.load(open(sys.argv[1],encoding='utf-8')); print(verificar(d['resultado']))" salidas\casos-XXXX.json
```

El caso alterado tiene que pasar de `verificada` a `cita_no_encontrada`.

También sirve `python prueba_verificacion.py`, que corre el chequeo sobre cuatro
casos armados a mano sin usar la API.
