<div align="center">

# Marco teórico

**Taller 01: Simulación de MANETs**

**ME01 — Modelos estocásticos y simulación en computación y comunicaciones**

**Universidad Nacional de Colombia**
</div>

## 1. Redes ad hoc móviles (MANET)

Una red ad hoc móvil (Mobile Ad Hoc Network, MANET) es un conjunto de nodos inalámbricos
móviles que forman una red temporal, sin infraestructura previa ni administración centralizada.
Los nodos se mueven con libertad y se organizan por sí mismos, así que la topología puede cambiar
de forma rápida e impredecible [1]. A diferencia de las redes celulares, donde las estaciones base
concentran la conmutación, en una MANET cada nodo funciona a la vez como terminal y como router:
reenvía los paquetes de otros nodos cuando el destino queda fuera del alcance directo del
emisor [1].

De esa definición se desprenden las características que distinguen a una MANET y que condicionan el
diseño de sus protocolos [1]. No hay infraestructura ni controlador central, de modo que la
coordinación es distribuida y entre pares. La topología es dinámica, porque el movimiento de los
nodos crea y rompe enlaces de manera continua y obliga a mantener o redescubrir rutas con
frecuencia. La comunicación es multisalto: dos nodos que no se alcanzan directamente se comunican
a través de nodos intermedios. Y los recursos son limitados, pues el medio inalámbrico se comparte
y tiene ancho de banda restringido, mientras que los dispositivos suelen estar acotados en energía
y cómputo. A todo esto se suma que el canal es propenso a errores por interferencia, pérdidas de
transmisión y problemas de terminal oculto.

El enrutamiento es, por eso, un problema central. Como el destino puede no ser alcanzable de forma
directa, hace falta un protocolo que establezca y mantenga rutas multisalto sobre una topología
que cambia y con dispositivos de recursos escasos [1]. Las familias de protocolos de enrutamiento
se tratan en la Sección 6. El texto guía de simulación de redes ad hoc del grupo TLÖN de la
Universidad Nacional [2] presenta estas redes como sistemas dinámicos y estocásticos, cuyo estudio
se aborda bien mediante simulación, que es el enfoque de este taller.

El sistema de este taller es una MANET. Un collar emite una señal periódica (beacon) que los
celulares cercanos escuchan, y la propia red ad hoc, sin servidor central, estima y comunica la
posición del collar. El collar y los celulares intercambian información por Wi-Fi en modo ad hoc,
y los mensajes de aplicación viajan sobre el protocolo de enrutamiento multisalto que se elija.

## 2. Organización jerárquica y clustering

Las redes ad hoc pueden configurarse con una arquitectura plana o una jerárquica [3]. En la plana
todos los nodos actúan de forma independiente y se encargan del enrutamiento y el reenvío sin
ningún control externo. Esa configuración escala mal: el tamaño de las tablas de enrutamiento crece
con el número de nodos y la capacidad de tráfico por nodo decae a medida que la red se agranda,
según el límite clásico de capacidad de Gupta y Kumar [3].

La arquitectura jerárquica surge de algoritmos de clustering que agrupan nodos vecinos en
clústeres para atender las necesidades de la red —enrutamiento, ahorro de energía, cooperación— y
repartir mejor la carga de trabajo [3]. En cada clúster se elige una cabeza de clúster
(clusterhead) que hace de intermediaria y concentra las tareas de coordinación y reenvío hacia las
capas de arriba [3]. Al distribuir la carga por niveles, la jerarquía alcanza la escalabilidad que
la arquitectura plana no logra.

El reto propio de la jerarquía está en equilibrar los recursos y la carga entre capas, porque las
superiores deben poder sostener el trabajo extra de servir de intermediarias [3]. Para describir
ese reparto, Ospina y Ortiz-Triviño proponen un modelo probabilístico basado en la distribución
geométrica truncada, que relaciona los recursos de un nodo con el total de su clúster, e
introducen un factor de crecimiento $j$: una constante que expresa la relación de recursos entre
dos capas sucesivas necesaria para garantizar escalabilidad [3]. Simulando en ns-3 arquitecturas
jerárquicas de dos y tres niveles, los autores estiman ese factor, lo modelan como una relación
lineal entre capas y obtienen un valor cercano a la razón áurea $\varphi = \tfrac{1+\sqrt{5}}{2}$
con un nivel de confianza del 95 % [3].

