# Extracción y validación: San Francisco

## Alcance
- Páginas PDF evaluadas: 46–49.
- Método: texto nativo por líneas y respaldo por coordenadas, sin OCR.
- Referencia: 45 registros transcritos de capturas del PDF.
- Resultado: 45 coincidencias, 0 falsos positivos y 0 falsos negativos.
- Precisión, recall y F1: 100 % para código, tarifa y unidad.
- Todas estas páginas se utilizaron durante el desarrollo.
- No constituye una prueba independiente del desempeño en otros documentos.

## Correcciones
- Evita confundir descripciones que empiezan por "Actividades" con títulos.
- Detiene la lectura al comenzar los parágrafos.
- Recupera por columnas las tarifas cuyo texto aparece desordenado.

## Limitaciones y pendientes
- Las descripciones no tienen una evaluación completa.
- Código 315: el texto nativo dice "intemet"; la imagen muestra "internet".
- Código 402: falta el paréntesis de cierre en el texto recuperado.
- La regla general sin código del parágrafo 1 y los descuentos no se extraen.
- Falta registrar al revisor humano de las referencias.
- Falta una prueba independiente y comprobar la página siguiente.
- Las salidas de data/processed están excluidas de Git.
