from decimal import ROUND_HALF_UP, Decimal
import json
import random
import time

# 1. GESTIÓN DE DATOS - usuarios.json

def cargar_datos_globales():
    """Carga el diccionario global de todos los usuarios desde 'usuarios.json'."""
    try:
        with open("usuarios.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {} 
    except json.JSONDecodeError:
        print("Advertencia: El archivo usuarios.json no tiene formato válido. Iniciando con datos vacíos.")
        return {}

def guardar_datos_globales(datos):
    """Guarda el diccionario global de todos los usuarios en 'usuarios.json'."""
    try:
        with open("usuarios.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

# 2 FUNCIONES DE AUTENTICACIÓN Y REGISTRO

def crear_usuario(datos_globales):
    """Permite crear un nuevo usuario, lo añade y retorna su nombre y datos."""
    print("REGISTRO DE NUEVO USUARIO")
    
    while True:
        usuario = input("Nombre de usuario (único): ").strip()
        if usuario in datos_globales:
            print(f"Error: El usuario '{usuario}' ya existe. Intente con otro.")
        elif not usuario:
            print("El nombre de usuario no puede estar vacío.")
        else:
            break

    while True:
        pin = input("PIN (4 dígitos): ").strip()
        if len(pin) == 4 and pin.isdigit():
            break
        else:
            print("Error: el PIN debe tener 4 números.")
            
    # Crea la estructura del nuevo usuario (formato que tendra en el json)
    datos_usuario = {
        "pin": pin,
        "cuentas": {}
    }
    datos_globales[usuario] = datos_usuario

    guardar_datos_globales(datos_globales)
    print(f"\nUsuario '{usuario}' creado exitosamente.")
    
    # Retorna el nombre y los datos para poder usarlo en crear_cuenta
    return usuario, datos_usuario

# 3 FUNCIONES DE GESTIÓN DE CUENTAS

def generar_iban(datos_globales):
    """Genera un IBAN de 3 dígitos único a través de TODOS los usuarios."""
    ibans_existentes = set()
    
    # Recorremos todas las cuentas de todos los usuarios para asegurar unicidad global
    for user_data in datos_globales.values():
        ibans_existentes.update(user_data["cuentas"].keys())
        
    while True:
        iban = str(random.randint(100, 999))
        if iban not in ibans_existentes:
            return iban

def crear_cuenta(datos_globales, usuario):
    print("\nCREAR NUEVA CUENTA")

    if usuario not in datos_globales:
        print("Error: usuario no válido.")
        return

    tipo = input("Tipo de cuenta (ahorros / corriente): ").strip().lower()
    if tipo not in ["ahorros", "corriente"]:
        print("Tipo de cuenta no válido.")
        return

    iban = generar_iban(datos_globales)

    datos_globales[usuario]["cuentas"][iban] = {
        "tipo": tipo,
        "saldo": 0.00
    }

    guardar_datos_globales(datos_globales)
    print(f"\nCuenta '{tipo}' creada correctamente con IBAN {iban}")




# -----------------------------------
# Inicio de sesión
# -----------------------------------

def cargar_usuarios(ruta_archivo="./usuarios.json"):
    """Carga la lista de usuarios desde un archivo JSON."""
    try:
        with open(ruta_archivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró el archivo usuarios.json")
        return []
    except json.JSONDecodeError:
        print("Error: El archivo usuarios.json tiene un formato incorrecto.")
        return []


def autenticar_usuario():
    """Valida usuario y PIN leyendo el archivo usuarios.json con máximo 3 intentos."""
    intentos = 3

    # Cargar usuarios desde el archivo JSON
    try:
        with open("usuarios.json", "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("Error: El archivo usuarios.json no existe.")
        return False
    except json.JSONDecodeError:
        print("Error: El archivo usuarios.json no tiene un formato válido.")
        return False

    while intentos > 0:
        usuario_input = input("Introduce tu nombre de usuario: ").strip()
        pin_input = input("Introduce tu PIN: ").strip()

        # Comprobar si el usuario existe
        if usuario_input not in usuarios:
            print("El usuario no existe.")
        else:
            # Obtener datos del usuario
            datos_usuario = usuarios[usuario_input]

            if datos_usuario["pin"] == pin_input:
                print("Acceso concedido.")
                # Devuelve también el nombre
                return usuario_input, datos_usuario
            else:
                print("PIN incorrecto.")

        intentos -= 1
        print(f"Intentos restantes: {intentos}")

    print("Demasiados intentos fallidos. Acceso bloqueado.")
    return False

# -----------------------------------
# Menú OPERACIONES
# -----------------------------------
def menu_operaciones(usuario, datos):
    while True:
        print(f"\n=== MENÚ DE OPERACIONES ({usuario}) ===")
        print("1. Consultar saldo")
        print("2. Ingresar dinero")
        print("3. Retirar dinero")
        print("4. Transferir dinero")
        print("5. Cerrar sesión")
        print("6. Crear cuenta")
        datos_globales = cargar_datos_globales()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            consultar_saldo(datos_globales[usuario])

        elif opcion == "2":
            ingresar_dinero(usuario)

        elif opcion == "3":
            retirar_dinero(usuario)

        elif opcion == "4":
            transferir(usuario)

        elif opcion == "5":
            print("Cerrando sesión...")
            break

        elif opcion == "6":
            crear_cuenta(datos_globales, usuario)


        else:
            print("Opción no válida.")


# -----------------------------------
# Selección de cuenta
# -----------------------------------

def seleccionar_cuenta(datos):
    cuentas = datos["cuentas"]

    if not cuentas:
        print("No tienes cuentas.")
        return None

    print("\nCuentas disponibles:")
    for num in cuentas:
        print(f"- {num}")

    cuenta = input("Selecciona una cuenta: ")

    if cuenta not in cuentas:
        print("Cuenta no válida.")
        return None

    return cuenta



# -----------------------------------
# Operaciones bancarias
# -----------------------------------

def consultar_saldo(datos_usuario):
    """Muestra el saldo de las cuentas del usuario actual."""
    cuentas = datos_usuario.get("cuentas", {})
    if not cuentas:
        print("\n[!] No tienes cuentas registradas.")
        return

    print("ESTADO DE TUS CUENTAS")
    for iban, info in cuentas.items():
        print(f"IBAN: {iban} | Tipo: {info['tipo'].upper()} | Saldo: €{info['saldo']:.2f}")

def validarCifra(cifra, datos, boolValidarRetiro):#Validará tanto si se ha introducido un numero y coherente y si tiene saldo para operaciones de retiro 
    try:
        if (datos["saldo"] < Decimal(cifra) and boolValidarRetiro) or Decimal(cifra)<= 0 or Decimal(cifra).as_tuple().exponent < -2 :#si no tiene fondos en caso de querer validarlo o si ha dado una cifra negativa
            #Siempre se compararán los fondos con la cifra indicada cuando boolRetiro sea true en caso contrario aunque la cifra introducida sea mayor que los fondos se skipeará este if, dado que se entiende que para ingresar no se necesita esa comprobacion
            if Decimal(cifra)<= 0 or Decimal(cifra).as_tuple().exponent < -2:
                print(f"ERROR: Valor incorrecto para la cifra {Decimal(cifra)} exponentes: {Decimal(cifra).as_tuple().exponent}")
                
            else:
                print("ERROR: Usted no dispone de saldo suficiente, por favor consulte su saldo")
            return False
        else:
            return True
    except: #en caso de que no sea un numero
        print("ERROR: Valor incorrecto para la cifra")
        return False

def ingresar_dinero(usuario):
    datos=cargar_datos_globales()
    datosUsuarioDict=datos[usuario]
    cuentaSeleccionada=""
    importe_a_ingresar=""

    if(not datosUsuarioDict['cuentas']):#verificar que tenga alguna cuenta
        print("Usted no dispone de cuenta alguna")
        return False
    
    #MOSTRANDO CUENTAS DE USUARIO
    keysCuentasDeUsuario=datosUsuarioDict["cuentas"].keys()
    print("\n|||CUENTA|||")
    print("de las siguientes cuentas:\n")
    #[print(f"{cuenta},\n") for cuenta in list(cuentasDeUsuario.keys]
    for cuenta in keysCuentasDeUsuario:
        
        print("||---||")
        print(f"||{cuenta}|| SALDO: {datosUsuarioDict['cuentas'][str(cuenta)]['saldo']}€")
        print("||---||\n")

    #SELECCION CUENTA
    while(True):
        cuentaSeleccionada=input("seleccione en cual desea ingresar (q para cancelar): ")
        if cuentaSeleccionada.lower()=="q":return False#Salida de metodo
        if cuentaSeleccionada in keysCuentasDeUsuario:break
        print("ERROR: La cuenta introducida no coincide con ninguna de tus cuentas.")

    #OBTENIENDO IMPORTA A INGRESAR
    print("\n|||IMPORTE|||")
    while(True):
        importe_a_ingresar=input(f"introduzca el importe que desea ingresar en su cuenta {cuentaSeleccionada} (q para cancelar): ")
        if importe_a_ingresar.lower()=="q":return False #Salida de metodo
        if(validarCifra(importe_a_ingresar, datosUsuarioDict['cuentas'][cuentaSeleccionada],False)):
            importe_a_ingresar = Decimal(importe_a_ingresar).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            break
    
    #MOSTRANDO Y CONFIRMANDO DATOS DE OPERACION
    print("\n|||CONFIRMACION|||")
    print(f"usted va a realizar un ingreso de {importe_a_ingresar}€ a su cuenta {cuentaSeleccionada}")
    while(True):
        confirmacion=input("¿DESEA CONFIRMAR ESTA OPERACION?, confirmar/denegar: ").lower().strip()
        if confirmacion=="confirmar":break
        if confirmacion=="denegar":return False#Salida de metodo
        print("ERROR: Introduzca confirmar o denegar")
    
    print("Realizando ingreso....")
    time.sleep(3)
    datos[usuario]['cuentas'][cuentaSeleccionada]['saldo']+=float(importe_a_ingresar)
    guardar_datos_globales(datos)
    print("Ingreso realizado, si desea ver su saldo restante consultelo con la operacion consultar saldo.")
    return True

def retirar_dinero(usuario):
    datos=cargar_datos_globales()
    datosUsuarioDict=datos[usuario]
    cuentaSeleccionada=""
    importe_a_sacar=""

    if(not datosUsuarioDict['cuentas']):#verificar que tenga alguna cuenta
        print("Usted no dispone de cuenta alguna")
        return False
    
    #MOSTRANDO CUENTAS DE USUARIO
    keysCuentasDeUsuario=datosUsuarioDict["cuentas"].keys()
    print("\n|||CUENTA|||")
    print("de las siguientes cuentas:\n")
    #[print(f"{cuenta},\n") for cuenta in list(cuentasDeUsuario.keys]
    for cuenta in keysCuentasDeUsuario:
        
        print("||---||")
        print(f"||{cuenta}|| SALDO: {datosUsuarioDict['cuentas'][str(cuenta)]['saldo']}€")
        print("||---||\n")

    #SELECCION CUENTA
    while(True):
        cuentaSeleccionada=input("seleccione desde que cuenta quiere retirar (q para cancelar): ")
        if cuentaSeleccionada.lower()=="q":return False#Salida de metodo
        if cuentaSeleccionada in keysCuentasDeUsuario:break
        print("ERROR: La cuenta introducida no coincide con ninguna de tus cuentas.")

    #OBTENIENDO IMPORTA A SACAR
    print("\n|||IMPORTE|||")
    while(True):
        importe_a_sacar=input(f"introduzca el importe que desea retirar de su cuenta {cuentaSeleccionada} (q para cancelar): ")
        if importe_a_sacar.lower()=="q":return False #Salida de metodo
        if(validarCifra(importe_a_sacar, datosUsuarioDict['cuentas'][cuentaSeleccionada], True)):
            importe_a_sacar=int(importe_a_sacar)
            break
    
    #MOSTRANDO Y CONFIRMANDO DATOS DE OPERACION
    print("\n|||CONFIRMACION|||")
    print(f"usted va a realizar una retirada de {importe_a_sacar}€ desde su cuenta {cuentaSeleccionada}")
    while(True):
        confirmacion=input("¿DESEA CONFIRMAR ESTA OPERACION?, confirmar/denegar: ").lower().strip()
        if confirmacion=="confirmar":break
        if confirmacion=="denegar":return False#Salida de metodo
        print("ERROR: Introduzca confirmar o denegar")
    
    print("Realizando retirada....")
    time.sleep(3)
    datos[usuario]['cuentas'][cuentaSeleccionada]['saldo']-=importe_a_sacar
    guardar_datos_globales(datos)
    return True


def transferir(usuario):
    #Retornará false si el usuario ha cancelado la operacion
    datos=cargar_datos_globales()
    UsuarioSesionActual=usuario

    #ORIGEN
    datosUsuario=datos[UsuarioSesionActual]
    cuentasUsuarioOrigen=dict(datosUsuario["cuentas"])
    cuentaOrigen=""#IBAN ORIGEN
    
    importe_a_transferir=0
    
    #DESTINO
    UsuarioDestino=""
    cuentaDestino=""#IBAN DESTINO
    
    
    if(not datosUsuario['cuentas']):#verificar que tenga alguna cuenta
        print("Usted no dispone de cuenta alguna")
        return False
    print("\n|||CUENTA ORIGEN|||")
    #MOSTRANDO CUENTAS DE ORIGEN
    keysCuentasDeUsuario=cuentasUsuarioOrigen.keys()
    print("de las siguientes cuentas:\n")
    #[print(f"{cuenta},\n") for cuenta in list(cuentasDeUsuario.keys]
    for cuenta in keysCuentasDeUsuario:
        
        print("||---||")
        print(f"||{cuenta}|| SALDO: {cuentasUsuarioOrigen[str(cuenta)]['saldo']}€")
        print("||---||\n")

    #SELECCION CUENTA ORIGEN
    while(True):
        cuentaOrigen=input("seleccione desde que cuenta quiere transferir (q para cancelar): ")
        if cuentaOrigen.lower()=="q":return False#Salida de metodo
        if cuentaOrigen in keysCuentasDeUsuario:break
        print("ERROR: La cuenta introducida no coincide con ninguna de tus cuentas.")
    
    print("\n|||IMPORTE|||")
    #OBTENIENDO IMPORTA A TRANSFERIR
    while(True):
        importe_a_transferir=input("introduzca el importe que desea transferir (q para cancelar): ")
        if importe_a_transferir.lower()=="q":return False #Salida de metodo
        if(validarCifra(importe_a_transferir, cuentasUsuarioOrigen[cuentaOrigen], True)):
            importe_a_transferir=int(importe_a_transferir)
            break
            
    
    print("\n|||CUENTA DESTINO|||")
    #OBTENIENDO CUENTA DESTINO
    while(True):
        cuentaInput=input("introduzca la cuenta a la que desea transferir (q para cancelar): ")
        if cuentaInput.lower()=="q":return False#Salida de metodo
        for usuario in list(datos.keys()):
            cuentasUsuarioDestino=list(dict(datos[usuario]["cuentas"]).keys())
            if cuentaInput in cuentasUsuarioDestino:
                cuentaDestino=cuentaInput
                UsuarioDestino=usuario
                break
        if(cuentaDestino):
            break
        print("ERROR: La cuenta introducida no coincide con ninguna de las cuentas registradas")
    print("\n|||CONFIRMACION|||")
    #MOSTRANDO Y CONFIRMANDO DATOS DE OPERACION
    print(f"usted va a realizar una transferencia de {importe_a_transferir}€ desde su cuenta {cuentaOrigen} a la cuenta destino {cuentaDestino} del destinatario {UsuarioDestino}")
    while(True):
        confirmacion=input("¿DESEA CONFIRMAR ESTA OPERACION?, confirmar/denegar: ").lower().strip()
        if confirmacion=="confirmar":break
        if confirmacion=="denegar":return False#Salida de metodo
        print("ERROR: Introduzca confirmar o denegar")
    
    print("Realizando transferencia....")
    time.sleep(3)

    datos[UsuarioSesionActual]['cuentas'][cuentaOrigen]['saldo']-=importe_a_transferir
    datos[UsuarioDestino]['cuentas'][cuentaDestino]['saldo']+=importe_a_transferir
    print("Transferencia realizada, si desea ver su saldo restante consultelo con la operacion consultar saldo.")
    guardar_datos_globales(datos)
    return True

if __name__=="__main__":
    
    #retirar_dinero("ruben")
    #INGRESAR
    datos={
                "tipo": "corriente",
                "saldo": 1
    }
    assert validarCifra("2", datos, False)==True,"No debe validar fondos menor que cifra"
    assert validarCifra("2.4", datos, False)==True,"No debe validar fondos menor que cifra"
    assert validarCifra("0", datos, False)==False,"No esta validando cifra a 0"
    assert validarCifra("-1", datos, False)==False,"No esta validando cifra a -1"
    assert validarCifra("-1.3", datos, False)==False,"No esta validando cifra a -1"
    assert validarCifra("0", datos, False)==False,"Debe validar cifra a numero"
    assert validarCifra("-1", datos, False)==False,"Debe validar cifra a numero"
    assert validarCifra("-1.6", datos, False)==False,"Debe validar cifra a numero"
    assert validarCifra("2", datos, False)==True,"Debe validar cifra a numero"
    assert validarCifra("2.4", datos, False)==True,"Debe validar cifra a numero"
    assert validarCifra("uno", datos, False)==False,"Debe validar cifra a numero"

    #RETIRAR
    assert validarCifra("2", datos, True)==False,"debe validar fondos menor que cifra"
    assert validarCifra("1", datos, True)==True,"tiene que dar True"
    assert validarCifra("0", datos, True)==False,"No esta validando cifra a 0"
    assert validarCifra("-1", datos, True)==False,"No esta validando cifra a -1"
    assert validarCifra("-1", datos, True)==False,"No esta validando cifra a -1"
    assert validarCifra("0", datos, True)==False,"Debe validar cifra a numero"
    assert validarCifra("-1", datos, True)==False,"Debe validar cifra a numero"
    assert validarCifra("-1.5", datos, True)==False,"Debe validar cifra a numero"
    assert validarCifra("1", datos, True)==True,"Debe validar cifra a numero"
    assert validarCifra("0.50", datos, True)==True,"Debe validar cifra a numero"
    assert validarCifra("0.500", datos, True)==False,"Debe validar cifra a numero"
    assert validarCifra("-0.50", datos, True)==False,"Debe validar cifra a numero"
    assert validarCifra("-0.500", datos, True)==False,"Debe validar cifra a numero"
    assert validarCifra("1.3", datos, True)==False,"Debe validar cifra a numero"
    assert validarCifra("2", datos, True)==False,"Debe validar cifra a numero"
    assert validarCifra("2.3", datos, True)==False,"Debe validar cifra a numero"
    assert validarCifra("uno", datos, True)==False,"Debe validar cifra a numero"
    print("TODO OK")