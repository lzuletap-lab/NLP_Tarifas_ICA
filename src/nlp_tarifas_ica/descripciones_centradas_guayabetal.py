"""Propuestas experimentales por centro vertical, sin OCR."""

import re


def proponer_descripcion_centrada(pagina, ciiu):
    resultado = {
        "ciiu": ciiu,
        "descripcion_propuesta": None,
        "desajuste_centro": None,
        "estado": "ancla_ausente_o_ambigua",
        "requiere_revision": True,
    }
    palabras = pagina.extract_words()
    codigos = [
        p for p in palabras
        if 155 <= p["x0"] < 210
        and re.fullmatch(r"\d{4}", p["text"])
    ]
    anclas = [p for p in codigos if p["text"] == ciiu]
    if len(anclas) != 1:
        return resultado

    ancla = anclas[0]
    centro_codigo = (ancla["top"] + ancla["bottom"]) / 2

    lineas = []
    for palabra in sorted(
        [p for p in palabras if 210 <= p["x0"] < 495],
        key=lambda p: ((p["top"] + p["bottom"]) / 2, p["x0"]),
    ):
        centro = (palabra["top"] + palabra["bottom"]) / 2
        if not lineas or abs(centro - lineas[-1]["centro"]) > 3:
            lineas.append({
                "centro": centro,
                "top": palabra["top"],
                "bottom": palabra["bottom"],
                "palabras": [palabra],
            })
        else:
            linea = lineas[-1]
            linea["top"] = min(linea["top"], palabra["top"])
            linea["bottom"] = max(linea["bottom"], palabra["bottom"])
            linea["palabras"].append(palabra)

    opciones = []
    for inicio in range(len(lineas)):
        for fin in range(inicio, min(inicio + 6, len(lineas))):
            bloque = lineas[inicio:fin + 1]
            arriba = bloque[0]["top"]
            abajo = bloque[-1]["bottom"]

            if not arriba <= centro_codigo <= abajo:
                continue
            if any(
                siguiente["top"] - anterior["bottom"] > 5
                for anterior, siguiente in zip(bloque, bloque[1:])
            ):
                continue

            asociados = [
                codigo for codigo in codigos
                if arriba <= (
                    codigo["top"] + codigo["bottom"]
                ) / 2 <= abajo
            ]
            if len(asociados) != 1:
                continue

            desajuste = abs((arriba + abajo) / 2 - centro_codigo)
            opciones.append((desajuste, inicio, fin))

    resultado["estado"] = "bloque_ausente_o_ambiguo"
    if not opciones:
        return resultado

    opciones.sort()
    mejor = opciones[0]
    if (
        len(opciones) > 1
        and abs(opciones[1][0] - mejor[0]) < 0.1
    ):
        return resultado

    desajuste, inicio, fin = mejor
    descripcion = " ".join(
        palabra["text"]
        for linea in lineas[inicio:fin + 1]
        for palabra in sorted(
            linea["palabras"], key=lambda p: p["x0"]
        )
    )
    resultado.update({
        "descripcion_propuesta": descripcion,
        "desajuste_centro": round(desajuste, 3),
        "estado": "propuesta_integridad_no_verificada",
    })
    return resultado
