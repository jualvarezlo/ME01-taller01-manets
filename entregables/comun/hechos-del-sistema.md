# Hechos del sistema (contexto compartido para los entregables)

Resumen técnico derivado directamente del código (`codigo/collar-sim.cc`, `codigo/estimador.h`,
`codigo/analisis/*.py`, `codigo/escenarios/base.conf`) y del `README.md`. Es la **fuente de verdad**
para los documentos b, c y e: todos deben usar estos mismos números y nombres. No inventar cifras de
resultados; los resultados experimentales son del literal f, que hace el grupo.

Última verificación contra el código: lectura de `collar-sim.cc` (topología, movilidad, canal,
mensajes, estimación) y de `estimador.h` / `localizar.py` (estimadores).

## 1. Historia y propósito

Un perro se pierde con un collar que emite un *beacon* cada segundo. Los celulares cercanos lo oyen,
miden el RSSI y conocen su posición por GPS. Con esas lecturas, la red ad hoc estima dónde está el
perro, y el dueño consulta esa estimación por la misma red. Es análogo a "Find My" de Apple, usado
como excusa para estudiar modelos de movilidad en una MANET jerárquica.

Simulación en **NS-3 3.46.1** (C++); análisis en **Python**.

## 2. Pregunta de investigación (definitiva, acordada por el grupo)

> ¿Cómo afecta el patrón de movilidad de los celulares que observan al error y a la frescura de la
> posición estimada de un collar por RSSI?

Hipótesis en tensión:
- Clústeres en movimiento cubren más área y oyen el collar más seguido → estimaciones más frescas.
- Celulares de un mismo bus están casi en el mismo punto → mala geometría para trilaterar → más error
  aunque haya muchas lecturas.

Variable independiente: el patrón de movilidad. Variables medidas (dependientes): error de
localización (m), frescura/edad de la estimación (s), y tasa de consultas respondidas.

## 3. Jerarquía (posición absoluta = suma de tres capas)

| Nivel | Qué es | Cuántos | Modelo de movilidad en NS-3 |
|---|---|---|---|
| 2 | Zonas: `sur` (y ∈ [0,150)) y `norte` (y ∈ [150,300)) | 2 | `ConstantPositionMobilityModel` (origen de la zona) |
| 1 | Clústeres | 4 | bus → `WaypointMobilityModel`; grupo → `RandomWaypointMobilityModel` |
| nodo | Celulares | 8 por clúster (32 total) | `RandomWalk2dMobilityModel` dentro de la caja del clúster |

Se arma con `HierarchicalMobilityModel`: se hace `SetParent(zona)` y `SetChild(movilidad local)`;
cada nodo agrega otro `HierarchicalMobilityModel` con el clúster como padre. Así la posición del nodo
es zona + clúster + desplazamiento propio.

Clústeres (de `kClusters` en `collar-sim.cc`):

| Clúster | Zona | Tipo | Caja de nodos (semi-ejes) | Rapidez de nodo |
|---|---|---|---|---|
| `bus-norte` | norte | BUS | 6.0 × 1.5 m | 0.5 m/s |
| `plaza` | norte | GROUP | 10.0 × 10.0 m | 1.0 m/s |
| `bus-sur` | sur | BUS | 6.0 × 1.5 m | 0.5 m/s |
| `paseador` | sur | GROUP | 3.0 × 3.0 m | 0.8 m/s |

Área total: 500 × 300 m. Las cajas del README (12×3, 20×20, 6×6) son los anchos completos
(2× semi-eje). La ruta del bus es rectangular: (50,30)→(450,30)→(450,120)→(50,120), relativa al
origen de su zona, recorrida en bucle a `busSpeed` con parada `busDwell` en cada esquina.

Cabezas: la cabeza de cada clúster es su nodo 0. Cabeza de zona norte = cabeza de `plaza`; cabeza de
zona sur = cabeza de `paseador` (de `kZones`: sur.headCluster=3 paseador, norte.headCluster=1 plaza).
El dueño viaja en `bus-norte` (`ownerCluster=0`). El perro es un nodo aparte, no pertenece a ningún
clúster, con `RandomWalk2dMobilityModel` a 0.3 m/s (o fijo si `dogMobility=false`).

## 4. Interruptores del experimento (variable independiente)

- `--clusterMobility=true/false`: ¿se mueven los clústeres (nivel 1)?
- `--nodeMobility=true/false`: ¿se mueven los nodos dentro de su clúster?
- Sus 4 combinaciones = los escenarios de movilidad: estático, solo-nodo, solo-clúster, clúster+nodo.
- `--routing=aodv|olsr|dsdv`: protocolo de enrutamiento.

