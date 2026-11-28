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


def extraer_tabla_san_vicente(
    ruta_pdf: str | Path,
    paginas: list[int],
) -> list[dict]:
    """Extrae tablas de tres columnas en páginas PDF indicadas.

    Las páginas se numeran desde 1.
    Requiere comprobar en el PDF que la unidad es por mil.
    Conserva el código tal como aparece en la fuente.
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

            # Completa el borde superior de filas abiertas al
            # continuar una tabla desde la página anterior.
            bordes_adicionales = []
            for tabla_detectada in pagina.find_tables():
                izquierda, arriba, derecha, _ = tabla_detectada.bbox

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
                        str(celda or "").strip()
                        for celda in fila
                    ]

                    if not re.fullmatch(r"\d{3,4}", codigo):
                        continue

                    tarifa_valida = bool(
                        re.fullmatch(r"\d+(?:[.,]\d+)?", tarifa)
                    )

                    registros.append({
                        "archivo": ruta.name,
                        "municipio": "San Vicente Ferrer",
                        "pagina": numero,
                        "codigo_fuente": codigo,
                        "descripcion": " ".join(descripcion.split()),
                        "tarifa_candidata": (
                            tarifa if tarifa_valida else None
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
