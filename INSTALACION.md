# Instalacion y uso

Detalle tecnico del proyecto. La descripcion del proceso de construccion esta en
`README.md`.

## Como esta armado

```
docs/          documentacion del circuito (la escribe la persona, no el agente)
evaluacion/    huecos dejados a proposito, para evaluar al agente (el agente no lo lee)
salidas/       reportes generados
qa_agent/
  config.py         modelo, rutas, limites, credencial
  herramientas.py   las 3 herramientas sobre docs/
  prompt.py         system prompt con la regla anti-invencion
  esquema.py        esquema JSON de la salida
  agente.py         loop de tool use
  verificacion.py   chequeo de citas contra los archivos reales
  reporte.py        render a Markdown
main.py                  CLI
prueba_verificacion.py   demuestra la verificacion de citas sin usar la API
```

## Como funciona

El agente **no** recibe la documentacion pegada en el prompt. Arranca a ciegas y
tiene que ir a buscarla:

1. `listar_documentos()` para ver que hay en `docs/`.
2. `leer_documento(nombre)` sobre los documentos relevantes.
3. `buscar_en_documentos(texto)` para confirmar si un termino esta documentado.
4. Cuando junto material suficiente, devuelve un JSON con las cinco secciones.

El ciclo es un loop manual sobre la Messages API (`qa_agent/agente.py`), no el
tool runner del SDK: en un trabajo sobre agentes conviene que el ciclo
*razonar -> llamar herramienta -> leer resultado -> decidir* este a la vista.

## Las tres capas anti-invencion

1. **Prompt** (`prompt.py`): la unica fuente valida es el texto de los
   documentos; el conocimiento general del modelo sobre suscripciones no vale.
   Ante la duda, informacion faltante y pregunta.
2. **Evidencia obligatoria** (`esquema.py`): el esquema exige que cada caso
   declare `documento` + `cita` textual. Sin cita el modelo no puede emitir un
   caso: no hay forma de expresarlo en el formato de salida.
3. **Verificacion en codigo** (`verificacion.py`): despues de generar, un
   chequeo comprueba que cada cita exista **literalmente** en el archivo citado.
   Si no aparece, el caso queda marcado en el reporte como evidencia sospechosa.

La capa 3 es la que hace la diferencia: no depende de que el modelo obedezca. La
comparacion normaliza espacios en blanco (el modelo puede reflowear un parrafo al
copiarlo) pero no palabras: si cambio una palabra, no pasa.

## Puesta en marcha

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

copy .env.example .env      # y pegar la ANTHROPIC_API_KEY dentro
```

Tambien sirve `$env:ANTHROPIC_API_KEY = "sk-ant-..."` en lugar del `.env`.

## Uso

```powershell
python main.py --solo-docs                  # que documentacion ve el agente (no usa la API)
python main.py                              # analiza todo el circuito
python main.py "alta pagando con tarjeta"   # acota el analisis
```

Cada corrida deja en `salidas/` un reporte `.md` legible y un `.json` con el
resultado crudo, la traza de herramientas y el resumen de verificacion.

Para ver la capa 3 funcionando sin gastar tokens (util para mostrar en la
defensa del trabajo):

```powershell
python prueba_verificacion.py
```

Alimenta la verificacion con cuatro casos armados a mano - una cita real, una
regla plausible que nadie documento, un documento inexistente y un caso sin
evidencia - y muestra como cada uno queda clasificado.

## Para empezar

1. Completá los tres archivos de `docs/` (leé `docs/README.md` primero: explica
   como escribir para que el agente pueda citarte).
2. Dejá algunos aspectos sin documentar a proposito y anotalos en
   `evaluacion/huecos-esperados.md`.
3. Corré el agente y compará.

## Decisiones tecnicas

- **Modelo**: `claude-opus-5`, con salida estructurada (`output_config.format`)
  para que el resultado sea un JSON validado y no texto libre que haya que
  parsear.
- **Sin RAG ni embeddings**: la documentacion de un circuito entra entera en
  contexto. Las herramientas leen archivos completos; agregar un indice
  vectorial seria complejidad sin beneficio a esta escala.
- **Sin dependencias mas alla del SDK**: la carga del `.env` son diez lineas en
  `config.py`.
- **Tope de vueltas** (`MAX_ITERACIONES`) para que un loop de herramientas no se
  vaya de mano.

## Limites conocidos

- La verificacion comprueba que la cita **exista**, no que la cita realmente
  respalde el caso. Un caso puede citar un parrafo correcto y sacar de ahi una
  conclusion que no se deduce. Eso todavia requiere lectura humana.
- El agente lee `.md` y `.txt`. No lee PDF, Word, Confluence ni imagenes.
- Sin cache de prompt: cada corrida vuelve a leer la documentacion desde cero.
  A esta escala el costo es de centavos.
