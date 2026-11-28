# NLP Tarifas ICA

Proyecto académico para extraer candidatos de actividades económicas,
códigos CIIU y tarifas ICA desde archivos PDF con texto extraíble.

El flujo actual no utiliza OCR. Incluye extractores específicos para
Guayabetal, San Vicente Ferrer, San Francisco y Santa Fe de Antioquia.
Las tablas de Medellín permanecen pendientes de extracción.
Los resultados son candidatos pendientes de revisión.

## Requisitos

- Python 3.13.
- Poetry 2.
- VS Code con soporte para notebooks de Jupyter.

## Instalación

Desde la carpeta raíz del repositorio:

```bash
poetry config virtualenvs.in-project true --local
poetry env use python3.13
poetry install
```

Si Python 3.13 no se encuentra con ese nombre, indicar la ruta de su
ejecutable en el comando `poetry env use`.

Las dependencias se gestionan mediante `pyproject.toml` y `poetry.lock`.

## Organización

| Ruta | Contenido |
|---|---|
| `src/nlp_tarifas_ica/lectura_pdf.py` | Lectura de texto por página |
| `src/nlp_tarifas_ica/normalizacion.py` | Normalización de espacios y saltos de línea |
| `src/nlp_tarifas_ica/segmentacion.py` | Segmentación por encabezados de artículos |
| `src/nlp_tarifas_ica/extraccion_tablas.py` | Extractores de Guayabetal y San Vicente Ferrer |
| `src/nlp_tarifas_ica/extraccion_san_francisco.py` | Extractor de San Francisco |
| `src/nlp_tarifas_ica/extraccion_santa_fe.py` | Extractor de Santa Fe de Antioquia |
| `scripts/` | Ejecución por lote y evaluación |
| `docs/estado_validacion_pdfs.md` | Estado consolidado de validación |
| `src/nlp_tarifas_ica/exportacion.py` | Exportación a CSV y JSON |
| `src/nlp_tarifas_ica/validacion.py` | Comparación con una referencia transcrita |
| `notebooks/01_flujo_principal.ipynb` | Ejecución del flujo y evaluación |
| `data/raw/` | PDF de entrada, almacenados localmente |
| `data/processed/` | Resultados generados, almacenados localmente |
| `data/referencia/` | Referencia utilizada para la evaluación |

Los notebooks originales de la raíz se conservan como antecedentes
exploratorios. El punto de entrada del flujo modular es
`notebooks/01_flujo_principal.ipynb`.

## Ejecución

1. Colocar el documento de entrada en `data/raw/` con el nombre:
   `Guayabetal_2021_31Diciembre_resolucion-no-010.pdf`.
2. Abrir `notebooks/01_flujo_principal.ipynb`.
3. Seleccionar el intérprete de `.venv` como kernel.
4. Reiniciar el kernel y seleccionar **Ejecutar todo**.

El PDF debe obtenerse por separado: los archivos de `data/raw/`
y los resultados de `data/processed/` están excluidos de Git.

El notebook lee el PDF, extrae candidatos, muestra una vista previa,
exporta los resultados y evalúa la página 9 contra la referencia.

La segmentación de artículos está disponible como módulo independiente.
La extracción de la tabla de Guayabetal utiliza posiciones del texto
y no depende de encontrar encabezados de artículos.

## Salidas

Se generan en `data/processed/`:

- `candidatos_guayabetal.csv`
- `candidatos_guayabetal.json`

Cada candidato conserva el archivo, la página, el código de actividad,
el CIIU, una descripción parcial, la tarifa candidata, la unidad,
la evidencia textual y el estado de revisión.

Las tarifas no recuperadas se conservan como `null` en JSON
y como campos vacíos en CSV. Los candidatos requieren revisión humana.

## Evaluación de desarrollo

Se transcribieron 35 registros de la página 9 del documento
de Guayabetal en `data/referencia/referencia_manual.csv`.
La identificación del revisor está pendiente de completar.

La comparación exige coincidencia de archivo, página, código de
actividad, CIIU, tarifa y unidad. Las descripciones no se evalúan.
Los duplicados se cuentan por ocurrencia.

