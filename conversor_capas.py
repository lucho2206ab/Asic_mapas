import geopandas as gpd
from pathlib import Path

DATA_DIR = Path("static/data")

SOURCE_CRS = "EPSG:22182"   # POSGAR Gauss Kruger Faja 2
TARGET_CRS = "EPSG:4326"    # WGS84

for file in DATA_DIR.glob("DerSuperfNuevo.geojson"):

    if file.stem.endswith("_wgs84"):
        continue

    print("Procesando:", file.name)

    gdf = gpd.read_file(file)

    # asignar CRS si no tiene
    gdf = gdf.set_crs(SOURCE_CRS, allow_override=True)

    # reproyectar
    gdf_wgs = gdf.to_crs(TARGET_CRS)

    output = file.with_name(file.stem + "_wgs84.geojson")

    gdf_wgs.to_file(output, driver="GeoJSON")

    print("✔ convertido:", output)