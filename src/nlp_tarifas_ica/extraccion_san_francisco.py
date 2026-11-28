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

            texto_pagina = pagina.extract_text() or ""
            texto_tabla = re.split(
                r"(?im)^\s*PAR[ÁA]\s*GRA",
                texto_pagina,
                maxsplit=1,
            )[0]

            for linea in texto_tabla.splitlines():
                limpia = linea.strip()
                titulo = re.sub(r"[^A-Z]", "", limpia.upper())

                if titulo.startswith("ACTIVIDAD") and not inicio.match(limpia):
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

            # Respaldo por columnas para tarifas desordenadas.
            # Coordenadas específicas del formato de San Francisco.
            pendientes = [
                r for r in registros
                if r["pagina"] == numero
                and r["tarifa_candidata"] is None
            ]
            if pendientes:
                palabras = pagina.extract_words()
                parrafos = [
                    p["top"] for p in palabras
                    if re.match(r"PAR[ÁA]GRA", p["text"], re.I)
                ]
                limite = min(parrafos) if parrafos else pagina.height - 35

                for registro in pendientes:
                    anclas = [
                        p for p in palabras
                        if p["text"] == registro["codigo_fuente"]
                        and p["x0"] < 125
                        and p["top"] < limite
                    ]
                    if len(anclas) != 1:
                        continue

                    ancla = anclas[0]
                    siguientes = [
                        p["top"] for p in palabras
                        if p["x0"] < 125
                        and re.fullmatch(r"\d{3}", p["text"])
                        and p["top"] > ancla["top"] + 5
                        and p["top"] < limite
                    ]
                    fin = min(siguientes + [limite])
                    arriba = max(0, ancla["top"] - 5)

                    tasa_palabras = sorted(
                        [
                            p for p in palabras
                            if p["x0"] >= 430
                            and arriba <= p["top"] < fin - 3
                        ],
                        key=lambda p: p["x0"],
                    )
                    tasa_texto = " ".join(p["text"] for p in tasa_palabras)
                    tasa = re.fullmatch(
                        r"(\d+(?:[.,]\d+)?)\s*[xX×]\s*[1lI]000",
                        tasa_texto,
                    )
                    descripcion = pagina.crop(
                        (125, arriba, 430, fin - 3)
                    ).extract_text() or ""

                    registro["descripcion"] = " ".join(descripcion.split())
                    registro["tarifa_candidata"] = (
                        tasa.group(1) if tasa else None
                    )
                    registro["unidad_candidata"] = (
                        "por_mil" if tasa else None
                    )
                    registro["evidencia"] = (
                        descripcion + "\nTarifa fuente: " + tasa_texto
                    )

            pagina.close()

    return registros
