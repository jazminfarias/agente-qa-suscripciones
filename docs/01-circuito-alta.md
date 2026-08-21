# Circuito de alta de suscripciones

## Para qué sirve

Cuando una persona completa el circuito de alta se convierte en suscriptor y
obtiene acceso a las notas cerradas, que son de mejor calidad que las abiertas.
También obtiene acceso a un foro de debates y a que le envíen newsletters.

## Por dónde entra la gente

- **Choque directo.** Desde cronista.com la persona va al botón que dice
  "Suscribite" y llega a cronista.com/suscripciones. Ahí va a ver los dos planes.
- **Choque premium.** Una persona anónima o registrada choca con una nota
  cerrada. Ahí aparece el paywall porque se blurea la nota.
- **Link a un plan con descuento.** Si es jubilado o estudiante, luego de
  completar un formulario, si está ok, la gente de call center le manda por
  correo un link directo a un plan con descuento que no es visible desde
  /suscripciones. Si es corporativo, también se le manda link si luego de un
  formulario está aprobado para que se suscriba a ese plan.
- **Email marketing.** También pueden llegar links de planes o de /suscripciones
  por email marketing, que puede ser disparado por marketing y otros por call
  center.

El formulario que completan jubilados, estudiantes y corporativos sucede antes,
en otro circuito.

## Quiénes participan

- La persona que se suscribe.
- El call center y marketing, que mandan los links. Su rol termina al mandar el
  link.
- Mercado Pago, cuando la persona elige pagar por ese medio.

## Antes de empezar

Para suscribirse hay que estar registrado por lo menos. Si la persona llega al
formulario de suscripción y elige un plan sin estar logueada o registrada, el
sistema le va a pedir que haga una de las dos.

Todo puede suceder en el mismo momento: primero anónimo, luego registrado y
luego suscriptor, pero ese es el orden.

## Estados de la persona

Son estos tres, y solo estos tres:

- **Anónimo:** no está logueado.
- **Registrado:** ya tenemos su correo, nombre y apellido. Puede registrarse con
  login social, o si no hace la contraseña desde la web. Puede ver algunas notas
  más.
- **Suscriptor (member):** alguien que ya pagó y va a seguir pagando.

## El circuito paso a paso

1. La persona llega a la landing de suscripciones (cronista.com/suscripciones)
   por choque directo, o choca con una nota cerrada por choque premium. Elige
   entre dos planes: Mensual o Anual.

2. **Paso 1.** Elija el plan que elija, si todavía no está logueada el sistema le
   pide que lo haga, por login social (Google, Facebook) o por login nativo
   (contraseña y mail guardados en el CMS). Y si no, le permite registrarse en el
   momento.

   - Si se loguea y ya es suscriptor, el sistema lo redirige a la Home y no le
     permite continuar el circuito de suscripción.
   - Si no es suscriptora, o recién se registra, pasa al paso 2.

3. **Paso 2.** El sistema le pide otros datos: teléfono, DNI, nombre y apellidos.
   Estos datos se piden siempre, incluso a una persona que ya estaba registrada
   de antes.

4. **Paso 3.** El sistema le permite elegir si pagar con tarjeta de crédito o de
   débito, o si quiere pagar con Mercado Pago.

5. Si sale todo ok, le sale un cartel de que ya es Member y va a ver un botón de
   "Volver al sitio", que debe redirigirla al return to, que es la url desde la
   cual chocó. Si era directo, vuelve a la Home. Si no lo era, vuelve a la nota
   premium.

Si el cobro sale mal, le da un error.

## Moverse hacia atrás dentro del circuito

Del paso 3 al paso 2 se puede volver. Del paso 2 al paso 1 no. Si quiere cambiar
de plan, tiene que volver directamente a /suscripciones.

## Notificaciones

La persona recibe un mail de bienvenida.
