"""Combina extracción y transcripciones sin alterar valores automáticos."""

import csv
from pathlib import Path

from nlp_tarifas_ica.extraccion_tablas import extraer_tabla_guayabetal
from nlp_tarifas_ica.exportacion import exportar_csv, exportar_json


def clave(r):
    return (
        r["archivo"], int(r["pagina"]),
        r["codigo_actividad"].strip(), r["ciiu"].strip(),
    )


def main():
    base = Path(__file__).resolve().parents[1]
    archivos = [
        p for p in (base / "data/raw").iterdir()
        if "guayabetal" in p.name.lower()
        and p.suffix.lower() == ".pdf"
    ]
    if len(archivos) != 1:
        raise ValueError("Debe existir un único PDF de Guayabetal.")

    candidatos = extraer_tabla_guayabetal(archivos[0])
    if not candidatos:
        raise ValueError("No se extrajeron candidatos.")

    fuentes = [
        "revision_parcial_guayabetal_p2_p4.csv",
        "revision_parcial_guayabetal_p5_p6.csv",
        "revision_parcial_guayabetal_p7_p8_p15.csv",
        "referencia_manual.csv",
    ]
    transcripciones = {}
    for nombre in fuentes:
        ruta = base / "data/referencia" / nombre
        with ruta.open(encoding="utf-8-sig", newline="") as archivo:
            for fila in csv.DictReader(archivo):
                k = clave(fila)
                if k in transcripciones:
                    raise ValueError(f"Referencia duplicada: {k}")
                transcripciones[k] = {
                    "tarifa": fila.get("tarifa_visible", fila.get("tarifa")),
                    "unidad": fila["unidad"],
                    "descripcion": fila.get(
                        "descripcion_visible", fila.get("descripcion", "")
                    ),
                    "revisor": fila.get("revisor", ""),
                    "fuente": "data/referencia/" + nombre,
                }

    enriquecidos = []
    completados = 0
    for candidato in candidatos:
        r = dict(candidato)
        automatica = r.get("tarifa_candidata")
        falta = automatica is None or not str(automatica).strip()
        revision = transcripciones.get(clave(r)) if falta else None

        r["tarifa_transcrita"] = None
        r["unidad_transcrita"] = None
        r["descripcion_transcrita"] = ""
        r["fuente_transcripcion"] = ""
        r["revisor_transcripcion"] = ""
        r["tarifa_propuesta"] = automatica
        r["origen_tarifa_propuesta"] = (
            "sin_tarifa" if falta else
            "extraccion_normalizada" if r.get("tarifa_normalizada")
            else "extraccion_automatica"
        )

        if revision and revision["tarifa"]:
            if revision["unidad"] != r["unidad_candidata"]:
                raise ValueError(f"Unidades diferentes: {clave(r)}")
            r["tarifa_transcrita"] = revision["tarifa"]
            r["unidad_transcrita"] = revision["unidad"]
            r["descripcion_transcrita"] = revision["descripcion"]
            r["fuente_transcripcion"] = revision["fuente"]
            r["revisor_transcripcion"] = revision["revisor"]
            r["tarifa_propuesta"] = revision["tarifa"]
            r["origen_tarifa_propuesta"] = "transcripcion_visual"
            completados += 1

        enriquecidos.append(r)

    salida = base / "data/processed"
    salida.mkdir(parents=True, exist_ok=True)
    exportar_json(
        enriquecidos, salida / "guayabetal_enriquecido.json"
    )
    exportar_csv(
        enriquecidos, salida / "guayabetal_enriquecido.csv"
    )

    print("Candidatos:", len(enriquecidos))
    print("Tarifas automáticas vacías:", sum(
        r["tarifa_candidata"] is None
        or not str(r["tarifa_candidata"]).strip()
        for r in enriquecidos
    ))
    print("Propuestas añadidas por transcripción:", completados)
    print("Sin tarifa propuesta:", sum(
        r["tarifa_propuesta"] is None
        or not str(r["tarifa_propuesta"]).strip()
        for r in enriquecidos
    ))
    print("Estado: pendiente de revisión.")
    print("Las propuestas transcritas no son predicciones automáticas.")
    print("No evaluar esta salida contra las referencias usadas para completarla.")


if __name__ == "__main__":
    main()