El sistema de este taller adopta una organización jerárquica de dos niveles de agrupamiento sobre
los nodos. Siguiendo la nomenclatura del enunciado, el primer nivel lo forman los clústeres y el
segundo las zonas:

| Nivel | Qué agrupa | Cuántos |
|---|---|---|
| Primer nivel | Clústeres (buses y grupos de personas) | 4 |
| Segundo nivel | Zonas geográficas (sur y norte) | 2 |
| nodo | Celulares observadores (8 por clúster) | 32 |

Hay, entonces, cuatro clústeres en el primer nivel y dos zonas en el segundo, lo que satisface y
supera el requisito del enunciado de al menos tres clústeres en el primer nivel y dos en el segundo.
Cada clúster tiene una cabeza (su nodo 0) que recibe los reportes de sus celulares. Cada zona toma
como cabeza a la de uno de sus clústeres, y son esas cabezas de zona las que estiman la posición del
collar y responden las consultas. Esta estructura reproduce, a la escala del experimento, la idea de
capas con funciones diferenciadas de [3], y es también el origen de la movilidad grupal que se
analiza en la Sección 3.

## 3. Modelos de movilidad

Los modelos de movilidad describen cómo cambian de posición los nodos durante la simulación, y
tienen un efecto directo sobre el desempeño de los protocolos [1]. Suelen agruparse en modelos de
entidad, donde cada nodo se mueve por su cuenta, y modelos de grupo, donde el movimiento de los
nodos está correlacionado [1].

### 3.1 Modelos individuales

El modelo de caminata aleatoria (Random Walk) está inspirado en el movimiento errático de muchas
entidades naturales. El nodo pasa de su posición actual a una nueva eligiendo al azar una dirección
y una rapidez dentro de rangos fijos, y las cambia cada cierto tiempo o cada cierta distancia
recorrida; al llegar al borde del área rebota con un ángulo que depende de la dirección de
llegada [1]. Es un modelo sin memoria, porque la velocidad actual no depende de la anterior, lo que
puede producir giros bruscos y paradas repentinas y hace que los nodos no se alejen mucho de su
punto de partida [1].

El modelo de punto de destino aleatorio (Random Waypoint) añade tiempos de pausa entre los cambios.
El nodo permanece un rato en un lugar, luego elige un destino al azar dentro del área y una rapidez
uniforme entre un mínimo y un máximo, se desplaza hacia ese destino y, al llegar, vuelve a esperar
antes de repetir [1]. Si la pausa es cero y los límites de rapidez coinciden, su comportamiento se
parece al de Random Walk [1]. Es uno de los modelos más usados para evaluar protocolos ad hoc [1].

### 3.2 Modelos grupales

Los modelos de entidad como Random Waypoint suponen que cada nodo se mueve con independencia de los
demás, algo que no refleja escenarios reales donde los nodos van de forma coordinada, como un
equipo que sigue a un líder [1]. Cuando hay correlación espacial entre las velocidades de distintos
nodos se habla de dependencia espacial de la velocidad, y para representarla se usan los modelos de
movilidad grupal [1].

El modelo de referencia es el Reference Point Group Mobility (RPGM). El grupo se mueve siguiendo un
punto lógico de referencia —su centro o líder— y cada nodo se desplaza en relación con ese punto,
sumando un movimiento individual al movimiento común del grupo [1]. Así todos los miembros
comparten una trayectoria general pero conservan cierta libertad local, lo que modela bien un
pelotón de personas o los pasajeros de un vehículo.

### 3.3 Movilidad en el sistema del taller

La jerarquía de la Sección 2 se traduce en una composición de modelos de movilidad: la posición
absoluta de cada celular es la suma de tres capas, el origen de su zona, el desplazamiento de su
clúster y su movimiento propio dentro del clúster. En concreto, la simulación usa Random Walk para
el movimiento individual de cada celular dentro de la caja de su clúster, y también para el collar;
Random Waypoint con pausas para los clústeres de tipo grupo, como la plaza o el paseador, que se
desplazan como un todo; y una trayectoria por puntos de ruta (waypoints) para los clústeres de tipo
bus, que recorren en bucle una ruta rectangular fija con paradas en las esquinas.

La idea clave es que, al combinar el movimiento del clúster (nivel 1) con el de cada nodo dentro de
una caja pequeña relativa al clúster, la jerarquía produce movilidad grupal: los celulares de un
mismo clúster comparten el desplazamiento del clúster y solo difieren en un pequeño término local,
que es justo la idea del RPGM de un punto de referencia común con desplazamientos relativos [1].
Esto importa para la pregunta del taller. Los celulares de un mismo bus están casi en el mismo
punto, una geometría pobre para localizar por distancias (Sección 5); en cambio, un clúster que se
mueve cubre más área y escucha el collar con más frecuencia. El patrón de movilidad de los
observadores es la variable independiente del experimento.

