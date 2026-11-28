# Diagnóstico de tarifas faltantes: Guayabetal

## Estado del extractor
- 439 candidatos en el documento.
- 17 candidatos sin tarifa después de la normalización; antes eran 18.
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
- Revisar visualmente los otros 13 casos sin tarifa fuera de la página 9.
- Evaluar las descripciones vacías, recortadas o con errores de texto.
- Registrar al revisor humano de la referencia.


## Normalización comprobada
- Página PDF 11, código municipal 311, CIIU 3812.
- La captura confirma una tarifa de 10 por mil.
- El texto nativo recupera la tarifa como "lo".
- Se normaliza "lo" a "10" únicamente en la columna de tarifa.
- Se conserva el texto original en evidencia y se marca tarifa_normalizada.
- La ejecución sobre el documento afectó únicamente este registro.
- Se mantienen 439 candidatos y quedan 17 sin tarifa.
- La evaluación de la página 9 conserva sus resultados anteriores.

## Salida enriquecida con transcripciones
Ejecución desde la raíz del proyecto:

    poetry run python scripts/enriquecer_guayabetal.py

- Genera data/processed/guayabetal_enriquecido.csv y .json.
- Conserva los 439 candidatos y sus valores automáticos originales.
- Completa 17 tarifas propuestas mediante transcripciones visuales.
- No quedan tarifas propuestas vacías.
- Registra el origen de cada tarifa propuesta y el archivo de transcripción.
- Mantiene las descripciones transcritas en un campo separado cuando existen.
- El revisor humano de las transcripciones sigue pendiente.
- Las propuestas transcritas no son predicciones automáticas.
- No evaluar esta salida contra las referencias usadas para completarla.
- La evaluación automática de la página 9 conserva 31 coincidencias
  y 4 falsos negativos.

## Evaluación parcial de descripciones
- Se evaluó la extracción automática, sin usar la salida enriquecida.
- Referencias: ocho descripciones de las revisiones parciales de
  páginas 5, 6, 7, 8 y 15.
- Comparación exacta normalizando únicamente espacios y Unicode NFC.
- Cinco coincidencias: CIIU 2640, 2910, 3011, 3012 y 6630.
- Dos descripciones vacías: CIIU 2399 y 4741.
- Una descripción recortada: CIIU 4723.
- Coincidencia exacta: 5/8 (62,5 %).
- La muestra se seleccionó por problemas de extracción; el porcentaje
  no representa la exactitud de las 439 descripciones.
- Las referencias siguen pendientes de revisión humana registrada.

## Pruebas de delimitación
- Las franjas calculadas entre códigos mezclaron texto de filas vecinas.
- La agrupación por espacios entre líneas produjo bloques ambiguos.
- Ninguna de estas dos reglas se incorporó al extractor.
