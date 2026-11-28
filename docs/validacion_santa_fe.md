# Extracción y validación: Santa Fe de Antioquia

## Alcance
- Páginas PDF procesadas: 29–44.
- Método: detección de tablas con pdfplumber y corrección de bordes superiores abiertos, sin OCR.
- Resultado: 468 candidatos pendientes de revisión.
- Salidas locales: data/processed/candidatos_santa_fe_p29_44.csv y .json.
- En la página 44, después de la tabla, comienzan parágrafos y el artículo 39.

## Controles del lote
- Candidatos sin tarifa: 0.
- Descripciones vacías: 0.
- Códigos duplicados dentro de una misma página: 0.
- Estos controles no garantizan que todas las filas o descripciones estén completas.

## Comparaciones realizadas
Se comparan código, tarifa y unidad; las descripciones no tienen evaluación completa.

| Página PDF | Referencia | Coincidencias | Faltantes |
|---|---:|---:|---:|
| 29 | 15 | 15 | 0 |
| 30 | 34 | 34 | 0 |
| 44 | 17 | 17 | 0 |

- Páginas 29 y 30 utilizadas para desarrollar el extractor.
- La prueba inicial de la página 30 omitió el código 722.
- Se recuperó completando el borde superior de la tabla.
- La página 44 se comprobó sin nuevos ajustes: códigos y tarifas coinciden.
- El control de la página 44 se ejecutó en terminal; su referencia aún no está guardada en CSV.

## Pendientes
- Registrar al revisor humano de las referencias.
- Guardar la referencia de la página 44 y automatizar las comprobaciones.
- Evaluar descripciones y ampliar la muestra de validación.
- Ampliar la evaluación automática más allá de las páginas 29 y 30.
- Tratar por separado las tablas de UVT y Régimen Simple.
- Los archivos de data/processed están excluidos de Git.


## Ejecución reproducible
Desde la raíz del proyecto:

    poetry run python scripts/extraer_santa_fe.py

Requiere el PDF en data/raw/ y las referencias en data/referencia/.
Extrae las páginas PDF 29–44 y genera CSV, JSON y resumen del lote.
Evalúa automáticamente solo las páginas 29 y 30.
Las salidas se guardan en data/processed/.
Los candidatos conservan el estado pendiente_revision.
Las descripciones no se evalúan.
