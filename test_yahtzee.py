import contextlib
import io
import unittest
from unittest.mock import patch
import yahtzee as y


class TestMotor(unittest.TestCase):
    def test_puntuaciones_base(self):
        cases = [
            ('ones',[1,1,2,3,4],2), ('twos',[2,2,2,3,4],6),
            ('threes',[3,3,3,3,5],12), ('fours',[4,4,1,2,3],8),
            ('fives',[5,5,5,1,2],15), ('sixes',[6,6,6,6,6],30),
            ('threeOfKind',[2,2,2,4,5],15), ('fourOfKind',[4,4,4,4,1],17),
            ('fullHouse',[2,2,3,3,3],25), ('smallStraight',[1,2,3,4,4],30),
            ('largeStraight',[2,3,4,5,6],40), ('yahtzee',[5]*5,50),
            ('chance',[1,2,3,4,5],15), ('fullHouse',[2]*5,0),
            ('largeStraight',[1,2,3,4,4],0), ('yahtzee',[1,1,1,1,2],0),
            ('threeOfKind',[1,2,3,4,5],0), ('fourOfKind',[2,2,2,3,3],0)
        ]
        for category,dice,expected in cases:
            with self.subTest(category=category,dice=dice):
                self.assertEqual(y.score_hand(category,dice),expected)

    def test_dados_conservados_no_se_cuentan(self):
        values=[1,2,3,4,5]
        with patch.object(y,'roll_single_die',side_effect=[6,6]) as roll:
            rolled=y.roll_dice(values,[True,False,True,False,True])
        stats=y.GameStats(); stats.update_from_roll(rolled)
        self.assertEqual(values,[1,6,3,6,5])
        self.assertEqual(roll.call_count,2)
        self.assertEqual(stats.total_rolls,2)
        self.assertEqual(dict(stats.face_hist),{6:2})

    def test_ultimo_lanzamiento_evalua_futuro(self):
        with patch.object(y,'roll_single_die',return_value=6):
            mask=y.choose_keep_mask_montecarlo([1]*5,1,['chance'],2)
        self.assertEqual(mask,[False]*5)

    def test_conservar_mano_maxima(self):
        self.assertEqual(y.choose_keep_mask_montecarlo([6]*5,1,['chance'],5),[True]*5)
        self.assertEqual(y.choose_keep_mask_montecarlo([1]*5,0,['chance'],5),[True]*5)

    def test_numero_real_de_simulaciones(self):
        with patch.object(y,'roll_single_die',return_value=6) as roll:
            value=y.simulate_expected_value_after_keeps([1]*5,[True]*4+[False],1,['chance'],7)
        self.assertEqual(roll.call_count,7)
        self.assertEqual(value,10)

    def test_configuracion_se_actualiza_y_se_propaga(self):
        with patch.object(y,'SIMS_PER_MASK',7), patch.object(y,'simulate_expected_value_after_keeps',return_value=1) as ev:
            y.choose_keep_mask_montecarlo([1]*5,1,['chance'])
            self.assertEqual(ev.call_count,32)
            self.assertTrue(all(call.args[4]==7 for call in ev.call_args_list))
        with patch.object(y,'simulate_expected_value_after_keeps',return_value=1) as ev:
            with contextlib.redirect_stdout(io.StringIO()):
                y.play_game(sims_per_mask=9)
            self.assertTrue(all(call.args[4]==9 for call in ev.call_args_list))

    def test_categoria_no_se_repite(self):
        p=y.PlayerState('Prueba'); p.set_score('ones',3)
        with self.assertRaises(ValueError): p.set_score('ones',4)
        self.assertEqual(p.total,3)

    def test_rechaza_simulaciones_invalidas(self):
        for n in [0,-1,1.5,True]:
            with self.subTest(n=n), self.assertRaises(ValueError):
                y.play_game(sims_per_mask=n)

    def test_partida_completa_reproducible(self):
        with contextlib.redirect_stdout(io.StringIO()):
            first=y.play_game(sims_per_mask=5,seed=42)
            second=y.play_game(sims_per_mask=5,seed=42)
        self.assertEqual(first,second)
        self.assertEqual(first.turn_in_round,13)
        self.assertEqual(first.current_player_idx,0)
        for player in first.players:
            self.assertEqual(len(player.scores),13)
            self.assertTrue(all(v is not None for v in player.scores.values()))
            self.assertEqual(player.total,sum(player.scores.values()) + player.upper_bonus + player.yahtzee_bonus)
        self.assertEqual(sum(first.stats.face_hist.values()),first.stats.total_rolls)
        self.assertGreaterEqual(first.stats.total_rolls,130)
        self.assertLessEqual(first.stats.total_rolls,390)


    def test_bonus_superior_umbral_y_no_se_duplica(self):
        p=y.PlayerState('Prueba')
        for c,n in [('sixes',30),('fives',25),('fours',4),('threes',3)]: p.set_score(c,n)
        self.assertEqual(p.upper_bonus,0)
        self.assertEqual(p.record_hand('ones',[1,2,3,4,5]),36)
        self.assertEqual(p.upper_bonus,35)
        p.record_hand('chance',[1,2,3,4,5])
        self.assertEqual(p.total,63+35+15)

    def test_yahtzee_adicional_obliga_superior(self):
        p=y.PlayerState('Prueba'); p.record_hand('yahtzee',[6]*5)
        self.assertEqual(p.yahtzee_bonus,0)
        self.assertEqual(p.scoring_options([6]*5),{'sixes':30})
        with self.assertRaises(ValueError): p.record_hand('chance',[6]*5)
        self.assertEqual(p.total,50)
        self.assertEqual(p.record_hand('sixes',[6]*5),130)
        self.assertEqual(p.yahtzee_bonus,100)

    def test_comodin_categorias_inferiores(self):
        p=y.PlayerState('Prueba'); p.set_score('yahtzee',50); p.set_score('sixes',18)
        options=p.scoring_options([6]*5)
        self.assertEqual(options,{'threeOfKind':30,'fourOfKind':30,'fullHouse':25,
                                 'smallStraight':30,'largeStraight':40,'chance':30})
        self.assertEqual(p.record_hand('largeStraight',[6]*5),140)
        self.assertEqual(p.record_hand('fullHouse',[6]*5),125)
        self.assertEqual(p.yahtzee_bonus,200)

    def test_yahtzee_en_cero_permite_comodin_sin_bono(self):
        p=y.PlayerState('Prueba'); p.set_score('yahtzee',0)
        self.assertEqual(p.scoring_options([3]*5),{'threes':15})
        self.assertEqual(p.record_hand('threes',[3]*5),15)
        self.assertEqual(p.record_hand('fullHouse',[3]*5),25)
        self.assertEqual(p.yahtzee_bonus,0)

    def test_comodin_sin_inferiores_anota_cero(self):
        p=y.PlayerState('Prueba')
        for c in y.CATEGORIES_ORDER[6:]: p.set_score(c,50 if c=='yahtzee' else 0)
        p.set_score('sixes',18)
        self.assertEqual(p.scoring_options([6]*5),{c:0 for c in y.CATEGORIES_ORDER[:5]})
        self.assertEqual(p.record_hand('ones',[6]*5),100)
        self.assertEqual(p.scores['ones'],0)

    def test_sin_yahtzee_previo_no_hay_comodin(self):
        p=y.PlayerState('Prueba')
        self.assertEqual(p.scoring_options([4]*5)['fullHouse'],0)
        self.assertEqual(p.best_option([4]*5),('yahtzee',50))

    def test_estimador_incluye_bonos_sin_alterar_jugador(self):
        p=y.PlayerState('Prueba'); p.set_score('yahtzee',50)
        before=dict(p.scores)
        ev=y.simulate_expected_value_after_keeps([6]*5,[True]*5,1,p.available_categories(),5,p)
        self.assertEqual(ev,130)
        self.assertEqual(p.scores,before)
        self.assertEqual(p.total,50)
        mask=y.choose_keep_mask_montecarlo([6]*5,1,p.available_categories(),5,p)
        self.assertEqual(mask,[True]*5)

    def test_decision_valora_bonus_superior(self):
        p=y.PlayerState('Prueba'); p.set_score('sixes',30); p.set_score('fives',25); p.set_score('fours',4)
        self.assertEqual(p.best_option([1,1,1,1,2]),('ones',39))

    def test_tres_tiradas_como_maximo(self):
        state=y.GameState([y.PlayerState('Prueba')])
        with patch.object(y,'choose_keep_mask_montecarlo',return_value=[False]*5), patch.object(y,'roll_single_die',return_value=2) as roll:
            y.play_one_turn(state,verbose=False,sims_per_mask=1)
        self.assertEqual(roll.call_count,15)
        self.assertEqual(state.rolls_left,0)
        self.assertEqual(state.stats.total_rolls,15)

    def test_marcador_empate(self):
        state=y.GameState([y.PlayerState('Uno'),y.PlayerState('Dos')])
        output=io.StringIO()
        with contextlib.redirect_stdout(output): y.print_scoreboard(state)
        self.assertIn('Ganador: Empate',output.getvalue())


if __name__=='__main__':
    unittest.main()
