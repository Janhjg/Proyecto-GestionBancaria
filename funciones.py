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

def crear_cuenta(datos_globales, datos_usuario):
    """Crea una cuenta para el usuario proporcionado."""
    print("\nCREAR NUEVA CUENTA")

    # Aseguramos que haya un usuario válido antes de continuar
    if datos_usuario is None:
        print("Error: Se requiere un objeto de usuario válido para crear una cuenta.")
        return

    tipo = input("Tipo de cuenta (ahorros / corriente): ").strip().lower()
    if tipo not in ["ahorros", "corriente"]:
        print("Tipo de cuenta no válido.")
        return

    # El IBAN se genera a nivel global
    iban = generar_iban(datos_globales) 

    # Agrega la cuenta al diccionario de cuentas del usuario actual
    datos_usuario["cuentas"][iban] = {
        "tipo": tipo,
        "saldo": 0.00
    }

    # Guardar la estructura global para que el cambio persista en usuarios.json
    guardar_datos_globales(datos_globales)
    print(f"\nCuenta de tipo '{tipo}' creada exitosamente con IBAN: {iban}")


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

        # Buscar usuario en el JSON
        usuario_encontrado = next(
            (u for u in usuarios if u.get("usuario") == usuario_input),
            None
        )

        if usuario_encontrado is None:
            print("El usuario no existe.")
        else:
            if usuario_encontrado.get("pin") == pin_input:
                print(f"Acceso concedido.")
                return usuario_encontrado
            else:
                print("PIN incorrecto.")

        intentos -= 1
        print(f"Intentos restantes: {intentos}")

    print("Demasiados intentos fallidos. Acceso bloqueado.")
    return False


#Operaciones bancarias

def consultar_saldo(saldo):
    print(f"Su saldo actual es: {saldo} euros.")
    return saldo

def ingresar_dinero(saldo):
    pass

def validarCifra(cifra, datos):#Validará tanto si se ha introducido un numero y coherente y si tiene saldo para operaciones de retiro 
    try:
        if datos["saldo"] >= int(cifra) > 0:
            return True
        elif int(cifra)<=0:
            print("ERROR: Valor incorrecto para la cifra")
            return False
        else:
            print("ERROR: Usted no dispone de saldo suficiente, por favor consulte su saldo")
            return False
    except: #en caso de que no sea un numero
        print("ERROR: Valor incorrecto para la cifra")
        return False
    
def retirar_dinero(usuario):
    datos=cargar_datos_globales()
    datosUsuario=datos[usuario]
    cuentasUsuario=datosUsuario["cuentas"]

    if(not datosUsuario['cuentas']):#verificar que tenga alguna cuenta
        print("Usted no dispone de cuenta alguna")
        return False
    
    #MOSTRANDO CUENTAS DE USUARIO
    keysCuentasDeUsuario=cuentasUsuario.keys()
    print("de las siguientes cuentas:\n")
    #[print(f"{cuenta},\n") for cuenta in list(cuentasDeUsuario.keys]
    for cuenta in keysCuentasDeUsuario:
        
        print("||---||")
        print(f"||{cuenta}|| SALDO: {cuentasUsuario[str(cuenta)]['saldo']}€")
        print("||---||\n")

    #SELECCION CUENTA
    while(True):
        cuentaSeleccionada=input("seleccione desde que cuenta quiere retirar (q para cancelar): ")
        if cuentaSeleccionada.lower()=="q":return False#Salida de metodo
        if cuentaSeleccionada in keysCuentasDeUsuario:break
        print("ERROR: La cuenta introducida no coincide con ninguna de tus cuentas.")

    #OBTENIENDO IMPORTA A SACAR
    while(True):
        importe_a_sacar=input(f"introduzca el importe que desea retirar de su cuenta {cuentaSeleccionada} (q para cancelar): ")
        if importe_a_sacar.lower()=="q":return False #Salida de metodo
        if(validarCifra(importe_a_sacar, cuentasUsuario[cuentaSeleccionada])):
            importe_a_sacar=int(importe_a_sacar)
            break
    
    #MOSTRANDO Y CONFIRMANDO DATOS DE OPERACION
    print(f"usted va a realizar una retirada de {importe_a_sacar}€ desde su cuenta {cuentaSeleccionada}")
    while(True):
        confirmacion=input("¿DESEA CONFIRMAR ESTA OPERACION?, confirmar/denegar: ").lower().strip()
        if confirmacion=="confirmar":break
        if confirmacion=="denegar":return False#Salida de metodo
        print("ERROR: Introduzca confirmar o denegar")
    
    print("Realizando retirada....")
    time.sleep(3)
    datosUsuario["cuentas"][cuentaSeleccionada]["saldo"]-=importe_a_sacar
    guardar_datos_globales(datos)
    return True

def transferir():
    pass

if __name__=="__main__":
    retirar_dinero("ruben")