## 4. Propagación de radio y RSSI

Para estimar la posición del collar a partir de la señal que reciben los celulares hace falta un
modelo de cómo la potencia recibida depende de la distancia. El RSSI (Received Signal Strength
Indicator) mide la potencia con la que un receptor decodifica una señal, normalmente en dBm, y es
el dato que cada celular anota al oír un beacon del collar.

El modelo de pérdida por trayectoria log-distancia establece que la potencia media recibida decae
con el logaritmo de la distancia, y el sombreado log-normal añade una componente aleatoria que
representa las variaciones por obstáculos y multitrayecto alrededor de esa media [1]. La potencia
recibida a una distancia $d$ queda entonces:

$$
P_r(d) = P_0 - 10\,n\,\log_{10}(d) + X_\sigma
$$

donde $P_0$ es la potencia a la distancia de referencia (aquí 1 m), $n$ es el exponente de pérdida
(vale 2 en espacio libre y crece en entornos con obstrucción) y $X_\sigma$ es el término de
sombreado, una variable aleatoria normal en dB con media cero y desviación $\sigma$ [1]. Como
$X_\sigma$ es gaussiana en la escala logarítmica (dB), la potencia recibida en escala lineal es
log-normal, de ahí el nombre del modelo [1].

En el taller el collar transmite por 802.11b (Wi-Fi en modo ad hoc) un beacon de difusión cada
segundo. El canal usa pérdida log-distancia con exponente $n = 2{,}7$ y una pérdida de referencia
de $40{,}05$ dB a 1 m (2,4 GHz), y el sombreado es normal en dB con $\sigma = 4$ dB. Así, $P_0$ es
la potencia de transmisión del collar menos la pérdida de referencia, y el término aleatorio
$X_\sigma \sim \mathcal{N}(0,\sigma^2)$ hace que dos lecturas tomadas a la misma distancia den
valores de RSSI distintos. Esta es la fuente de aleatoriedad central del modelo de radio (véase la
Sección 8).

Conviene anotar un artefacto del modelo. Lejos del collar solo se decodifican los beacons que, por
un sombreado favorable, llegan más fuertes de lo esperado; al ajustar RSSI contra distancia sobre
esas lecturas, el exponente estimado sale menor que el real (del orden de 1,6 en vez de 2,7) y la
distancia estimada tiende a quedar corta. Con sombreado nulo ($\sigma = 0$) el ajuste recupera el
exponente exacto. Además, en la simulación el sombreado se sortea de forma independiente por
paquete, mientras que en la realidad está correlacionado en espacio y tiempo, por lo que promediar
lecturas ayuda más aquí que en la vida real.

## 5. Localización con RSSI

A partir de las lecturas de RSSI y de las posiciones GPS de los celulares que oyeron el beacon, la
cabeza de zona estima dónde está el collar. El taller implementa tres estimadores de complejidad
creciente.

El primero es el del vecino más cercano. Toma como estimación la posición GPS del celular que
reportó el mayor RSSI, suponiendo que la señal más fuerte viene del observador más próximo. Es la
línea base, análoga a servicios tipo Find My: simple y robusta, pero con una resolución limitada
por la separación entre observadores.

El segundo es el centroide ponderado. Calcula el centroide de las posiciones GPS de los
observadores, pesando cada una por la potencia en escala lineal (mW), con peso
$w = 10^{\,\text{RSSI}/10}$. Los celulares con señal más fuerte pesan más, de modo que la
estimación se acerca a los observadores próximos sin depender de un único máximo.

El tercero es la trilateración. Convierte cada RSSI en una distancia estimada invirtiendo el modelo
de pérdida log-distancia,

$$
\hat{d} = 10^{\,(P_0 - \text{RSSI})/(10\,n)},
$$

y busca la posición del collar compatible con esas distancias. Como las ecuaciones de distancia son
no lineales en las coordenadas, el problema es de mínimos cuadrados no lineales: se minimiza el
error entre las distancias medidas y las predichas, con pesos $1/\hat{d}^2$ que dan más peso a los
observadores cercanos. La simulación lo resuelve con el método de Gauss-Newton, partiendo del
centroide como estimación inicial, y exige al menos tres celulares distintos. Para evitar
soluciones inestables cuando los observadores están casi alineados o superpuestos (una geometría
degenerada), controla el número de condición de la matriz normal $2\times 2$ y descarta la
estimación si supera un umbral.

