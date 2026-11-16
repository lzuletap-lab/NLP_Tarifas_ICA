"""Lectura de texto nativo de archivos PDF."""

from pathlib import Path

import pdfplumber


def leer_pdf(ruta_pdf: str | Path) -> list[dict]:
    """Extrae texto por página. Las páginas sin texto se conservan vacías."""
    ruta = Path(ruta_pdf)

    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    if ruta.suffix.lower() != ".pdf":
        raise ValueError("El archivo debe ser un PDF.")

    paginas = []

    with pdfplumber.open(ruta) as pdf:
        for numero, pagina in enumerate(pdf.pages, start=1):
            paginas.append({
                "archivo": ruta.name,
                "pagina": numero,
                "texto": pagina.extract_text() or "",
                "metodo": "texto_nativo",
            })
            pagina.close()

    return paginas


def unir_texto(paginas: list[dict]) -> str:
    """Une el texto de las páginas respetando su orden."""
    return "\n".join(pagina["texto"] for pagina in paginas)