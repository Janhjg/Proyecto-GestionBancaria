import funciones
import os
import json

print("Ejecutando archivo:", os.path.abspath(__file__))
if __name__ == "__main__":
 
    while True:
        print("\n=== BANCO TERMINAL ===")
        print("1. Crear nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            datos_globales = funciones.cargar_datos_globales()

            print("INICIANDO PRUEBA DE CREACIÓN")

            # 1. Crear un nuevo usuario
            # La función retorna el nombre del nuevo usuario y sus datos
            nuevo_usuario_nombre, datos_del_usuario_creado = funciones.crear_usuario(datos_globales)

            
        elif opcion == "2":
            login = funciones.autenticar_usuario()
            if login:
                usuario, datos = login
                print(f"\nBienvenido, {usuario}!")
        elif opcion == "3":
            print("Saliendo de la aplicación...")
            exit()
        else:
            print("Opción no válida. Intenta de nuevo.")
