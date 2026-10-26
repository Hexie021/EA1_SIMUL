"""Guarda una partida reproducible para el informe y la demostración de la EA1."""
import argparse
import contextlib
import hashlib
import io
import json
import platform
from pathlib import Path

from yahtzee import play_game, print_scoreboard, print_stats


def generate_evidence(sims=300, seed=42):
    output = Path(__file__).resolve().parent / 'resultados'
    output.mkdir(exist_ok=True)
    console = io.StringIO()
    with contextlib.redirect_stdout(console):
        state = play_game(verbose_each_turn=True, sims_per_mask=sims, seed=seed)
        print_scoreboard(state)
        print_stats(state)
    p1, p2 = state.players
    winner = p1.name if p1.total > p2.total else p2.name if p2.total > p1.total else 'Empate'
    result = {
        'configuracion': {'simulaciones_por_alternativa': sims, 'semilla': seed,
                          'python': platform.python_version(),
                          'sha256_motor': hashlib.sha256(Path(__file__).with_name('yahtzee.py').read_bytes()).hexdigest()},
        'rondas': state.turn_in_round,
        'jugadores': [{'nombre': p.name, 'categorias': p.scores,
                       'subtotal_superior': p.upper_subtotal, 'bono_superior': p.upper_bonus,
                       'bonos_yahtzee': p.yahtzee_bonus, 'total': p.total} for p in state.players],
        'ganador': winner,
        'dados_lanzados': state.stats.total_rolls,
        'frecuencias': {str(face): state.stats.face_hist.get(face, 0) for face in range(1, 7)},
    }
    # Comprobaciones sobre la evidencia antes de guardarla.
    assert result['rondas'] == 13
    assert sum(result['frecuencias'].values()) == result['dados_lanzados']
    for p in result['jugadores']:
        assert len(p['categorias']) == 13 and all(v is not None for v in p['categorias'].values())
        assert p['total'] == sum(p['categorias'].values()) + p['bono_superior'] + p['bonos_yahtzee']
    header = f'EA1 - Evidencia de ejecución\nSimulaciones por alternativa: {sims}\nSemilla: {seed}\n\n'
    (output / 'partida.txt').write_text(header + console.getvalue(), encoding='utf-8')
    (output / 'resumen.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Evidencias guardadas en: {output}')
    print(f'{p1.name}: {p1.total} | {p2.name}: {p2.total} | Ganador: {winner}')
    print(f'Dados lanzados: {state.stats.total_rolls}')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sims', type=int, default=300)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    if args.sims <= 0:
        parser.error('--sims debe ser positivo')
    generate_evidence(args.sims, args.seed)
