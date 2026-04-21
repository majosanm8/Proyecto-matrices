# -*- coding: utf-8 -*-



def formatear_resultados(filas: list[dict])-> list[dict]:
    
    if not filas:
        return []
    
    for r in filas:
        if "identificacion" in r and r ["identificacion"] is not None:
            try:
                r["identificacion"] =str(int(r["identificacion"]))
            except(ValueError, TypeError):
                r["identificacion"] =str(r["identificacion"])
                

    return filas