Los candidatos sin tarifa se consideran abstenciones. Si su registro
esperado no se recupera mediante otra predicción completa, cuenta
como falso negativo. Una predicción completa con tarifa incorrecta
produce un falso positivo y deja un falso negativo.

| Indicador | Resultado |
|---|---:|
| Registros de referencia | 35 |
| Verdaderos positivos | 31 |
| Falsos positivos | 0 |
| Falsos negativos | 4 |
| Candidatos sin tarifa | 4 |
| Precisión sobre predicciones completas | 100,00 % |
| Recall | 88,57 % |
| F1 | 93,94 % |

Esta página ya se utilizó para diagnosticar el extractor y constituye
una muestra de desarrollo. Los resultados no representan una prueba
independiente ni permiten generalizar a otros documentos.

## Ejecución por lote y evaluación consolidada

Desde la raíz del proyecto, con los PDF disponibles en data/raw/:

    poetry run python scripts/extraer_san_vicente.py
    poetry run python scripts/extraer_san_francisco.py
    poetry run python scripts/extraer_santa_fe.py
    poetry run python scripts/evaluar_extractores.py

La evaluación consolidada ejecuta los cuatro extractores automáticos,
incluido Guayabetal. Los nombres de los PDF deben coincidir con los
registrados en los CSV de referencia.

Genera data/processed/evaluacion_extractores.json.

### Resultados reproducibles

| Documento | Candidatos | Sin tarifa | Descripciones vacías | Páginas evaluadas | VP / FP / FN | F1 |
|---|---:|---:|---:|---|---|---:|
| Guayabetal | 439 | 17 | 70 | 9 | 31 / 0 / 4 | 93,94 % |
| San Vicente Ferrer | 468 | 0 | 0 | 38, 39 y 42 | 88 / 0 / 0 | 100 % |
| San Francisco | 45 | 0 | 0 | 46–49 | 45 / 0 / 0 | 100 % |
| Santa Fe de Antioquia | 468 | 0 | 0 | 29 y 30 | 49 / 0 / 0 | 100 % |

Los conteos corresponden al lote completo. Las métricas evalúan códigos,
tarifa y unidad exclusivamente en las páginas indicadas.
No se detectaron códigos duplicados dentro de una misma página.

Los controles adicionales de San Vicente p54 y Santa Fe p44 quedan
separados: sus referencias aún no están guardadas en CSV.
Las métricas son provisionales y las referencias requieren revisión
humana registrada. No constituyen una prueba independiente.

### Enriquecimiento de Guayabetal

    poetry run python scripts/enriquecer_guayabetal.py

Genera data/processed/guayabetal_enriquecido.csv y .json.
Conserva los valores automáticos originales y añade 17 tarifas propuestas
mediante transcripciones visuales, con su procedencia.
No quedan tarifas propuestas vacías; las 17 tarifas automáticas
ausentes permanecen identificables.

Las propuestas transcritas no son predicciones automáticas.
No evaluar esta salida contra las referencias usadas para completarla.
La revisión humana sigue pendiente.

### Experimentos de descripciones

    poetry run python scripts/evaluar_descripciones_guayabetal.py

Compara el extractor actual con el método experimental por bloques
sobre ocho descripciones seleccionadas.
Los métodos por bloques y por centros permanecen experimentales
y no sustituyen al extractor principal.

Consultar docs/diagnostico_guayabetal.md para los resultados y límites.

## Limitaciones y trabajo pendiente

- Se utiliza texto nativo, sin OCR. Su presencia no garantiza que
  todas las filas, tarifas o descripciones sean recuperables.
- Los extractores están adaptados a formatos concretos.
- Guayabetal conserva 17 tarifas automáticas ausentes y
  70 descripciones vacías, además de textos parciales y errores de caracteres.
- La presencia o longitud de una descripción no demuestra integridad.
- Las descripciones solo tienen evaluaciones sobre muestras seleccionadas.
- Medellín permanece pendiente de extracción de tablas y sin métricas.
- Falta completar y registrar la revisión humana de las referencias.
- Se requiere ampliar la evaluación a páginas y documentos independientes.
- Las métricas de extracción no validan los clasificadores exploratorios.
- Los candidatos y las propuestas enriquecidas no son datos aprobados.

Consultar docs/estado_validacion_pdfs.md para el alcance de cada documento.
