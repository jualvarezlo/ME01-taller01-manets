# e. Manual de usuario y manual técnico (PDF)

**Qué pide la norma:** «un archivo PDF con el manual de usuario y manual técnico» (§3.1.1 e). El correo del
profesor los recalca. Los escribe el grupo. Pueden ir en un solo PDF con dos partes.

## Manual de usuario: para quien corre la simulación y lee resultados

Esqueleto (solo títulos):
1. Qué hace el programa (en una página)
2. Requisitos (sistema operativo; lo ya instalado)
3. Correr una simulación
   - con los valores por defecto;
   - con un archivo de escenario (`--conf`, ver `codigo/escenarios/base.conf`).
4. Parámetros (tabla: nombre, qué controla, valor por defecto, rango razonable)
5. Correr el experimento completo (`analisis/experimento.py`)
6. Archivos de salida (qué trae cada CSV, `escena.png`, `netanim.xml`)
7. Ver la animación en NetAnim
8. Problemas frecuentes

Fuentes en el repo:
- `codigo/escenarios/base.conf`: todos los parámetros, comentados;
- el binario con `--help`;
- README del taller, sección «Código» (comandos).

## Manual técnico: para quien instala, mantiene o modifica el código

Esqueleto (solo títulos):
1. Arquitectura (remite al diseño, literal c)
2. Instalación paso a paso
   - ns-3 3.46.1;
   - NetAnim;
   - ns3-ai y el venv de Python.
3. Compilación (`./ns3 build scratch/manets/collar-sim`; qué hace `codigo/CMakeLists.txt`)
4. Estructura del código: archivo por archivo y función por función
5. Modelo de simulación: jerarquía, movilidad, canal, mensajes y estimación
6. Integración ns3-ai: memoria compartida, `ns3ai/collar-msg.h`, el binding, el ciclo de Python
7. Cómo extender
   - otro estimador (`estimar_peticion()` o `estimador.h`);
   - otro clúster o zona (`kClusters`, `kZones`);
   - otro protocolo.
8. Reproducibilidad: `RngRun`, `parametros.txt`, `parametros_texto.txt`
9. Problemas conocidos y decisiones
   - cola ARP;
   - el doble `CppSetFinished`;
   - `NS3_FAST_LINKERS=OFF`;
   - DEFIANCE retirado del árbol.

Fuentes en el repo:
- README del taller, secciones «Entorno» y «Código»: comandos exactos, errores encontrados y cómo se resolvieron;
- comentarios en `collar-sim.cc`.

Encabezado con los autores: ver [`../autores.md`](../autores.md).
