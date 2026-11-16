"""Extracción inicial de candidatos de la tabla de Guayabetal."""

from pathlib import Path
import re

import pdfplumber


def extraer_tabla_guayabetal(ruta_pdf: str | Path) -> list[dict]:
    """Extrae candidatos por posición. Requiere revisión humana."""
    ruta = Path(ruta_pdf)
    registros = []

    with pdfplumber.open(ruta) as pdf:
        for numero, pagina in enumerate(pdf.pages, start=1):
            palabras = pagina.extract_words()

            # Columna del código de actividad municipal.
            inicios = [
                palabra
                for palabra in palabras
                if 110 <= palabra["x0"] < 155
                and re.fullmatch(r"\d{3}", palabra["text"])
            ]

            for inicio in inicios:
                fila = sorted(
                    [
                        palabra
                        for palabra in palabras
                        if abs(palabra["top"] - inicio["top"]) < 5
                    ],
                    key=lambda palabra: palabra["x0"],
                )

                ciiu = [
                    palabra["text"]
                    for palabra in fila
                    if 155 <= palabra["x0"] < 210
                    and re.fullmatch(r"\d{4}", palabra["text"])
                ]

                # No confundir títulos de sección con filas CIIU.
                if len(ciiu) != 1:
                    continue

                tarifas = [
                    palabra["text"]
                    for palabra in fila
                    if 495 <= palabra["x0"] < 550
                    and re.fullmatch(r"\d+(?:[.,]\d+)?", palabra["text"])
                ]

                descripcion = " ".join(
                    palabra["text"]
                    for palabra in fila
                    if 210 <= palabra["x0"] < 495
                )

                registros.append({
                    "archivo": ruta.name,
                    "pagina": numero,
                    "codigo_actividad": inicio["text"],
                    "ciiu": ciiu[0],
                    "descripcion_parcial": descripcion,
                    "tarifa_candidata": (
                        tarifas[0] if len(tarifas) == 1 else None
                    ),
                    "unidad_candidata": "por_mil",
                    "evidencia": " ".join(p["text"] for p in fila),
                    "estado": "pendiente_revision",
                    "requiere_revision": True,
                })

            pagina.close()

    return registros