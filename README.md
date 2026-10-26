# EA1 de Simulación — Yahtzee con Montecarlo

En este repositorio desarrollo la EA1 del curso de Simulación de la IU Digital de Antioquia. El punto de partida es el cuaderno de Python que compartió el profe en clase.

## Qué pide la actividad

Simular una partida de Yahtzee para dos jugadores, con cinco dados de seis caras y hasta tres lanzamientos por turno. Cada cara tiene una probabilidad de 1/6, correspondiente a una distribución uniforme discreta.

Para decidir cuáles dados conservar, el programa utiliza Montecarlo: simula posibles resultados de cada alternativa y compara sus puntuaciones promedio. Aunque la rúbrica menciona Markov, el profe aclaró que para esta actividad corresponde trabajar con Montecarlo.

## Lo que llevo hasta ahora

Conservé el cuaderno original y organicé el código del juego en `yahtzee.py` para trabajar sobre una sola versión del programa. En esta primera etapa quedaron corregidos tres puntos:

- Que se utilice realmente la cantidad de simulaciones configurada.
- Que la decisión contemple el último lanzamiento disponible.
- Que las estadísticas cuenten solo los dados que se lanzaron, sin volver a contar los conservados.

La estrategia evalúa el siguiente lanzamiento y vuelve a tomar una decisión después de cada tirada real. Es una aproximación de un paso; no garantiza la mejor puntuación de toda la partida.

En la segunda etapa completé la puntuación clásica y amplié las pruebas a 19. Todas pasaron, incluida una partida completa con dos jugadores y trece turnos por jugador. El marcador ahora separa los puntos por categoría y las bonificaciones.

## Archivos

- `simulacion_01.ipynb`: cuaderno base del profe, sin modificaciones.
- `yahtzee.py`: versión del juego sobre la que estoy desarrollando la actividad.
- `test_yahtzee.py`: pruebas de puntuación base, decisiones, configuración y registro de lanzamientos.
- `generar_evidencias.py`: ejecuta y guarda la partida utilizada como evidencia.
- `resultados/`: detalle de turnos, resumen de la partida y registro de pruebas.
- `.gitignore`: evita incluir archivos temporales y entornos locales.

## Cómo ejecutarlo

Para ejecutar `yahtzee.py` y sus pruebas se necesita Python 3. Estos archivos usan la biblioteca estándar, por lo que no requieren paquetes adicionales.

Desde la carpeta del repositorio, ejecutar:

```bash
python yahtzee.py --sims 30 --seed 42
```

Para ver los lanzamientos y las decisiones de cada turno:

```bash
python yahtzee.py --sims 30 --seed 42 --detalle
```

Para comprobar las pruebas:

```bash
python -m unittest -v test_yahtzee
```

`--sims` define cuántas simulaciones se realizan por alternativa. `--seed` fija la semilla para repetir una partida con la misma configuración. Si cambia la cantidad de simulaciones, también cambia el consumo de números aleatorios; por eso, mantener la semilla no asegura las mismas tiradas entre configuraciones distintas.

## Resultados de la ejecución

Para la evidencia de la EA1 ejecuté el programa con **300 simulaciones por alternativa y semilla 42**, usando Python 3.12.14. Repetí la ejecución con la misma configuración y obtuve los mismos resultados y turnos.

| Resultado | Jugador 1 | Jugador 2 |
| --- | ---: | ---: |
| Puntuación total | 175 | 211 |
| Subtotal de la sección superior | 32 | 50 |
| Bonificación superior | 0 | 0 |
| Bonificaciones por Yahtzee | 0 | 0 |

Ganó el jugador 2 por 36 puntos. Ambos completaron sus trece categorías y se registraron **244 dados realmente lanzados**, sin incluir los escenarios internos de Montecarlo. En esta partida no se activaron bonificaciones; esos casos sí se comprobaron en las pruebas.

Un ejemplo aparece en el primer turno del jugador 1: empezó con `[6, 1, 1, 6, 3]`, conservó los dos seis y terminó con `[6, 6, 5, 6, 4]`. Anotó 27 puntos en trío. El detalle permite seguir qué dados decidió conservar en cada lanzamiento.

Esta partida muestra el funcionamiento del programa. No demuestra que una cantidad de simulaciones sea mejor que otra ni que la estrategia sea óptima. Las frecuencias de las caras tampoco tienen que ser exactamente iguales en una muestra de 244 dados.

Para volver a generar los archivos de evidencia:

```bash
python generar_evidencias.py --sims 300 --seed 42
```

Este comando reemplaza `resultados/partida.txt` y `resultados/resumen.json` con la nueva ejecución. El resumen registra la configuración, la versión de Python y la huella SHA-256 del archivo del motor utilizado. `resultados/pruebas.txt` conserva el registro de las 19 pruebas satisfactorias de esta etapa; se pueden volver a ejecutar con el comando de pruebas indicado arriba.

## Reglas de puntuación

La versión actual incluye las trece categorías del cuaderno y las reglas que faltaban para el juego clásico:

- Bono de 35 puntos al alcanzar 63 o más en la sección superior.
- Bono de 100 por cada Yahtzee adicional si la casilla Yahtzee ya tiene 50.
- Con la casilla Yahtzee ocupada, cinco dados iguales deben anotarse primero en la categoría superior correspondiente si está libre. Si está ocupada, se usa una categoría inferior disponible como comodín. Si tampoco quedan categorías inferiores, se registra cero en una superior libre.
- Si Yahtzee se había anotado con cero, aplica el comodín pero no el bono de 100.

Montecarlo evalúa los puntos que se sumarían al total, incluidos los bonos inmediatos, sin modificar la hoja del jugador durante las simulaciones. Las pruebas verifican estos casos aunque no aparezcan en una partida particular.

Referencia para estas reglas: [instrucciones de Hasbro](https://www.hasbro.com/common/instruct/yahtzee.pdf) y [aclaración de Hasbro sobre Yahtzee adicional y comodín](https://hasbro-apac-eng.custhelp.com/app/answers/detail/a_id/975/).

## Qué falta

Completar el Word con estas evidencias y preparar la demostración del video. El código, las instrucciones y los resultados de ejecución ya están disponibles en el repositorio.

## Sobre el cuaderno de clase

El cuaderno original puede abrirse en Jupyter o Google Colab. Incluye NumPy, pandas, Matplotlib, Seaborn y Graphviz; para generar sus diagramas también necesita el ejecutable `dot`. Sus celdas contienen versiones repetidas del motor y sus salidas guardadas corresponden al material recibido. La ejecución completa de ese cuaderno no se ha validado en este desarrollo.

## Seguimiento y entrega

El trabajo se registra por avances mediante commits y push, para que se pueda revisar cómo se construyó la solución. En GitHub quedan el desarrollo y sus instrucciones. El Word se entrega por separado e incluirá el enlace a este repositorio; el video mostrará el funcionamiento y explicará el uso de Montecarlo.

**Estudiante:** Esteban Jaramillo Garro.

**Código base:** material del curso compartido por el docente Julián Andrés Loaiza López. Las modificaciones de la EA1 se pueden consultar en el historial del repositorio.
