# c. Diseño de la solución (PDF + fuentes de los diagramas)

**Qué pide la norma:** «diseño de la aplicación o solución», con diagramas de flujo, diagramas de bloques,
pseudocódigo o UML (§3.1.1 c). Los diagramas los hace el grupo. Las fuentes editables (`.drawio`, etc.) van
en [`diagramas/`](diagramas/) y el PDF final, aquí.

**Diagramas sugeridos y en qué parte del código basarse:**

| Diagrama | Qué muestra | Dónde está en el código |
|---|---|---|
| Arquitectura (bloques) | Simulación NS-3 ↔ archivos CSV ↔ scripts de análisis; con ns3-ai, el estimador en Python | `codigo/collar-sim.cc`, `codigo/analisis/`, `codigo/ns3ai/` |
| Jerarquía | 2 zonas (nivel 2) → 4 clústeres (nivel 1) → 8 celulares cada uno; cabezas de clúster y de zona; perro aparte | `kZones`, `kClusters` en `collar-sim.cc` |
| Movilidad en capas | posición = zona + clúster (ruta del bus o Random Waypoint) + nodo (Random Walk) | `HierarchicalMobilityModel` en `collar-sim.cc` |
| Mensajes (secuencia) | R, V, E, Q, A, X: quién envía a quién y cuándo | comentario inicial y `HandleMsg()` en `collar-sim.cc` |
| Flujo de la cabeza de zona | cada `estInterval`: filtrar ventana → estimar → enviar E; al recibir Q: elegir/fusionar → A | `EstimateTick()`, `BestEstimate()` |
| Flujo del estimador | cercano / centroide / trilateración (Gauss-Newton) | `codigo/estimador.h`, `analisis/localizar.py` |
| Flujo del experimento | factorial × réplicas → corridas en paralelo → CSV → tablas | `analisis/experimento.py` |

Encabezado con los autores: ver [`../autores.md`](../autores.md).
