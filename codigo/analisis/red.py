"""Métricas de red de una corrida: entrega y latencia de cada tipo de mensaje y calidad de las consultas.

Lee mensajes.csv, reportes.csv, consultas.csv y estimaciones_red.csv. Solo cuenta lo enviado antes de
simTime - --margen, para no tomar como perdido lo que no alcanzó a llegar porque la simulación terminó.

Uso:
  ~/tools/ns3ai-venv/bin/python analisis/red.py resultados/<corrida> [--margen 5]

Escribe <corrida>/resumen_red.csv e imprime el resumen.
"""

import argparse
import csv
import math
from pathlib import Path

import numpy as np

TIPOS = {"R": "reporte", "V": "relevo", "E": "intercambio", "Q": "consulta", "A": "respuesta",
         "X": "cruda"}


def _leer(carpeta: Path, nombre: str) -> list[dict]:
    with open(carpeta / nombre) as f:
        return list(csv.DictReader(f))


def _num(v: str) -> float:
    return float(v) if v != "" else math.nan


def _estad(valores: list[float], prefijo: str) -> dict:
    v = np.array([x for x in valores if not math.isnan(x)])
    return {
        f"{prefijo}_mediana": float(np.median(v)) if len(v) else math.nan,
        f"{prefijo}_p90": float(np.percentile(v, 90)) if len(v) else math.nan,
    }


def resumir_red(corrida: Path, margen: float = 5.0) -> dict:
    params = {}
    for linea in (corrida / "parametros.txt").read_text().splitlines():
        clave, _, valor = linea.partition("=")
        params[clave] = float(valor)
    limite = params["simTime"] - margen
    r: dict = {}

    # Mensajes por tipo (salto de aplicación). Los locales (origen == destino) no pasan por la red.
    mensajes = [m for m in _leer(corrida, "mensajes.csv") if float(m["t_envio"]) < limite]
    for letra, nombre in TIPOS.items():
        red = [m for m in mensajes if m["tipo"] == letra and m["origen"] != m["destino"]]
        llegaron = [m for m in red if m["t_llegada"] != ""]
        r[f"{nombre}_enviados"] = len(red)
        r[f"{nombre}_entrega"] = len(llegaron) / len(red) if red else math.nan
        r.update(_estad([float(m["t_llegada"]) - float(m["t_envio"]) for m in llegaron],
                        f"{nombre}_latencia_s"))
    r["bytes_aplicacion"] = sum(int(m["bytes"]) for m in mensajes if m["origen"] != m["destino"])

    # Lectura -> cabeza de zona, extremo a extremo (incluye el retardo aleatorio antes de enviar).
    reportes = [x for x in _leer(corrida, "reportes.csv") if float(x["t_lectura"]) < limite]
    llegaron = [x for x in reportes if x["t_en_cabeza_zona"] != ""]
    r["lecturas"] = len(reportes)
    r["lecturas_entrega"] = len(llegaron) / len(reportes) if reportes else math.nan
    r.update(_estad([float(x["t_en_cabeza_zona"]) - float(x["t_lectura"]) for x in llegaron],
                    "lecturas_latencia_s"))

    # Estimaciones en las cabezas de zona.
    est = _leer(corrida, "estimaciones_red.csv")
    validas = [e for e in est if e["valida"] == "1"]
    r["estimaciones_red_disponibilidad"] = len(validas) / len(est) if est else math.nan
    r.update(_estad([float(e["error_m"]) for e in validas], "estimaciones_red_error_m"))

    # Consultas del dueño.
    consultas = [q for q in _leer(corrida, "consultas.csv") if float(q["t_envio"]) < limite]
    respondidas = [q for q in consultas if q["t_respuesta"] != ""]
    con_est = [q for q in respondidas if q["con_estimacion"] == "1"]
    r["consultas"] = len(consultas)
    r["consultas_respondidas"] = len(respondidas) / len(consultas) if consultas else math.nan
    r["consultas_exito"] = len(con_est) / len(consultas) if consultas else math.nan
    r.update(_estad([float(q["t_respuesta"]) - float(q["t_envio"]) for q in respondidas],
                    "consultas_rtt_s"))
    r.update(_estad([float(q["t_respuesta"]) - float(q["t_estimacion"]) for q in con_est],
                    "respuesta_edad_s"))
    r.update(_estad([_num(q["error_m"]) for q in con_est], "respuesta_error_m"))

    with open(corrida / "resumen_red.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(r.keys()))
        w.writeheader()
        w.writerow(r)
    return r


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("corrida", type=Path)
    ap.add_argument("--margen", type=float, default=5.0)
    args = ap.parse_args()
    r = resumir_red(args.corrida, args.margen)

    print(args.corrida)
    print(f"{'mensaje':<13}{'enviados':>9}{'entrega':>9}{'lat. med.':>11}{'lat. p90':>10}")
    for nombre in TIPOS.values():
        print(f"{nombre:<13}{r[f'{nombre}_enviados']:>9}{r[f'{nombre}_entrega']:>9.1%}"
              f"{r[f'{nombre}_latencia_s_mediana'] * 1000:>9.1f}ms{r[f'{nombre}_latencia_s_p90'] * 1000:>8.0f}ms")
    print(f"lecturas -> cabeza de zona: {r['lecturas_entrega']:.1%} de {r['lecturas']}, "
          f"mediana {r['lecturas_latencia_s_mediana']:.3f} s")
    print(f"estimaciones en la red: disponibles {r['estimaciones_red_disponibilidad']:.1%}, "
          f"error mediano {r['estimaciones_red_error_m_mediana']:.1f} m")
    print(f"consultas: {r['consultas']}, respondidas {r['consultas_respondidas']:.1%}, "
          f"con estimación {r['consultas_exito']:.1%}, rtt mediano {r['consultas_rtt_s_mediana'] * 1000:.0f} ms, "
          f"edad mediana {r['respuesta_edad_s_mediana']:.1f} s, error mediano {r['respuesta_error_m_mediana']:.1f} m")


if __name__ == "__main__":
    main()
