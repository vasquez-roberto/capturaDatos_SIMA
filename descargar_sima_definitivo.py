import json
import re
import pandas as pd
import requests

# Catálogo oficial de las 15 estaciones de la Red SIMA en el Área Metropolitana de Monterrey
ESTACIONES_SIMA = [
    {
        "param": "CENTRO",
        "zona": "CENTRO",
        "municipio": "Monterrey",
        "lat": 25.6760139,
        "lon": -100.338553,
        "clave": "CE",
    },
    {
        "param": "SURESTE",
        "zona": "SURESTE",
        "municipio": "Guadalupe",
        "lat": 25.6654972,
        "lon": -100.243653,
        "clave": "SE",
    },
    {
        "param": "NORESTE",
        "zona": "NORESTE",
        "municipio": "San Nicolás",
        "lat": 25.74503,
        "lon": -100.25317,
        "clave": "NE",
    },
    {
        "param": "NOROESTE",
        "zona": "NOROESTE",
        "municipio": "Monterrey",
        "lat": 25.7629306,
        "lon": -100.369578,
        "clave": "NO",
    },
    {
        "param": "SUROESTE",
        "zona": "SUROESTE",
        "municipio": "Santa Catarina",
        "lat": 25.6794444,
        "lon": -100.467831,
        "clave": "SO",
    },
    {
        "param": "GARCIA",
        "zona": "NOROESTE 2",
        "municipio": "García",
        "lat": 25.8004639,
        "lon": -100.585011,
        "clave": "NO2",
    },
    {
        "param": "NORTE",
        "zona": "NORTE",
        "municipio": "Escobedo",
        "lat": 25.7988361,
        "lon": -100.327164,
        "clave": "N",
    },
    {
        "param": "NORESTE2",
        "zona": "NORESTE 2",
        "municipio": "Apodaca",
        "lat": 25.777475,
        "lon": -100.1882,
        "clave": "NE2",
    },
    {
        "param": "SURESTE2",
        "zona": "SURESTE 2",
        "municipio": "Juárez",
        "lat": 25.646126,
        "lon": -100.095616,
        "clave": "SE2",
    },
    {
        "param": "[SAN Pedro]",
        "zona": "SUROESTE 2",
        "municipio": "San Pedro",
        "lat": 25.665275,
        "lon": -100.412853,
        "clave": "SO2",
    },
    {
        "param": "SURESTE3",
        "zona": "SURESTE 3",
        "municipio": "Cadereyta",
        "lat": 25.6008639,
        "lon": -99.9953028,
        "clave": "SE3",
    },
    {
        "param": "NORTE2",
        "zona": "NORTE 2",
        "municipio": "San Nicolás",
        "lat": 25.7297587,
        "lon": -100.310019,
        "clave": "N2",
    },
    {
        "param": "SUR",
        "zona": "SUR",
        "municipio": "Monterrey",
        "lat": 25.6169806,
        "lon": -100.273936,
        "clave": "S",
    },
    {
        "param": "PESQUERIA",
        "zona": "ESTE",
        "municipio": "Pesquería",
        "lat": 25.7905833,
        "lon": -100.078411,
        "clave": "NE3",
    },
    {
        "param": "NOROESTE3",
        "zona": "NOROESTE 3",
        "municipio": "García",
        "lat": 25.785,
        "lon": -100.46361112,
        "clave": "NO3",
    },
]

BASE_URL_REPORTE = (
    "https://aire.nl.gob.mx/SIMA2017reportes/ReporteDiariosimaIcars_L3.php"
)
BASE_URL_API_CONC = (
    "https://aire.nl.gob.mx/SIMA2017reportes/api_conc_correcto.php"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
}

registros = []

print("Descargando datos en vivo de las 15 estaciones mediante JSON directo...\n")

for est in ESTACIONES_SIMA:
  session = requests.Session()
  url_estacion = f"{BASE_URL_REPORTE}?estacion1={est['param']}"

  # Crear sesión e inicializar cookies de la estación
  session.get(url_estacion, headers=HEADERS, timeout=10)

  # Consultar la API interna de concentraciones
  url_json = f"{BASE_URL_API_CONC}?estacion1={est['param']}"
  resp_json = session.get(url_json, headers=HEADERS, timeout=10)

  pm10_val = None
  pm25_val = None

  try:
    data = resp_json.json()
    for item in data:
      param_nombre = str(item.get("Parameter", "")).upper()
      valor = item.get("HrAveData")

      if "PM10" in param_nombre:
        pm10_val = valor
      elif "PM2" in param_nombre or "PM25" in param_nombre:
        pm25_val = valor

    print(f"OK -> {est['zona']}: PM10 = {pm10_val}, PM2.5 = {pm25_val}")

  except Exception as e:
    print(f"Error procesando {est['zona']}: {e}")

  registros.append({
      "zona": est["zona"],
      "estacion_param": est["param"],
      "clave": est["clave"],
      "municipio": est["municipio"],
      "lat": est["lat"],
      "lon": est["lon"],
      "pm10_ugm3": pm10_val,
      "pm25_ugm3": pm25_val,
  })

# Convertir a DataFrame
df = pd.DataFrame(registros)

# Convertir columnas a numéricas para análisis (reemplaza 'ND' por valores vacíos NaN en numérico)
df["pm10_num"] = pd.to_numeric(df["pm10_ugm3"], errors="coerce")
df["pm25_num"] = pd.to_numeric(df["pm25_ugm3"], errors="coerce")

# Exportar el resultado a un archivo CSV en la carpeta local
NOMBRE_CSV = "sima_lecturas_estaciones.csv"
df.to_csv(NOMBRE_CSV, index=False, encoding="utf-8-sig")

print("\n--------------------------------------------------")
print(f"Extracción completada. Archivo CSV guardado: '{NOMBRE_CSV}'")
print("--------------------------------------------------")

# Imprimir la tabla formateada en consola
print(
    df[[
        "zona",
        "municipio",
        "clave",
        "pm10_ugm3",
        "pm25_ugm3",
        "lat",
        "lon",
    ]].to_string(index=False)
)