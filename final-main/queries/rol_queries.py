# -*- coding: utf-8 -*-

# 🔎 Consulta principal por rol + aplicativo
QUERY_BUSCAR_ROL = """
SELECT
    usuario,
    cargo,
    area,
    dependencia,
    rol,
    aplicativo
FROM usuarios
WHERE LOWER(rol) = LOWER(:rol)
  AND LOWER(aplicativo) = LOWER(:aplicativo)
ORDER BY usuario
"""


# 📂 Lista de aplicativos únicos (para UI)
QUERY_OBTENER_APLICATIVOS = """
SELECT DISTINCT aplicativo
FROM usuarios
WHERE aplicativo IS NOT NULL
  AND aplicativo <> ''
ORDER BY aplicativo
"""


# 📌 Roles por aplicativo
QUERY_OBTENER_ROLES_POR_APP = """
SELECT DISTINCT rol
FROM usuarios
WHERE LOWER(aplicativo) = LOWER(:aplicativo)
  AND rol IS NOT NULL
  AND rol <> ''
ORDER BY rol
"""