# Diagnóstico de tarifas faltantes: Guayabetal

## Estado del extractor
- 439 candidatos en el documento.
- 18 candidatos sin tarifa.
- Página PDF 9: 35 registros de referencia, 31 coincidencias,
  0 falsos positivos y 4 falsos negativos.
- Precisión: 100 %. Recall: 88,57 %. F1: 93,94 %.

## Casos revisados visualmente en la página 9
| Código municipal | CIIU | Tarifa visible por mil |
|---|---|---:|
| 219 | 4791 | 9 |
| 303 | 4520 | 4 |
| 304 | 8610 | 2 |
| 304 | 8699 | 2 |

## Diagnóstico
- Las tarifas están en filas individuales, según la captura.
- No se detectaron tablas ni bordes horizontales con el método probado.
- No se encontraron caracteres en la columna de tarifa
  (495 <= x0 < 550), a menos de 8 puntos de la posición vertical
  de cada uno de los cuatro códigos.
- Las cifras cercanas detectadas corresponden a otras filas.
- No se amplió la tolerancia para evitar asociaciones incorrectas.
- No se ha determinado la causa interna de la ausencia de esos caracteres.

## Tratamiento
- Se conserva la extracción automática original, con tarifas vacías.
- Las tarifas transcritas del PDF permanecen en la referencia.
- Una corrección manual debe guardarse por separado y registrar
  su procedencia y revisor.
- No se utiliza OCR.

## Pendientes
- Diagnosticar los otros 14 candidatos sin tarifa.
- Evaluar las descripciones vacías, recortadas o con errores de texto.
- Registrar al revisor humano de la referencia.
