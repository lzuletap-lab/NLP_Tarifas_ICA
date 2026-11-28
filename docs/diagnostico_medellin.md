# Diagnóstico de extracción: Medellín

## Archivo
Antioquia - Medellin_Acuerdo_67_2008_15_de_diciembre.pdf

## Evidencia
- Página PDF 9: 2809 caracteres, 403 palabras y una tabla detectada.
- Se recupera el título del artículo 51.
- No se recuperan las filas industriales visibles en la captura.
- Página PDF 10: 100 caracteres, 4 palabras y una tabla detectada.
- Solo se recuperan el encabezado y el número impreso 11.
- La tabla detectada contiene celdas vacías.

## Conclusión
El contenido de las tablas de tarifas no se recupera con la lectura
de texto nativo utilizada actualmente.
Detectar texto o bordes de tabla no demuestra que sus filas sean legibles.
No se ha determinado la causa interna de esta limitación del PDF.

## Estado
Pendiente de extracción. No equivale a ausencia de tarifas en el documento.
No se han calculado métricas de precisión, recall o F1 para Medellín.

## Alcance
- No se utiliza OCR.
- No se asignan tarifas de otros municipios.
- Una transcripción manual debe identificarse como tal y mantenerse
  separada de los resultados de extracción automática.
- Las páginas se identifican por su posición en el PDF, que puede diferir
  del número impreso.
