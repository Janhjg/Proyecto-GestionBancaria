import json

def cargar_usuarios():
    with open("usuarios.json", "r") as archivo:
        return json.load(archivo)

def guardar_usuarios(usuarios):
    with open("usuarios.json", "w") as archivo:
        json.dump(usuarios, archivo, indent=4)

def crear_usuario(usuarios):
    print("CREAR NUEVO USUARIO")
    
    while True:
        nuevo = input("Nuevo nombre de usuario: ").strip()
        if not nuevo:
            print("Error: el nombre no puede estar vacío.")
            continue
        if nuevo in usuarios:
            print("Error: ese usuario ya existe. Intenta con otro nombre.")
            continue
        
        pin = input("PIN (4 dígitos): ").strip()
        if len(pin) != 4:
            print("Error: el PIN debe tener exactamente 4 dígitos.")
            continue

        usuarios[nuevo] = {"pin": pin, "saldo": 0}
        guardar_usuarios(usuarios)
        print(f"Usuario '{nuevo}' creado exitosamente.")
        break

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
