"""Evaluación de candidatos frente a páginas anotadas completamente."""

from collections import Counter
from decimal import Decimal


def evaluar_extraccion(
    referencia: list[dict],
    candidatos: list[dict],
    paginas_evaluadas: list[tuple[str, int]],
) -> dict:
    """Compara códigos, tarifa y unidad con coincidencia exacta.

    Cada página indicada debe estar anotada completamente.
    Los candidatos sin tarifa se consideran abstenciones.
    Las descripciones no se evalúan.
    """
    alcance = {
        (archivo, int(pagina))
        for archivo, pagina in paginas_evaluadas
    }
    if not alcance:
        raise ValueError("Debe indicar las páginas evaluadas.")

    def en_alcance(registro):
        return (
            registro["archivo"],
            int(registro["pagina"]),
        ) in alcance

    def clave(registro, campo_tarifa, campo_unidad):
        tarifa = Decimal(
            str(registro[campo_tarifa]).strip().replace(",", ".")
        )
        if not tarifa.is_finite():
            raise ValueError("La tarifa debe ser un número finito.")

        return (
            registro["archivo"],
            int(registro["pagina"]),
            str(registro["codigo_actividad"]).strip(),
            str(registro["ciiu"]).strip(),
            tarifa,
            registro[campo_unidad],
        )

    referencia = [r for r in referencia if en_alcance(r)]
    candidatos = [r for r in candidatos if en_alcance(r)]

    completos = [
        r for r in candidatos
        if r.get("tarifa_candidata") is not None
        and str(r["tarifa_candidata"]).strip() != ""
    ]

    esperados = Counter(
        clave(r, "tarifa", "unidad")
        for r in referencia
    )
    obtenidos = Counter(
        clave(r, "tarifa_candidata", "unidad_candidata")
        for r in completos
    )

    verdaderos_positivos = sum((esperados & obtenidos).values())
    falsos_positivos = sum((obtenidos - esperados).values())
    falsos_negativos = sum((esperados - obtenidos).values())

    total_predicciones = verdaderos_positivos + falsos_positivos
    total_referencia = verdaderos_positivos + falsos_negativos

    precision = (
        verdaderos_positivos / total_predicciones
        if total_predicciones else None
    )
    recall = (
        verdaderos_positivos / total_referencia
        if total_referencia else None
    )
    denominador_f1 = (
        2 * verdaderos_positivos
        + falsos_positivos
        + falsos_negativos
    )
    f1 = (
        2 * verdaderos_positivos / denominador_f1
        if denominador_f1 else None
    )

    return {
        "paginas_evaluadas": [
            {"archivo": archivo, "pagina": pagina}
            for archivo, pagina in sorted(alcance)
        ],
        "registros_referencia": total_referencia,
        "candidatos": len(candidatos),
        "candidatos_sin_tarifa": len(candidatos) - len(completos),
        "verdaderos_positivos": verdaderos_positivos,
        "falsos_positivos": falsos_positivos,
        "falsos_negativos": falsos_negativos,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }