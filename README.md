# Agente de QA funcional para alta de suscripciones

## Qué construí

Un agente que lee la documentación funcional de un circuito de alta de
suscripciones —archivos de texto locales, escritos por mí en lenguaje natural— y
genera casos de prueba: positivos, negativos, borde, información faltante y
preguntas para el analista funcional. Sirve para detectar, antes de empezar a
testear, qué está definido y qué no. Su restricción central es que no puede
inventar reglas de negocio: si la documentación no dice qué debería ocurrir,
declara el hueco y pregunta en lugar de escribir un caso.

## Cómo se lo pedí

No escribí código manualmente. Describí el objetivo, aporté el conocimiento
funcional del circuito, revisé cada decisión y cada resultado, y fui iterando con
Claude Code. Estas son las instrucciones que definieron el proyecto, en orden.

**1. Pedido inicial, completo y textual**

> Quiero construir un proyecto pequeño para una materia de creación de agentes
> con IA.
>
> Quiero crear un agente de QA funcional que analice documentación sobre un
> circuito de alta de suscripciones y genere casos de prueba.
>
> El agente debe poder consultar la documentación disponible sobre el circuito
> antes de generar los casos. A partir de esa información quiero que genere:
>
> casos positivos;
> casos negativos;
> casos borde;
> información faltante;
> preguntas para el analista funcional.
>
> Hay una regla especialmente importante: el agente no debe inventar reglas de
> negocio ni comportamientos que no estén documentados. Si no tiene información
> suficiente para determinar qué debería ocurrir, debe indicarlo como información
> faltante y formular una pregunta.
>
> Quiero una primera versión mínima que funcione con archivos locales. Mantené el
> alcance pequeño, pensado para un proyecto que pueda completarse en una tarde.
>
> Yo no voy a escribir código manualmente. Quiero que construyas vos el proyecto,
> tomando las decisiones técnicas necesarias. Antes de empezar, explicame
> brevemente qué proponés construir y cómo funcionaría.

**2. No generar documentación ficticia**

> Quiero proporcionar yo la documentación del circuito, porque conozco el
> funcionamiento real. No quiero que inventes documentación de ejemplo. Ayudame a
> crear la carpeta y la estructura necesaria para que yo pueda darte la
> información funcional en lenguaje natural. Empecemos con pocos documentos y
> dejemos deliberadamente algunos aspectos sin documentar para poder evaluar si
> el agente detecta información faltante sin inventarla.

**3. Relevamiento acotado, con mi conocimiento**

> Quiero que me ayudes a completar los tres documentos de docs/ usando
> exclusivamente mi conocimiento funcional. No inventes ni completes información
> por tu cuenta. Haceme las preguntas necesarias en lenguaje no técnico, de a
> pocas por vez. Si algo no lo sé o no te lo especifico, dejalo sin documentar.

**4. No completar lo que no especifiqué**

> Documentala como regla, pero no inventes qué mensaje muestra ni exactamente
> cómo responde el sistema ante ese caso si yo no te lo especifiqué.

> La frase "Si el cobro sale mal, le da un error" dejala tal cual, sin agregar
> ninguna información.

**5. Conservar los huecos deliberados como evaluación**

> Mantené los 7 huecos originales y completá únicamente las columnas de
> resultado. No agregues los huecos nuevos a esa tabla, porque quiero conservarla
> como la evaluación que definimos antes de correr el agente.

## Qué funciona

El agente no recibe la documentación pegada en el prompt: arranca sin verla y
tiene tres herramientas para ir a buscarla —listar los documentos, leer uno
completo y buscar un término—. Decide solo cuáles usa y en qué orden. En la
corrida final listó los documentos, leyó los tres y después hizo ocho búsquedas
puntuales ("reintent", "cancel", "expira", "error") para confirmar que algo no
estuviera documentado antes de declararlo faltante. Cada caso que genera está
obligado a declarar el documento y una cita textual, y un chequeo posterior
verifica que esa cita exista literalmente en el archivo.

Resultado de la corrida: 25 casos —13 positivos, 7 negativos, 5 borde—, los 25
con cita verificada y ninguna marcada como sospechosa, más 12 registros de
información faltante y 12 preguntas para el analista. Detectó 6 de los 7 huecos
que yo había dejado a propósito y anotado antes de ejecutarlo, y no inventó
ninguna regla. Encontró además seis huecos que no habíamos anticipado, entre
ellos qué pasa con la renovación de un alta hecha un día 31 y a dónde vuelve el
usuario si entró por un link de email marketing.

## Qué falta o qué falló

Antes de la primera corrida real el agente no encontró la API key: yo la había
definido como variable de entorno en mi propia terminal, y el proceso del agente
no la hereda. Se resolvió con un archivo `.env`, y de paso se corrigió la lectura
para que el BOM que agrega Notepad al guardar no la rompiera en silencio.

La primera ejecución completa falló por `max_tokens`. El loop de herramientas
funcionó bien —doce llamadas, los tres documentos leídos— pero la respuesta se
cortó a mitad de camino, porque el razonamiento interno del modelo consume parte
del presupuesto de salida. Se ajustó a streaming con 64000 tokens y la segunda
ejecución corrió completa.

Limitaciones que quedaron:

- No detectó el hueco del período de prueba. Al no haber ninguna mención en la
  documentación, no tuvo nada de dónde agarrarse.
- Las citas salen cortadas a mitad de oración, porque los documentos tienen salto
  de línea a los 80 caracteres y el modelo copia una línea en lugar de una frase
  completa.
- El caso CN-05 afirma que los cuatro datos del paso 2 son obligatorios, pero la
  cita que trae no dice eso: la frase que lo respalda es la siguiente. Es
  correcto pero mal atribuido, y la verificación automática no puede verlo porque
  solo comprueba que la cita exista, no que sostenga el caso.
- CP-13 y CB-04 son el mismo caso duplicado con distinto nombre.
- Hay una sola corrida exitosa, así que no tengo ninguna medida de qué tan
  estable es el resultado.

## Qué aprendí

Entendí que un agente no es solamente un prompt: este decide qué herramientas usa
y en qué orden, y verlo buscar "reintent" o "cancel" para confirmar una ausencia
me mostró que ahí hay una lógica propia y no solo texto generado. Aprendí que la
calidad de la documentación condiciona el resultado más que el modelo: mis frases
vagas produjeron huecos y mis frases afirmativas produjeron casos. Vi que decir
"no inventes" no alcanza —lo que funcionó fue obligarlo a citar y después
verificar esas citas contra el archivo—, y que aun así queda un margen que solo
aparece leyendo. Por eso la revisión humana sigue siendo necesaria: el caso mal
atribuido pasó todos los controles automáticos. Y me quedó claro que definir de
antemano qué esperaba que detectara fue lo que convirtió una demo en una
evaluación.
