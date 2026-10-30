# Taller 01 — Simulación de MANETs

**Vale 20 % (componente T).** Entrega: **miércoles 4 nov 2026, 11:59 pm.**
Enunciado completo: el correo del profesor del 5 oct; en la copia local, [enunciado.md](enunciado.md).

> **Para el equipo:**
> - [`codigo/`](codigo/): la simulación y el análisis. Cómo correrlo: sección «Código».
> - [`codigo/escenarios/base.conf`](codigo/escenarios/base.conf): todos los parámetros, para probar.
> - [`entregables/`](entregables/README.md): la estructura de los literales a–f y el correo de entrega.
> - En el repositorio **no van** `fuentes/` (libros y material del curso, con derechos de autor) ni
>   `enunciado.md` (trae los enlaces privados al Drive del curso); los tienen en el correo del profesor.

## Qué piden, en corto

- **Indagación** (pregunta de investigación, al estilo Newton) sobre **modelos de movilidad en MANET**.
  Dificultad intermedia. Responderla con el **método científico** (hipótesis → experimento → análisis).
- **Sistema MANET jerárquico:** ≥ 3 clústeres en el primer nivel y ≥ 2 en el segundo.
- **Movilidad en dos niveles:** se mueve el clúster entero *y* se mueven los nodos dentro de él.
- Implementado en **NS-3** (3.43 según los videos; 3.46 es la última). ns3-ai es deseable, **no** obligatorio
  (instalado de todos modos, ver Entorno).
- Documentar resultados, análisis, conclusiones y recomendaciones.
- Modelo de referencia: Ospina y Ortiz Triviño, «Estimation of a growth factor to achieve scalable ad hoc networks»
  (Ingeniería y Universidad, Javeriana).

## Cómo se entrega — no va al buzón

- **Un** estudiante **responde el correo del 5 oct, solo al profesor**, desde el correo institucional.
- En el cuerpo: **nombres y apellidos completos** de cada integrante + **el rol** que tuvo cada uno.
- Adjuntos: como mínimo, los entregables de una **tarea automatizada** (§3.1.1 de los lineamientos):

| | Entregable | Estado |
|---|---|---|
| a | PDF — marco teórico (MANETs, clustering jerárquico, modelos de movilidad) | ⬜ |
| b | PDF — descripción y justificación del problema (la indagación) | ⬜ |
| c | Diseño de la solución (diagramas de bloques / flujo / UML) | ⬜ |
| d | Código fuente completo (+ versión de NS-3 y de cualquier librería no estándar) | ⬜ |
| e | PDF — **manual de usuario** y **manual técnico** (el correo los recalca) | ⬜ |
| f | Experimentación y análisis de **≥ 3 escenarios** de prueba | ⬜ |

Se puede entregar un solo documento con todo, si queda claro dónde está cada literal.
Todos los entregables llevan los datos de **todos** los autores.

Probablemente haya **sustentación** extraclase (§3.1.3); el monitor asigna horario.

## Reglas que aplican

- Grupos de **máximo 7** (el correo amplía los 5 de los lineamientos).
- §3.3.1: lenguaje estándar + una librería de estructuras de datos; lo demás requiere permiso. NS-3 y ns3-ai
  vienen autorizados por el propio enunciado.
- §3.3.2: **ningún motor de IA** para hacer el taller, salvo excepción pedida por escrito al profesor.
  - **Excepción concedida (informada el 29 oct):** se puede usar IA para el **proceso NS-3** (código,
    simulación, entorno). **Los documentos y la entrega los hacen humanos**: informe, análisis, conclusiones,
    recomendaciones, manual técnico, manual de usuario y el correo de entrega. Guardar la autorización
    (correo o captura) junto al taller.

## Entorno (instalado 29 oct)

Versiones (van en el entregable d):

| Pieza | Versión | Dónde |
|---|---|---|
| ns-3 | **3.46.1** (ns-allinone-3.46.1) | `~/tools/ns-allinone-3.46.1/ns-3.46.1` |
| NetAnim | **3.110** (Qt 5.15.19) | `~/tools/netanim/build/bin/netanim` |
| Compilador | Apple clang 21.0.0, arm64 | macOS 27.0.1 |
| Build | CMake 4.4.5 · Ninja 1.13.2 · ccache 4.14.2 | Homebrew |

