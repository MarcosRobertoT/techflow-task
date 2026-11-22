import pytest
from validacao import validar_titulo, validar_status


def test_titulo_valido_remove_espacos():
    assert validar_titulo("  Criar login  ") == "Criar login"


def test_titulo_vazio_gera_erro():
    with pytest.raises(ValueError):
        validar_titulo("   ")


def test_titulo_nao_texto_gera_erro():
    with pytest.raises(ValueError):
        validar_titulo(None)


def test_titulo_muito_longo_gera_erro():
    with pytest.raises(ValueError):
        validar_titulo("a" * 101)


def test_status_valido():
    assert validar_status("Em Progresso") == "Em Progresso"


def test_status_invalido_gera_erro():
    with pytest.raises(ValueError):
        validar_status("Feito")
