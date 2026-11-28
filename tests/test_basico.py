"""Pruebas unitarias basicas."""
from nlp_tarifas_ica.normalizacion import normalizar_texto
from nlp_tarifas_ica.validacion import evaluar_extraccion

def test_normalizar_texto():
    assert normalizar_texto("ARTÍCULO 25.\r\nTarifa:\u00a0 7,5 por mil") == "ARTÍCULO 25.\nTarifa: 7,5 por mil"

def test_evaluar_extraccion():
    ref = [{"archivo": "a.pdf", "pagina": "1", "codigo_actividad": "101", "ciiu": "1011", "tarifa": "5", "unidad": "por_mil"}]
    cand = [{"archivo": "a.pdf", "pagina": 1, "codigo_actividad": "101", "ciiu": "1011", "tarifa_candidata": "5", "unidad_candidata": "por_mil"}]
    res = evaluar_extraccion(ref, cand, paginas_evaluadas=[("a.pdf", 1)])
    assert res["verdaderos_positivos"] == 1 and res["f1"] == 1.0