- Configurado con `./ns3 configure --enable-examples --enable-tests -G Ninja -- -DNS3_FAST_LINKERS=OFF`.
  **`NS3_FAST_LINKERS=OFF` es obligatorio en este Mac:** con el `lld` de Homebrew el enlazado falla
  («could not load TAPI file … libc++.tbd: unknown architecture»).
- Desde 3.45 el allinone ya **no trae NetAnim**: se clonó de https://gitlab.com/nsnam/netanim (tag `netanim-3.110`).
- **Código del taller:** `codigo/` está enlazado como `ns-3.46.1/scratch/manets` (symlink). Una subcarpeta de
  `scratch/` debe tener **exactamente un** `.cc` con `main()`; se corre con
  `./ns3 run scratch/manets/<archivo-sin-.cc>` desde `ns-3.46.1/`.
- Clases confirmadas en 3.46.1: `HierarchicalMobilityModel`, `GroupMobilityHelper`, `GaussMarkovMobilityModel`,
  `RandomWaypointMobilityModel`. Ejemplos útiles: `src/mobility/examples/reference-point-group-mobility-example.cc`
  (movilidad grupal RPGM = buses), `examples/routing/manet-routing-compare.cc`,
  `examples/wireless/mixed-wired-wireless.cc`, `examples/wireless/wifi-aggregation.cc`.
- NetAnim: el script escribe un `.xml` con `AnimationInterface`; se abre con
  `~/tools/netanim/build/bin/netanim`.

### ns3-ai (instalado 29 oct)

Puente de memoria compartida entre la simulación (C++) y Python: los datos salen **mientras corre**, sin
pasar por archivos de traza enormes (p. ej. RSSI por paso → estimador de trilateración en numpy/pandas).
El enunciado lo pide «deseable, mas no necesario» y recomienda instalar NS-3 «con el componente de AI».

| Pieza | Versión | Dónde |
|---|---|---|
| ns3-ai | fork **DEFIANCE v1.45.2**, ya incluido en el allinone 3.46.1 (no se clonó `hust-diangroup`) | `ns-3.46.1/contrib/ai` |
| Dependencias C++ | Boost 1.92.0 · protobuf 36.2 · pybind11 3.1.0 | Homebrew |
| Python | 3.13.x en venv: numpy, pandas, matplotlib, protobuf, gymnasium, ray[rllib] | `~/tools/ns3ai-venv` |

- Configurar **con el Python del venv** (si no, los bindings quedan para otra versión de Python):
  `./ns3 configure --enable-examples --enable-tests -G Ninja -- -DNS3_FAST_LINKERS=OFF -DPython_EXECUTABLE=$HOME/tools/ns3ai-venv/bin/python -DPython3_EXECUTABLE=$HOME/tools/ns3ai-venv/bin/python`
- Paquetes Python del módulo: `pip install -e contrib/ai/python_utils` y `pip install -e contrib/ai/model/gym-interface/py`.
- **Tres arreglos locales** (originales guardados como `.orig` / carpeta aparte):
  1. `contrib/ai/examples/a-plus-b/CMakeLists.txt`: los bindings `ns3ai_apb_py_stru`/`_vec` no enlazaban
     `${libcore}` → en macOS fallaban al importar («symbol not found … ns3::Time::StaticInit»). Si un binding
     propio da ese error: `target_link_libraries(<binding> PRIVATE ${libcore})`.
  2. `contrib/ai/python_utils/ns3ai_utils.py`: `Experiment` creaba la memoria compartida como `ns3-ai`, pero
     el lado C++ la busca como `ns3-ai_single_trial` → C++ moría con «interprocess_exception: No such file or
     directory». Se cambió el `segName` por defecto a `ns3-ai_single_trial` (error del fork, no de macOS).
  3. `contrib/defiance` (multiagente RL sobre ns3-ai; no lo necesitamos) se movió a
     `~/tools/ns3-contrib-disabled/`: su librería de tests no enlaza `point-to-point` en macOS y rompía
     `./ns3 build`. El README del allinone recomienda quitar los contrib que den problemas.
- La primera compilación a veces falla con «'messages.pb.h' file not found» (carrera con protoc); volver a
  correr `./ns3 build` lo resuelve.
