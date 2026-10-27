"""Experimento de estabilidad sobre una decisión fija de Yahtzee."""
import itertools
import json
import math
import random
import statistics
from fractions import Fraction
from pathlib import Path

from yahtzee import best_category_score, simulate_expected_value_after_keeps

DICE = [3, 3, 5, 2, 6]
KEEP = [True, True, False, False, False]
CATEGORIES = ['threes', 'fullHouse', 'threeOfKind', 'chance']
SIZES = [10, 100, 1000, 10000]
REPETITIONS = 30


def exact_reference():
    # Los 216 triples ordenados son equiprobables; se usa la misma puntuación
    # del motor. Esto da una referencia exacta, no otra estimación Montecarlo.
    scores = [best_category_score([3, 3, *tail], CATEGORIES)[1]
              for tail in itertools.product(range(1, 7), repeat=3)]
    mean = Fraction(sum(scores), len(scores))
    variance = sum((Fraction(v) - mean) ** 2 for v in scores) / len(scores)
    return mean, float(variance)


def run_experiment():
    reference, variance = exact_reference()
    rows = []
    rng_state = random.getstate()
    try:
        for n in SIZES:
            seeds = [20261026 + n * 100 + i for i in range(REPETITIONS)]
            estimates = []
            for seed in seeds:
                random.seed(seed)
                estimates.append(simulate_expected_value_after_keeps(DICE, KEEP, 1, CATEGORIES, n))
            rows.append({'n': n, 'semillas': seeds, 'estimaciones': estimates,
                         'promedio': statistics.mean(estimates),
                         'desviacion_entre_repeticiones': statistics.stdev(estimates),
                         'error_absoluto_medio': statistics.mean(abs(x-float(reference)) for x in estimates),
                         'error_estandar_teorico': math.sqrt(variance / n)})
    finally:
        random.setstate(rng_state)
    result = {'mano': DICE, 'conservar': KEEP, 'categorias': CATEGORIES,
              'lanzamientos_futuros': 1, 'repeticiones_por_n': REPETITIONS,
              'resultados_equiprobables': 216, 'media_exacta_fraccion': str(reference),
              'media_exacta': float(reference), 'varianza_puntuacion': variance,
              'comparacion': rows}
    output = Path(__file__).resolve().parent / 'resultados'
    output.mkdir(exist_ok=True)
    (output/'convergencia.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines = ['# Estabilidad de la estimación Montecarlo', '',
             'Mano [3, 3, 5, 2, 6]; se conservan los dos tres y se relanzan tres dados una vez.',
             'Categorías disponibles: treses, full house, trío y chance. Treinta repeticiones con semillas distintas por tamaño.',
             f'Referencia exacta: {reference} = {float(reference):.6f} puntos, calculada sobre 216 resultados equiprobables.', '',
             '| Simulaciones | Promedio | Desviación entre repeticiones | Error absoluto medio | Error estándar teórico |',
             '| ---: | ---: | ---: | ---: | ---: |']
    for row in rows:
        lines.append(f"| {row['n']} | {row['promedio']:.4f} | {row['desviacion_entre_repeticiones']:.4f} | {row['error_absoluto_medio']:.4f} | {row['error_estandar_teorico']:.4f} |")
    lines += ['', 'La desviación mide cuánto cambian las estimaciones entre las 30 repeticiones. El error absoluto medio compara cada estimación con la referencia exacta.',
              'Bajo lanzamientos independientes y uniformes, la puntuación tiene media y varianza finitas. La Ley de los Grandes Números implica que el promedio converge a su esperanza. La varianza del promedio es la varianza de la puntuación dividida por N.',
              'La evidencia finita ilustra esa estabilidad; no prueba la ley ni garantiza mejoras monótonas en cada repetición o más puntos en una partida. El experimento fija una decisión y no mide el sesgo de elegir el máximo entre varias estimaciones.', '',
              'Fuente teórica: https://stat135.berkeley.edu/fall-2026/Modules/14-Consistency.html']
    (output/'convergencia.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('\n'.join(lines))
    return result


if __name__ == '__main__':
    run_experiment()
