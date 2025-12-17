import json
import random

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

def consultar_saldo(datos_usuario):
    """Muestra el saldo de las cuentas del usuario actual."""
    cuentas = datos_usuario.get("cuentas", {})
    if not cuentas:
        print("\n[!] No tienes cuentas registradas.")
        return

    print("ESTADO DE TUS CUENTAS")
    for iban, info in cuentas.items():
        print(f"IBAN: {iban} | Tipo: {info['tipo'].upper()} | Saldo: €{info['saldo']:.2f}")

def ingresar_dinero(saldo):
    cantidad = int(input("Teclee la cantidad a ingresar: "))
    saldo = saldo + cantidad
    print(f"Has ingresado {cantidad} euros. Su nuevo saldo es: {saldo} euros.")
    return saldo

def retirar_dinero(saldo):
    cantidad = int(input("Teclee la cantidad a retirar: "))
    if cantidad > saldo:
        print("Fondos insuficientes")
    else:
        saldo -= cantidad
        print(f"Ha retirado {cantidad}, su saldo actual es: {saldo} euros.")
    return saldo


def transferir():
    pass