## 5. Canal de radio (componente estocástico principal)

- Collar emite por **802.11b** (Wi-Fi ad hoc), beacon broadcast cada `beaconInterval` (1 s) de
  `beaconSize` (32 B), a `collarTxDbm` (0 dBm).
- Pérdida: `LogDistancePropagationLossModel` con exponente `pathLossExp` (2.7) y pérdida de
  referencia `refLossDb` (40.05 dB a 1 m, 2.4 GHz).
- Sombreado: normal en dB, `shadowSigmaDb` (4 dB) → RSSI log-normal. Es la aleatoriedad clave: dos
  lecturas a la misma distancia dan RSSI distintos. Con `shadowSigmaDb=0` no hay sombreado.
- Cada celular que decodifica el beacon (trace `MonitorSnifferRx`) registra el RSSI (`signalNoise.signal`)
  y su posición GPS = posición real + ruido normal `gpsSigma` (4 m) por eje.
- Modelo: P_r(d) = P0 − 10·n·log10(d) + X, con X ~ N(0, σ²). (P0 = collarTxDbm − refLossDb.)

## 6. Protocolo de mensajes de aplicación (UDP sobre el enrutamiento elegido)

| Tipo | Nombre | De → a | Cuándo |
|---|---|---|---|
| R | reporte | celular → cabeza de su clúster | cada lectura, tras jitter 0–`reportJitterMs` (100 ms) |
| V | relevo | cabeza de clúster → cabeza de zona | al recibir un reporte |
| E | intercambio | cabeza de zona → otra cabeza de zona | cada estimación (`estInterval`) |
| Q | consulta | dueño → cabeza de su zona | cada `queryInterval` (uniforme 0.5×–1.5×) |
| A | respuesta | cabeza de zona → dueño | al recibir una consulta |
| X | cruda | cabeza de zona → otra cabeza de zona | cada lectura, solo con `zoneFusion=raw` |

Lógica (de `HandleMsg`): un R que llega a un nodo que no es cabeza de zona se reenvía como V hacia la
cabeza de zona; si el nodo ya es cabeza de zona, se entrega localmente (`DeliverReport`). Las cabezas
de zona acumulan lecturas en una ventana.

## 7. Estimación (idéntica en C++ `estimador.h` y Python `localizar.py`)

Cada `estInterval` (5 s), cada cabeza de zona descarta lecturas más viejas que `estWindow` (10 s) y
estima con la ventana (`EstimateTick`). Métodos (`estMethod`):

- `cercano`: posición GPS del celular con mayor RSSI (línea base tipo Find My).
- `centroide`: centroide de posiciones GPS ponderado por potencia lineal (mW), w = 10^(RSSI/10).
- `trilateracion`: distancias d̂ = 10^((P0−RSSI)/(10n)); mínimos cuadrados no lineales con pesos
  1/d̂², resueltos por Gauss-Newton desde el centroide; requiere ≥3 celulares distintos. Control de
  geometría degenerada por número de condición de la matriz normal 2×2 (umbral 1e8).

Fusión de zonas (`zoneFusion`), en `BestEstimate`:
- `none` (defecto): cada cabeza estima solo con su zona; al dueño le llega la de más observadores, o
  la más reciente si alguna supera `estWindow`.
- `raw`: cada cabeza reenvía las lecturas crudas de su zona a la otra (mensaje X); ambas estiman con
  todo.
- `merge`: cada una estima por su lado y, al contestar, se promedian ponderando por número de
  observadores.

## 8. ns3-ai (opcional, `--estimator=python`)

Con `estimator=python`, en cada estimación la simulación se detiene, pasa la ventana de lecturas a
Python por memoria compartida (`ns3ai/collar-msg.h`, `collar_py.cc`) y sigue con la posición que
Python devuelve. Python usa la misma función que `localizar.py`. Permite cambiar el estimador (p. ej.
Kalman o un modelo entrenado) editando `analisis/ns3ai_estimador.py` sin tocar C++. Requiere que ns-3
se haya compilado con ns3-ai (Boost, protobuf, pybind11); `CMakeLists.txt` define `COLLAR_CON_NS3AI`
solo si el módulo ai existe. Verificado: C++ vs Python difieren ≤ 3 cm en una corrida de 300 s.

## 9. Herramientas de ejecución y análisis

