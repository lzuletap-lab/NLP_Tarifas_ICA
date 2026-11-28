"""Comparación provisional de dos métodos sobre la misma muestra."""

import csv
import json
import unicodedata
from pathlib import Path

import pdfplumber

from nlp_tarifas_ica.descripciones_guayabetal import proponer_descripcion
from nlp_tarifas_ica.extraccion_tablas import extraer_tabla_guayabetal


def normalizar(texto):
    return " ".join(unicodedata.normalize("NFC", texto).split())


def clave(r):
    return (
        r["archivo"], int(r["pagina"]),
        r["codigo_actividad"].strip(), r["ciiu"].strip(),
    )


def main():
    base = Path(__file__).resolve().parents[1]
    referencias = []
    for nombre in (
        "revision_parcial_guayabetal_p5_p6.csv",
        "revision_parcial_guayabetal_p7_p8_p15.csv",
    ):
        with (base / "data/referencia" / nombre).open(
            encoding="utf-8-sig", newline=""
        ) as archivo:
            referencias.extend(csv.DictReader(archivo))

    nombres = {r["archivo"] for r in referencias}
    if len(nombres) != 1:
        raise ValueError("Las referencias deben corresponder a un solo PDF.")
    ruta_pdf = base / "data/raw" / nombres.pop()

    candidatos = {}
    for r in extraer_tabla_guayabetal(ruta_pdf):
        candidatos.setdefault(clave(r), []).append(r)

    resultados = []
    with pdfplumber.open(ruta_pdf) as pdf:
        for referencia in referencias:
            opciones = candidatos.get(clave(referencia), [])
            if len(opciones) != 1:
                raise ValueError(f"Candidato ausente o ambiguo: {clave(referencia)}")

            actual = opciones[0]["descripcion_parcial"]
            propuesta = proponer_descripcion(
                pdf.pages[int(referencia["pagina"]) - 1],
                referencia["ciiu"],
            )
            esperado = normalizar(referencia["descripcion_visible"])

            for metodo, texto in (
                ("actual", actual),
                ("experimental", propuesta["descripcion_propuesta"]),
            ):
                obtenido = normalizar(texto or "")
                resultados.append({
                    "pagina": int(referencia["pagina"]),
                    "ciiu": referencia["ciiu"],
                    "metodo": metodo,
                    "referencia": esperado,
                    "descripcion": texto,
                    "coincidencia_exacta": obtenido == esperado,
                    "coincidencia_sin_mayusculas": (
                        obtenido.casefold() == esperado.casefold()
                    ),
                    "sin_propuesta": texto is None,
                    "estado_propuesta": (
                        propuesta["estado"] if metodo == "experimental"
                        else "extraccion_actual"
                    ),
                })

    resumen = {}
    for metodo in ("actual", "experimental"):
        filas = [r for r in resultados if r["metodo"] == metodo]
        resumen[metodo] = {
            "casos": len(filas),
            "coincidencias_exactas": sum(
                r["coincidencia_exacta"] for r in filas
            ),
            "coincidencias_sin_mayusculas": sum(
                r["coincidencia_sin_mayusculas"] for r in filas
            ),
            "sin_propuesta": sum(r["sin_propuesta"] for r in filas),
        }

    salida = base / "data/processed/comparacion_descripciones_guayabetal.json"
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(
        json.dumps(
            {"resumen": resumen, "detalle": resultados},
            ensure_ascii=False, indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    print("Reporte:", salida)
    print("Muestra seleccionada; revisión humana pendiente.")
    print("No se modificaron candidatos ni tarifas.")


if __name__ == "__main__":
    main()
