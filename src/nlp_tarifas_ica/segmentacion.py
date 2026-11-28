"""Segmentación de artículos con trazabilidad por página."""

import re

from .normalizacion import normalizar_texto


PATRON_ARTICULO = re.compile(
    r"^[ \t]*art[ií]culo[ \t]+(?P<numero>\d+)\b[^\n]*",
    flags=re.IGNORECASE | re.MULTILINE,
)


def segmentar_articulos(paginas: list[dict]) -> list[dict]:
    """Separa artículos por encabezados al inicio de una línea.

    Recibe las páginas de un único PDF, en su orden original.
    Devuelve una lista vacía si no encuentra encabezados.
    """
    partes = []
    limites = []
    posicion = 0

    for pagina in paginas:
        texto = normalizar_texto(pagina["texto"]) + "\n"
        partes.append(texto)
        limites.append({
            "inicio": posicion,
            "fin": posicion + len(texto),
            "pagina": pagina["pagina"],
        })
        posicion += len(texto)

    texto_completo = "".join(partes)
    encabezados = list(PATRON_ARTICULO.finditer(texto_completo))
    articulos = []

    for indice, encabezado in enumerate(encabezados):
        inicio = encabezado.start()
        fin = (
            encabezados[indice + 1].start()
            if indice + 1 < len(encabezados)
            else len(texto_completo)
        )

        # Excluir espacios finales al determinar la última página.
        fragmento = texto_completo[inicio:fin].rstrip()
        fin_con_texto = inicio + len(fragmento)

        paginas_articulo = [
            limite["pagina"]
            for limite in limites
            if limite["inicio"] < fin_con_texto
            and limite["fin"] > inicio
        ]

        articulos.append({
            "archivo": paginas[0]["archivo"],
            "numero": encabezado.group("numero"),
            "encabezado": encabezado.group().strip(),
            "pagina_inicio": paginas_articulo[0],
            "pagina_fin": paginas_articulo[-1],
            "texto": fragmento,
        })

    return articulos