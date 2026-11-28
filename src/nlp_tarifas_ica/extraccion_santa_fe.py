"""Extracción de tablas de Santa Fe de Antioquia, sin OCR."""

from pathlib import Path
import re

import pdfplumber


def extraer_tabla_santa_fe(
    ruta_pdf: str | Path,
    paginas: list[int],
) -> list[dict]:
    """Extrae candidatos de páginas de tablas seleccionadas previamente.

    Las páginas se numeran desde 1. Requiere confirmar en el
    documento que las tablas seleccionadas expresan tarifas por mil.
    """
    if not paginas:
        raise ValueError("Debe indicar las páginas que desea procesar.")

    ruta = Path(ruta_pdf)
    registros = []

    with pdfplumber.open(ruta) as pdf:
        numeros = sorted(set(paginas))
        if any(n < 1 or n > len(pdf.pages) for n in numeros):
            raise ValueError("Hay páginas fuera del documento.")

        for numero in numeros:
            pagina = pdf.pages[numero - 1]

            # Completa filas iniciales con borde superior abierto.
            bordes_adicionales = []
            for detectada in pagina.find_tables():
                izquierda, arriba, derecha, _ = detectada.bbox
                verticales = [
                    borde for borde in pagina.edges
                    if borde["orientation"] == "v"
                    and izquierda - 3 <= borde["x0"] <= derecha + 3
                    and borde["top"] < arriba - 3
                    and borde["bottom"] >= arriba - 3
                ]
                if not verticales:
                    continue

                techo = min(borde["top"] for borde in verticales)
                bordes_adicionales.append({
                    "object_type": "line",
                    "x0": izquierda,
                    "x1": derecha,
                    "top": techo,
                    "bottom": techo,
                    "width": derecha - izquierda,
                    "height": 0,
                })

            ajustes = (
                {"explicit_horizontal_lines": bordes_adicionales}
                if bordes_adicionales else {}
            )
            for tabla in pagina.extract_tables(ajustes):
                for fila in tabla:
                    if len(fila) != 3:
                        continue

                    codigo, descripcion, tarifa = [
                        str(celda or "").strip() for celda in fila
                    ]
                    if not re.fullmatch(r"\d{3,4}", codigo):
                        continue

                    registros.append({
                        "archivo": ruta.name,
                        "municipio": "Santa Fe de Antioquia",
                        "pagina": numero,
                        "codigo_fuente": codigo,
                        "descripcion": " ".join(descripcion.split()),
                        "tarifa_candidata": (
                            tarifa
                            if re.fullmatch(r"\d+(?:[.,]\d+)?", tarifa)
                            else None
                        ),
                        "unidad_candidata": "por_mil",
                        "evidencia": " | ".join(
                            str(celda or "") for celda in fila
                        ),
                        "estado": "pendiente_revision",
                        "requiere_revision": True,
                    })

            pagina.close()

    return registros
