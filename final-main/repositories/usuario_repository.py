# -*- coding: utf-8 -*-
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from db import get_engine
from queries.usuario_queries import QUERY_BUSCAR_USUARIO

logger = logging.getLogger(__name__)


def repo_buscar_usuario(usuario: str) -> list[dict]:
    """
    Busca usuarios por coincidencia parcial (LIKE)
    """
    try:
        if not usuario:
            return []

        # 🔹 Sanitización segura
        busqueda = f"%{(usuario or '').strip()}%"

        params = {
            "usuario": busqueda
        }

        # 🔹 Uso de transacción (mejor práctica)
        with get_engine().begin() as conn:
            resultado = conn.execute(text(QUERY_BUSCAR_USUARIO), params)
            rows = [dict(row._mapping) for row in resultado]

        return rows

    except SQLAlchemyError as e:
        logger.error("❌ Error consultando usuario: %s", e, exc_info=True)
        raise RuntimeError("Error al consultar usuario") from e