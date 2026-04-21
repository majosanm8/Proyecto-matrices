import logging
from flask import Blueprint, render_template, request, jsonify
from services.rol_service import buscar_por_rol
from repositories.rol_repository import (
    repo_obtener_aplicativos,
    repo_obtener_roles_por_app
)
logger = logging.getLogger(__name__)
rol_bp = Blueprint("rol", __name__)


@rol_bp.route("/rol", methods=["GET","POST"])
def consulta_rol():

    resultados = []
    error = None
    aplicativo_val = ""
    rol_val = ""

    aplicativos = repo_obtener_aplicativos()

    if request.method == "POST":

        aplicativo_val = request.form.get("aplicativo","").strip()
        rol_val = request.form.get("rol","").strip()

        if not aplicativo_val or not rol_val:
            error = "Por favor, complete ambos campos: Aplicativo y Rol."
        else:
            try:
                resultados = buscar_por_rol(rol_val, aplicativo_val)
            except Exception as e:
                logger.error("Error al buscar por Rol: '%s' en Aplicativo: '%s'", rol_val, aplicativo_val, exc_info=True)
                error = "Ocurrió un error al realizar la búsqueda."

    return render_template(
        "consulta_rol.html",
        resultados=resultados,
        aplicativos=aplicativos,
        aplicativo_val=aplicativo_val,
        rol_val=rol_val,
        error=error
    )


@rol_bp.route("/api/roles/<path:aplicativo>")
def api_roles(aplicativo):
    try:
        roles = repo_obtener_roles_por_app(aplicativo)
        return jsonify(roles)
    except Exception as e:
        logger.error("Error al obtener roles para Aplicativo: '%s'", aplicativo, exc_info=True)
        roles = []
        return jsonify([]), 500


