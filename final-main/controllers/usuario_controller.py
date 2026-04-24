# -*- coding: utf-8 -*-
import logging
from flask import Blueprint, render_template, request

from services.usuario_service import buscar_por_usuario

logger = logging.getLogger(__name__)

usuario_bp = Blueprint("usuario", __name__)


@usuario_bp.route("/consulta-usuario", methods=["GET", "POST"])
def consulta_usuario():

    resultados = []
    error = None
    usuario_val = ""

    if request.method == "POST":

        usuario_val = (request.form.get("usuario") or "").strip()

        if not usuario_val:
            error = "Debe ingresar un usuario"
        else:
            try:
                resultados = buscar_por_usuario(usuario_val)

                # 🔹 Feedback si no hay resultados
                if not resultados:
                    error = "No se encontraron coincidencias"

            except Exception as e:
                logger.error("Error consultando usuario: %s", e, exc_info=True)
                error = "Ocurrió un error al consultar"

    return render_template(
        "consulta_usuario.html",
        resultados=resultados,
        usuario_val=usuario_val,
        error=error
    )