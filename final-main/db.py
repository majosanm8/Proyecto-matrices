# -*- coding: utf-8 -*-
import logging
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# 🔹 Obtener la ruta del directorio donde está este archivo (db.py)
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, ".env")

# 🔹 Cargar variables de entorno desde la ruta específica
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"✅ .env cargado desde: {dotenv_path}")
else:
    print(f"⚠️ No se encontró .env en {dotenv_path}")

logger = logging.getLogger(__name__)

# Engine global (singleton)
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
    database_url = os.getenv("DATABASE_URL")

    # 🔹 Fallback para desarrollo
    if not database_url:
        logger.warning("DATABASE_URL no definida, usando SQLite por defecto")
        database_url = "sqlite:///dev.db"

    # Argumentos base para el engine
    engine_kwargs = {
        "echo": True,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
    }

    # 🔹 Solo agregar pool_size y max_overflow si NO es SQLite
    if not database_url.startswith("sqlite"):
        engine_kwargs.update({
            "pool_size": 20,
            "max_overflow": 10,
            "pool_timeout": 30,
        })

    logger.info("Intentando conectar a: %s", database_url.split('@')[-1] if '@' in database_url else database_url)

    try:
        engine = create_engine(database_url, **engine_kwargs)

        # 🔹 Validar conexión de forma explícita
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            # En SQLAlchemy 2.0+ algunas operaciones pueden requerir commit explícito
            # aunque SELECT 1 no lo necesite, es buena práctica si se usa con transacciones.
            
        logger.info("✅ Conexión a la base de datos establecida correctamente")
        return engine

    except Exception as e:
        logger.critical("❌ No se pudo conectar a la base de datos: %s", e)
        # Si falla el engine, podemos intentar retornar un engine de fallback o simplemente fallar
        raise SQLAlchemyError(f"Error crítico de conexión: {e}") from e