- Los `apb.py` llaman `./ns3 run` por dentro, que compila lo pendiente: compilar todo **antes** de probar.
  `ns3ai_utils` lanza la simulación en otro grupo de procesos: si se corta Python a la fuerza, el proceso
  C++ puede quedar huérfano al 100 % de CPU → `pkill -f ns3ai_` (o el nombre del ejecutable).
- **Prueba (29 oct): pasa.** `~/tools/ns3ai-run-apb.sh use-msg-stru` (tope de 90 s) o
  `cd contrib/ai/examples/a-plus-b/use-msg-stru && ~/tools/ns3ai-venv/bin/python apb.py`.
  `use-msg-stru`: 10 000 idas y vueltas C++→Python→C++, 0 sumas erradas, ~8 s. `use-msg-vec`: 30 000 sumas,
  0 erradas. `use-gym` **no corre**: el fork rechaza espacios `uint` («Use int instead!») y ese ejemplo
  todavía declara `uint32_t`. Es el ejemplo el que está desactualizado; en código propio, usar espacios `int`.

## Idea de indagación — borrador (24 oct)

> Idea de Miguel; esto es el encuadre para discutir con Juan Sebastián, no la versión final.

**Contexto:** perro perdido con un collar que emite señales (al estilo Find My de Apple). Los celulares
alrededor conocen su propia posición por GPS; del collar solo reciben **intensidad de señal (RSSI)**, que es
aleatoria. Con eso se **triangula** la posición del perro, que se comparte por la red ad hoc; quien lo busca
lanza una consulta que recorre la red. Escenario en el campus: peatones, grupos en edificios y **buses**
(clústeres que se mueven completos mientras sus pasajeros se mueven adentro).

**Ajuste clave:** el enunciado exige una indagación **sobre modelos de movilidad**. La movilidad es la
**variable independiente**; la localización es **lo que se mide**.

**Pregunta (borrador):**
> ¿Cómo afecta el patrón de movilidad de los nodos observadores (estáticos, peatones con Random Waypoint,
> clústeres que se mueven en bloque como buses) al error y a la frescura de la posición estimada de un collar
> por trilateración RSSI?

**Hipótesis en tensión:**
- Los clústeres móviles cubren más área → oyen el collar más seguido → estimación **más fresca**.
- Pero los nodos de un bus están casi en el mismo punto → mala geometría para trilaterar → **más error**,
  aunque haya muchas lecturas.

**Línea base:** Find My no triangula; cada teléfono reporta *su propia* posición GPS como ubicación aproximada
del dispositivo. Comparar «posición del reportero más cercano» vs. «trilateración ponderada por RSSI».

**Componente estocástico:** pérdida log-distancia + **sombreado log-normal** (± desvanecimiento) en ns-3
(`LogDistancePropagationLossModel`, `RandomPropagationLossModel`, Nakagami). RSSI por paquete con el trace
`MonitorSnifferRx`.

**Jerarquía** (≥ 3 clústeres en nivel 1, 2 en nivel 2):
- Nivel 1: 2 buses, un grupo en plaza/edificio, el grupo del paseador de perros.
- Nivel 2: dos zonas del campus (p. ej. norte y sur), cada una agrupa clústeres de nivel 1 vía cabeza de clúster/gateway.
- Movilidad en dos niveles: `HierarchicalMobilityModel` (padre = bus/grupo, hijo = nodo dentro) y
  `GroupMobilityHelper` — **verificar que estén en 3.43**.

**Escenarios** (≥ 3; cruzar factores con diseño factorial, libro cap. 3):

| # | Escenario | Qué prueba |
|---|---|---|
| E1 | Observadores estáticos | Control |
| E2 | Movilidad individual (Random Waypoint) | Movilidad a nivel de nodo |
| E3 | Buses: clústeres móviles + movimiento interno | Movilidad a nivel de clúster vs. nodo |
| E4 | Paseador con varios perros, collares iguales | Asociación lectura ↔ perro (opcional, ver abajo) |

Factores candidatos: tipo de movilidad · densidad de observadores · σ del sombreado.
Métricas: error de localización (m) vs. posición real · latencia/frescura de actualización · tasa de entrega
de la consulta.

**Alcance recortado (11 días, 1–2 personas, ns-3 nuevo):**
- **Se queda:** movilidad jerárquica, recolección de RSSI, trilateración, error vs. verdad, latencia.
- **Se simplifica:** difusión de la estimación y consulta del «perro perdido» → inundación o AODV hacia un
  nodo gateway; medir entrega y latencia. Sin protocolo de consulta propio.
