# d. Código fuente completo + versiones

**Qué pide la norma:** «código fuente completo de la herramienta construida (incluidas las versiones
utilizadas de librerías que no se encuentran en la instalación estándar del software)» (§3.1.1 d).

El código está en [`../../codigo/`](../../codigo/). Esta carpeta solo guarda el `.zip` que se adjunta al
correo y la tabla de versiones.

**Armar el zip** (desde `talleres/taller-01-manets/`), sin resultados ni binarios:
```bash
zip -r entregables/d-codigo/Taller01_MANETs_d_codigo.zip codigo -x 'codigo/resultados/*' -x '*.so' -x '*/__pycache__/*'
```

**Versiones usadas** (medidas el 29 oct 2026 en el Mac de desarrollo):

| Pieza | Versión | Para qué |
|---|---|---|
| ns-3 | 3.46.1 (ns-allinone-3.46.1) | Simulador |
| ns3-ai | fork DEFIANCE v1.45.2 (incluido en ns-allinone-3.46.1, `contrib/ai`) | Estimador en Python durante la simulación (opcional) |
| NetAnim | 3.110 (Qt 5.15.19) | Animación (opcional) |
| Compilador | Apple clang 21.0.0, arm64, macOS 27.0.1 | |
| CMake / Ninja / ccache | 4.4.5 / 1.13.2 / 4.14.2 | Compilación |
| Boost / protobuf / pybind11 | 1.92.0 / 36.2 / 3.1.0 | Dependencias de ns3-ai |
| Python | 3.13.5 (venv `~/tools/ns3ai-venv`) | Análisis y estimador ns3-ai |
| numpy / pandas / matplotlib | 2.5.4 / 3.1.0 / 3.11.2 | Análisis y gráficas |
| gymnasium / ray / protobuf (Python) | 1.2.2 / 2.59.0 / 7.36.2 | Los exige ns3-ai; el taller no los usa directamente |

**Cambios locales a ns-3/ns3-ai** que hay que declarar (detalle en el README del taller, sección Entorno):
1. `contrib/ai/examples/a-plus-b/CMakeLists.txt`: enlace a `libcore` (solo macOS; no afecta al taller).
2. `contrib/ai/python_utils/ns3ai_utils.py`: nombre por defecto de la memoria compartida. El taller no lo
   usa: `ns3ai_estimador.py` pasa el nombre explícito.
3. `contrib/defiance` retirado del árbol: no compilaba en macOS y el taller no lo usa.

Cómo instalar y correr: eso va en el manual técnico ([`../e-manuales/`](../e-manuales/)).
