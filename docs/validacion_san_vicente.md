# Extracción y validación: San Vicente Ferrer

## Alcance
- PDF: Antioquia - San Vicente Ferrer_Acuerdo 081 ESTATUTO TRIBUTARIO_22_diciembre.pdf
- Páginas PDF procesadas: 38 a 54, ambas incluidas.
- Método: texto nativo y detección de tablas con pdfplumber, sin OCR.
- Resultado: 468 candidatos pendientes de revisión.
- Salidas locales: data/processed/candidatos_san_vicente_p38_54.csv y .json.

## Controles del lote
- Candidatos sin tarifa: 0.
- Candidatos con descripción vacía: 0.
- Códigos repetidos dentro de una misma página: 0.
- Estos controles no demuestran que todas las filas o descripciones estén completas.

## Comparación con referencias transcritas del PDF
Se comparan código, tarifa y unidad; las descripciones no se evalúan.

| Página PDF | Referencia | Coincidencias | Falsos positivos | Falsos negativos |
|---|---:|---:|---:|---:|
| 38 | 28 | 28 | 0 | 0 |
| 39 | 32 | 32 | 0 | 0 |
| 42 | 28 | 28 | 0 | 0 |
| 54 | 17 | 17 | 0 | 0 |

## Desarrollo y correcciones
- Páginas 38 y 39 utilizadas para desarrollar el extractor.
- La primera prueba de la página 39 recuperó 31 de 32 registros.
- Se corrigió la detección de filas iniciales sin borde superior.
- Páginas 42 y 54 comprobadas sin nuevos ajustes al extractor.
- En la referencia de la página 42 se corrigió una transcripción:
  código 2818, tarifa 6 por mil, según la captura del PDF.
- La comparación de la página 54 se ejecutó en terminal;
  su referencia todavía no está guardada en un CSV.
- La comprobación de Guayabetal conservó su resultado anterior:
  31 coincidencias, 0 falsos positivos y 4 falsos negativos en la página 9.

## Pendientes
- Registrar el revisor humano de las referencias.
- Guardar la referencia de la página 54 y automatizar las comprobaciones.
- Evaluar integridad y exactitud de las descripciones.
- Ampliar la validación a otras páginas y documentos.
- Confirmar en la página siguiente que el intervalo de tablas termina en la 54.
- Integrar la ejecución por lote y la evaluación en un script o notebook.
- Los archivos de data/processed son locales y están excluidos de Git.

## Ejecución reproducible
Desde la raíz del proyecto:

```bash
poetry run python scripts/extraer_san_vicente.py


```

Requiere el PDF de San Vicente Ferrer en data/raw/.
Genera el CSV, el JSON de candidatos y un resumen por página en
data/processed/. Las salidas mantienen el estado pendiente_revision.

Se comprobó visualmente que la página PDF 55 contiene artículos
y no continúa la tabla anterior. El intervalo procesado es 38–54.
