"""Propuestas experimentales de descripción mediante bloques de texto."""

import re


def proponer_descripcion(pagina, ciiu: str) -> dict:
    """Propone un bloque; no garantiza que la descripción esté completa."""
    palabras = pagina.extract_words()
    codigos = [
        p for p in palabras
        if 155 <= p["x0"] < 210
        and re.fullmatch(r"\d{4}", p["text"])
    ]
    anclas = [p for p in codigos if p["text"] == ciiu]
    resultado = {
        "ciiu": ciiu,
        "descripcion_propuesta": None,
        "estado": "ancla_ausente_o_ambigua",
        "requiere_revision": True,
    }
    if len(anclas) != 1:
        return resultado

    ancla = anclas[0]
    centro_codigo = (ancla["top"] + ancla["bottom"]) / 2
    seleccion = sorted(
        [
            p for p in palabras
            if 210 <= p["x0"] < 495
            and abs(p["top"] - ancla["top"]) < 45
        ],
        key=lambda p: ((p["top"] + p["bottom"]) / 2, p["x0"]),
    )

    lineas = []
    for palabra in seleccion:
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

    bloques = []
    for linea in lineas:
        if not bloques or linea["top"] - bloques[-1]["bottom"] > 2.5:
            bloques.append({
                "top": linea["top"],
                "bottom": linea["bottom"],
                "lineas": [linea],
            })
        else:
            bloques[-1]["bottom"] = max(
                bloques[-1]["bottom"], linea["bottom"]
            )
            bloques[-1]["lineas"].append(linea)

    opciones = [
        b for b in bloques
        if b["top"] <= centro_codigo <= b["bottom"]
    ]
    resultado["estado"] = "bloque_ausente_o_ambiguo"
    if len(opciones) != 1:
        return resultado

    bloque = opciones[0]
    asociados = [
        c for c in codigos
        if bloque["top"]
        <= (c["top"] + c["bottom"]) / 2
        <= bloque["bottom"]
    ]
    if len(asociados) != 1:
        return resultado

    resultado["descripcion_propuesta"] = " ".join(
        " ".join(
            p["text"]
            for p in sorted(linea["palabras"], key=lambda p: p["x0"])
        )
        for linea in bloque["lineas"]
    )
    resultado["estado"] = "propuesta_integridad_no_verificada"
    return resultado
