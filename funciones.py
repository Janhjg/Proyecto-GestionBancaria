import json
import random

# -----------------------------------
# Cargar / Guardar datos
# -----------------------------------
def cargar_datos():
    try:
        with open("usuarios.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {
            "usuario": "",
            "pin": "",
            "cuentas": {}
        }

def guardar_datos(datos):
    with open("usuarios.json", "w") as archivo:
        json.dump(datos, archivo, indent=4)


# -----------------------------------
# Crear usuario principal
# -----------------------------------
def crear_usuario(datos):
    print("=== CREAR USUARIO PRINCIPAL ===")
    
    if datos["usuario"]:
        print(f"Ya existe un usuario registrado: {datos['usuario']}")
        return

    usuario = input("Nombre de usuario: ").strip()
    pin = input("PIN (4 dígitos): ").strip()

    if len(pin) != 4 or not pin.isdigit():
        print("Error: el PIN debe tener 4 números.")
        return

    datos["usuario"] = usuario
    datos["pin"] = pin
    datos["cuentas"] = {}

    guardar_datos(datos)
    print(f"Usuario '{usuario}' creado exitosamente.")


# -----------------------------------
# Generar IBAN único de 3 dígitos
# -----------------------------------
def generar_iban(datos):
    while True:
        iban = str(random.randint(100, 999))
        if iban not in datos["cuentas"]:
            return iban


# -----------------------------------
# Crear nueva cuenta bancaria
# -----------------------------------
def crear_cuenta(datos):
    print("=== CREAR NUEVA CUENTA ===")

    if not datos["usuario"]:
        print("Primero debes crear el usuario principal.")
        return

    tipo = input("Tipo de cuenta (ahorros / corriente): ").strip()
    if tipo not in ["ahorros", "corriente"]:
        print("Tipo de cuenta no válido.")
        return

    iban = generar_iban(datos)

    datos["cuentas"][iban] = {
        "tipo": tipo,
        "saldo": 0
    }

    guardar_datos(datos)
    print(f"Cuenta creada exitosamente con IBAN: {iban}")


datos = cargar_datos()

crear_usuario(datos)
crear_cuenta(datos)


#Operaciones bancarias

def consultar_saldo():
    saldo = 1000
    print(f"Su saldo actual es: {saldo} euros.")

def ingresar_dinero(n):
    saldo = saldo + n
    cantidad_ingreso = int(input("Teclee la cantidad a ingresar: "))
    saldo = int(saldo) + int(cantidad_ingreso)
    print(f"Has ingresado {cantidad_ingreso} euros. Su nuevo saldo es: {saldo} euros.") 

def retirar_dinero(n):
    saldo = saldo - n
    cantidad_retiro = input("Teclee la cantidad a retirar: ")
    if cantidad_retiro > saldo:
         print("Fondos insuficientes")
    else:
        saldo = saldo - cantidad_retiro
        print(f"Ha retirado {cantidad_retiro}, su saldo actual es de {saldo}")

def transferir():
    pass
