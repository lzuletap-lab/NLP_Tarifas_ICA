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

## Experimento de propuestas por bloques
- Módulo: src/nlp_tarifas_ica/descripciones_guayabetal.py.
- Función: proponer_descripcion(pagina, ciiu).
- No modifica las descripciones ni las tarifas del extractor principal.
- Prueba en seis casos seleccionados: páginas 3, 5, 7, 8, 10 y 12.
- Coincidencias exactas: 3/6.
- Coincidencias sin distinguir mayúsculas: 5/6.
- CIIU 2022 mantiene una descripción recortada.
- CIIU 4741 y 8720 presentan diferencias de mayúsculas.
- Todas las propuestas requieren revisión; un bloque único no garantiza
  que la descripción esté completa.
- Resultados exploratorios sobre casos seleccionados, sin alcance global.
- La muestra difiere de la evaluación anterior de ocho descripciones;
  sus porcentajes no se comparan directamente.
- Los reportes JSON se guardaron localmente en data/processed/.

## Comparación reproducible sobre los mismos ocho casos
Comando:

    poetry run python scripts/evaluar_descripciones_guayabetal.py

- Método actual: 5/8 coincidencias exactas y 5/8 sin distinguir mayúsculas.
- Método experimental: 7/8 exactas y 8/8 sin distinguir mayúsculas.
- Se incluyen todos los casos de la muestra en ambos métodos.
- sin_propuesta cuenta valores None; no cuenta cadenas vacías.
- No se modifican los candidatos ni las tarifas.
- Muestra seleccionada y referencias pendientes de revisión humana.
- El caso 2022 no pertenece a estos ocho y mantiene un recorte conocido.
- El método experimental aún no sustituye al extractor principal.

## Diagnóstico experimental sobre los 439 candidatos
- Se generaron 318 propuestas con integridad no verificada.
- En 121 casos no se identificó un bloque único.
- El extractor actual devuelve 70 descripciones vacías.
- El método experimental propone texto para 12 de esas 70.
- Quedan 58 descripciones originalmente vacías sin propuesta.
- Ninguna propuesta es más corta que la descripción original.
- La longitud no demuestra integridad: el caso 2022 sigue recortado.
- Estos resultados miden cobertura y alertas, no exactitud.
- No se sustituyeron descripciones del extractor principal.
- Detalle local: data/processed/diagnostico_descripciones_lote.json.
