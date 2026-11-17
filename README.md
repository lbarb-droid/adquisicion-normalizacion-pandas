# Adquisición y normalización con Pandas — 50.000 ventas

Proyecto educativo con datos **sintéticos** de una empresa comercial durante 2025.

## Contenido

- `datos/ventas.csv`: 50.000 transacciones con ID, producto, cantidad, fecha y canal.
- `datos/productos.xlsx`: catálogo de 500 productos, categoría y precio.
- `procesar_ventas.py`: limpieza, unión, validación, cálculo y exportación.
- `salida/ventas_normalizadas.parquet`: se genera al ejecutar el script.

## Requisitos

Python 3.12+ y librerías `pandas`, `openpyxl`, `pyarrow` (en `requirements.txt`).

## Ejecución en Windows (PowerShell)

1. Descomprimir el ZIP y abrir **esta carpeta** en VS Code.
2. Abrir la terminal y ejecutar:

```powershell
py -m pip install -r requirements.txt
py procesar_ventas.py
```

3. Comprobar el archivo `salida/ventas_normalizadas.parquet` y subirlo a GitHub junto con el resto del proyecto.

## Metodología

1. Cargar CSV y Excel con Pandas y OpenPyXL.
2. Homogeneizar `id_producto` como texto en ambas fuentes; convertir fechas a `datetime` y valores numéricos.
3. Excluir fechas, cantidades o IDs nulos; cantidades no positivas; productos con precios inválidos.
4. Hacer `merge` por `id_producto` con relación muchos-a-uno y registrar transacciones sin correspondencia.
5. Calcular `total_venta = cantidad * precio_unitario`.
6. Verificar ausencia de nulos en campos críticos, exportar a Parquet y volver a leer para comprobar.

## Calidad de datos

El CSV contiene errores sintéticos intencionales: fechas inválidas, cantidades vacías o negativas e IDs inexistentes. El script los trata antes de exportar. Los valores de ventas son ficticios, no representan una empresa real.

## Resultado

La cantidad final de registros es menor a 50.000 por la depuración de datos. El archivo Parquet **no está pre-generado en este ZIP**: requiere ejecutar el script con `pyarrow` instalado.
