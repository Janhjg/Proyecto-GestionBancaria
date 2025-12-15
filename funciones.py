import json
import random
import time

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


# datos = cargar_datos()

# crear_usuario(datos)
# crear_cuenta(datos)


#Operaciones bancarias

def consultar_saldo():
    pass

def ingresar_dinero():
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

def retirar_dinero():
    pass

def transferir(usuario):
#Retornará false si el usuario ha cancelado la operacion
    datos=cargar_datos()
    
    UsuarioSesionActual=usuario
    datosUsuario=datos[UsuarioSesionActual]
    cuentaOrigen=""#IBAN ORIGEN
    importe_a_transferir=0
    cuentaDestino=""#IBAN DESTINO
    UsuarioDestino=""
    
    if(not datosUsuario["cuentas"]):#verificar que tenga alguna cuenta
        print("Usted no dispone de cuenta alguna")
        return False
    
    #MOSTRANDO CUENTAS DE ORIGEN
    #muestra el saldo de cada uno
    cuentasDeUsuario=list(dict(datosUsuario["cuentas"]).keys())
    print("de las siguientes cuentas:\n")
    #[print(f"{cuenta},\n") for cuenta in list(cuentasDeUsuario.keys]
    for cuenta in cuentasDeUsuario:
        print("||---||")
        print(f"||{cuenta}||")
        print("||---||\n")

    #SELECCION CUENTA ORIGEN
    while(True):
        cuentaOrigen=input("seleccione desde que cuenta quiere transferir (q para cancelar): ")
        if cuentaOrigen.lower()=="q":return False#Salida de metodo
        if cuentaOrigen in cuentasDeUsuario:break
        print("ERROR: La cuenta introducida no coincide con ninguna de tus cuentas.")
    

    #OBTENIENDO IMPORTA A TRANSFERIR
    while(True):
        importe_a_transferir=input("introduzca el importe que desea transferir (q para cancelar): ")
        if importe_a_transferir.lower()=="q":return False #Salida de metodo
        if(validarCifra(importe_a_transferir, datosUsuario["cuentas"][cuentaOrigen])):
            importe_a_transferir=int(importe_a_transferir)
            break
            
    
            
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

    #MOSTRANDO Y CONFIRMANDO DATOS DE OPERACION
    print(f"usted va a realizar una transferencia de {importe_a_transferir}€ desde su cuenta {cuentaOrigen} a la cuenta destino {cuentaDestino} del usuario {UsuarioDestino}")
    while(True):
        confirmacion=input("¿DESEA CONFIRMAR ESTA OPERACION?, confirmar/denegar: ").lower().strip()
        if confirmacion=="confirmar":break
        if confirmacion=="denegar":return False#Salida de metodo
        print("ERROR: Introduzca confirmar o denegar")
    
    print("Realizando transferencia....")
    time.sleep(3)

    datosUsuario["cuentas"][cuentaOrigen]["saldo"]-=importe_a_transferir
    datos[UsuarioDestino]["cuentas"][cuentaDestino]["saldo"]+=importe_a_transferir
    print("Transferencia realizada, si desea ver su saldo restante consultelo con la operacion consultar saldo.")
    guardar_datos(datos)
    
        

if __name__=="__main__":
    transferir("ruben")
    # print(prueba.values().mapping.)
