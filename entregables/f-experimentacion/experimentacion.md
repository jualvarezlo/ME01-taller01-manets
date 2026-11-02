<div align="center">

# Experimentación y análisis de resultados

**Taller 01: Simulación de MANETs**

**ME01 — Modelos estocásticos y simulación en computación y comunicaciones**

**Universidad Nacional de Colombia**
</div>

> **Esqueleto para completar por el grupo.** Este archivo tiene la estructura del literal f y los
> comandos listos para generar los datos. Las tablas, gráficas y el análisis los escribe el grupo a
> partir de las corridas. Donde aparezca `[...]` o una tabla vacía, hay que rellenarlo. Borren esta
> nota antes de entregar.

## 1. Diseño del experimento

El experimento responde la pregunta del literal b: cómo afecta el patrón de movilidad al error y a la
frescura de la localización por RSSI. Se usa un diseño factorial con réplicas, descrito en el
literal c (Sección 8) y automatizado en `analisis/experimento.py`.

**Factores y niveles.**

| Factor | Niveles | Cómo se controla |
|---|---|---|
| Movilidad de clúster | sí / no (`clusterMobility`) | lo cruza `experimento.py` |
| Movilidad de nodo | sí / no (`nodeMobility`) | lo cruza `experimento.py` |
| Protocolo de enrutamiento | `aodv`, `olsr`, `dsdv` | opción `--routing` |
| *(otros factores por escenario)* | *[...]* | en el `.conf` del escenario |

La combinación de movilidad de clúster y de nodo da los cuatro escenarios de movilidad: estático,
solo-nodo, solo-clúster y clúster+nodo.

**Réplicas y semillas.** Cada tratamiento se corre `[N]` veces (recomendado: 10) con `--RngRun`
distinto, para estimar la media de cada métrica con su intervalo de confianza.

**Duración.** Cada corrida simula `[simTime]` s (por defecto 600).

**Variables de respuesta.** Error de localización (m), frescura o edad de la estimación (s) y tasa de
consultas respondidas; su origen en los CSV está en el literal b (Sección 5.2).

## 2. Escenarios

Se definen cuatro escenarios. El primero responde la pregunta en condiciones por defecto; los otros
tres comprueban si esa respuesta es robusta al variar, uno a uno, los factores secundarios que el
literal b dejó señalados: densidad, sombreado y fusión de zonas. En los cuatro, `experimento.py`
cruza siempre las 4 combinaciones de movilidad con los 3 protocolos, así que el factor principal
(la movilidad) se estudia dentro de cada escenario.

| # | Nombre | Archivo(s) de parámetros | Qué cambia frente a `base.conf` | Qué prueba |
|---|---|---|---|---|
| E1 | Caso base | `E1.conf` | nada (valores por defecto) | el efecto de la movilidad en condiciones por defecto |
| E2 | Densidad | `E2-densidad-baja.conf` (`nodesPerCluster=4`), `E2-densidad-alta.conf` (`=16`) | observadores por clúster (base: 8) | si más observadores compensan la mala geometría del bus |
| E3 | Sombreado | `E3-sombreado-cero.conf` (`shadowSigmaDb=0`), `E3-sombreado-alto.conf` (`=8`) | ruido del canal (base: 4 dB) | si el patrón de movilidad que gana cambia con el ruido del canal |
| E4 | Fusión de zonas | `E4-fusion-raw.conf`, `E4-fusion-merge.conf` (el nivel `none` es E1) | `zoneFusion` (base: none) | si la forma de combinar las dos zonas altera la conclusión |

Los archivos `.conf` están en `codigo/escenarios/`. Cada uno trae un comentario con su propósito y el
comando para correrlo. E2, E3 y E4 tienen más de un nivel, de modo que cada nivel es una corrida
aparte; `experimento.py` fija un solo valor del `.conf` por corrida y lo cruza con las movilidades y
los protocolos.

### Cómo generar los datos

Desde `codigo/`, con el entorno cargado (`source entorno.sh`):

```bash
# E1 — caso base
python analisis/experimento.py --nombre E1 --reps 10 --routing aodv olsr dsdv -- --conf=escenarios/E1.conf

# E2 — densidad (dos niveles)
python analisis/experimento.py --nombre E2-densidad-baja --reps 10 --routing aodv olsr dsdv -- --conf=escenarios/E2-densidad-baja.conf
python analisis/experimento.py --nombre E2-densidad-alta --reps 10 --routing aodv olsr dsdv -- --conf=escenarios/E2-densidad-alta.conf

# E3 — sombreado (dos niveles)
python analisis/experimento.py --nombre E3-sombreado-cero --reps 10 --routing aodv olsr dsdv -- --conf=escenarios/E3-sombreado-cero.conf
python analisis/experimento.py --nombre E3-sombreado-alto --reps 10 --routing aodv olsr dsdv -- --conf=escenarios/E3-sombreado-alto.conf

# E4 — fusión de zonas (none ya es E1; faltan raw y merge)
python analisis/experimento.py --nombre E4-fusion-raw   --reps 10 --routing aodv olsr dsdv -- --conf=escenarios/E4-fusion-raw.conf
python analisis/experimento.py --nombre E4-fusion-merge --reps 10 --routing aodv olsr dsdv -- --conf=escenarios/E4-fusion-merge.conf
```

Cada comando deja en `codigo/resultados/<nombre>/`: `experimento.csv` (error de localización por
método y réplica), `experimento_red.csv` (métricas de red y de consultas por réplica) y `comando.txt`
(el comando exacto, para reproducir). Para la figura de una corrida suelta:

