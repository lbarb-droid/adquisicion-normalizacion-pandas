"""Consolidación reproducible de 50.000 transacciones y 500 productos."""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
DATOS = BASE / "datos"
SALIDA = BASE / "salida" / "ventas_normalizadas.parquet"


def procesar():
    ventas = pd.read_csv(DATOS / "ventas.csv", dtype={"id_producto": "string"})
    productos = pd.read_excel(DATOS / "productos.xlsx", engine="openpyxl", dtype={"id_producto": "string"})
    print(f"Transacciones originales: {len(ventas):,}; productos: {len(productos):,}")

    ventas["id_producto"] = ventas["id_producto"].str.strip()
    productos["id_producto"] = productos["id_producto"].str.strip()
    ventas["fecha"] = pd.to_datetime(ventas["fecha"], errors="coerce")
    ventas["cantidad"] = pd.to_numeric(ventas["cantidad"], errors="coerce")
    productos["precio_unitario"] = pd.to_numeric(productos["precio_unitario"], errors="coerce")

    productos = productos.dropna(subset=["id_producto", "nombre_producto", "precio_unitario"])
    productos = productos[productos["precio_unitario"] > 0].copy()
    if productos["id_producto"].duplicated().any():
        raise ValueError("El catálogo contiene IDs de producto duplicados")

    ventas = ventas.dropna(subset=["id_producto", "cantidad", "fecha"]).copy()
    ventas = ventas[ventas["cantidad"] > 0].copy()
    ventas["cantidad"] = ventas["cantidad"].astype("int64")

    resultado = ventas.merge(productos, on="id_producto", how="left", validate="many_to_one", indicator=True)
    sin_catalogo = int((resultado["_merge"] == "left_only").sum())
    resultado = resultado[resultado["_merge"] == "both"].drop(columns="_merge").copy()
    resultado["total_venta"] = (resultado["cantidad"] * resultado["precio_unitario"]).round(2)
    criticos = ["id_producto", "cantidad", "fecha", "nombre_producto", "precio_unitario", "total_venta"]
    assert not resultado[criticos].isna().any().any(), "Hay nulos en campos críticos"
    assert pd.api.types.is_datetime64_any_dtype(resultado["fecha"])
    assert len(resultado) > 0

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    resultado.to_parquet(SALIDA, engine="pyarrow", index=False)
    comprobacion = pd.read_parquet(SALIDA)
    assert len(comprobacion) == len(resultado)
    print(f"Ventas sin producto en catálogo: {sin_catalogo:,}")
    print(f"Transacciones válidas exportadas: {len(resultado):,}")
    print(f"Total vendido: ${resultado['total_venta'].sum():,.2f}")
    print(f"Parquet generado: {SALIDA}")


if __name__ == "__main__":
    procesar()