- `codigo/simular`: corre una simulación (por defecto 600 s), escribe en `--outDir`.
- `codigo/compilar`: recompila el binario tras cambios en `.cc`/`.h`.
- `analisis/localizar.py`: estima offline con todas las lecturas, imprime error por método, escribe
  `estimaciones.csv` y `resumen.csv`.
- `analisis/red.py`: cuántos mensajes llegaron y cuánto tardaron.
- `analisis/graficar.py`: dibuja trayectorias y estimaciones en `escena.png`.
- `analisis/experimento.py`: corre el factorial (4 movilidades × protocolos × réplicas con semillas),
  en paralelo, y deja tablas en `resultados/<nombre>/`.
- `analisis/ns3ai_estimador.py`: lanza la simulación con el estimador en Python.

## 10. Archivos de salida (en `--outDir`)

`rssi.csv` (cada lectura: observador, GPS, posición real del perro, RSSI, distancia),
`posiciones.csv` (posición de cada nodo cada `posLogInterval`=1 s), `nodos.csv` (clúster/zona/rol),
`mensajes.csv` (cada mensaje con hora de envío y llegada; vacía si se perdió), `reportes.csv` (cada
lectura con hora de llegada a su cabeza de zona), `estimaciones_red.csv` (cada estimación con error
contra la real), `consultas.csv` (cada consulta: si tuvo respuesta, demora, antigüedad, error),
`parametros.txt` / `parametros_texto.txt` (parámetros y semilla), `netanim.xml` (solo con
`netanim=true`).

## 11. Parámetros (de `codigo/escenarios/base.conf`, con sus valores por defecto)

Movilidad: `clusterMobility=true`, `nodeMobility=true`. Tamaño/duración: `nodesPerCluster=8`,
`simTime=600`. Clústeres: `busSpeed=6`, `busDwell=20`, `groupSpeedMin=0.5`, `groupSpeedMax=1.5`,
`groupPause=30`. Perro: `dogMobility=true`, `dogX=300`, `dogY=140`, `dogSpeed=0.3`. Collar/radio:
`beaconInterval=1`, `beaconSize=32`, `collarTxDbm=0`, `phoneTxDbm=16`, `rxSensitivityDbm=-95`,
`phoneDataMode=DsssRate1Mbps`. Canal: `pathLossExp=2.7`, `refLossDb=40.05`, `shadowSigmaDb=4`,
`gpsSigma=4`. Red: `routing=aodv`, `arpQueue=64`, `reportJitterMs=100`. Estimación/consultas:
`estMethod=trilateracion`, `estimator=cpp`, `estWindow=10`, `estInterval=5`, `zoneFusion=none`,
`queryInterval=10`, `queryStart=20`, `ownerCluster=0`. Salida: `posLogInterval=1`, `netanim=false`.

## 12. Efectos/artefactos del modelo a declarar (de "Qué declarar en el informe" del README)

Supuestos y artefactos, no conclusiones:
- Lejos del collar solo se decodifican beacons con sombreado favorable → lecturas lejanas salen más
  fuertes de lo que deberían; ajuste RSSI vs distancia da exponente ~1.6 en vez de 2.7, y la
  trilateración subestima distancias. Sin sombreado el ajuste da 2.7 exacto.
- El sombreado se sortea independiente por paquete; en la realidad está correlacionado en espacio y
  tiempo, así que promediar lecturas ayuda más en la simulación que en la vida real.
- ns-3 guarda solo 3 paquetes por vecino durante ARP; los relevos salen en ráfaga y con AODV se
  perdía ~40%. Subir la cola a 64 (`arpQueue`) subió la entrega con AODV de 57% a 93%.
- Con `zoneFusion=none` cada cabeza solo ve su zona y su estimación se sesga hacia ella.
- Con AODV, ~22% de las consultas del dueño quedaron sin respuesta (rutas AODV vencen a 3 s y las
  consultas llegan cada ~10 s). Con OLSR y DSDV fue 1–7%.
- `zoneFusion=raw` duplica lecturas pero el tráfico extra bajó la entrega de relevos de 99% a 67% en
  una prueba con DSDV.
- 802.11b reemplaza a Bluetooth (lo que usaría un collar real); ns-3 no trae Bluetooth.

> Nota: estos porcentajes son observaciones de pruebas durante el desarrollo, útiles como supuestos a
> declarar. Los resultados formales del experimento son del literal f (grupo). No presentarlos como
> conclusiones.

## 13. Autores

Leer de `entregables/autores.md`. A la fecha solo figura **Miguel Ángel Buitrago Castillo**; el resto
de la tabla está vacío. En el encabezado de cada documento, poner la lista tal como esté en
`autores.md` y señalar que queda pendiente completarla.
