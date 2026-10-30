"""Rutas compartidas por los scripts de análisis."""

from pathlib import Path

NS3_DIR = Path.home() / "tools/ns-allinone-3.46.1/ns-3.46.1"
BINARIO = NS3_DIR / "build/scratch/manets/ns3.46.1-collar-sim-default"
CODIGO = Path(__file__).resolve().parent.parent

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
