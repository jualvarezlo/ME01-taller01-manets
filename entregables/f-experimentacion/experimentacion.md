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

Al menos tres escenarios, según los lineamientos. Completar la tabla y crear un `.conf` por escenario
en `codigo/escenarios/`.

| # | Nombre | Archivo de parámetros | Qué cambia frente a `base.conf` | Qué prueba |
|---|---|---|---|---|
| E1 | *[...]* | `codigo/escenarios/E1.conf` | *[...]* | *[...]* |
| E2 | *[...]* | `codigo/escenarios/E2.conf` | *[...]* | *[...]* |
| E3 | *[...]* | `codigo/escenarios/E3.conf` | *[...]* | *[...]* |

> Sugerencia de escenarios (a criterio del grupo): E1 podría ser el caso base variando solo el
> protocolo; E2 podría subir o bajar la densidad (`nodesPerCluster`); E3 podría cambiar el sombreado
> (`shadowSigmaDb`) o la fusión de zonas (`zoneFusion`). Lo importante es que cada escenario aísle un
> factor y que los tres juntos ayuden a responder la pregunta.

### Cómo generar los datos

Desde `codigo/`, con el entorno cargado (`source entorno.sh`), para cada escenario:

```bash
python analisis/experimento.py --nombre E1 --reps 10 --routing aodv olsr dsdv -- --conf=escenarios/E1.conf
python analisis/experimento.py --nombre E2 --reps 10 --routing aodv olsr dsdv -- --conf=escenarios/E2.conf
python analisis/experimento.py --nombre E3 --reps 10 --routing aodv olsr dsdv -- --conf=escenarios/E3.conf
```

Cada comando deja en `codigo/resultados/<nombre>/`: `experimento.csv` (error de localización por
método y réplica), `experimento_red.csv` (métricas de red y de consultas por réplica) y `comando.txt`
(el comando exacto, para reproducir). Para la figura de una corrida suelta:

```bash
python analisis/graficar.py resultados/<carpeta_de_una_corrida>
```

## 3. Resultados por escenario

Para cada escenario, incluir la tabla resumen (media ± desviación o intervalo de confianza entre
réplicas) y al menos una gráfica. Las plantillas de tabla siguen las columnas que imprime
`experimento.py`.

### 3.1 Escenario E1 — *[nombre]*

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

Gráficas (insertar los `.png` que generen):

![Figura F1. [descripción].]([ruta/a/la/grafica.png])

Comentario de E1: *[qué se observa en este escenario]*

### 3.2 Escenario E2 — *[nombre]*

*(misma estructura que E1)*

### 3.3 Escenario E3 — *[nombre]*

*(misma estructura que E1)*

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