- **Se descarta:** tiempo de vuelo (ToF). Requiere Wi-Fi FTM/802.11mc, que ns-3 principal no modela bien → va
  en recomendaciones/trabajo futuro.
- **E4 solo vale con IDs anónimos o rotativos** (privacidad tipo Find My): ahí hay que resolver qué lectura
  es de qué perro. Con ID fijo es trivial (solo más contención). Va de último o como extra.

## Código (`codigo/`, estado 29 oct) — hecho con IA bajo la excepción

| Archivo | Qué hace |
|---|---|
| `collar-sim.cc` | Simulación NS-3: jerarquía, movilidad, Wi-Fi ad hoc, beacon del collar, RSSI, enrutamiento, reportes, consultas. |
| `estimador.h` | Los 3 estimadores en C++ (los usan las cabezas de zona). Es la misma matemática de `localizar.py`. |
| `analisis/localizar.py` | Localización de referencia **fuera de línea**: usa todas las lecturas de `rssi.csv`, sin pasar por la red. |
| `analisis/red.py` | Métricas de red de una corrida: entrega y latencia por tipo de mensaje, y consultas. |
| `analisis/experimento.py` | Corre el factorial (clúster × nodo × enrutamiento) con réplicas, en paralelo. |
| `analisis/graficar.py` | `escena.png` de una corrida: trayectorias, perro, estimaciones fuera de línea y de la red. |
| `analisis/ns3ai_estimador.py` | Corre la simulación con el estimador de las cabezas de zona **en Python, vía ns3-ai**. |
| `analisis/rutas.py` | Rutas compartidas (ns-3, binario, `codigo/`). |
| `ns3ai/collar-msg.h`, `ns3ai/collar_py.cc` | Mensajes C++ ↔ Python y su binding pybind11 (`collar_ns3ai_py`). |
| `CMakeLists.txt` | Le dice a ns-3 que compile la simulación **y** el binding. Sin este archivo, ns-3 solo arma el programa. |

### ns3-ai en el taller (29 oct)

- **Qué hace:** con `--estimator=python`, cada vez que una cabeza de zona estima (cada 5 s), C++ pone sus
  lecturas de la ventana en memoria compartida, la simulación se detiene, y Python calcula con
  `localizar.estimar()` (la misma función del análisis fuera de línea) y devuelve la posición. Con
  `--estimator=cpp` (por defecto) se usa `estimador.h` y no hace falta Python.
- **Cómo se lanza:** Python crea la memoria compartida, así que se arranca desde Python:
  `~/tools/ns3ai-venv/bin/python analisis/ns3ai_estimador.py -- --outDir=$PWD/resultados/demo-py [...]`.
  En el factorial: `experimento.py ... --estimador python`. Cada corrida usa una memoria con nombre
  único (`--ns3aiTrial`), así que pueden ir en paralelo.
- **Verificado:** misma corrida (RngRun 3, 300 s) con los dos estimadores. Lecturas, posiciones,
  mensajes, reportes y consultas salen **idénticos byte a byte**. Las 118 estimaciones coinciden en
  validez y difieren a lo sumo 3 cm, por la tolerancia de parada de Gauss-Newton. Tarda 20.9 s frente a
  20.3 s en C++.
  `experimento.py --estimador python` corrió 8 corridas en paralelo sin dejar procesos huérfanos.
- **Para qué sirve más allá de esto:** cambiar el estimador por cualquier cosa en Python (otro modelo de
  canal, un filtro de Kalman sobre las estimaciones, un modelo aprendido) sin tocar el C++. Basta con cambiar
  `estimar_peticion()`.
- **Cuidado:**
  - Las dos partes esperan en espera activa: cada corrida ocupa ~2 núcleos al 100 %. Por eso `experimento.py`
    usa la mitad de corridas en paralelo con `--estimador python`.
  - No llamar `CppSetFinished()` a mano: el destructor de ns3-ai ya lo hace, y una segunda llamada deja el
    programa colgado al 100 % de CPU después de escribir los resultados. Pasó durante las pruebas.
  - Caben 512 lecturas por ventana; si hay más, van las más recientes y `parametros_texto.txt` cuenta las
    ventanas truncadas (`ventanasTruncadas`).
  - Si se cambia `collar-msg.h`, recompilar: el binding y el programa deben tener el mismo layout.

