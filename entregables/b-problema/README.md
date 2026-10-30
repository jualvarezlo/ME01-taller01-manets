# b. Descripción y justificación del problema (PDF)

**Qué pide la norma:** «descripción y justificación del problema a resolver» (§3.1.1 b). El enunciado del
taller agrega:
- una **indagación** (pregunta de investigación, «al estilo Newton») **sobre modelos de movilidad en
  MANET**, de dificultad intermedia;
- responderla con el **método científico**.

Lo escribe el grupo. El borrador de la idea está en el README del taller, sección «Idea de indagación».

**Esqueleto** (solo títulos):
1. Contexto: el perro perdido y el collar con beacon
2. Pregunta de investigación
3. Hipótesis
4. Justificación: por qué importa y por qué la movilidad es la variable
5. Variables
   - independientes (factores);
   - dependientes (métricas);
   - controladas (parámetros fijos)
6. Método: cómo se va a responder (diseño del experimento; ver el literal f)
7. Alcance y supuestos (qué se simplifica y por qué)

**Datos del código útiles para las secciones 5 y 7:**
- Factores disponibles:
  - `clusterMobility` y `nodeMobility` (diseño 2 × 2);
  - `routing` (aodv, olsr, dsdv);
  - `zoneFusion` (none, raw, merge);
  - `estMethod`;
  - densidad (`nodesPerCluster`);
  - sombreado (`shadowSigmaDb`).
  La lista completa está en `../../codigo/escenarios/base.conf`.
- Métricas que ya se miden:
  - error de localización (m), disponibilidad y frescura;
  - entrega y latencia por tipo de mensaje;
  - éxito, RTT, edad y error de las consultas del dueño.
- Supuestos del modelo que conviene declarar (ver «Hallazgos» en el README del taller):
  - sombreado independiente por paquete;
  - cola ARP de 64;
  - 802.11b como sustituto de BLE;
  - censura de lecturas por debajo de ~−90 dBm.

Encabezado con los autores: ver [`../autores.md`](../autores.md).
