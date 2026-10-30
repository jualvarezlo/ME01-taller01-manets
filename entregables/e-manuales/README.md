# e. Manual de usuario y manual técnico

Los lineamientos piden "un archivo PDF con el manual de usuario y manual técnico", y el correo del profesor
los vuelve a mencionar. Los escribe el grupo. Pueden ir en un solo PDF con dos partes.

## Manual de usuario

Es para quien corre la simulación y lee los resultados, sin tocar el código. Un posible orden:
1. Qué hace el programa, en una página
2. Qué hay que tener instalado
3. Correr una simulación con los valores por defecto, y con un archivo de escenario
4. Tabla de parámetros: nombre, qué controla, valor por defecto y un rango razonable
5. Correr el experimento completo
6. Qué trae cada archivo de salida
7. Ver la animación en NetAnim
8. Problemas frecuentes

Material de partida en el repositorio:
- las secciones "Correr", "Probar con otros parámetros" y "Archivos de salida" del [README](../../README.md);
- [`codigo/escenarios/base.conf`](../../codigo/escenarios/base.conf), con todos los parámetros comentados;
- `./simular --help`.

## Manual técnico

Es para quien instala, mantiene o modifica el código. Un posible orden:
1. Arquitectura, remitiendo al diseño del literal c
2. Instalación de ns-3, ns3-ai y NetAnim
3. Cómo se compila, y qué hace `codigo/CMakeLists.txt`
4. Estructura del código, archivo por archivo
5. El modelo: jerarquía, movilidad, canal, mensajes y estimación
6. La integración con ns3-ai: la memoria compartida, `ns3ai/collar-msg.h`, el binding y el ciclo de Python
7. Cómo agregar un estimador, un clúster o un protocolo
8. Reproducibilidad: semillas y archivos de parámetros
9. Problemas conocidos y decisiones que tomamos

Material de partida en el repositorio:
- [INSTALACION.md](../../INSTALACION.md), con los pasos y los errores conocidos;
- la sección "Qué simula" del README;
- los comentarios de `collar-sim.cc`.

El encabezado lleva los nombres de [`../autores.md`](../autores.md).
