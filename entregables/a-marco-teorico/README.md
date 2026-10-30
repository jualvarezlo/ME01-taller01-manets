# a. Marco teórico

Los lineamientos piden "un archivo PDF con el marco teórico". Lo escribe el grupo.

Estos son los temas que el marco teórico no puede dejar por fuera, porque la simulación los usa:
- qué es una MANET y cómo se enruta en ella;
- clustering jerárquico: clústeres, cabezas de clúster y niveles. Nosotros usamos 4 clústeres en el primer
  nivel y 2 zonas en el segundo;
- modelos de movilidad individuales, como Random Walk y Random Waypoint, y grupales, como Reference Point Group
  Mobility;
- propagación de radio: pérdida log-distancia y sombreado log-normal, y qué es el RSSI;
- localización por RSSI: vecino más cercano, centroide ponderado y trilateración;
- AODV, que busca rutas cuando las necesita, y OLSR y DSDV, que las mantienen todo el tiempo;
- qué es aleatorio en el modelo y con qué distribución;
- NS-3 como simulador de eventos discretos, y ns3-ai si lo usamos.

Las fuentes vienen del Drive del curso. Están descritas en la sección "Material del curso" del
[README](../../README.md). Las más útiles para este literal son el capítulo 8 de Sarkar, sobre modelos de
movilidad, los capítulos 2, 4 y 6 del libro de Zárate Ceballos y otros, y el artículo de Ospina y Ortiz
Triviño.

Un posible orden, para ajustar como quieran:
1. Redes ad hoc móviles
2. Organización jerárquica y clustering
3. Modelos de movilidad
4. Propagación de radio y RSSI
5. Localización con RSSI
6. Enrutamiento en MANET
7. Simulación de eventos discretos con NS-3
8. Referencias

El encabezado lleva los nombres de [`../autores.md`](../autores.md).
