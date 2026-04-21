QUERY_BUSCAR_USUARIO = """
    SELECT
        usuario,
        identificacion,
        nombre_completo,
        cargo,
        area,
        dependencia,
        rol,
        aplicativo
    FROM usuarios
    WHERE LOWER(usuario) LIKE LOWER(:usuario)
       OR LOWER(nombre_completo) LIKE LOWER(:usuario)
       OR CAST(identificacion AS TEXT) LIKE :usuario
    ORDER BY aplicativo
"""
# -*- coding: utf-8 -*-