La calidad de la trilateración depende mucho de la geometría de los observadores. Si todos están
casi en el mismo punto, como los celulares de un mismo bus (Sección 3), las circunferencias de
distancia se cortan en un ángulo muy pequeño y el error crece aunque haya muchas lecturas. Ese es
el núcleo de la hipótesis en tensión del taller: más lecturas no garantizan mejor localización si
la geometría es mala. El mismo procedimiento de estimación está implementado igual en C++ y en
Python, lo que permite sustituir el estimador sin tocar el resto de la simulación (Sección 7).

## 6. Enrutamiento en MANET

Los protocolos de enrutamiento de MANET se dividen en dos grandes familias según cuándo construyen
las rutas [1]. Los proactivos (table-driven) mantienen rutas hacia todos los destinos de forma
permanente, propagando actualizaciones periódicas y por eventos y guardándolas en tablas; derivan
de los algoritmos de vector-distancia y de estado de enlace [1]. Tienen la ruta lista de inmediato,
a costa de un tráfico de control constante. Los reactivos (bajo demanda) descubren una ruta solo
cuando se necesita, lo que reduce el tráfico de control pero añade una latencia inicial de
descubrimiento [1].

El taller puede seleccionar tres protocolos:

| Protocolo | Familia | Idea central |
|---|---|---|
| AODV [6] | Reactivo (bajo demanda) | Crea rutas solo cuando hacen falta, con descubrimiento por inundación (RREQ/RREP), y usa números de secuencia de destino para evitar bucles. |
| OLSR [7] | Proactivo, estado de enlace | Optimiza la inundación de estado de enlace con multipoint relays (MPR), que reducen las retransmisiones necesarias para llegar a los vecinos a dos saltos. |
| DSDV [8] | Proactivo, vector-distancia | Mantiene una ruta por destino en una tabla y usa un número de secuencia de destino, que crece ante cambios de vecindad, para garantizar rutas sin bucles. |

AODV es reactivo: en vez de mantener una lista completa de rutas, las crea bajo demanda; el
descubrimiento arranca cuando el origen no tiene una ruta válida y la petición se reenvía hacia el
destino [1], [6]. DSDV es un protocolo proactivo de vector-distancia adaptado a MANET que usa
números de secuencia de destino para evitar bucles [1], [8]. OLSR es una optimización de los
protocolos de estado de enlace cuyo punto clave son los multipoint relays [1], [7].

La diferencia entre reactivo y proactivo tiene consecuencias observables en el sistema del taller.
Con AODV las rutas descubiertas vencen tras pocos segundos, así que las consultas del dueño, que
llegan espaciadas en el tiempo, pueden encontrar la ruta caducada y quedar sin respuesta con más
frecuencia que con OLSR o DSDV, que mantienen las rutas de forma permanente. El protocolo de
enrutamiento es, junto con el patrón de movilidad, un factor del experimento.

## 7. Simulación de eventos discretos con NS-3 y ns3-ai

### 7.1 Simulación de eventos discretos y NS-3

La simulación de eventos discretos (Discrete-Event Simulation, DES) representa la evolución del
sistema mediante eventos que ocurren en instantes de tiempo determinados; cada evento es una
llamada a una función o clase con un identificador único [2]. Sus componentes esenciales son una
cola de eventos, que guarda los pendientes; un reloj de simulación, una variable global que marca
el tiempo y salta hasta el siguiente evento programado, quedándose congelada mientras un evento se
ejecuta; y las variables de estado que describen el sistema [2]. El reloj puede avanzar al
siguiente evento (next-event time advance) o en incrementos fijos (fixed-increment time
advance) [2].

NS-3 es un simulador de redes de eventos discretos, de código abierto, orientado a la investigación
y la docencia. Permite modelar un entorno de red completo, con nodos, dispositivos, canales, pilas
de protocolos, modelos de movilidad y enrutamiento, mediante guiones en C++ y Python, y exportar
trazas (.pcap, .tr) para su análisis [2], [4]. Sus abstracciones principales —nodos, dispositivos,
canales, aplicaciones y helpers— se enlazan para construir el escenario, y un planificador controla
la cola de eventos y el avance del reloj [2]. El taller usa NS-3 3.46 para la simulación en C++ y
Python para el análisis posterior.

