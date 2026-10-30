# c. Diseño de la solución

Los lineamientos piden el diseño de la solución con diagramas de flujo, diagramas de bloques, pseudocódigo o
UML. Los diagramas los hace el grupo. Guarden los archivos editables, por ejemplo los `.drawio`, en
[`diagramas/`](diagramas/), y el PDF final en esta carpeta.

Diagramas que tendría sentido hacer, con la parte del código de la que salen:

| Diagrama | Qué muestra | Dónde mirar |
|---|---|---|
| Arquitectura | La simulación escribe CSV y los scripts de Python los leen. Con ns3-ai, Python además estima durante la simulación | `codigo/collar-sim.cc`, `codigo/analisis/`, `codigo/ns3ai/` |
| Jerarquía | 2 zonas, 4 clústeres, 8 celulares por clúster, las cabezas y el perro aparte | `kZones` y `kClusters` en `collar-sim.cc` |
| Movilidad | La posición como suma de zona, clúster y nodo | el bloque "movilidad jerárquica" de `collar-sim.cc` |
| Secuencia de mensajes | R, V, E, Q, A y X: quién le manda qué a quién | la tabla del README y `HandleMsg()` |
| Flujo de la cabeza de zona | Cada 5 s filtra la ventana, estima y avisa a la otra zona. Al recibir una consulta, elige o promedia y contesta | `EstimateTick()` y `BestEstimate()` |
| Flujo del estimador | Los tres métodos, incluida la iteración de Gauss-Newton | `codigo/estimador.h` y `analisis/localizar.py` |
| Flujo del experimento | Combinaciones por réplicas, corridas en paralelo, tablas | `analisis/experimento.py` |

El encabezado lleva los nombres de [`../autores.md`](../autores.md).
