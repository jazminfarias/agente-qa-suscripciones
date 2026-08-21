# Datos del alta y validaciones

## Registro con login social

La persona puede registrarse con login social, con Google o Facebook. Quien entra
con login social queda registrado de una, sin pasar por el código de confirmación
por mail.

## Registro nativo

El registro nativo pide nombre, apellido, correo y crear una contraseña. La
contraseña tiene que tener un mínimo de 8 caracteres y una mayúscula.

Hay que confirmar el mail antes de poder terminar el registro. Llega un correo
con un código muy largo que hay que poner en el registro para validar.

## Login nativo

El login nativo se hace con la contraseña y el mail guardados en el CMS.

## Datos que pide el paso 2

En el paso 2 el sistema pide teléfono, DNI, nombre y apellidos. Los cuatro son
obligatorios.

## Validaciones

No hay validaciones de formato en los campos.

El email no puede estar repetido al momento del registro.

## Mensajes de error

Los mensajes de error son genéricos, y dicen algo tipo "contacta a tu entidad
bancaria" o "saldo insuficiente".
