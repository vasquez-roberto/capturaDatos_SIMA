# Red SIMA Monterrey API (ETL & GIS Pipeline)

Pipeline de extracción, procesamiento, clasificación normativa y exportación espacial para los datos de calidad del aire ($PM_{10}$ y $PM_{2.5}$) de las 15 estaciones del **Sistema Integral de Monitoreo Ambiental (SIMA)** de la Zona Metropolitana de Monterrey.

---

## 🔬 ¿Cómo se Recolectan los Datos? (Mecanismo de Extracción)

En lugar de utilizar scrapers basados en navegadores pesados (como Playwright o Selenium) que renderizan mapas JS interactivos, este sistema realiza consultas HTTP ligeras directamente a la arquitectura asíncrona del servidor institucional del SIMA:

1. **Inicialización de Sesión HTTP:** El script `descargar_sima_definitivo.py` simula la navegación a `ReporteDiariosimaIcars_L3.php?estacion1={CODIGO}` para establecer las cookies de sesión requeridas por el servidor.
2. **Consulta al Endpoint JSON Interno:** Mediante la misma sesión, se consulta el endpoint interno `api_conc_correcto.php?estacion1={CODIGO}` que alimenta dinámicamente las tablas DataTables del portal oficial.
3. **Parsing Directo:** Se extraen las concentraciones horarias de $PM_{10}$ y $PM_{2.5}$ en un arreglo JSON nativo, reduciendo el tiempo total de ejecución de las 15 estaciones a menos de 2 segundos y eliminando la necesidad de parsing complejo con expresiones regulares.

---

## 🛠️ Estructura del Pipeline

- **`descargar_sima_definitivo.py`**: Recorre las 15 estaciones oficiales y exporta las lecturas crudas a `sima_lecturas_estaciones.csv`.
- **`generar_geojson.py`**: Lee la captura reciente, evalúa la concentración según la norma de calidad del aire (Bueno, Aceptable, Mala, Muy mala, Extremadamente mala) y genera la capa espacial `sima_estaciones.geojson` (EPSG:4326) formateada para ArcGIS.
- **`actualizar_historico.py`**: Anexa las lecturas capturadas al archivo acumulativo permanente `sima_historico.csv` junto a una marca de tiempo fija (`timestamp`).

---

## 📐 Clasificación de Calidad del Aire Incorporada

### $PM_{2.5}$ ($\mu g/m^3$)
- **$\le 15$**: Bueno
- **$16 - 33$**: Aceptable
- **$34 - 79$**: Mala
- **$80 - 130$**: Muy mala
- **$> 130$**: Extremadamente mala

### $PM_{10}$ ($\mu g/m^3$)
- **$\le 45$**: Bueno
- **$46 - 60$**: Aceptable
- **$61 - 132$**: Mala
- **$133 - 213$**: Muy mala
- **$> 213$**: Extremadamente mala

---

## 🚀 Ejecución Local

```powershell
# Instalar dependencias
pip install requests pandas numpy

# Ejecutar el flujo en secuencia
py descargar_sima_definitivo.py
py generar_geojson.py
py actualizar_historico.py
