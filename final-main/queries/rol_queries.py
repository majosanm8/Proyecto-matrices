# -*- coding: utf-8 -*-

# consulta principal por rol
QUERY_BUSCAR_ROL = """
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
WHERE rol = :rol
  AND aplicativo = :aplicativo
ORDER BY usuario
"""


# obtener lista de aplicativos
QUERY_OBTENER_APLICATIVOS = """
SELECT DISTINCT aplicativo
FROM usuarios
WHERE aplicativo IS NOT NULL AND aplicativo != ''
ORDER BY aplicativo
"""

QUERY_OBTENER_ROLES_POR_APP = """
SELECT DISTINCT rol
FROM usuarios
WHERE LOWER(aplicativo) = LOWER(:aplicativo)
  AND rol IS NOT NULL AND rol != ''
ORDER BY rol
"""