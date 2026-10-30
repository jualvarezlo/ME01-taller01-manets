"""Corre collar-sim con el estimador de las cabezas de zona en Python, conectado por ns3-ai.

Este script crea la memoria compartida, lanza la simulación con --estimator=python y atiende cada
petición de estimación con localizar.estimar(): la misma función que usa el análisis fuera de línea.
Mientras Python calcula, la simulación está detenida.

Uso (desde codigo/):
  python analisis/ns3ai_estimador.py -- --outDir=resultados/demo-py [...]

Todo lo que va después de "--" se pasa a collar-sim.
"""

import argparse
import os
import subprocess
import sys
import threading
import uuid
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from localizar import METODOS, estimar  # noqa: E402
from rutas import BINARIO, CODIGO, NS3_DIR, absolutizar  # noqa: E402

sys.path.insert(0, str(CODIGO / "ns3ai"))
import collar_ns3ai_py as ns3ai  # noqa: E402

TAM_MEMORIA = 1 << 20  # la Peticion ocupa ~19 KB; el valor por defecto de ns3-ai (4 KB) no alcanza


def estimar_peticion(p) -> np.ndarray | None:
    """Arma la ventana con el formato de localizar.py (t, observador, x, y, rssi) y estima."""
    ventana = np.column_stack([p.t_lectura(), p.observador().astype(float), p.x(), p.y(), p.rssi()])
    return estimar(ventana.reshape(-1, 5), p.p0, p.n)[METODOS[p.metodo]]


def correr(args_sim: list[str], trial: str | None = None) -> tuple[int, int]:
    """Lanza la simulación y atiende sus peticiones. Devuelve (código de salida, peticiones)."""
    trial = trial or f"collar_{os.getpid()}_{uuid.uuid4().hex[:8]}"
    seg = f"ns3-ai_{trial}"  # mismo nombre que arma Ns3AiMsgInterface::BuildSegmentName()
    iface = ns3ai.Ns3AiMsgInterfaceImpl(True, False, True, TAM_MEMORIA, seg, seg + "2py",
                                        seg + "2cpp", seg + "lock")
    # Van al final para que ningún --conf (base.conf trae estimator = cpp) los pise.
    proc = subprocess.Popen([str(BINARIO), *args_sim, "--estimator=python", f"--ns3aiTrial={trial}"],
                            cwd=NS3_DIR)

    # Si la simulación muere sin avisar que terminó, PyRecvBegin esperaría para siempre.
    terminado = threading.Event()

    def vigilar() -> None:
        rc = proc.wait()
        if not terminado.wait(5.0):
            print(f"ns3ai_estimador: collar-sim terminó (código {rc}) sin cerrar ns3-ai", file=sys.stderr)
            os._exit(rc or 1)

    threading.Thread(target=vigilar, daemon=True).start()

    peticiones = 0
    while True:
        iface.PyRecvBegin()
        if iface.PyGetFinished():
            break
        pos = estimar_peticion(iface.GetCpp2PyStruct())
        iface.PyRecvEnd()

        iface.PySendBegin()
        r = iface.GetPy2CppStruct()
        r.valida = int(pos is not None)
        r.x, r.y = (float(pos[0]), float(pos[1])) if pos is not None else (0.0, 0.0)
        iface.PySendEnd()
        peticiones += 1

    terminado.set()
    rc = proc.wait()
    del iface  # el creador borra la memoria compartida
    return rc, peticiones


def main() -> None:
    argv = sys.argv[1:]
    args_sim = []
    if "--" in argv:
        args_sim = absolutizar(argv[argv.index("--") + 1:])
        argv = argv[:argv.index("--")]
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trial", default=None, help="nombre de la memoria compartida (por defecto, uno único)")
    args = ap.parse_args(argv)

    rc, peticiones = correr(args_sim, args.trial)
    print(f"ns3ai_estimador: {peticiones} peticiones atendidas en Python", flush=True)
    sys.exit(rc)


if __name__ == "__main__":
    main()
