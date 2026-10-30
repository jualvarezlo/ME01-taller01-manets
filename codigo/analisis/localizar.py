"""Estima la posición del collar a partir de rssi.csv y la compara con la verdad (posiciones.csv).

Métodos, evaluados cada --paso segundos con las lecturas de la ventana (t - --ventana, t]:
  cercano      línea base tipo Find My: posición GPS del celular con el RSSI más alto.
  centroide    centroide de las posiciones GPS ponderado por potencia lineal (mW).
  trilateracion mínimos cuadrados no lineales sobre distancias d = 10^((P0 - RSSI) / (10 n)),
               pesos 1/d^2, Gauss-Newton desde el centroide. Necesita >= 3 celulares distintos.

Uso:
  python analisis/localizar.py resultados/<corrida> [--paso 5] [--ventana 10]

Escribe <corrida>/estimaciones.csv y <corrida>/resumen.csv, e imprime el resumen.
"""

import argparse
import csv
import math
from pathlib import Path

import numpy as np

METODOS = ("cercano", "centroide", "trilateracion")


def leer_parametros(carpeta: Path) -> dict:
    params = {}
    for linea in (carpeta / "parametros.txt").read_text().splitlines():
        clave, _, valor = linea.partition("=")
        params[clave] = float(valor)
    return params


def leer_lecturas(carpeta: Path) -> np.ndarray:
    """Columnas: t, observador, gps_x, gps_y, rssi_dbm."""
    filas = []
    with open(carpeta / "rssi.csv") as f:
        for r in csv.DictReader(f):
            filas.append((float(r["t"]), int(r["observador"]), float(r["gps_x"]),
                          float(r["gps_y"]), float(r["rssi_dbm"])))
    return np.array(filas, dtype=float).reshape(-1, 5)


def leer_verdad(carpeta: Path) -> tuple[np.ndarray, np.ndarray]:
    """Trayectoria del collar: tiempos y posiciones (x, y)."""
    t, xy = [], []
    with open(carpeta / "posiciones.csv") as f:
        for r in csv.DictReader(f):
            if r["rol"] == "collar":
                t.append(float(r["t"]))
                xy.append((float(r["x"]), float(r["y"])))
    return np.array(t), np.array(xy)


def verdad_en(t_verdad: np.ndarray, xy_verdad: np.ndarray, t: float) -> np.ndarray:
    return np.array([np.interp(t, t_verdad, xy_verdad[:, 0]),
                     np.interp(t, t_verdad, xy_verdad[:, 1])])


def rssi_a_distancia(rssi: np.ndarray, p0: float, n: float) -> np.ndarray:
    return 10 ** ((p0 - rssi) / (10 * n))


def trilaterar(anclas: np.ndarray, dist: np.ndarray, inicio: np.ndarray,
               iteraciones: int = 50) -> np.ndarray | None:
    """Gauss-Newton para min sum w_i (||x - a_i|| - d_i)^2 con w_i = 1/d_i^2."""
    w = 1.0 / np.maximum(dist, 1.0) ** 2
    x = inicio.astype(float).copy()
    for _ in range(iteraciones):
        diff = x - anclas
        r = np.linalg.norm(diff, axis=1)
        r = np.maximum(r, 1e-6)
        residuo = r - dist
        jac = diff / r[:, None]
        jtw = jac.T * w
        a = jtw @ jac
        if np.linalg.cond(a) > 1e8:  # geometría degenerada (anclas casi colineales o juntas)
            return None
        paso = np.linalg.solve(a, -jtw @ residuo)
        x += paso
        if np.linalg.norm(paso) < 1e-3:
            break
    return x


def estimar(ventana: np.ndarray, p0: float, n: float) -> dict:
    """ventana: filas (t, observador, gps_x, gps_y, rssi)."""
    est = {m: None for m in METODOS}
    if len(ventana) == 0:
        return est
    xy = ventana[:, 2:4]
    rssi = ventana[:, 4]

    est["cercano"] = xy[np.argmax(rssi)]

    peso = 10 ** (rssi / 10)  # mW
    centro = (xy * peso[:, None]).sum(axis=0) / peso.sum()
    est["centroide"] = centro

    if len(np.unique(ventana[:, 1])) >= 3:
        est["trilateracion"] = trilaterar(xy, rssi_a_distancia(rssi, p0, n), centro)
    return est


