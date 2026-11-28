"""Normalización de texto para extraer artículos, códigos y tarifas."""

import re
import unicodedata


def normalizar_texto(texto: str) -> str:
    """Normaliza espacios sin eliminar cifras, signos ni saltos de línea."""
    texto = unicodedata.normalize("NFC", texto)
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = texto.replace("\u00a0", " ")
    texto = re.sub(r"[^\S\n]+", " ", texto)
    texto = "\n".join(linea.strip() for linea in texto.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", texto).strip()