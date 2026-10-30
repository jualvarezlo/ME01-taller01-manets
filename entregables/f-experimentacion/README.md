# f. Experimentación y análisis de resultados

Los lineamientos piden documentar la experimentación y el análisis de al menos 3 escenarios de prueba. El
correo del profesor pide además resultados, análisis, conclusiones y recomendaciones. Las corridas y las
tablas las produce el código; el análisis lo escribe el grupo.

Los escenarios los define el grupo. Esta tabla sirve para registrarlos:

| # | Nombre | Archivo de parámetros | Qué cambia frente a `base.conf` | Qué prueba |
|---|---|---|---|---|
| E1 | | `codigo/escenarios/E1.conf` | | |
| E2 | | `codigo/escenarios/E2.conf` | | |
| E3 | | `codigo/escenarios/E3.conf` | | |

`analisis/experimento.py` ya cruza la movilidad de clúster con la de nodo, lo que da 4 combinaciones, y cada
una con los protocolos que se le pidan. Los demás factores se fijan por escenario en su archivo `.conf`.

Para producir los datos de un escenario, desde `codigo/` y con el entorno cargado:

```bash
python analisis/experimento.py --nombre E1 --reps 10 --routing aodv olsr dsdv -- --conf=escenarios/E1.conf
```

Eso deja en `codigo/resultados/E1/`:
- `experimento.csv`, con el error de localización por método y réplica;
- `experimento_red.csv`, con las métricas de red y de consultas por réplica;
- `comando.txt`, con el comando exacto.

Para ver una corrida suelta, `analisis/graficar.py` dibuja su `escena.png`.

Un posible orden del documento:
1. Diseño del experimento: factores, niveles, réplicas, semillas y duración
2. Escenarios, con la tabla de arriba completa
3. Resultados por escenario, con tablas y gráficas
4. Análisis: ¿se cumplen las hipótesis del literal b? Incluyan la variación entre réplicas, con intervalos de
   confianza
5. Conclusiones
6. Recomendaciones y trabajo futuro

Antes de sacar conclusiones, lean la sección "Qué declarar en el informe" del [README](../../README.md). Ahí
están los efectos del modelo que ya vimos y que pueden confundir el análisis.

El encabezado lleva los nombres de [`../autores.md`](../autores.md).
