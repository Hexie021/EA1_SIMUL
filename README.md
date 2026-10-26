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

También quedaron nueve pruebas de funcionamiento. Todas pasaron, incluida una partida completa con dos jugadores y trece turnos por jugador.

## Archivos

- `simulacion_01.ipynb`: cuaderno base del profe, sin modificaciones.
- `yahtzee.py`: versión del juego sobre la que estoy desarrollando la actividad.
- `test_yahtzee.py`: pruebas de puntuación base, decisiones, configuración y registro de lanzamientos.
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

En la prueba de esta etapa, con 30 simulaciones y semilla 42, el jugador 1 obtuvo 148 puntos y el jugador 2 obtuvo 203. Se registraron 251 dados lanzados. Son resultados de comprobación de la versión actual; los resultados para el informe se obtendrán cuando esté terminado el programa.

## Qué falta

La consigna habla de Yahtzee clásico. Antes de cerrar el juego falta revisar y completar las bonificaciones y la regla de comodín, que no están implementadas en el cuaderno base. Esto responde al alcance de juego clásico; no es una indicación adicional del profe.

Después se comprobará la versión completa y se obtendrán las evidencias para los resultados y las conclusiones de la EA1.

## Sobre el cuaderno de clase

El cuaderno original puede abrirse en Jupyter o Google Colab. Incluye NumPy, pandas, Matplotlib, Seaborn y Graphviz; para generar sus diagramas también necesita el ejecutable `dot`. Sus celdas contienen versiones repetidas del motor y sus salidas guardadas corresponden al material recibido. La ejecución completa de ese cuaderno no se ha validado en este desarrollo.

## Seguimiento y entrega

El trabajo se registra por avances mediante commits y push, para que se pueda revisar cómo se construyó la solución. En GitHub quedan el desarrollo y sus instrucciones. El Word se entrega por separado e incluirá el enlace a este repositorio; el video mostrará el funcionamiento y explicará el uso de Montecarlo.

**Estudiante:** Esteban Jaramillo Garro.

**Código base:** material del curso compartido por el docente Julián Andrés Loaiza López. Las modificaciones de la EA1 se pueden consultar en el historial del repositorio.
