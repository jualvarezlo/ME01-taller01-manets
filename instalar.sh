#!/usr/bin/env bash
# Instala ns-3 3.46.1 para el taller y deja todo listo para correr codigo/.
#
#   ./instalar.sh [carpeta]        por defecto ~/ns3
#
# Variables opcionales:
#   NS3_TARBALL=/ruta/ns-allinone-3.46.1.tar.bz2   usar un archivo ya descargado
#   SIN_NS3AI=1                                     compilar sin ns3-ai aunque estén sus dependencias
#
# Qué hace (ver INSTALACION.md):
#   1. revisa las dependencias;
#   2. descarga y descomprime ns-allinone-3.46.1;
#   3. crea el entorno de Python en .venv/;
#   4. enlaza codigo/ como scratch/manets dentro de ns-3;
#   5. configura y compila solo los módulos que usa el taller;
#   6. escribe entorno.sh;
#   7. corre una simulación corta de prueba.
set -euo pipefail

VERSION=3.46.1
URL="https://www.nsnam.org/releases/ns-allinone-$VERSION.tar.bz2"
MODULOS="core;network;internet;mobility;wifi;propagation;aodv;olsr;dsdv;netanim"

repo="$(cd "$(dirname "$0")" && pwd)"
destino="${1:-$HOME/ns3}"
mkdir -p "$destino"
destino="$(cd "$destino" && pwd)"
so="$(uname -s)"

paso() { printf '\n==> %s\n' "$*"; }
falla() { printf '\nERROR: %s\n' "$*" >&2; exit 1; }

# ------------------------------------------------------------------ 1. dependencias
paso "Revisando dependencias"
faltan=()
for cmd in python3 cmake c++ tar bzip2; do
    command -v "$cmd" >/dev/null || faltan+=("$cmd")
done
command -v curl >/dev/null || command -v wget >/dev/null || faltan+=("curl")
python3 -m venv --help >/dev/null 2>&1 || faltan+=("python3-venv")
if [ ${#faltan[@]} -gt 0 ]; then
    echo "Faltan: ${faltan[*]}"
    if [ "$so" = "Darwin" ]; then
        echo "Instalar con:  xcode-select --install && brew install cmake ninja python"
    else
        echo "Instalar con:  sudo apt install g++ cmake ninja-build python3 python3-dev python3-venv curl bzip2"
    fi
    exit 1
fi

generador=()
if command -v ninja >/dev/null; then
    generador=(-G Ninja)
else
    echo "Aviso: no hay ninja; se compila con make (más lento)."
fi

# ns3-ai necesita Boost, protobuf y pybind11. Si faltan, se instala sin ns3-ai.
con_ns3ai=0
if [ "${SIN_NS3AI:-0}" != "1" ]; then
    incluir=(/usr/include /usr/local/include /opt/homebrew/include)
    hay() { for d in "${incluir[@]}"; do [ -e "$d/$1" ] && return 0; done; return 1; }
    if hay boost/interprocess/managed_shared_memory.hpp && hay pybind11/pybind11.h \
        && command -v protoc >/dev/null; then
        con_ns3ai=1
        MODULOS="$MODULOS;ai"
    else
        echo "Aviso: faltan dependencias de ns3-ai; se instala sin él (no habrá --estimator=python)."
        if [ "$so" = "Darwin" ]; then
            echo "  Para tenerlo:  brew install boost protobuf pybind11   y volver a correr este script."
        else
            echo "  Para tenerlo:  sudo apt install libboost-all-dev libprotobuf-dev protobuf-compiler pybind11-dev"
            echo "                 y volver a correr este script."
        fi
    fi
fi

# ------------------------------------------------------------------ 2. ns-3
ns3="$destino/ns-allinone-$VERSION/ns-$VERSION"
if [ -d "$ns3" ]; then
    paso "ns-3 ya está en $ns3"
else
    tarball="${NS3_TARBALL:-$destino/ns-allinone-$VERSION.tar.bz2}"
    if [ ! -f "$tarball" ]; then
        paso "Descargando $URL (~80 MB)"
        if command -v curl >/dev/null; then
            curl -fL -o "$tarball" "$URL"
        else
            wget -O "$tarball" "$URL"
        fi
    fi
    paso "Descomprimiendo en $destino"
    tar -xjf "$tarball" -C "$destino"
fi
[ -x "$ns3/ns3" ] || falla "no encuentro $ns3/ns3"

# ------------------------------------------------------------------ 3. Python
paso "Creando el entorno de Python en $repo/.venv"
[ -d "$repo/.venv" ] || python3 -m venv "$repo/.venv"
"$repo/.venv/bin/pip" install -q --upgrade pip
"$repo/.venv/bin/pip" install -q -r "$repo/codigo/requirements.txt"
python_venv="$repo/.venv/bin/python"

# ------------------------------------------------------------------ 4. enlace
enlace="$ns3/scratch/manets"
if [ -e "$enlace" ] && [ ! -L "$enlace" ]; then
    falla "$enlace ya existe y no es un enlace simbólico; muévalo y vuelva a correr."
fi
ln -sfn "$repo/codigo" "$enlace"
paso "Enlazado: $enlace -> $repo/codigo"

# ------------------------------------------------------------------ 5. compilar
paso "Configurando ns-3 (módulos: $MODULOS)"
cd "$ns3"
# NS3_FAST_LINKERS=OFF: en macOS, el lld de Homebrew no sabe enlazar contra libc++ del sistema.
./ns3 configure "${generador[@]}" --enable-modules="$MODULOS" \
    -- -DNS3_FAST_LINKERS=OFF -DPython_EXECUTABLE="$python_venv" -DPython3_EXECUTABLE="$python_venv"
paso "Compilando (la primera vez tarda varios minutos)"
./ns3 build scratch/manets/collar-sim

# ------------------------------------------------------------------ 6. entorno.sh
cat >"$repo/entorno.sh" <<EOF
# Generado por instalar.sh. Uso, en cada terminal nueva:  source entorno.sh
export NS3_DIR="$ns3"
source "$repo/.venv/bin/activate"
EOF

# ------------------------------------------------------------------ 7. prueba
paso "Prueba: 30 s de simulación"
prueba="$repo/codigo/resultados/prueba-instalacion"
"$repo/codigo/simular" --simTime=30 --outDir="$prueba"
if [ "$con_ns3ai" = "1" ]; then
    paso "Prueba de ns3-ai: el estimador en Python"
    NS3_DIR="$ns3" "$python_venv" "$repo/codigo/analisis/ns3ai_estimador.py" -- --simTime=30 \
        --outDir="$prueba-ns3ai"
fi

paso "Listo"
echo "ns-3:     $ns3"
echo "ns3-ai:   $([ "$con_ns3ai" = "1" ] && echo sí || echo no)"
echo
echo "En cada terminal nueva, desde la raíz del repositorio:"
echo "  source entorno.sh"
echo "  cd codigo"
echo "  ./simular --help"
