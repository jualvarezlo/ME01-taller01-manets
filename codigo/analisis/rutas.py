"""Rutas compartidas por los scripts de análisis.

La carpeta de ns-3 (la que tiene el script ./ns3) sale de la variable de entorno NS3_DIR. Si no está
definida, se lee de entorno.sh, que instalar.sh deja en la raíz del repositorio.
"""

import os
import re
import sys
from pathlib import Path

CODIGO = Path(__file__).resolve().parent.parent
REPO = CODIGO.parent


def _buscar_ns3_dir() -> Path:
    valor = os.environ.get("NS3_DIR")
    entorno = REPO / "entorno.sh"
    if not valor and entorno.exists():
        m = re.search(r'^export NS3_DIR="?([^"\n]+)"?', entorno.read_text(), re.MULTILINE)
        valor = m.group(1) if m else None
    if not valor:
        sys.exit("No encuentro ns-3. Corre ./instalar.sh (ver INSTALACION.md) o define NS3_DIR "
                 "con la ruta a la carpeta ns-3.46.1.")
    ruta = Path(valor).expanduser()
    if not (ruta / "ns3").exists():
        sys.exit(f"NS3_DIR={ruta} no parece una carpeta de ns-3 (no tiene el script ./ns3).")
    return ruta


def _buscar_binario(ns3_dir: Path) -> Path:
    # El nombre depende de la versión y del perfil de compilación (default, debug, optimized).
    candidatos = sorted((ns3_dir / "build/scratch/manets").glob("ns3.*-collar-sim-*"),
                        key=lambda p: p.stat().st_mtime, reverse=True)
    return candidatos[0] if candidatos else ns3_dir / "build/scratch/manets/ns3.46.1-collar-sim-default"


NS3_DIR = _buscar_ns3_dir()
BINARIO = _buscar_binario(NS3_DIR)

RUTAS_EN_ARGS = ("--conf=", "--outDir=")


def absolutizar(args: list[str]) -> list[str]:
    """La simulación corre con cwd = NS3_DIR: convierte --conf= y --outDir= relativos en absolutos
    respecto a la carpeta desde donde se llamó el script."""
    salida = []
    for a in args:
        for prefijo in RUTAS_EN_ARGS:
            if a.startswith(prefijo) and not Path(a[len(prefijo):]).is_absolute():
                a = prefijo + str(Path(a[len(prefijo):]).resolve())
        salida.append(a)
    return salida
