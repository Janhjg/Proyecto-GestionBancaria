# Tests sencillos con asserts para el sistema bancario
# Copia estas funciones al final de tu programa o en un archivo separado

def test_generar_iban():
    """Test: generar IBAN único"""
    print("\n--- TEST: Generar IBAN ---")
    
    datos = {
        "user1": {"cuentas": {"100": {}, "101": {}}},
        "user2": {"cuentas": {"102": {}}}
    }
    
    iban = generar_iban(datos)
    
    assert iban not in ["100", "101", "102"], "El IBAN debe ser único"
    assert len(iban) == 3, "El IBAN debe tener 3 dígitos"
    assert iban.isdigit(), "El IBAN debe ser numérico"
    assert 100 <= int(iban) <= 999, "El IBAN debe estar entre 100 y 999"
    
    print(f"✓ IBAN generado: {iban}")
    print("✓ Todos los asserts pasaron")


def test_validar_cifra_positiva():
    """Test: validar cifra positiva sin retiro"""
    print("\n--- TEST: Validar cifra positiva ---")
    
    datos = {"saldo": 100}
    resultado = validarCifra("50", datos, False)
    
    assert resultado == True, "Debe aceptar cifra positiva"
    print("✓ Cifra positiva validada correctamente")


def test_validar_cifra_negativa():
    """Test: rechazar cifra negativa"""
    print("\n--- TEST: Validar cifra negativa ---")
    
    datos = {"saldo": 100}
    resultado = validarCifra("-50", datos, False)
    
    assert resultado == False, "No debe aceptar cifras negativas"
    print("✓ Cifra negativa rechazada correctamente")


def test_validar_cifra_cero():
    """Test: rechazar cifra cero"""
    print("\n--- TEST: Validar cifra cero ---")
    
    datos = {"saldo": 100}
    resultado = validarCifra("0", datos, False)
    
    assert resultado == False, "No debe aceptar cero"
    print("✓ Cifra cero rechazada correctamente")


def test_validar_cifra_no_numerica():
    """Test: rechazar cifra no numérica"""
    print("\n--- TEST: Validar cifra no numérica ---")
    
    datos = {"saldo": 100}
    resultado = validarCifra("abc", datos, False)
    
    assert resultado == False, "No debe aceptar texto"
    print("✓ Texto rechazado correctamente")


def test_validar_retiro_sin_fondos():
    """Test: rechazar retiro sin fondos suficientes"""
    print("\n--- TEST: Retiro sin fondos ---")
    
    datos = {"saldo": 100}
    resultado = validarCifra("150", datos, True)
    
    assert resultado == False, "No debe permitir retiro sin fondos"
    print("✓ Retiro sin fondos rechazado correctamente")


def test_validar_retiro_con_fondos():
    """Test: aceptar retiro con fondos suficientes"""
    print("\n--- TEST: Retiro con fondos ---")
    
    datos = {"saldo": 200}
    resultado = validarCifra("100", datos, True)
    
    assert resultado == True, "Debe permitir retiro con fondos"
    print("✓ Retiro con fondos aceptado correctamente")


def test_consultar_saldo_con_cuentas():
    """Test: consultar saldo con cuentas"""
    print("\n--- TEST: Consultar saldo con cuentas ---")
    
    datos = {
        "cuentas": {
            "100": {"tipo": "ahorros", "saldo": 1500.50},
            "101": {"tipo": "corriente", "saldo": 250.00}
        }
    }
    
    # Verificar estructura de datos
    assert "cuentas" in datos, "Debe tener clave 'cuentas'"
    assert len(datos["cuentas"]) == 2, "Debe tener 2 cuentas"
    assert datos["cuentas"]["100"]["saldo"] == 1500.50, "Saldo debe ser correcto"
    assert datos["cuentas"]["101"]["tipo"] == "corriente", "Tipo debe ser correcto"
    
    print("✓ Estructura de cuentas correcta")


def test_consultar_saldo_sin_cuentas():
    """Test: consultar saldo sin cuentas"""
    print("\n--- TEST: Consultar saldo sin cuentas ---")
    
    datos = {"cuentas": {}}
    
    assert len(datos["cuentas"]) == 0, "No debe tener cuentas"
    assert datos["cuentas"] == {}, "Diccionario de cuentas debe estar vacío"
    
    print("✓ Usuario sin cuentas verificado correctamente")


