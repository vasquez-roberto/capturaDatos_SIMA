import json
import numpy as np
import pandas as pd


def clasificar_calidad_aire_pm25(valor):
  if valor is None or (isinstance(valor, float) and np.isnan(valor)):
    return "Sin datos"
  if valor <= 15:
    return "Bueno"
  if valor <= 33:
    return "Aceptable"
  if valor <= 79:
    return "Mala"
  if valor <= 130:
    return "Muy mala"
  return "Extremadamente mala"


def clasificar_calidad_aire_pm10(valor):
  if valor is None or (isinstance(valor, float) and np.isnan(valor)):
    return "Sin datos"
  if valor <= 45:
    return "Bueno"
  if valor <= 60:
    return "Aceptable"
  if valor <= 132:
    return "Mala"
  if valor <= 213:
    return "Muy mala"
  return "Extremadamente mala"


print("Generando GeoJSON estructurado para ArcGIS...")

try:
  df = pd.read_csv("sima_lecturas_estaciones.csv")
  features = []

  for _, row in df.iterrows():
    pm10_val = (
        None if pd.isna(row.get("pm10_num")) else float(row.get("pm10_num"))
    )
    pm25_val = (
        None if pd.isna(row.get("pm25_num")) else float(row.get("pm25_num"))
    )

    nivel_pm10 = clasificar_calidad_aire_pm10(pm10_val)
    nivel_pm25 = clasificar_calidad_aire_pm25(pm25_val)

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(row["lon"]), float(row["lat"])],
        },
        "properties": {
            "Estacion": str(row["zona"]),
            "Clave": str(row["clave"]),
            "Zona": str(row["zona"]),
            "Municipio": str(row["municipio"]),
            "PM10_ugm3": pm10_val if pm10_val is not None else "ND",
            "PM10_Nivel": nivel_pm10,
            "PM25_ugm3": pm25_val if pm25_val is not None else "ND",
            "PM25_Nivel": nivel_pm25,
        },
    }
    features.append(feature)

  geojson_data = {
      "type": "FeatureCollection",
      "crs": {
          "type": "name",
          "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"},
      },
      "features": features,
  }

  NOMBRE_GEOJSON = "sima_estaciones.geojson"
  with open(NOMBRE_GEOJSON, "w", encoding="utf-8") as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=2)

  print("--------------------------------------------------")
  print(f"Éxito: GeoJSON generado correctamente en '{NOMBRE_GEOJSON}'.")
  print("Propiedades optimizadas para tarjetas/popups de ArcGIS.")
  print("--------------------------------------------------")

except FileNotFoundError:
  print("Error: No se encontró el archivo 'sima_lecturas_estaciones.csv'.")
except Exception as e:
  print(f"Ocurrió un error al generar el GeoJSON: {e}")
