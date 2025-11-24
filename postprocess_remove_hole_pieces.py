import numpy as np

from preprocess_hole_instance import read_outer_inner  # reutilizamos la lectura
import Leertxt_caract
import Auxvarios
import FuncionesN  # o Funciones, según uses en esta rama
import SCcompletanuevo1  # este módulo ejecuta y deja colltodos com la partición

def point_in_polygon(point, poly):
    """
    Test sencillo punto-en-polígono (ray casting).
    poly: array (k,2) con vértices en orden.
    """
    x, y = point
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        # revisa intersección con rayo horizontal
        cond = ( (y1 > y) != (y2 > y) )
        if cond:
            x_int = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x_int > x:
                inside = not inside
    return inside

def centroid_of_indices(indices, x, y):
    """
    Tus piezas se guardan usualmente como índices en colltodos.
    Calculamos el centroide geométrico de esos puntos.
    """
    xs = [x[i] for i in indices]
    ys = [y[i] for i in indices]
    return (sum(xs)/len(xs), sum(ys)/len(ys))

def get_final_pieces_excluding_hole(inst_txt):
    # 1. Leer outer/inner originales
    outer, inner = read_outer_inner(inst_txt)
    inner_poly = inner  # np.array

    # 2. Ejecutar tu pipeline sobre inst10_simple.txt
    #    Asumimos que Auxvarios.archivonum ya apunta al *_simple.txt.
    vertices,lineas,collnotches,lista0,angulito,filas,x,y,convenoconve,sentiang,opuesto = \
        Leertxt_caract.leertxt(Auxvarios.aordenar, Auxvarios.archivonum)

    # Importar módulo que corre todo (ya ejecuta al importar) y deja colltodos
    import SCcompletanuevo1  # noqa: F401

    # Ahora deberíamos tener colltodos en algún sitio:
    from SCcombi import colltodos  # ajusta esto según dónde quede realmente

    final_pieces = []
    for piece in colltodos:
        # piece: lista de índices enteros (como en tu código)
        cx, cy = centroid_of_indices(piece, x, y)
        if not point_in_polygon((cx, cy), inner_poly):
            final_pieces.append(piece)

    return final_pieces, outer, inner_poly, x, y
