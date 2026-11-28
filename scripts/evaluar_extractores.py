"""Controles y evaluación provisional de cuatro extractores, sin OCR."""

import csv
import json
from collections import Counter
from pathlib import Path

from nlp_tarifas_ica.extraccion_tablas import (
    extraer_tabla_guayabetal,
    extraer_tabla_san_vicente,
)
from nlp_tarifas_ica.extraccion_san_francisco import extraer_tabla_san_francisco
from nlp_tarifas_ica.extraccion_santa_fe import extraer_tabla_santa_fe
from nlp_tarifas_ica.validacion import evaluar_extraccion


BASE = Path(__file__).resolve().parents[1]

CASOS = [
    (
        "Guayabetal", extraer_tabla_guayabetal, None,
        ["referencia_manual.csv"],
        ("codigo_actividad", "ciiu"), "descripcion_parcial",
    ),
    (
        "San Vicente Ferrer", extraer_tabla_san_vicente,
        list(range(38, 55)),
        [
            "referencia_san_vicente_p38.csv",
            "referencia_san_vicente_p39.csv",
            "referencia_san_vicente_p42.csv",
        ],
        ("codigo_fuente",), "descripcion",
    ),
    (
        "San Francisco", extraer_tabla_san_francisco,
        list(range(46, 50)),
        [
            "referencia_san_francisco_p46_47.csv",
            "referencia_san_francisco_p48.csv",
            "referencia_san_francisco_p49.csv",
        ],
        ("codigo_fuente",), "descripcion",
    ),
    (
        "Santa Fe de Antioquia", extraer_tabla_santa_fe,
        list(range(29, 45)),
        [
            "referencia_santa_fe_p29.csv",
            "referencia_santa_fe_p30.csv",
        ],
        ("codigo_fuente",), "descripcion",
    ),
]


def vacio(valor):
    return valor is None or not str(valor).strip()


def main():
    documentos = []

    for nombre, extractor, paginas, fuentes, codigos, descripcion in CASOS:
        referencia = []
        requeridos = {"archivo", "pagina", "tarifa", "unidad", *codigos}

        for fuente in fuentes:
            ruta = BASE / "data/referencia" / fuente
            with ruta.open(encoding="utf-8-sig", newline="") as archivo:
                lector = csv.DictReader(archivo)
                if not requeridos.issubset(lector.fieldnames or []):
                    raise ValueError(f"Columnas incompletas: {fuente}")
                filas = list(lector)

            if not filas or any(
                None in r
                or any(vacio(r.get(c)) for c in requeridos)
                for r in filas
            ):
                raise ValueError(f"Referencia incompleta: {fuente}")
            referencia.extend(filas)

        nombres = {r["archivo"] for r in referencia}
        if len(nombres) != 1:
            raise ValueError(f"{nombre}: referencias de varios PDF.")

        archivo_pdf = next(iter(nombres))
        if Path(archivo_pdf).name != archivo_pdf:
            raise ValueError("Nombre de PDF inválido.")

        pdf = BASE / "data/raw" / archivo_pdf
        if not pdf.is_file():
            raise FileNotFoundError(pdf)

        def clave(r):
            return (
                r["archivo"], int(r["pagina"]),
                *(str(r[c]).strip() for c in codigos),
            )

        claves_ref = [clave(r) for r in referencia]
        if len(claves_ref) != len(set(claves_ref)):
            raise ValueError(f"{nombre}: referencias duplicadas.")

        alcance = sorted({
            (r["archivo"], int(r["pagina"])) for r in referencia
        })
        if paginas is not None and any(
            p not in paginas for _, p in alcance
        ):
            raise ValueError(f"{nombre}: referencia fuera del lote.")

        candidatos = (
            extractor(pdf)
            if paginas is None
            else extractor(pdf, paginas=paginas)
        )
        if not candidatos:
            raise RuntimeError(f"{nombre}: no se extrajeron candidatos.")

        for r in candidatos:
            for campo in (
                "archivo", "pagina", descripcion,
                "tarifa_candidata", "unidad_candidata", *codigos,
            ):
                if campo not in r:
                    raise ValueError(f"{nombre}: falta {campo}.")
            if r["archivo"] != archivo_pdf:
                raise ValueError(f"{nombre}: archivo inesperado.")
            if paginas is not None and int(r["pagina"]) not in paginas:
                raise ValueError(f"{nombre}: candidato fuera del lote.")

        frecuencias = Counter(clave(r) for r in candidatos)
        duplicados = [
            {
                "archivo": k[0],
                "pagina": k[1],
                "codigos": dict(zip(codigos, k[2:])),
                "cantidad": cantidad,
            }
            for k, cantidad in sorted(frecuencias.items())
            if cantidad > 1
        ]

        por_pagina = []
        for pagina in sorted({int(r["pagina"]) for r in candidatos}):
            filas = [r for r in candidatos if int(r["pagina"]) == pagina]
            por_pagina.append({
                "pagina": pagina,
                "candidatos": len(filas),
                "sin_tarifa": sum(
                    vacio(r["tarifa_candidata"]) for r in filas
                ),
                "descripcion_vacia": sum(
                    vacio(r[descripcion]) for r in filas
                ),
            })

        metricas = evaluar_extraccion(
            referencia,
            candidatos,
            paginas_evaluadas=alcance,
            campos_codigo=codigos,
        )
        documento = {
            "documento": nombre,
            "archivo": archivo_pdf,
            "referencias": fuentes,
            "referencias_sin_revisor": sum(
                vacio(r.get("revisor")) for r in referencia
            ),
            "total_candidatos": len(candidatos),
            "sin_tarifa": sum(
                vacio(r["tarifa_candidata"]) for r in candidatos
            ),
            "descripciones_vacias": sum(
                vacio(r[descripcion]) for r in candidatos
            ),
            "duplicados_adicionales": sum(
                r["cantidad"] - 1 for r in duplicados
            ),
            "duplicados": duplicados,
            "paginas": por_pagina,
            "evaluacion": metricas,
        }
        documentos.append(documento)

        print(f"\n{nombre}")
        for campo in (
            "total_candidatos", "sin_tarifa",
            "descripciones_vacias", "duplicados_adicionales",
        ):
            print(f"{campo}: {documento[campo]}")
        print(
            "VP / FP / FN:",
            metricas["verdaderos_positivos"],
            metricas["falsos_positivos"],
            metricas["falsos_negativos"],
        )
        print("F1:", metricas["f1"])

    reporte = {
        "estado": "evaluacion_provisional",
        "alcance": "Códigos, tarifa y unidad en páginas de referencia.",
        "limitaciones": [
            "Referencias pendientes de revisión humana.",
            "Las descripciones solo se comprueban por presencia de texto.",
            "Resultados de desarrollo; no estiman exactitud global.",
            "No se evalúan salidas enriquecidas con transcripciones.",
            "Medellín permanece pendiente de extracción.",
            "San Vicente p54 y Santa Fe p44 no se incluyen en las métricas.",
        ],
        "documentos": documentos,
    }
    salida = BASE / "data/processed/evaluacion_extractores.json"
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(
        json.dumps(reporte, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("\nReporte:", salida)
    print("Métricas provisionales; descripciones sin evaluar por exactitud.")


if __name__ == "__main__":
    main()
