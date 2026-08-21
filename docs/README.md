# Como escribir la documentacion del circuito

Esta carpeta es la unica fuente de verdad del agente. Todo lo que el agente
afirme tiene que estar escrito aca; todo lo que falte aca deberia aparecer en el
reporte como informacion faltante.

## Reglas de la carpeta

- El agente lee los archivos `.md` y `.txt` de `docs/`.
- **No** lee este `README.md` ni ningun archivo que empiece con `_`. Si querés
  guardar un borrador sin que el agente lo vea, llamalo `_borrador.md`.
- Escribí en lenguaje natural, como se lo explicarias a alguien que se suma al
  equipo. No hace falta formato especial: parrafos, listas y tablas alcanzan.

## Como escribir para que el agente pueda citarte

El agente esta obligado a respaldar cada caso de prueba con una **cita textual**
de estos documentos, y un chequeo automatico verifica que la cita exista de
verdad. Eso funciona mejor si escribis reglas **afirmativas y autocontenidas**,
de una o dos oraciones:

- Bien: "El email es obligatorio y debe tener formato valido. Si no lo tiene, el
  formulario muestra el error 'Email invalido' y no permite continuar."
- Mal: "Validamos el email como siempre."

Cuanto mas concreto el texto (mensajes exactos, cantidades, plazos, nombres de
estados), mas concretos van a ser los casos de prueba.

## Que conviene cubrir

Los tres archivos que estan en esta carpeta son un punto de partida:

| Archivo | Contenido |
| --- | --- |
| `01-circuito-alta.md` | El flujo de alta paso a paso, actores y estados |
| `02-datos-y-validaciones.md` | Campos del formulario, formatos, mensajes de error |
| `03-planes-y-cobro.md` | Planes disponibles, medios de pago, cobro y comprobante |

Podés renombrarlos, partirlos o agregar otros. El agente se adapta a lo que
encuentre.

## Sobre los huecos deliberados

Para este trabajo practico conviene **no** documentar todo. Dejá afuera a
proposito algunos aspectos que un analista de QA necesitaria, por ejemplo:

- que pasa cuando el medio de pago es rechazado;
- si se puede dar de alta dos veces la misma persona;
- cuanto tiempo vive un alta a medio terminar;
- que pasa si el usuario cierra el navegador en el paso del pago.

No escribas "esto no esta definido" en los documentos: simplemente **no lo
menciones**. La prueba del agente es detectar el silencio, no leer un cartel.

Antes de correr el agente, anotá los huecos que dejaste en
`../evaluacion/huecos-esperados.md`. Ese archivo esta fuera de `docs/`, asi que
el agente no lo ve, y te sirve para comparar despues: cuantos huecos detecto,
cuantos se le pasaron, y si invento alguna regla que vos nunca escribiste.
