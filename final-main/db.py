# -*- coding: utf-8 -*-
import logging
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# 🔹 Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Cargar .env solo si existe (local), en Render no existe y está bien
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    logger.info(f"✅ .env cargado desde: {dotenv_path}")
else:
    logger.info("ℹ️ Sin archivo .env — usando variables de entorno del sistema (Render)")

# 🔹 Engine global (singleton)
_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = _crear_engine()
    return _engine


def _crear_engine():
    # Lee de os.environ primero (Render), luego del .env (local)
    database_url = os.environ.get("DATABASE_URL") or os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("❌ DATABASE_URL no está definida. Configúrala en Render > Environment o en el .env local")

    # Ocultar contraseña en logs
    safe_url = database_url.split("@")[-1] if "@" in database_url else database_url
    logger.info(f"🔌 Conectando a: {safe_url}")

    engine_kwargs = {
        "echo": False,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "connect_args": {
            "sslmode": "require"  # Obligatorio para Supabase
        }
    }

    if not database_url.startswith("sqlite"):
        engine_kwargs.update({
            "pool_size": 10,
            "max_overflow": 5,
            "pool_timeout": 30,
        })

    try:
        engine = create_engine(database_url, **engine_kwargs)

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        logger.info("✅ Conexión a la base de datos establecida correctamente")
        return engine

    except Exception as e:
        logger.critical(f"❌ Error al conectar a la DB: {e}")
        raise SQLAlchemyError(f"Error de conexión: {e}") from e