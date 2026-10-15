# Red SIMA Monterrey API

Pipeline en Python para la extracción, estructuración, exportación a **GeoJSON (ArcGIS)** y almacenamiento histórico acumulativo de lecturas de $PM_{10}$ y $PM_{2.5}$ de las 15 estaciones del SIMA en la Zona Metropolitana de Monterrey.

---

## 📁 Archivos del Proyecto

- **`descargar_sima_definitivo.py`**: Descarga las lecturas en vivo desde la API interna (`api_conc_correcto.php`) y genera `sima_lecturas_estaciones.csv`.
- **`generar_geojson.py`**: Convierte el CSV a `sima_estaciones.geojson` (EPSG:4326) listo para capas en ArcGIS Online / Pro.
- **`actualizar_historico.py`**: Asigna marca temporal (`timestamp`) y anexa las 15 lecturas al archivo acumulativo `sima_historico.csv`.

---

## 🛠️ Ejecución Local

```powershell
# 1. Instalar dependencias necesarias
pip install requests pandas

# 2. Correr el flujo completo en orden
py descargar_sima_definitivo.py
py generar_geojson.py
py actualizar_historico.py