### 7.2 ns3-ai

ns3-ai es un módulo que conecta NS-3 con algoritmos externos escritos en Python, pasando los datos
entre ambos por memoria compartida [5]. En el taller, con la opción de estimador en Python, en cada
instante de estimación la simulación se detiene, entrega a Python la ventana de lecturas y continúa
con la posición que Python devuelve. Esto permite cambiar el estimador de localización, por ejemplo
por un filtro de Kalman o un modelo entrenado, sin tocar el código C++. Su uso es opcional y
requiere compilar NS-3 con el módulo correspondiente.

## 8. Componentes aleatorios del modelo

Como este es un estudio en el marco de los modelos estocásticos, conviene dejar explícito qué es
aleatorio en la simulación y con qué distribución, pues de ahí sale la variabilidad de los
resultados. La salida de una simulación es, por su naturaleza, aleatoria: con un conjunto distinto
de números aleatorios, el mismo escenario produce una realización distinta, y por eso se corren
varias réplicas independientes, reiniciando los números aleatorios, para estimar las métricas de
interés y sus intervalos de confianza [2].

Las fuentes de aleatoriedad del modelo son cuatro. El sombreado del canal es el término
$X_\sigma \sim \mathcal{N}(0, \sigma^2)$ del modelo log-distancia (Sección 4), con $\sigma = 4$ dB;
se sortea por paquete y hace aleatorio el RSSI medido, de modo que en escala lineal la potencia
recibida es log-normal [1]. Es la aleatoriedad dominante: con $\sigma = 0$ el sombreado desaparece
y el canal se vuelve determinista. El error de GPS es un ruido gaussiano independiente por eje, con
desviación de 4 m, que la posición reportada de cada celular suma a la real e introduce
incertidumbre en las anclas de la localización. La movilidad aleatoria viene de Random Walk y
Random Waypoint, que eligen al azar direcciones, rapideces uniformes entre un mínimo y un máximo y,
en Random Waypoint, destinos y pausas (Sección 3) [1], lo que vuelve aleatoria la geometría de
observadores en cada instante de estimación. Por último, la temporización de la aplicación añade su
parte: los reportes salen tras un retardo aleatorio y las consultas del dueño se espacian con un
intervalo uniforme alrededor de su valor nominal, lo que aleatoriza la carga y los instantes de
medición.

El error y la frescura de la posición estimada son, por tanto, variables aleatorias cuyo
comportamiento depende del patrón de movilidad y del protocolo de enrutamiento. Caracterizar esa
dependencia es el objeto del experimento (literal f).

## 9. Referencias

[1] S. K. Sarkar, T. G. Basavaraju, y C. Puttamadappa, *Ad Hoc Mobile Wireless Networks: Principles, Protocols, and Applications*, 2.ª ed. Boca Raton, FL, EE. UU.: CRC Press, 2013.

[2] H. Zárate Ceballos, J. Parra Amaris, H. Jiménez Jiménez, D. Romero Rincón, O. Agudelo Rojas, y J. E. Ortiz Triviño, *Wireless Network Simulation: A Guide using Ad Hoc Networks and the ns-3 Simulator*.

[3] J. P. Ospina-López y J. E. Ortiz-Triviño, "Estimation of a growth factor to achieve scalable ad hoc networks", *Ingeniería y Universidad*, vol. 21, n.º 1, pp. 49–70, 2017, doi: 10.11144/Javeriana.iyu21-1.egfa.

[4] nsnam, "ns-3 Network Simulator", versión 3.46. [En línea]. Disponible: https://www.nsnam.org/

[5] H. Yin *et al.*, "ns3-ai: Fostering Artificial Intelligence Algorithms for Networking Research", en *Proc. Workshop on ns-3 (WNS3)*, 2020. [En línea]. Disponible: https://github.com/hust-diangroup/ns3-ai

[6] C. Perkins, E. Belding-Royer, y S. Das, "Ad hoc On-Demand Distance Vector (AODV) Routing", IETF, RFC 3561, jul. 2003.

[7] T. Clausen y P. Jacquet, "Optimized Link State Routing Protocol (OLSR)", IETF, RFC 3626, oct. 2003.

[8] C. E. Perkins y P. Bhagwat, "Highly dynamic Destination-Sequenced Distance-Vector routing (DSDV) for mobile computers", en *Proc. ACM SIGCOMM*, 1994, pp. 234–244.