**Modelo implementado:**
- **Jerarquía:** nivel 2 = zonas `sur` (y 0–150) y `norte` (y 150–300) en un área de 500 × 300 m. Nivel 1 =
  4 clústeres, 2 por zona: `bus-norte`, `plaza`, `bus-sur`, `paseador`. Por defecto 8 celulares por clúster;
  el nodo 0 de cada clúster se marca como cabeza (solo etiqueta por ahora).
- **Movilidad**, como suma de capas con `HierarchicalMobilityModel` anidado:
  - zona: fija;
  - clúster: bus con `WaypointMobilityModel` (ruta rectangular, 6 m/s, paradas de 20 s) o grupo con
    `RandomWaypoint` dentro de la zona;
  - nodo: `RandomWalk2d` dentro de la caja del clúster (bus 12 × 3 m, plaza 20 × 20 m, paseador 6 × 6 m).
  - El perro perdido es un nodo aparte con `RandomWalk2d` a 0.3 m/s.
- **Interruptores:** `--clusterMobility` y `--nodeMobility` (0/1) dan las 4 combinaciones del factorial:
  estático, solo-nodo, solo-clúster, clúster+nodo.
- **Canal:** 802.11b a 1 Mbps, ad hoc. Pérdida log-distancia (n = 2.7, 40.05 dB a 1 m) más sombreado
  normal en dB (σ = 4 dB, `RandomPropagationLossModel`). El collar transmite a 0 dBm y los celulares a
  16 dBm; sensibilidad −95 dBm.
- **Medición:** el trace `MonitorSnifferRx` da el RSSI de cada beacon decodificado. La posición GPS es la
  verdad más un error N(0, 4 m) por eje.
- **Métodos** (`localizar.py` y `estimador.h`): `cercano` (línea base tipo Find My), `centroide` ponderado
  por potencia y `trilateracion` (mínimos cuadrados no lineales, necesita ≥ 3 celulares distintos).
  Por defecto estima cada 5 s con ventana de 10 s.
- **Red** (`--routing=aodv|olsr|dsdv`): los celulares enrutan, el collar no. Mensajes UDP de aplicación:

  | Tipo | Ruta | Cuándo |
  |---|---|---|
  | R reporte | celular → cabeza de su clúster | cada lectura RSSI, tras un retardo aleatorio de 0–100 ms |
  | V relevo | cabeza de clúster → cabeza de zona | al recibir un reporte |
  | E intercambio | cabeza de zona → la otra cabeza de zona | cada estimación válida |
  | Q consulta | dueño → cabeza de su zona | intervalo uniforme de 5–15 s (media 10 s), desde t = 20 s |
  | A respuesta | cabeza de zona → dueño | al recibir la consulta |
  | X cruda | cabeza de zona → la otra cabeza de zona | cada lectura de su zona; solo con `--zoneFusion=raw` |

  - Las cabezas de zona son la cabeza de `plaza` (norte) y la de `paseador` (sur). Cada una estima con las
    lecturas que le llegaron.
  - **`--zoneFusion`** decide cómo se combinan las dos zonas:

    | Valor | Qué hace |
    |---|---|
    | `none` (defecto) | Cada cabeza estima solo con su zona. Al dueño le llega la mejor: si las dos están frescas (≤ 10 s), la de más observadores; si no, la más reciente. |
    | `raw` | Cada cabeza reenvía las lecturas crudas de su zona a la otra (mensaje X), así que las dos estiman con todo lo que llegó. |
    | `merge` | Cada una estima por su lado; al contestar, si las dos están frescas, se promedian ponderadas por observadores (`zona_estimacion = -1` en `consultas.csv`). |
  - El dueño es el nodo 1 de `bus-norte` (`--ownerCluster`). El estimador de la red es `--estMethod`
    (por defecto `trilateracion`).
  - `--arpQueue=64`: con los 3 paquetes que trae ns-3 por defecto, AODV perdía ~40 % de los relevos
    (ver Hallazgos).

