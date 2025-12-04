# Inicio

# 1. Gestión de usuario
 
 ## 1.1 Crear nuevo usuario
  * Crear nuevo usuario : Permite registrarse un nuevo usuario añadiéndolo a un archivo JSON que se usará para almacenar los datos de los usuarios.
  * Inicio de sesión : El usuario introduce sus credenciales y si coincide con algún valor de la lista accede a la aplicación. Si no, da error.
  * Validación : Validar si el nombre de usuario es un string y el pin un número entero.
  * Evitar perfiles duplicados : Verificar que el nuevo usuario registrado no coincide con ningún valor de la lista.
    
### campos que va a tener usuario
  * ID cuenta
  * nombre de usuario
  * PIN
  * saldo

## Validaciones necesarias:

 Validar que el nombre de usuario es un string no vacío.

 Validar que el PIN es un entero de 4 dígitos.

 Validar que no existe otro usuario con el mismo nombre.

 Validar que el JSON se actualiza correctamente.

 Saldo inicial ≥ 0.

## 1.2 Inicio de sesión

Descripción:
El usuario introduce nombre de usuario y PIN y, si coinciden con un usuario del archivo JSON, accede a la aplicación.

Validaciones:

Comprobar que el nombre existe.

Comprobar que el PIN coincide con el usuario.

Manejar intentos fallidos (si queréis poner un máximo, opcional).

# 2. Operaciones bancarias

 ## 2.1 Consultar saldo

 Descripción:
 Muestra el saldo actual del usuario logueado.

 Validaciones:

 Comprobar que el usuario está logueado.

 Comprobar que el saldo existe y es un número.

 ## 2.2 Ingresar dinero

 Descripción:
 Incrementa el saldo actual del usuario.

 Validaciones:

 Comprobar que la cantidad a ingresar es un número positivo.

 Actualizar el valor en memoria y luego en el JSON.


 ## 2.3 Retirar dinero

 Descripción:
 Resta la cantidad del saldo del usuario.

 Validaciones:

 Cantidad válida y positiva.

 El usuario tiene saldo suficiente.

 Actualizar el JSON.


 ## 2.4 Transferir entre usuarios

 Descripción:
 Resta cantidad del usuario origen y la suma al usuario destino.

 Validaciones:

 Usuario destino existe.

 Cantidad positiva.

 Saldo suficiente.

 Actualizar saldos de ambos usuarios en JSON.

 Evitar transferencias a uno mismo.

# 3. Menú

 ## 3.1 Menú inicio de sesión
 Descripción:
 Un menú de inicio que permite seleccionar las siguientes opciones:

 ### * Iniciar sesión

 ### *Crear nuevo usuario

 ### *Salir


## 3.2 Menú usuario
Descripción: Este menú aparece solo después de que el usuario haya iniciado sesión correctamente.
Y permite las siguientes opciones:

 ### * Consultar saldo

 ### *Ingresar dinero

 ### *Retirar dinero

 ### *Transferencia a otra cuenta
