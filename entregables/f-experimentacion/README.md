# f. Experimentación y análisis de resultados (PDF)

**Qué pide la norma:** «documentación de la experimentación y análisis de resultados para al menos
3 escenarios de prueba» (§3.1.1 f). El enunciado pide además resultados, análisis, conclusiones y
recomendaciones. El análisis lo escribe el grupo. Las corridas y las tablas las produce el código.

**Escenarios:** los define el grupo. Plantilla para registrarlos:

| # | Nombre | Archivo `--conf` | Qué cambia frente a la base | Qué prueba |
|---|---|---|---|---|
| E1 | | `codigo/escenarios/…conf` | | |
| E2 | | | | |
| E3 | | | | |

El diseño factorial ya armado en `analisis/experimento.py` cruza `clusterMobility` × `nodeMobility`
(estático, solo-nodo, solo-clúster, clúster+nodo) × `routing`, con `--reps` réplicas por combinación.
Otros factores se fijan por escenario con `-- --conf=...` o `-- --zoneFusion=raw`, etc.

**Cómo producir los datos** (desde `codigo/`):
```bash
~/tools/ns3ai-venv/bin/python analisis/experimento.py --nombre E1 --reps 10 --routing aodv olsr dsdv -- --conf=escenarios/E1.conf
```
Deja en `codigo/resultados/E1/`:
- `experimento.csv`: localización fuera de línea, por método y réplica;
- `experimento_red.csv`: métricas de red y consultas, por réplica;
- `comando.txt`: el comando exacto que se corrió.

Para una corrida suelta, `analisis/graficar.py` dibuja `escena.png`.

**Esqueleto del documento** (solo títulos):
1. Diseño del experimento: factores, niveles, réplicas, semillas (`RngRun`), duración
2. Escenarios (la tabla de arriba, completa)
3. Resultados por escenario: tablas y gráficas
4. Análisis: ¿se cumplen las hipótesis del literal b? Incluir la variabilidad entre réplicas (intervalos de
   confianza)
5. Conclusiones
6. Recomendaciones y trabajo futuro

**Ojo al analizar:** los supuestos y artefactos que ya se detectaron están en la sección «Hallazgos del
código» del README del taller:
- censura de lecturas débiles;
- sombreado independiente por paquete;
- cola ARP;
- sesgo de cada zona hacia su lado;
- costo de tráfico de `zoneFusion=raw`.

Encabezado con los autores: ver [`../autores.md`](../autores.md).
