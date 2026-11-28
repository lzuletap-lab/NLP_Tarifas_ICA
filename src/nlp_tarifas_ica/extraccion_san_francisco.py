"""Extracción por líneas de texto nativo, sin OCR."""

from pathlib import Path
import re

import pdfplumber


def extraer_tabla_san_francisco(
    ruta_pdf: str | Path,
    paginas: list[int],
) -> list[dict]:
    """Extrae candidatos de páginas de tablas indicadas desde 1.

    Las páginas deben seleccionarse previamente.
    Las descripciones que continúan en otra página requieren revisión.
    """
    if not paginas:
        raise ValueError("Debe indicar las páginas que desea procesar.")

    ruta = Path(ruta_pdf)
    inicio = re.compile(r"^\s*(\d{3})\s+(.+)$")
    tarifa = re.compile(
        r"\s+(\d+(?:[.,]\d+)?)\s*[xX×]\s*[1lI]000\s*$"
    )
    registros = []

    with pdfplumber.open(ruta) as pdf:
        numeros = sorted(set(paginas))
        if any(n < 1 or n > len(pdf.pages) for n in numeros):
            raise ValueError("Hay páginas fuera del documento.")

        for numero in numeros:
            pagina = pdf.pages[numero - 1]
            actual = None

            for linea in (pagina.extract_text() or "").splitlines():
                limpia = linea.strip()
                titulo = re.sub(r"[^A-Z]", "", limpia.upper())

                if titulo.startswith("ACTIVIDAD"):
                    if actual:
                        registros.append(actual)
                        actual = None
                    continue

                if limpia == str(numero):
                    continue

                coincidencia = inicio.match(limpia)
                if coincidencia:
                    if actual:
                        registros.append(actual)

                    codigo, contenido = coincidencia.groups()
                    tasa = tarifa.search(contenido)
                    actual = {
                        "archivo": ruta.name,
                        "municipio": "San Francisco",
                        "pagina": numero,
                        "codigo_fuente": codigo,
                        "descripcion": (
                            contenido[:tasa.start()].strip()
                            if tasa else contenido
                        ),
                        "tarifa_candidata": (
                            tasa.group(1) if tasa else None
                        ),
                        "unidad_candidata": (
                            "por_mil" if tasa else None
                        ),
                        "evidencia": linea,
                        "estado": "pendiente_revision",
                        "requiere_revision": True,
                    }

                elif actual and limpia:
                    actual["descripcion"] += " " + limpia
                    actual["evidencia"] += "\n" + linea

            if actual:
                registros.append(actual)

            pagina.close()

    return registros
