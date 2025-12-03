import json

def cargar_usuarios():
    with open("usuarios.json", "r") as archivo:
        return json.load(archivo)

def guardar_usuarios(usuarios):
    with open("usuarios.json", "w") as archivo:
        json.dump(usuarios, archivo, indent=4)

def crear_usuario(usuarios):
    print("CREAR NUEVO USUARIO")
    
    nuevo = input("Nuevo nombre de usuario: ")

    if nuevo in usuarios:
        print("Ese usuario ya existe")
        return

    pin = input("PIN (4 dígitos): ")

    if len(pin) != 4:
        print("El PIN debe tener exactamente 4 caracteres.")
        return

    usuarios[nuevo] = {
        "pin": pin,
        "saldo": 0
    }

    guardar_usuarios(usuarios)

    print(f"Usuario {nuevo} creado exitosamente.")

usuarios = cargar_usuarios()
crear_usuario(usuarios)


#Operaciones bancarias

def consultar_saldo():
    pass

def ingresar_dinero():
    pass 

def retirar_dinero():
    pass

def transferir():
    pass