**Correr (desde `codigo/`):**
```
~/tools/ns-allinone-3.46.1/ns-3.46.1/build/scratch/manets/ns3.46.1-collar-sim-default --netanim=1 --outDir=$PWD/resultados/demo
~/tools/ns3ai-venv/bin/python analisis/localizar.py resultados/demo
~/tools/ns3ai-venv/bin/python analisis/red.py resultados/demo
~/tools/ns3ai-venv/bin/python analisis/graficar.py resultados/demo
~/tools/ns3ai-venv/bin/python analisis/experimento.py --nombre factorial --reps 10 --routing aodv olsr dsdv -- --simTime=600
~/tools/ns3ai-venv/bin/python analisis/ns3ai_estimador.py -- --outDir=$PWD/resultados/demo-py   # con ns3-ai
```
- Después de cambiar el `.cc`, compilar con `./ns3 build scratch/manets/collar-sim` desde `ns-3.46.1/`
  (`experimento.py` lo hace solo, salvo con `--sin-compilar`).
- **Parámetros para el equipo:** todos están en
  [`codigo/escenarios/base.conf`](codigo/escenarios/base.conf), comentados y con sus valores por defecto.
  Para probar algo:
  1. copiar el archivo (p. ej. `escenarios/mi-prueba.conf`) y cambiar lo que se quiera;
  2. correr con `--conf=escenarios/mi-prueba.conf`.

  Funciona en el binario, en `experimento.py` y en `ns3ai_estimador.py`. Lo que se pase después de
  `--conf` en la línea de comandos gana. Lista siempre al día: el binario con `--help`.
- Cada corrida guarda `parametros.txt` (números, incluido `RngRun`) y `parametros_texto.txt` (enrutamiento,
  estimador, `zoneFusion` y los `--conf` usados), para poder reproducirla.

**Verificado (29 oct):**
- Las posiciones cuadran con zona + ruta + caja.
- Sin sombreado, el ajuste RSSI vs. distancia real da exactamente P0 = −40.05 y n = 2.70.
- Los 5 tipos de mensaje circulan con los 3 protocolos. Cada mensaje, reporte y consulta queda en su CSV
  con hora de envío y de llegada. Lo enviado en los últimos 5 s no se cuenta como perdido.
- **Tiempos:** una corrida de 600 s tarda ~0.4 s sin red y ~15–50 s con red (AODV es el más lento). El
  factorial 3 enrutamientos × 4 movilidades × 10 réplicas (120 corridas) tarda ~5 min en paralelo y ocupa
  134 MB (casi todo es `posiciones.csv`).
- Resultados de prueba en `resultados/factorial-red-prueba/` (tablas en `factorial-red-prueba.log`). Son
  de humo: los parámetros no están decididos.

**Hallazgos del código, no conclusiones** (el análisis lo hacen ustedes):
- **Cola ARP:** ns-3 guarda solo 3 paquetes por vecino sin resolver. Como los relevos salen en ráfagas
  (una por beacon), cada cambio de siguiente salto botaba el resto. Con AODV, el relevo bus-norte → plaza
  entregaba 10 %. Con 64 paquetes, la entrega de relevos con AODV pasó de 57 % a 93 %. Es un artefacto de
  ns-3, no del protocolo; mencionarlo como supuesto.
- **Partición por zonas:** cada cabeza de zona solo recibe las lecturas de su zona, así que sus
  estimaciones quedan sesgadas hacia su lado (se ve en `escena.png`). En la prueba, el error de la
  respuesta al dueño (~80–105 m) sale mayor que el de la localización fuera de línea con todas las
  lecturas.
- **AODV y consultas espaciadas:** con AODV, ~22 % de las consultas quedaron sin respuesta (12 % de las
  consultas y 10 % de las respuestas se pierden). Con consultas cada ~10 s y rutas que caducan a los 3 s,
  casi cada consulta tiene que redescubrir la ruta. Con OLSR/DSDV, que son proactivos, la cifra es
  ~1–7 %.
- **Censura:** con sombreado, solo se decodifican beacons por encima de ~−90 dBm. Lejos, solo llegan los que
  tuvieron sombreado favorable, así que el ajuste da n ≈ 1.6 en vez de 2.7 y las distancias estimadas salen
  cortas.
- `RandomPropagationLossModel` sortea el sombreado **independiente por paquete**, sin correlación espacial
  ni temporal: promediar lecturas lo reduce más de lo que pasaría en la realidad. Mencionarlo como
  supuesto, o cambiarlo.
