import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pages.mapa import avistamentos_na_rota

def test_rota_encontra_avistamentos():
    # Santos → Lisboa: rota atlântica conhecida, deve ter avistamentos
    resultado = avistamentos_na_rota(-23.96, -46.33, 38.72, -9.14)
    assert len(resultado) > 0

def test_rota_remota_sem_avistamentos():
    # ponto isolado no Pacífico Sul, longe de tudo
    resultado = avistamentos_na_rota(-60.0, -160.0, -61.0, -161.0, corredor=2.0)
    assert resultado == []

def test_corredor_maior_retorna_mais():
    estreito = avistamentos_na_rota(-23.96, -46.33, 38.72, -9.14, corredor=3.0)
    largo    = avistamentos_na_rota(-23.96, -46.33, 38.72, -9.14, corredor=15.0)
    assert len(largo) >= len(estreito)
