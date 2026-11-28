"""Extracción por lote y evaluación parcial de Santa Fe, sin OCR."""

import csv
import json
from collections import Counter
from pathlib import Path

from nlp_tarifas_ica.extraccion_santa_fe import extraer_tabla_santa_fe
from nlp_tarifas_ica.exportacion import exportar_csv, exportar_json
from nlp_tarifas_ica.validacion import evaluar_extraccion


def main():
    base = Path(__file__).resolve().parents[1]
    archivos = [
        p for p in (base / "data/raw").iterdir()
        if "Santa fe de Antioquia" in p.name
        and p.suffix.lower() == ".pdf"
    ]
    if len(archivos) != 1:
        raise ValueError("Debe existir un único PDF de Santa Fe de Antioquia.")

    pdf = archivos[0]
    referencia = []
    for pagina in (29, 30):
        ruta = base / f"data/referencia/referencia_santa_fe_p{pagina}.csv"
        with ruta.open(encoding="utf-8-sig", newline="") as archivo:
            referencia.extend(csv.DictReader(archivo))

    if {r["archivo"] for r in referencia} != {pdf.name}:
        raise ValueError("El PDF no coincide con las referencias.")

    candidatos = extraer_tabla_santa_fe(
        pdf, paginas=list(range(29, 45))
    )
    if not candidatos:
        raise RuntimeError("No se extrajeron registros.")

    resultado = evaluar_extraccion(
        referencia,
        candidatos,
        paginas_evaluadas=[(pdf.name, 29), (pdf.name, 30)],
        campos_codigo=("codigo_fuente",),
    )

    claves = Counter(
        (r["pagina"], r["codigo_fuente"]) for r in candidatos
    )
    resumen = {
        "archivo": pdf.name,
        "estado": "pendiente_revision",
        "total_candidatos": len(candidatos),
        "paginas": [
            {
                "pagina": pagina,
                "candidatos": sum(
                    r["pagina"] == pagina for r in candidatos
                ),
            }
            for pagina in range(29, 45)
        ],
        "sin_tarifa": sum(
            r["tarifa_candidata"] is None for r in candidatos
        ),
        "descripcion_vacia": sum(
            not r["descripcion"].strip() for r in candidatos
        ),
        "duplicados_por_pagina": [
            {"pagina": p, "codigo_fuente": c, "cantidad": n}
            for (p, c), n in claves.items() if n > 1
        ],
    }

    salida = base / "data/processed"
    salida.mkdir(parents=True, exist_ok=True)
    exportar_csv(candidatos, salida / "candidatos_santa_fe_p29_44.csv")
    exportar_json(candidatos, salida / "candidatos_santa_fe_p29_44.json")
    exportar_json(resumen, salida / "resumen_santa_fe_p29_44.json")
    exportar_json(resultado, salida / "evaluacion_santa_fe_p29_30.json")

    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    print("\nEVALUACIÓN DE DESARROLLO: SOLO PÁGINAS 29 Y 30")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    print("Las descripciones no se evalúan.")


if __name__ == "__main__":
    main()