- **Costo de `zoneFusion=raw`:** en una prueba de 300 s con DSDV:
  - salieron ~2 400 mensajes X;
  - las dos cabezas pasaron a estimar con ~79 lecturas por ventana (contra ~48 sin reenvío);
  - la entrega de relevos bajó a 67 % (contra ~99 % con `none`), por el tráfico extra alrededor de las
    cabezas de zona.

  Con `merge`, 23 de 29 respuestas salieron fusionadas. Es una sola corrida: es un indicio, no un
  resultado.

**Pendiente en el código:**
- [ ] Parámetros del experimento: los fija el grupo probando con archivos `--conf` (29 oct: todos los
      parámetros quedaron accesibles en `escenarios/base.conf`).
- [x] Difusión de la estimación y consulta del «perro perdido» por la red, con AODV/OLSR/DSDV como factor.
      Mide entrega y latencia (29 oct). No hay inundación pura: ns-3 no la trae y habría que programarla.
- [x] Combinar las dos zonas: `--zoneFusion=none|raw|merge` (29 oct). Las dos alternativas son válidas;
      por defecto quedan separadas (`none`).
- [ ] Sobrecarga de enrutamiento (paquetes de control de AODV/OLSR/DSDV): todavía no se mide.
- [x] Usar ns3-ai: el estimador de las cabezas de zona corre en Python durante la simulación (29 oct).
- [ ] Opcional: E4, el paseador con collares (asociar cada lectura con su perro).

## Abierto

- [x] **Grupo:** hay grupo (29 oct). Falta llenar [`entregables/autores.md`](entregables/autores.md)
      (nombres del SIA y roles) y decidir quién responde el correo.
- [x] «Tres clústeres en el primer nivel y dos en el segundo» se lee como lo implementa el código (confirmado
      el 29 oct): 2 zonas (nivel 2), cada una con sus clústeres; 4 clústeres en el nivel 1.
- [ ] **Pregunta de investigación e hipótesis finales:** las define el resto del grupo (borrador arriba;
      estructura en [`entregables/b-problema/`](entregables/b-problema/)).
- [ ] Entregables a–f: la estructura está en [`entregables/`](entregables/README.md); los escribe el grupo.
- [x] Material de Drive bajado a `fuentes/` (24 oct) — ver índice abajo.
- [x] Artículo de referencia (punto 4) en `fuentes/4-articulo/` (24 oct).
- [x] Instalar NS-3 en el Mac, con NetAnim y ns3-ai (29 oct) — ver Entorno.

## Fuentes (`fuentes/`, una carpeta por literal del correo)

Lo marcado con ★ es lo que más pesa para *este* taller (movilidad + clústeres + NS-3).

**`2a-manets/` — carpeta MANETS de la biblioteca digital**

| Archivo | Qué es |
|---|---|
| ★ `Subir Kumar Sarkar … Ad Hoc Mobile Wireless Networks … (2013).pdf` | Libro, 325 págs. **Cap. 8: modelos de movilidad** (random walk, random waypoint, random direction, Gauss–Markov, city section; dependencia temporal y espacial) y sus limitaciones. §3.4.7: CBRP (enrutamiento por clústeres). Base del marco teórico. |
| `Redes Ad Hoc (1).pdf` | En realidad es Barbeau y Kranakis, *Principles of Ad Hoc Networking*, 277 págs. §5.5 clustering, §5.7.2 enrutamiento jerárquico. |
| `RedesAdhoc-IoT.pptx` | Diapositivas del grupo TLÖN (UNAL), 108. IoT, redes ad hoc, nubes móviles, BATMAN; trae el ciclo de vida de un clúster (formación → operación → mantenimiento). |
| `Presentación 1.pptx` | 48 diapositivas: motivación de redes inalámbricas, ad hoc, nube móvil, cooperación. |
| `Presentación3.pptx` | 37 diapositivas: protocolos de enrutamiento, parte I. |
| `Protocolo Batman.pptx`, `batman protocol.docx` | Protocolo B.A.T.M.A.N. (diapositivas + texto en inglés). Útil solo si se compara enrutamiento. |

**`2b-ns3/` — carpeta NS-3 de la biblioteca (cubre también los literales c y d)**

