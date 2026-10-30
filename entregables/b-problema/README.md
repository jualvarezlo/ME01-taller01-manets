# b. Descripción y justificación del problema

Los lineamientos piden "un archivo PDF con descripción y justificación del problema a resolver". El correo del
profesor agrega que el problema debe ser una pregunta de investigación sobre modelos de movilidad en MANET, de
dificultad intermedia, y que se responde con el método científico. Lo escribe el grupo.

El borrador de la pregunta y de las hipótesis está en la sección "Borrador de la pregunta de investigación" del
[README](../../README.md).

Un posible orden:
1. Contexto: el perro perdido y su collar
2. Pregunta de investigación
3. Hipótesis
4. Por qué importa, y por qué la movilidad es la variable que estudiamos
5. Variables: las que cambiamos, las que medimos y las que dejamos fijas
6. Método: cómo vamos a responder la pregunta. El detalle va en el literal f
7. Alcance y supuestos

Para la sección 5, el código ya permite variar:
- la movilidad de clústeres y de nodos, `clusterMobility` y `nodeMobility`;
- el protocolo de enrutamiento, `routing`;
- la forma de combinar las zonas, `zoneFusion`;
- el método de estimación, `estMethod`;
- la densidad, `nodesPerCluster`;
- el sombreado, `shadowSigmaDb`.

Todos están en [`codigo/escenarios/base.conf`](../../codigo/escenarios/base.conf).

Lo que ya se mide:
- el error de localización en metros;
- si hubo estimación y qué tan vieja era;
- cuántos mensajes llegan y cuánto tardan;
- si el dueño recibió respuesta, cuánto tardó y qué tan errada estaba.

Para la sección 7, la sección "Qué declarar en el informe" del README lista los supuestos que conviene poner
por escrito.

El encabezado lleva los nombres de [`../autores.md`](../autores.md).
