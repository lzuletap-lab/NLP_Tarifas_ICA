"""Exportación de candidatos sin modificar sus valores."""

import csv
import json
from pathlib import Path


def exportar_json(registros: list[dict], ruta: str | Path) -> Path:
    """Guarda los registros; conserva los valores faltantes como null."""
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps(registros, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return destino


def exportar_csv(registros: list[dict], ruta: str | Path) -> Path:
    """Guarda los registros en CSV; los valores faltantes quedan vacíos."""
    if not registros:
        raise ValueError("No hay registros para exportar a CSV.")

    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)

    columnas = list(dict.fromkeys(
        clave for registro in registros for clave in registro
    ))

    with destino.open("w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(registros)

    return destino