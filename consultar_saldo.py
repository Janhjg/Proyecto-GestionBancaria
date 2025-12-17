from funciones import *

def consultar_saldo(datos_usuario):
    """Muestra el saldo de las cuentas del usuario actual."""
    cuentas = datos_usuario.get("cuentas", {})
    if not cuentas:
        print("\n[!] No tienes cuentas registradas.")
        return

    print("\n--- ESTADO DE TUS CUENTAS ---")
    for iban, info in cuentas.items():
        print(f"IBAN: {iban} | Tipo: {info['tipo'].upper()} | Saldo: €{info['saldo']:.2f}")
    