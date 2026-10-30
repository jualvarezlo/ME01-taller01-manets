# Instalación

Sirve para macOS y para Ubuntu. En Windows hay que usar Ubuntu dentro de WSL, porque ns-3 no compila en
Windows directamente.

Lo probamos de cero en un Mac con Apple silicon el 29 de octubre de 2026 y tardó 2 minutos con 13 núcleos.
En un portátil de 4 núcleos cuenten de 5 a 10 minutos. En Ubuntu todavía no lo ha probado nadie. Si a alguien
le falla, que avise en el grupo con el error.

## 1. Dependencias del sistema

macOS, con [Homebrew](https://brew.sh):

```bash
xcode-select --install
brew install cmake ninja python boost protobuf pybind11
```

Ubuntu, o Ubuntu en WSL:

```bash
sudo apt update
sudo apt install g++ cmake ninja-build python3 python3-dev python3-venv curl bzip2 git \
    libboost-all-dev libprotobuf-dev protobuf-compiler pybind11-dev
```

Boost, protobuf y pybind11 son para ns3-ai. Sin ellos todo funciona igual, menos el estimador en Python
(`--estimator=python`).

Para instalar WSL en Windows, abran PowerShell como administrador, corran `wsl --install`, reinicien y abran
"Ubuntu" desde el menú de inicio. Clonen el repositorio dentro de Ubuntu, por ejemplo en `~/`, y no en
`/mnt/c/...`: desde las carpetas de Windows ns-3 compila muchísimo más lento.

## 2. Clonar y correr el instalador

```bash
git clone https://github.com/mbuitragocUNAL/ME01-taller01-manets.git
cd ME01-taller01-manets
./instalar.sh
```

ns-3 queda en `~/ns3`. Para ponerlo en otra parte: `./instalar.sh ~/otra/carpeta`.

El script hace esto, en orden:
1. revisa que estén las dependencias y dice cómo instalar las que falten;
2. descarga ns-allinone-3.46.1, unos 80 MB, y lo descomprime;
3. crea un entorno de Python en `.venv/`, dentro del repositorio, con numpy y matplotlib;
4. enlaza la carpeta `codigo/` dentro de ns-3, en `scratch/manets`, que es donde ns-3 busca programas propios;
5. configura ns-3 con los módulos que usamos, y ns3-ai si están sus dependencias, y compila;
6. escribe `entorno.sh` con la ruta de ns-3 y la activación del entorno de Python;
7. corre una simulación de 30 s y, si hay ns3-ai, otra con el estimador en Python.

Si al final dice "Listo", quedó bien. Se puede correr otra vez sin problema: lo que ya está hecho no lo repite.

## 3. Uso diario

En cada terminal nueva, desde la raíz del repositorio:

```bash
source entorno.sh
cd codigo
./simular --help
```

Después de cambiar un `.cc` o un `.h`, `./compilar`. Cómo correr simulaciones y experimentos está en el
[README](README.md#correr).

## 4. NetAnim, opcional

NetAnim muestra la animación que la simulación escribe con `--netanim=true`. Desde ns-3.45 no viene en el
paquete, así que se compila aparte. Necesita Qt 5.

```bash
# macOS
brew install qt@5
# Ubuntu
sudo apt install qtbase5-dev qt5-qmake
```

```bash
git clone https://gitlab.com/nsnam/netanim.git ~/netanim
cd ~/netanim
git checkout netanim-3.110
mkdir build && cd build
cmake .. -G Ninja -DCMAKE_PREFIX_PATH="$(brew --prefix qt@5 2>/dev/null)" -DCMAKE_DISABLE_FIND_PACKAGE_Qt6=ON
ninja
./bin/netanim
```

En Ubuntu, `brew --prefix` no existe y esa parte queda vacía, que es lo que se necesita. Dentro de NetAnim,
abran el `netanim.xml` de la carpeta de resultados.

## Problemas conocidos

| Mensaje o síntoma | Qué hacer |
|---|---|
| `No encuentro ns-3` | Falta `source entorno.sh` en esa terminal, o no se ha corrido `./instalar.sh`. |
| `La simulación no está compilada` | `./compilar` desde `codigo/`. |
| `--estimator=python necesita ns3-ai` | ns-3 se compiló sin ns3-ai porque faltaba Boost, protobuf o pybind11. Instálenlos y corran `./instalar.sh` otra vez. |
| `could not load TAPI file … libc++.tbd: unknown architecture`, en macOS | Es el enlazador `lld` de Homebrew. `instalar.sh` ya lo desactiva con `-DNS3_FAST_LINKERS=OFF`; si configuran ns-3 a mano, agreguen esa opción. |
| `'messages.pb.h' file not found` al compilar | Una carrera en la compilación de ns3-ai. Vuelvan a correr `./compilar`. |
| Una corrida con `--estimator=python` que no termina | El lanzador corta la espera si la simulación muere sin avisar. Si aun así queda algo corriendo, `pkill -f collar-sim` lo detiene. |
