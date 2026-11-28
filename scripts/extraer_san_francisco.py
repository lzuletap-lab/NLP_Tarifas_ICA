"""Extrae y evalúa las tablas de San Francisco, sin OCR."""

import csv
import json
from pathlib import Path

from nlp_tarifas_ica.extraccion_san_francisco import extraer_tabla_san_francisco
from nlp_tarifas_ica.exportacion import exportar_csv, exportar_json
from nlp_tarifas_ica.validacion import evaluar_extraccion


def main():
    base = Path(__file__).resolve().parents[1]
    archivos = [
        p for p in (base / "data/raw").iterdir()
        if "San Francisco" in p.name and p.suffix.lower() == ".pdf"
    ]
    if len(archivos) != 1:
        raise ValueError("Debe existir un único PDF de San Francisco.")

    pdf = archivos[0]
    paginas = [46, 47, 48, 49]
    referencia = []

    for nombre in (
        "referencia_san_francisco_p46_47.csv",
        "referencia_san_francisco_p48.csv",
        "referencia_san_francisco_p49.csv",
    ):
        with (base / "data/referencia" / nombre).open(
            encoding="utf-8-sig", newline=""
        ) as archivo:
            referencia.extend(csv.DictReader(archivo))

    if {r["archivo"] for r in referencia} != {pdf.name}:
        raise ValueError("El PDF no coincide con el de las referencias.")

    candidatos = extraer_tabla_san_francisco(pdf, paginas=paginas)
    if not candidatos:
        raise RuntimeError("No se extrajeron registros.")

    resultado = evaluar_extraccion(
        referencia,
        candidatos,
        paginas_evaluadas=[(pdf.name, p) for p in paginas],
        campos_codigo=("codigo_fuente",),
    )

    salida = base / "data/processed"
    salida.mkdir(parents=True, exist_ok=True)
    exportar_csv(
        candidatos, salida / "candidatos_san_francisco_p46_49.csv"
    )
    exportar_json(
        candidatos, salida / "candidatos_san_francisco_p46_49.json"
    )
    exportar_json(
        resultado, salida / "evaluacion_san_francisco_p46_49.json"
    )

    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    print("Salidas guardadas en:", salida)
    print("Evaluación de desarrollo; las descripciones no se evalúan.")


if __name__ == "__main__":
    main()
