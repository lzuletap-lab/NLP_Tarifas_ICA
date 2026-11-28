# Estado de extracción y validación de PDF

## Alcance
Lectura de texto nativo, sin OCR. El chatbot no forma parte de este trabajo.
Los registros son candidatos pendientes de revisión, no datos aprobados.

## Resultados
| Documento | Extracción | Comparación realizada |
|---|---|---|
| Guayabetal | 439 candidatos; 17 sin tarifa automática | Página 9: 31 coincidencias, 0 falsos positivos y 4 falsos negativos; F1 93,94 % |
| San Vicente Ferrer | 468 candidatos, páginas PDF 38–54 | 105 coincidencias en páginas 38, 39, 42 y 54 |
| San Francisco | 45 candidatos, páginas PDF 46–49 | 45 coincidencias; todas las páginas utilizadas durante el desarrollo |
| Santa Fe de Antioquia | 468 candidatos, páginas PDF 29–44 | 66 coincidencias en páginas 29, 30 y 44 |
| Medellín | Tablas pendientes de extracción | Contenido visible no recuperado por el método actual; sin métricas |

Las comparaciones cuantitativas evalúan códigos, tarifa y unidad.
Los controles de San Vicente página 54 y Santa Fe página 44 se realizaron
en terminal; sus referencias aún no están guardadas en CSV.
Las descripciones no tienen una evaluación completa.
Los resultados parciales no representan el desempeño sobre todos los documentos.

## Ejecución
Desde la raíz del proyecto, con los PDF disponibles en data/raw/:

    poetry run python scripts/extraer_san_vicente.py
    poetry run python scripts/extraer_san_francisco.py
    poetry run python scripts/extraer_santa_fe.py
    poetry run python scripts/enriquecer_guayabetal.py

San Vicente extrae el lote y genera controles.
San Francisco extrae y evalúa las páginas 46–49.
Santa Fe extrae el lote y evalúa automáticamente solo las páginas 29–30.
Guayabetal genera una salida enriquecida separada de la extracción automática.

## Guayabetal: transcripciones
- Una tarifa se recuperó normalizando "lo" a "10", con evidencia conservada.
- Las otras 17 tarifas propuestas provienen de transcripciones visuales.
- La salida enriquecida mantiene los valores automáticos originales.
- No quedan tarifas propuestas vacías, pero el revisor sigue pendiente.
- No evaluar la salida enriquecida contra las referencias usadas para completarla.

## Pendientes prioritarios
1. Revisar las referencias contra los PDF y registrar al revisor.
2. Guardar las referencias y automatizar los controles de las páginas finales.
3. Ampliar las pruebas en páginas y documentos no usados para ajustar el código.
4. Evaluar descripciones completas, errores de texto y filas omitidas.
5. Revisar por separado reglas sin código, descuentos, UVT y Régimen Simple.
6. Mantener Medellín como pendiente, documentando la limitación sin OCR.

## Archivos y colaboración
- Código: src/nlp_tarifas_ica/.
- Ejecución: scripts/.
- Referencias y transcripciones: data/referencia/.
- Diagnósticos y alcance de las pruebas: docs/.
- PDF de entrada y resultados de data/processed/ están excluidos de Git.
- Los colaboradores deben disponer de los PDF para reproducir las ejecuciones.
- Los cambios están en feature/estructura-poetry; no se confirma su integración
  en develop o main.


## Evaluación consolidada reproducible
Desde la raíz del proyecto:

    poetry run python scripts/evaluar_extractores.py

Genera data/processed/evaluacion_extractores.json.
Utiliza las salidas automáticas originales de los cuatro extractores.

| Documento | Candidatos | Sin tarifa | Descripciones vacías | VP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| Guayabetal | 439 | 17 | 70 | 31 | 0 | 4 |
| San Vicente Ferrer | 468 | 0 | 0 | 88 | 0 | 0 |
| San Francisco | 45 | 0 | 0 | 45 | 0 | 0 |
| Santa Fe de Antioquia | 468 | 0 | 0 | 49 | 0 | 0 |

- No se detectaron códigos duplicados dentro de una misma página.
- Las métricas evalúan códigos, tarifa y unidad en páginas con referencia.
- Las descripciones solo se comprueban por presencia de texto.
- Los controles de San Vicente p54 y Santa Fe p44 quedan separados;
  sus referencias aún no están guardadas en CSV.
- No se evalúan las salidas enriquecidas con transcripciones.
- Medellín sigue pendiente de extracción.
- Métricas provisionales, con revisión humana de referencias pendiente.
