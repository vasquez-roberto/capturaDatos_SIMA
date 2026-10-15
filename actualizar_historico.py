from datetime import datetime
import os
import pandas as pd

print("Actualizando archivo de lecturas históricas de la Red SIMA...")

ARCHIVO_LECTURAS = "sima_lecturas_estaciones.csv"
ARCHIVO_HISTORICO = "sima_historico.csv"

try:
  if not os.path.exists(ARCHIVO_LECTURAS):
    print(
        f"Error: No existe el archivo de lectura actual '{ARCHIVO_LECTURAS}'."
    )
  else:
    # 1. Cargar la captura actual
    df_actual = pd.read_csv(ARCHIVO_LECTURAS)

    # 2. Generar timestamp redondeado a la hora fija
    fecha_hora_captura = datetime.now().strftime("%Y-%m-%d %H:00:00")
    df_actual["timestamp"] = fecha_hora_captura

    # Reorganizar columnas
    columnas_orden = [
        "timestamp",
        "clave",
        "zona",
        "municipio",
        "pm10_ugm3",
        "pm25_ugm3",
        "pm10_num",
        "pm25_num",
        "lat",
        "lon",
    ]

    df_a_guardar = df_actual[columnas_orden]

    # 3. Anexar o crear el historico acumulativo
    if not os.path.exists(ARCHIVO_HISTORICO):
      df_a_guardar.to_csv(
          ARCHIVO_HISTORICO, index=False, encoding="utf-8-sig"
      )
      print(
          f"Se creó el archivo histórico '{ARCHIVO_HISTORICO}' con"
          f" {len(df_a_guardar)} registros."
      )
    else:
      df_a_guardar.to_csv(
          ARCHIVO_HISTORICO,
          mode="a",
          header=False,
          index=False,
          encoding="utf-8-sig",
      )
      print(
          f"Se anexaron {len(df_a_guardar)} registros a '{ARCHIVO_HISTORICO}'"
          f" ({fecha_hora_captura})."
      )

    print("--------------------------------------------------")
    print("Histórico actualizado exitosamente.")
    print("--------------------------------------------------")

except Exception as e:
  print(f"Ocurrió un error actualizando el histórico: {e}")