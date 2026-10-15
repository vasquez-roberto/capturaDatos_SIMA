import json
import pandas as pd

print("Generando GeoJSON a partir de 'sima_lecturas_estaciones.csv'...")

try:
  # 1. Leer el CSV recien generado
  df = pd.read_csv("sima_lecturas_estaciones.csv")

  features = []

  # 2. Construir objetos Feature para GIS
  for _, row in df.iterrows():
    pm10 = None if pd.isna(row.get("pm10_num")) else float(row.get("pm10_num"))
    pm25 = None if pd.isna(row.get("pm25_num")) else float(row.get("pm25_num"))

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(row["lon"]), float(row["lat"])],
        },
        "properties": {
            "zona": str(row["zona"]),
            "municipio": str(row["municipio"]),
            "clave": str(row["clave"]),
            "estacion_param": str(row["estacion_param"]),
            "pm10_ugm3": (
                str(row["pm10_ugm3"]) if not pd.isna(row["pm10_ugm3"]) else "ND"
            ),
            "pm25_ugm3": (
                str(row["pm25_ugm3"]) if not pd.isna(row["pm25_ugm3"]) else "ND"
            ),
            "pm10_num": pm10,
            "pm25_num": pm25,
        },
    }
    features.append(feature)

  # 3. Estructura FeatureCollection (EPSG:4326)
  geojson_data = {
      "type": "FeatureCollection",
      "crs": {
          "type": "name",
          "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"},
      },
      "features": features,
  }

  # 4. Guardar en disco
  NOMBRE_GEOJSON = "sima_estaciones.geojson"
  with open(NOMBRE_GEOJSON, "w", encoding="utf-8") as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=2)

  print("--------------------------------------------------")
  print(f"Éxito: Archivo GeoJSON generado en '{NOMBRE_GEOJSON}'.")
  print("Listo para importar en capas de ArcGIS Online / Pro.")
  print("--------------------------------------------------")

except FileNotFoundError:
  print("Error: No se encontró 'sima_lecturas_estaciones.csv'.")
except Exception as e:
  print(f"Ocurrió un error al generar el GeoJSON: {e}")