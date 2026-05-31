import json

CAMPOS = [
    "id", "key", "especie", "risco", "risco_class",
    "latitude", "longitude", "emoji", "ameaca_pct",
]

def carregar():
    with open("data/sereias.json", encoding="utf-8") as f:
        return json.load(f)

def test_campos_obrigatorios():
    for s in carregar():
        for campo in CAMPOS:
            assert campo in s, f"{s['especie']} sem o campo '{campo}'"

def test_risco_valido():
    for s in carregar():
        assert s["risco"] in ("alto", "medio", "baixo")

def test_coordenadas_validas():
    for s in carregar():
        assert -90  <= s["latitude"]  <= 90
        assert -180 <= s["longitude"] <= 180

def test_keys_unicas():
    keys = [s["key"] for s in carregar()]
    assert len(keys) == len(set(keys))
