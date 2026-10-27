# Estabilidad de la estimación Montecarlo

Mano [3, 3, 5, 2, 6]; se conservan los dos tres y se relanzan tres dados una vez.
Categorías disponibles: treses, full house, trío y chance. Treinta repeticiones con semillas distintas por tamaño.
Referencia exacta: 3737/216 = 17.300926 puntos, calculada sobre 216 resultados equiprobables.

| Simulaciones | Promedio | Desviación entre repeticiones | Error absoluto medio | Error estándar teórico |
| ---: | ---: | ---: | ---: | ---: |
| 10 | 17.4467 | 1.1085 | 0.9667 | 1.1453 |
| 100 | 17.3053 | 0.3640 | 0.2895 | 0.3622 |
| 1000 | 17.2968 | 0.1140 | 0.0877 | 0.1145 |
| 10000 | 17.2871 | 0.0382 | 0.0324 | 0.0362 |

La desviación mide cuánto cambian las estimaciones entre las 30 repeticiones. El error absoluto medio compara cada estimación con la referencia exacta.
Bajo lanzamientos independientes y uniformes, la puntuación tiene media y varianza finitas. La Ley de los Grandes Números implica que el promedio converge a su esperanza. La varianza del promedio es la varianza de la puntuación dividida por N.
La evidencia finita ilustra esa estabilidad; no prueba la ley ni garantiza mejoras monótonas en cada repetición o más puntos en una partida. El experimento fija una decisión y no mide el sesgo de elegir el máximo entre varias estimaciones.

Fuente teórica: https://stat135.berkeley.edu/fall-2026/Modules/14-Consistency.html