| Archivo | Qué es |
|---|---|
| ★ `Instalacion NS-3 Versión 3.43/` | Video de instalación (Sarmiento Pulido) + `.txt` con los comandos — **literal c**. |
| ★ `MEXX_ Dudas Instalación NS-3 & Tres ejemplos….mp4` | Dudas de instalación + comentario de **tres ejemplos de MANETs** — **literal d**. |
| ★ `VideosAnimacionesMANETsPlanasYjerarquicas/` | 5 animaciones: `flat-static`, `flat-mobility`, `flat-mobility-2`, **`Hierarchical-2-levels`**, **`Hierarchical-3-level`**. Muestran lo que hay que construir. |
| `Instalación ns3-ai Versión 1.2.0/` | Video + `.txt` de instalación de ns3-ai (opcional). |
| `Intrucciones del video de instalación NS-3.35.txt` | Comandos de una versión vieja (3.35). |
| `Copia de ns3gym_arxiv (1).pdf`, `gawlowicz19_mswim (3) (1).pdf` | Artículos de ns3-gym (predecesor de ns3-ai). Solo si se usa IA. |

**Literales e y f — ejemplos de NS-3 (enlaces en el enunciado, doxygen de 3.27)**
Vienen con la instalación: `examples/wireless/mixed-wired-wireless.cc` (clústeres como LANs enlazadas) y
`examples/wireless/wifi-aggregation.cc` (varios AP como clústeres).

**`2g-libro/` — ★ Zárate Ceballos et al., *Wireless Network Simulation: A Guide using Ad Hoc Networks and the ns-3 Simulator***
263 págs.; Ortiz Triviño es coautor, así que es el libro con el que piensa el profesor.

| Capítulo | Para qué sirve aquí |
|---|---|
| 1 Introducción a la simulación | Marco teórico: modelos, simulación vs. emulación, especificación formal en ns-3 |
| 2 Redes inalámbricas y ad hoc (§ *MANET Clusters*, p. 41) | Marco teórico de MANETs y clústeres |
| ★ 3 Diseño de experimentos (factoriales 2ᵏ y 2ᵏ⁻ᵖ) | Cómo diseñar los ≥ 3 escenarios con rigor (método científico) |
| ★ 4 Simulación con ns-3 | Primer script, NetAnim, tracing, argumentos por línea de comandos |
| ★ 5 Análisis de resultados | Transitorio vs. estacionario, réplicas, intervalos de confianza |
| ★ 6 Simulación de MANETs en ns-3 | Red ad hoc simple, modelo Wi-Fi, sockets, gráficas; ejemplo completo con análisis |
| 7 MANETs y PLC | No aplica |
| Apéndice B | Instalación de ns-3 |

**`4-articulo/` — ★ Ospina-López y Ortiz-Triviño (2017), «Estimation of a growth factor to achieve scalable ad hoc networks»**
*Ingeniería y Universidad* 21(1), 49–70. DOI 10.11144/Javeriana.iyu21-1.egfa. 22 págs.
El ejemplo de indagación resuelta que da el profesor: arquitectura jerárquica (2 y 3 capas), modelo con
**geométrica truncada** (→ tarea 22), factor de crecimiento φ entre capas estimado por simulación en ns-3.
Estructura: introducción · materiales y métodos (§1.2 trabajos relacionados) · resultados (§2.1 φ, §2.2 estimación)
· conclusiones. **Tabla de parámetros en la p. 13** (500 m × 500 m; 6 clústeres × 6 nodos; Friis; pérdida
constante; tráfico Poisson; **movilidad Random Waypoint**) — buen molde para la tabla de parámetros propia.

## Calendario propuesto (11 días)

| Fecha | Qué |
|---|---|
| Sáb 24 – dom 25 oct | Cerrar grupo · instalar NS-3 · leer el artículo de referencia · ver el video de los 3 ejemplos |
| Lun 26 oct | Conversatorio (quiz tarea 25) · **formular la indagación e hipótesis** con el grupo |
| Mar 27 – mié 28 oct | Diseño: topología jerárquica, movilidad de clúster y de nodo, métricas, 3+ escenarios |
| Jue 29 oct – dom 1 nov | Implementación y corridas |
| Lun 2 – mar 3 nov | Análisis de resultados · marco teórico · manuales · diseño en PDF |
| **Mié 4 nov** | Revisión final y **respuesta al correo antes de las 11:59 pm** |

Ojo: la **tarea 26** (opcional, bono) vence el 2 nov, en plena semana de implementación, y las
**tareas 31–34** (manuscritas, lista del 26 oct) vencen el **dom 1 nov**.
