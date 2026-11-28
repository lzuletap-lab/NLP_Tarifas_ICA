# NLP Tarifas ICA

Proyecto académico para extraer candidatos de actividades económicas,
códigos CIIU y tarifas ICA desde archivos PDF con texto extraíble.

El flujo actual no utiliza OCR. El extractor de tablas está configurado
para el formato del documento de Guayabetal.

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
| `src/nlp_tarifas_ica/extraccion_tablas.py` | Extracción de candidatos del formato Guayabetal |
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

## Limitaciones y trabajo pendiente

- Se procesa únicamente texto extraíble de PDF, sin OCR.
- Las páginas sin texto no pueden procesarse mediante este flujo.
- Las posiciones de las columnas están configuradas para Guayabetal.
- Algunas descripciones quedan incompletas o vacías.
- Algunas tarifas no se recuperan.
- Los 439 candidatos obtenidos del documento completo no constituyen
  una medida de precisión ni de cobertura.
- Falta completar y registrar la revisión humana de la referencia.
- Se requiere ampliar la referencia a páginas y documentos independientes.
- Falta evaluar otros formatos y la calidad de las descripciones.
- Las métricas anteriores evalúan extracción; no validan los
  clasificadores exploratorios de los notebooks originales.