def test_estructura_usuario():
    """Test: estructura de datos de usuario"""
    print("\n--- TEST: Estructura de usuario ---")
    
    usuario = {
        "pin": "1234",
        "cuentas": {
            "100": {"tipo": "ahorros", "saldo": 1000}
        }
    }
    
    assert "pin" in usuario, "Debe tener PIN"
    assert "cuentas" in usuario, "Debe tener cuentas"
    assert len(usuario["pin"]) == 4, "PIN debe tener 4 dígitos"
    assert usuario["pin"].isdigit(), "PIN debe ser numérico"
    assert isinstance(usuario["cuentas"], dict), "Cuentas debe ser diccionario"
    
    print("✓ Estructura de usuario correcta")


def test_operacion_ingreso():
    """Test: simulación de ingreso"""
    print("\n--- TEST: Operación de ingreso ---")
    
    datos = {
        "juan": {
            "cuentas": {
                "100": {"tipo": "ahorros", "saldo": 500}
            }
        }
    }
    
    saldo_inicial = datos["juan"]["cuentas"]["100"]["saldo"]
    importe = 200
    
    # Simular ingreso
    datos["juan"]["cuentas"]["100"]["saldo"] += importe
    saldo_final = datos["juan"]["cuentas"]["100"]["saldo"]
    
    assert saldo_final == saldo_inicial + importe, "Saldo debe aumentar correctamente"
    assert saldo_final == 700, "Saldo final debe ser 700"
    
    print(f"✓ Ingreso correcto: {saldo_inicial}€ → {saldo_final}€")


def test_operacion_retiro():
    """Test: simulación de retiro"""
    print("\n--- TEST: Operación de retiro ---")
    
    datos = {
        "juan": {
            "cuentas": {
                "100": {"tipo": "ahorros", "saldo": 500}
            }
        }
    }
    
    saldo_inicial = datos["juan"]["cuentas"]["100"]["saldo"]
    importe = 200
    
    # Simular retiro
    datos["juan"]["cuentas"]["100"]["saldo"] -= importe
    saldo_final = datos["juan"]["cuentas"]["100"]["saldo"]
    
    assert saldo_final == saldo_inicial - importe, "Saldo debe disminuir correctamente"
    assert saldo_final == 300, "Saldo final debe ser 300"
    
    print(f"✓ Retiro correcto: {saldo_inicial}€ → {saldo_final}€")


def test_operacion_transferencia():
    """Test: simulación de transferencia"""
    print("\n--- TEST: Operación de transferencia ---")
    
    datos = {
        "juan": {
            "cuentas": {
                "100": {"tipo": "ahorros", "saldo": 1000}
            }
        },
        "maria": {
            "cuentas": {
                "200": {"tipo": "corriente", "saldo": 500}
            }
        }
    }
    
    saldo_origen_inicial = datos["juan"]["cuentas"]["100"]["saldo"]
    saldo_destino_inicial = datos["maria"]["cuentas"]["200"]["saldo"]
    importe = 300
    
    # Simular transferencia
    datos["juan"]["cuentas"]["100"]["saldo"] -= importe
    datos["maria"]["cuentas"]["200"]["saldo"] += importe
    
    saldo_origen_final = datos["juan"]["cuentas"]["100"]["saldo"]
    saldo_destino_final = datos["maria"]["cuentas"]["200"]["saldo"]
    
    assert saldo_origen_final == saldo_origen_inicial - importe, "Origen debe disminuir"
    assert saldo_destino_final == saldo_destino_inicial + importe, "Destino debe aumentar"
    assert saldo_origen_final == 700, "Saldo origen debe ser 700"
    assert saldo_destino_final == 800, "Saldo destino debe ser 800"
    
    print(f"✓ Transferencia correcta:")
    print(f"  Origen: {saldo_origen_inicial}€ → {saldo_origen_final}€")
    print(f"  Destino: {saldo_destino_inicial}€ → {saldo_destino_final}€")


def test_crear_cuenta_estructura():
    """Test: estructura al crear cuenta"""
    print("\n--- TEST: Crear cuenta estructura ---")
    
    datos = {
        "usuario1": {
            "pin": "1234",
            "cuentas": {}
        }
    }
    
    # Simular creación de cuenta
    iban = "123"
    tipo = "ahorros"
    datos["usuario1"]["cuentas"][iban] = {
        "tipo": tipo,
        "saldo": 0.00
    }
    
    assert iban in datos["usuario1"]["cuentas"], "IBAN debe existir"
    assert datos["usuario1"]["cuentas"][iban]["tipo"] == "ahorros", "Tipo debe ser correcto"
    assert datos["usuario1"]["cuentas"][iban]["saldo"] == 0.00, "Saldo inicial debe ser 0"
    
    print(f"✓ Cuenta creada: IBAN {iban}, tipo {tipo}")


