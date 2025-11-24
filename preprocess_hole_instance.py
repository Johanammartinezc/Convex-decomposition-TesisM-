import numpy as np

def read_outer_inner(path):
    outer = []
    inner = []
    mode = None
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            low = line.lower()
            if low == "outer":
                mode = "outer"
                continue
            if low == "inner":
                mode = "inner"
                continue
            x, y = map(float, line.split())
            if mode == "outer":
                outer.append((x, y))
            elif mode == "inner":
                inner.append((x, y))
    return np.array(outer), np.array(inner)

def build_simple_polygon(outer, inner):
    """
    Construye un polígono simple conectando outer e inner con un puente.
    Estrategia simple (pero válida en nuestros ejemplos convexos):
    - Elegimos el vértice del outer con mayor x.
    - Elegimos el vértice del inner con mayor x.
    - Conectamos outer_max -> inner_max -> recorre inner en sentido horario
      -> vuelve a outer_max.
    """
    # índice de mayor x en outer e inner
    i_o = np.argmax(outer[:, 0])
    i_i = np.argmax(inner[:, 0])

    # outer ccw tal cual
    outer_cycle = outer.tolist()

    # reordenamos inner para iniciar en i_i
    inner_cycle = inner.tolist()
    inner_cycle = inner_cycle[i_i:] + inner_cycle[:i_i]
    # y lo invertimos para cambiar el sentido
    inner_cycle = inner_cycle[::-1]

    O = outer_cycle
    I = inner_cycle

    # polígono simple: recorro outer completo, luego puente, luego inner, luego de vuelta
    # Representación típica:
    # O[0..i_o], O[i_o]→I[0], I[0..], I[-1]→O[i_o], O[i_o..fin]
    simple = []

    # 1) parte de outer desde 0 hasta i_o
    simple.extend(O[:i_o+1])

    # 2) puente a inner
    simple.append(I[0])

    # 3) recorrer inner completo
    simple.extend(I[1:])

    # 4) volver a outer_max (cierra el "corridor")
    simple.append(O[i_o])

    # 5) resto del outer desde i_o+1 hasta el final
    simple.extend(O[i_o+1:])

    return np.array(simple)

def write_simple_polygon(simple_coords, path_out):
    with open(path_out, "w") as f:
        for x, y in simple_coords:
            f.write(f"{x:.4f}\t{y:.4f}\n")

if __name__ == "__main__":
    # ejemplo para inst10
    in_path = "inst10.txt"
    out_path = "inst10_simple.txt"

    outer, inner = read_outer_inner(in_path)
    simple = build_simple_polygon(outer, inner)
    write_simple_polygon(simple, out_path)
    print(f"Polígono simple guardado en {out_path}")
