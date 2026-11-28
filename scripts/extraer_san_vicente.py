"""Extrae candidatos de las páginas PDF 38 a 54, sin OCR."""

from collections import Counter
from pathlib import Path

from nlp_tarifas_ica.extraccion_tablas import extraer_tabla_san_vicente
from nlp_tarifas_ica.exportacion import exportar_csv, exportar_json


def main():
    base = Path(__file__).resolve().parents[1]
    archivos = [
        p for p in (base / "data/raw").iterdir()
        if "San Vicente Ferrer" in p.name
        and p.suffix.lower() == ".pdf"
    ]
    if len(archivos) != 1:
        raise ValueError("Debe existir un único PDF de San Vicente Ferrer.")

    paginas = list(range(38, 55))
    registros = extraer_tabla_san_vicente(
        archivos[0], paginas=paginas
    )

    if not registros:
        raise RuntimeError("No se extrajeron registros.")

    salida = base / "data/processed"
    salida.mkdir(parents=True, exist_ok=True)

    exportar_json(
        registros, salida / "candidatos_san_vicente_p38_54.json"
    )
    exportar_csv(
        registros, salida / "candidatos_san_vicente_p38_54.csv"
    )

    resumen = []
    for pagina in paginas:
        filas = [r for r in registros if r["pagina"] == pagina]
        dato = {
            "pagina": pagina,
            "candidatos": len(filas),
            "sin_tarifa": sum(
                r["tarifa_candidata"] is None for r in filas
            ),
            "descripcion_vacia": sum(
                not r["descripcion"].strip() for r in filas
            ),
        }
        resumen.append(dato)
        print(dato)

    claves = Counter(
        (r["pagina"], r["codigo_fuente"]) for r in registros
    )
    duplicados = [
        {"pagina": p, "codigo_fuente": c, "cantidad": n}
        for (p, c), n in claves.items()
        if n > 1
    ]

    exportar_json(
        {
            "archivo": archivos[0].name,
            "estado": "pendiente_revision",
            "total_candidatos": len(registros),
            "resumen_paginas": resumen,
            "duplicados_por_pagina": duplicados,
        },
        salida / "resumen_san_vicente_p38_54.json",
    )

    print("\nTotal de candidatos:", len(registros))
    print("Duplicados por página:", duplicados)
    print("Salidas guardadas en:", salida)


if __name__ == "__main__":
    main()
