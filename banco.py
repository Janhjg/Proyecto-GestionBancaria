import funciones
import os

print("Ejecutando archivo:", os.path.abspath(__file__))
if __name__ == "__main__":
 
 while True:
        print("\n=== BANCO TERMINAL ===")
        print("1. Crear nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            # llamada a funciones de Jahn
            pass
        elif opcion == "2":
            user = funciones.autenticar_usuario()
            if user:
                print(f"\nBienvenido, {user['usuario']}!")
                    # Devuelves el usuario para pasar al menú principal de operaciones
        elif opcion == "3":
            print("Saliendo de la aplicación...")
            exit()
        else:
            print("Opción no válida. Intenta de nuevo.")
