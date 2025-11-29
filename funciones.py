#DEFINICIONES PARA LA GESTION DEL USUARIO

def crear_usuario():
    pass
    
def login(usuarios):
    print("INICIO DE SESIÓN")
    usuario = input("Usuario:")

    if usuario not in usuarios:
        print("Usuario no encontrado")
        return None

    pin = input("PIN: ")

    if pin != usuario[pin]:
        print("PIN incorrecto")
        return None

    print(f" Bienvenido {usuario}")
    return usuario


#Operaciones bancarias

def consultar_saldo():
    pass

def ingresar_dinero():
    pass 

def retirar_dinero():
    pass

def transferir():
    pass