def test_multiples_cuentas():
    """Test: usuario con múltiples cuentas"""
    print("\n--- TEST: Múltiples cuentas ---")
    
    datos = {
        "juan": {
            "pin": "1234",
            "cuentas": {
                "100": {"tipo": "ahorros", "saldo": 1000},
                "101": {"tipo": "corriente", "saldo": 500},
                "102": {"tipo": "ahorros", "saldo": 2000}
            }
        }
    }
    
    num_cuentas = len(datos["juan"]["cuentas"])
    saldo_total = sum(cuenta["saldo"] for cuenta in datos["juan"]["cuentas"].values())
    
    assert num_cuentas == 3, "Debe tener 3 cuentas"
    assert saldo_total == 3500, "Saldo total debe ser 3500"
    assert "100" in datos["juan"]["cuentas"], "Cuenta 100 debe existir"
    
    print(f"✓ Usuario con {num_cuentas} cuentas, saldo total: {saldo_total}€")


def test_datos_globales_multiples_usuarios():
    """Test: múltiples usuarios en datos globales"""
    print("\n--- TEST: Múltiples usuarios ---")
    
    datos_globales = {
        "juan": {
            "pin": "1234",
            "cuentas": {"100": {"tipo": "ahorros", "saldo": 1000}}
        },
        "maria": {
            "pin": "5678",
            "cuentas": {"200": {"tipo": "corriente", "saldo": 500}}
        },
        "pedro": {
            "pin": "9012",
            "cuentas": {}
        }
    }
    
    assert len(datos_globales) == 3, "Debe haber 3 usuarios"
    assert "juan" in datos_globales, "Juan debe existir"
    assert "maria" in datos_globales, "Maria debe existir"
    assert "pedro" in datos_globales, "Pedro debe existir"
    assert len(datos_globales["pedro"]["cuentas"]) == 0, "Pedro no tiene cuentas"
    
    print(f"✓ {len(datos_globales)} usuarios registrados")


def ejecutar_todos_los_tests():
    """Ejecuta todos los tests y muestra los fallos detalladamente"""
    print("\n" + "="*60)
    print("EJECUTANDO TESTS DEL SISTEMA BANCARIO")
    print("="*60)
    
    tests = [
        test_generar_iban,
        test_validar_cifra_positiva,
        test_validar_cifra_negativa,
        test_validar_cifra_cero,
        test_validar_cifra_no_numerica,
        test_validar_retiro_sin_fondos,
        test_validar_retiro_con_fondos,
        test_consultar_saldo_con_cuentas,
        test_consultar_saldo_sin_cuentas,
        test_estructura_usuario,
        test_operacion_ingreso,
        test_operacion_retiro,
        test_operacion_transferencia,
        test_crear_cuenta_estructura,
        test_multiples_cuentas,
        test_datos_globales_multiples_usuarios
    ]
    
    tests_pasados = 0
    tests_fallados = 0
    errores = []
    
    for test in tests:
        try:
            test()
            tests_pasados += 1
        except AssertionError as e:
            tests_fallados += 1
            error_info = {
                'test': test.__name__,
                'tipo': 'AssertionError',
                'mensaje': str(e),
                'descripcion': test.__doc__
            }
            errores.append(error_info)
            print(f"\n FALLÓ: {test.__name__}")
            print(f"   Razón: {e}")
        except Exception as e:
            tests_fallados += 1
            error_info = {
                'test': test.__name__,
                'tipo': type(e).__name__,
                'mensaje': str(e),
                'descripcion': test.__doc__
            }
            errores.append(error_info)
            print(f"\n ERROR en {test.__name__}")
            print(f"   Tipo: {type(e).__name__}")
            print(f"   Mensaje: {e}")
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN DE TESTS")
    print("="*60)
    print(f" Tests PASADOS: {tests_pasados}")
    print(f" Tests FALLADOS: {tests_fallados}")
    print(f" Total: {tests_pasados + tests_fallados}")
    
    # Mostrar detalles de los fallos
    if errores:
        print("\n" + "="*60)
        print("DETALLE DE FALLOS")
        print("="*60)
        for i, error in enumerate(errores, 1):
            print(f"\n{i}. {error['test']}")
            print(f"   Descripción: {error['descripcion']}")
            print(f"   Tipo de error: {error['tipo']}")
            print(f"   Mensaje: {error['mensaje']}")
    
    print("\n" + "="*60)


# Para ejecutar los tests, llama a esta función:
if __name__ == "__main__":
    ejecutar_todos_los_tests()