```bash
python analisis/graficar.py resultados/<carpeta_de_una_corrida>
```

> Carga de cómputo: cada comando son 4 movilidades × 3 protocolos × 10 réplicas = 120 corridas de
> `simTime` segundos. En total, los siete comandos suman 840 corridas. Si el tiempo aprieta, se puede
> bajar `--reps` (por ejemplo a 5) para una primera pasada, o recortar E4 y dejarlo como trabajo
> futuro; con tres escenarios (E1, E2, E3) ya se supera el mínimo de los lineamientos.

## 3. Resultados por escenario

Para cada escenario, incluir la tabla resumen (media ± desviación o intervalo de confianza entre
réplicas) y al menos una gráfica. Las plantillas de tabla siguen las columnas que imprime
`experimento.py` y las que trae `experimento_red.csv`.

### 3.1 E1 — Caso base

Tabla de localización (de `experimento.csv`):

| Movilidad | Protocolo | Método | Error mediano (m) | Frescura (s) | Disponibilidad |
|---|---|---|---|---|---|
| estático | aodv | trilateracion | *[...]* | *[...]* | *[...]* |
| solo-nodo | aodv | trilateracion | *[...]* | *[...]* | *[...]* |
| solo-clúster | aodv | trilateracion | *[...]* | *[...]* | *[...]* |
| clúster+nodo | aodv | trilateracion | *[...]* | *[...]* | *[...]* |
| *(… demás combinaciones y protocolos)* | | | | | |

Tabla de red y consultas (de `experimento_red.csv`):

| Movilidad | Protocolo | Entrega lecturas | Consultas respondidas | RTT mediano (ms) | Edad respuesta (s) | Error respuesta (m) |
|---|---|---|---|---|---|---|
| *[...]* | | | | | | |

![Figura F1. [descripción].]([ruta/a/la/grafica.png])

Comentario de E1: *[qué se observa en el caso base]*

### 3.2 E2 — Densidad (baja vs alta)

Comparar `E2-densidad-baja` (4 por clúster) con `E2-densidad-alta` (16) y con el caso base (8, de E1).

| Densidad | Movilidad | Protocolo | Error mediano (m) | Disponibilidad trilateración |
|---|---|---|---|---|
| 4 | *[...]* | | | |
| 8 (base) | *[...]* | | | |
| 16 | *[...]* | | | |

Comentario de E2: *[¿más observadores compensan la geometría del bus?]*

### 3.3 E3 — Sombreado (cero vs alto)

Comparar `E3-sombreado-cero` (0 dB) con `E3-sombreado-alto` (8 dB) y con el caso base (4 dB, de E1).

| Sombreado (dB) | Movilidad | Protocolo | Error mediano (m) | Frescura (s) |
|---|---|---|---|---|
| 0 | *[...]* | | | |
| 4 (base) | *[...]* | | | |
| 8 | *[...]* | | | |

Comentario de E3: *[¿el patrón de movilidad que gana cambia con el ruido del canal?]*

### 3.4 E4 — Fusión de zonas (none vs raw vs merge)

Comparar `none` (de E1), `E4-fusion-raw` y `E4-fusion-merge`.

| zoneFusion | Movilidad | Protocolo | Error respuesta (m) | Entrega relevos | Consultas respondidas |
|---|---|---|---|---|---|
| none (base) | *[...]* | | | | |
| raw | *[...]* | | | | |
| merge | *[...]* | | | | |

Comentario de E4: *[¿compensa el tráfico extra de raw/merge la mejora en el error?]*

## 4. Análisis

Contrastar con las hipótesis del literal b (la tensión frescura ↔ geometría). Guía de lo que conviene
discutir:

- ¿La movilidad de clúster mejora la frescura? ¿En cuánto, y es estadísticamente distinguible entre
  réplicas (intervalos de confianza que no se solapan)?
- ¿La movilidad empeora el error por geometría pobre, sobre todo en los clústeres tipo bus? ¿Se ve en
  la trilateración más que en el centroide o el cercano?
- Efecto del protocolo: ¿AODV deja más consultas sin respuesta que OLSR y DSDV, como sugieren las
  pruebas de desarrollo?
- Interacción entre factores: ¿el efecto de la movilidad depende del protocolo, la densidad o el
  sombreado?

> Antes de concluir, revisar la sección "Qué declarar en el informe" del README del repositorio y la
> Sección 7 del literal b: hay artefactos del modelo (sesgo de lecturas lejanas, sombreado
> independiente por paquete, cola ARP, caducidad de rutas en AODV, sesgo de `zoneFusion=none`) que
> pueden confundir el análisis y deben tenerse en cuenta al interpretar los números.

## 5. Conclusiones

*[Respuesta a la pregunta de investigación, apoyada en los resultados de la Sección 4. Decir si las
hipótesis del literal b se cumplen, se cumplen en parte o se refutan, y bajo qué condiciones.]*

## 6. Recomendaciones y trabajo futuro

*[Recomendaciones prácticas derivadas del estudio y líneas de trabajo futuro: por ejemplo medir
distancia por tiempo de vuelo (Wi-Fi FTM), correlacionar el sombreado en espacio y tiempo, probar un
estimador por filtro de Kalman vía ns3-ai, o modelar paradas donde suban y bajen pasajeros.]*

## 7. Referencias

Reutilizar la numeración de los demás literales si se cita. La lista base está en
`entregables/comun/referencias.md`.