def analizar(corrida: Path, paso: float = 5.0, ventana: float = 10.0,
             p0: float | None = None, n: float | None = None) -> list[dict]:
    """Estima, escribe estimaciones.csv y resumen.csv en la corrida y devuelve el resumen."""
    params = leer_parametros(corrida)
    p0 = p0 if p0 is not None else params["collarTxDbm"] - params["refLossDb"]
    n = n if n is not None else params["pathLossExp"]

    lecturas = leer_lecturas(corrida)
    t_verdad, xy_verdad = leer_verdad(corrida)
    t_fin = params["simTime"]

    filas = []
    t = ventana
    while t <= t_fin + 1e-9:
        en_ventana = lecturas[(lecturas[:, 0] > t - ventana) & (lecturas[:, 0] <= t)]
        previas = lecturas[lecturas[:, 0] <= t]
        frescura = t - previas[:, 0].max() if len(previas) else math.inf
        verdad = verdad_en(t_verdad, xy_verdad, t)
        n_obs = len(np.unique(en_ventana[:, 1])) if len(en_ventana) else 0
        for metodo, pos in estimar(en_ventana, p0, n).items():
            err = float(np.linalg.norm(pos - verdad)) if pos is not None else math.nan
            filas.append({
                "t": round(t, 3), "metodo": metodo,
                "x": pos[0] if pos is not None else math.nan,
                "y": pos[1] if pos is not None else math.nan,
                "verdad_x": verdad[0], "verdad_y": verdad[1], "error_m": err,
                "lecturas": len(en_ventana), "observadores": n_obs, "frescura_s": frescura,
            })
        t += paso

    with open(corrida / "estimaciones.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    resumen = []
    for metodo in METODOS:
        errores = np.array([f["error_m"] for f in filas if f["metodo"] == metodo])
        validos = errores[~np.isnan(errores)]
        frescura = np.array([f["frescura_s"] for f in filas if f["metodo"] == metodo])
        frescura = frescura[np.isfinite(frescura)]
        resumen.append({
            "metodo": metodo,
            "estimaciones": len(errores),
            "disponibilidad": len(validos) / len(errores) if len(errores) else 0.0,
            "error_medio_m": validos.mean() if len(validos) else math.nan,
            "error_mediana_m": np.median(validos) if len(validos) else math.nan,
            "error_p90_m": np.percentile(validos, 90) if len(validos) else math.nan,
            "frescura_media_s": frescura.mean() if len(frescura) else math.nan,
        })
    with open(corrida / "resumen.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(resumen[0].keys()))
        w.writeheader()
        w.writerows(resumen)
    return resumen


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("corrida", type=Path)
    ap.add_argument("--paso", type=float, default=5.0, help="cada cuántos segundos se estima")
    ap.add_argument("--ventana", type=float, default=10.0, help="segundos de lecturas que se usan")
    ap.add_argument("--p0", type=float, default=None,
                    help="RSSI a 1 m (dBm); por defecto collarTxDbm - refLossDb de la corrida")
    ap.add_argument("--n", type=float, default=None,
                    help="exponente de pérdida; por defecto el de la corrida")
    args = ap.parse_args()

    resumen = analizar(args.corrida, args.paso, args.ventana, args.p0, args.n)
    print(f"{args.corrida}  (paso={args.paso}s, ventana={args.ventana}s)")
    print(f"{'metodo':<14}{'disp.':>7}{'media':>9}{'mediana':>9}{'p90':>9}{'fresc.':>8}")
    for r in resumen:
        print(f"{r['metodo']:<14}{r['disponibilidad']:>7.2f}{r['error_medio_m']:>9.1f}"
              f"{r['error_mediana_m']:>9.1f}{r['error_p90_m']:>9.1f}{r['frescura_media_s']:>8.2f}")


if __name__ == "__main__":
    main()
