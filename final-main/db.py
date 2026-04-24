# -*- coding: utf-8 -*-
import logging
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# 🔹 Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Cargar .env desde la raíz del proyecto
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    logger.info(f"✅ .env cargado desde: {dotenv_path}")
else:
    logger.warning(f"⚠️ No se encontró .env en {dotenv_path}")

# 🔹 Engine global (singleton)
_engine = None


def get_engine():
    """
    Retorna una instancia única del engine (singleton).
    """
    global _engine

    if _engine is None:
        _engine = _crear_engine()

    return _engine


def _crear_engine():
    """
    Crea y valida la conexión a la base de datos.
    """
    # Forzar recarga de variables de entorno
    load_dotenv(dotenv_path, override=True)
    database_url = os.getenv("DATABASE_URL")

    # 🔹 Validación obligatoria
    if not database_url:
        raise ValueError("❌ DATABASE_URL no está definida en el .env")

    # 🔹 Seguridad: ocultar contraseña en logs
    safe_url = database_url.split("@")[-1] if "@" in database_url else database_url
    logger.info(f"🔌 Intentando conectar a: {safe_url}")

    # 🔹 Configuración del engine
    engine_kwargs = {
        "echo": False,              # Cambia a True si quieres ver queries
        "pool_pre_ping": True,      # Verifica conexiones muertas
        "pool_recycle": 3600,       # Recicla conexiones cada 1 hora
        "connect_args": {
            "sslmode": "require"    # 🔥 OBLIGATORIO para Supabase
        }
    }

    # 🔹 Configuración de pool solo si no es SQLite
    if not database_url.startswith("sqlite"):
        engine_kwargs.update({
            "pool_size": 10,
            "max_overflow": 5,
            "pool_timeout": 30,
        })

    try:
        engine = create_engine(database_url, **engine_kwargs)

        # 🔹 Validar conexión
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        logger.info("✅ Conexión a la base de datos establecida correctamente")
        return engine

    except Exception as e:
        logger.critical(f"❌ Error crítico al conectar a la DB: {e}")
        raise SQLAlchemyError(f"Error de conexión: {e}") from e