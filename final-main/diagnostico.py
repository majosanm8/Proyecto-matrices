# -*- coding: utf-8 -*-
from sqlalchemy import text
from db import get_engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("diagnostico")

def diagnosticar():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            # 1. Verificar si la tabla existe
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'usuarios'
                );
            """))
            existe = result.scalar()
            
            if not existe:
                logger.error("❌ La tabla 'usuarios' NO existe en la base de datos.")
                return

            # 2. Contar registros
            result = conn.execute(text("SELECT COUNT(*) FROM usuarios"))
            count = result.scalar()
            logger.info(f"✅ La tabla 'usuarios' existe y tiene {count} registros.")

            if count > 0:
                # 3. Mostrar una muestra con nombres de columnas
                result = conn.execute(text("SELECT * FROM usuarios LIMIT 5"))
                logger.info(f"Columnas detectadas: {result.keys()}")
                rows = result.fetchall()
                logger.info("Muestra de datos:")
                for row in rows:
                    logger.info(dict(row._mapping))
            else:
                logger.warning("⚠️ La tabla 'usuarios' está vacía. Debes ejecutar sync_excel.py.")

    except Exception as e:
        logger.error(f"❌ Error durante el diagnóstico: {e}")

if __name__ == "__main__":
    diagnosticar()
