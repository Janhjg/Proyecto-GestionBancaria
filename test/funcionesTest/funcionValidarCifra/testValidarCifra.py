from validarCifra import validarCifra
import pytest
datos={'saldo':4}
@pytest.mark.parametrize(
    "cifra, datos, boolRetiro, esperado",
    [
        (1, datos, False, True)
    ]
)
def test_validarCifra(cifra, datos, boolRetiro, esperado):
    assert validarCifra(cifra, datos, boolRetiro) == esperado
