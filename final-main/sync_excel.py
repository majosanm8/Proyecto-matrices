# -*- coding: utf-8 -*-
import pandas as pd
import os
import time
from sqlalchemy import text
from db import get_engine

# 📂 CAMBIA ESTA RUTA a la carpeta donde tienes TODOS los Excel en OneDrive
RUTA_CARPETA = r"C:\Users\USER\OneDrive - Universidad Libre\Consulta"

# 📥 Leer todos los Excel de la carpeta
def obtener_archivos():
    if not os.path.exists(RUTA_CARPETA):
        raise FileNotFoundError(f"No se encontró la carpeta: {RUTA_CARPETA}")

    archivos = [
        f for f in os.listdir(RUTA_CARPETA)
        if f.endswith(".xlsx") or f.endswith(".xls")
    ]

    if not archivos:
        print("⚠️ No se encontraron archivos Excel en la carpeta")

    return archivos


# 🧹 Limpiar datos de un archivo
def limpiar_datos(df, nombre_archivo):
    aplicativo = os.path.splitext(nombre_archivo)[0]  # SAP.xlsx → "SAP"
    print(f"🧹 Limpiando datos de: {aplicativo}")

    df = df.fillna("")

    df.columns = [
        "usuario",
        "cargo",
        "area",
        "dependencia",
        "rol",
        "aplicativo"
    ]

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    # Si la columna aplicativo viene vacía, la llenamos con el nombre del archivo
    df["aplicativo"] = df["aplicativo"].apply(
        lambda x: x if x and x != "nan" else aplicativo
    )

    return df


# 💾 Insertar en PostgreSQL (Supabase)
def insertar_datos(df, aplicativo):
    print(f"💾 Insertando {len(df)} registros de: {aplicativo}...")

    engine = get_engine()

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO usuarios (
                    usuario, cargo, area, dependencia, rol, aplicativo
                )
                VALUES (
                    :usuario, :cargo, :area, :dependencia, :rol, :aplicativo
                )
                ON CONFLICT (usuario)
                DO UPDATE SET
                    cargo = EXCLUDED.cargo,
                    area = EXCLUDED.area,
                    dependencia = EXCLUDED.dependencia,
                    rol = EXCLUDED.rol,
                    aplicativo = EXCLUDED.aplicativo
            """), row.to_dict())

    print(f"✅ {aplicativo} — insertado/actualizado correctamente")


# 🧠 Procesar todos los archivos de la carpeta
def main():
    archivos = obtener_archivos()
    total = len(archivos)
    print(f"\n📂 Se encontraron {total} archivo(s) Excel\n{'─'*40}")

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(RUTA_CARPETA, archivo)
        aplicativo = os.path.splitext(archivo)[0]
        print(f"\n[{i}/{total}] 📄 Procesando: {archivo}")

        try:
            df = pd.read_excel(ruta)
            df = limpiar_datos(df, archivo)
            insertar_datos(df, aplicativo)
        except Exception as e:
            print(f"❌ Error procesando {archivo}: {e}")
            continue

    print(f"\n{'─'*40}\n🎉 Sync completado: {total} archivo(s) procesados")


# 🔄 AUTO-SYNC — detecta cambios en cualquier archivo de la carpeta
def auto_sync(intervalo=30):
    print("🔄 Modo automático activado... revisando cada 30 segundos")
    estado_anterior = {}

    while True:
        try:
            archivos = obtener_archivos()
            hubo_cambios = False

            for archivo in archivos:
                ruta = os.path.join(RUTA_CARPETA, archivo)
                mod = os.path.getmtime(ruta)

                if estado_anterior.get(archivo) != mod:
                    print(f"\n📡 Cambio detectado: {archivo}")
                    aplicativo = os.path.splitext(archivo)[0]

                    try:
                        df = pd.read_excel(ruta)
                        df = limpiar_datos(df, archivo)
                        insertar_datos(df, aplicativo)
                        estado_anterior[archivo] = mod
                        hubo_cambios = True
                    except Exception as e:
                        print(f"❌ Error en {archivo}: {e}")

            if not hubo_cambios:
                print(".", end="", flush=True)

        except Exception as e:
            print(f"\n❌ Error general en sync: {e}")

        time.sleep(intervalo)


if __name__ == "__main__":
    # 👉 Ejecuta UNA vez todos los archivos:
    main()

    # 👉 O activa el modo automático (detecta cambios):
    # auto_sync()