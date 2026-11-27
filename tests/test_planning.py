import json
import sys
import unittest
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from score_destinations import score
from calculate_budget import calculate
from validate_itinerary import validate


class ScoringTests(unittest.TestCase):
    def test_example_ranks_and_score(self):
        data = json.loads((ROOT / 'examples/goa-group-input.json').read_text())
        result = score(data)
        self.assertEqual(result['ranked_places'][0]['id'], 'sample-beach')
        self.assertAlmostEqual(result['ranked_places'][0]['score'], 79.5)

    def test_neutral_missing_signals(self):
        result = score({'places': [{'id': 'x', 'name': 'X', 'category': 'cafes'}]})
        self.assertEqual(result['ranked_places'][0]['score'], 37.5)
        self.assertTrue(result['warnings'])

    def test_vote_cap(self):
        base = {'id': 'x', 'name': 'X', 'category': 'cafes', 'votes': 10}
        a = score({'places': [base]})['ranked_places'][0]['score']
        b = score({'places': [dict(base, votes=100)]})['ranked_places'][0]['score']
        self.assertEqual(a, b)

    def test_excluded_and_duplicates(self):
        p = {'id': 'x', 'name': 'X', 'category': 'cafes'}
        self.assertEqual(score({'places': [dict(p, excluded=True)]})['ranked_places'], [])
        with self.assertRaises(ValueError):
            score({'places': [p, p]})

    def test_reject_bad_inputs(self):
        p = {'id': 'x', 'name': 'X', 'category': 'cafes', 'rating': 6}
        with self.assertRaises(ValueError):
            score({'places': [p]})
        with self.assertRaises(ValueError):
            score({'places': [dict(p, rating=4, votes=-1)]})
        with self.assertRaises(ValueError):
            score({'places': [dict(p, rating=4, latitude=100)]})

    def test_deterministic_tie(self):
        places = [{'id': 'b', 'name': 'B', 'category': 'cafes'}, {'id': 'a', 'name': 'A', 'category': 'cafes'}]
        self.assertEqual([x['id'] for x in score({'places': places})['ranked_places']], ['a', 'b'])


class BudgetTests(unittest.TestCase):
    def test_example_budget(self):
        d = json.loads((ROOT / 'examples/goa-budget.json').read_text())
        r = calculate(d)
        self.assertEqual(r['group_total'], 18000)
        self.assertEqual(r['per_person_if_evenly_split'], 4500)
        self.assertEqual(r['remaining_budget'], 6000)
        self.assertFalse(r['over_budget'])

    def test_over_budget(self):
        r = calculate({'participants': 2, 'currency': 'INR', 'group_limit': 100, 'items': [{'name': 'Tickets', 'amount': 60, 'basis': 'per_person'}]})
        self.assertTrue(r['over_budget'])

    def test_reject_invalid_budget(self):
        with self.assertRaises(ValueError):
            calculate({'participants': 0, 'currency': 'INR', 'items': []})
        with self.assertRaises(ValueError):
            calculate({'participants': 1, 'currency': 'INR', 'items': [{'name': 'x', 'amount': -1, 'basis': 'group'}]})


class ItineraryTests(unittest.TestCase):
    def test_example_valid(self):
        d = json.loads((ROOT / 'examples/goa-itinerary.json').read_text())
        self.assertTrue(validate(d)['valid'])

    def test_overlap(self):
        d = {'timezone': 'Asia/Kolkata', 'days': [{'date': '2026-12-01', 'activities': [{'name': 'A', 'start': '09:00', 'end': '11:00'}, {'name': 'B', 'start': '10:30', 'end': '12:00'}]}]}
        r = validate(d)
        self.assertFalse(r['valid'])
        self.assertTrue(any('overlap' in e for e in r['errors']))

    def test_bad_time_and_cost(self):
        d = {'timezone': 'Asia/Kolkata', 'days': [{'date': '2026-12-01', 'activities': [{'name': 'A', 'start': '12:00', 'end': '11:00', 'cost': -2}]}]}
        self.assertFalse(validate(d)['valid'])

    def test_empty_days(self):
        self.assertFalse(validate({'timezone': 'UTC', 'days': []})['valid'])


class StandaloneCliTests(unittest.TestCase):
    def test_all_helpers_accept_stdin(self):
        for script, fixture in [('score_destinations.py','goa-group-input.json'), ('calculate_budget.py','goa-budget.json'), ('validate_itinerary.py','goa-itinerary.json')]:
            with self.subTest(script=script):
                result = subprocess.run([sys.executable, str(ROOT / 'scripts' / script), '--input', '-'], input=(ROOT / 'examples' / fixture).read_text(), text=True, capture_output=True, check=True, timeout=10)
                self.assertIsInstance(json.loads(result.stdout), dict)


class ReleaseRegressionTests(unittest.TestCase):
    def test_non_object_input(self):
        for fn in (score, calculate, validate):
            with self.subTest(fn=fn.__name__), self.assertRaises(ValueError):
                fn([])

    def test_nested_overlap(self):
        d = {'timezone': 'UTC', 'days': [{'date': '2026-12-01', 'activities': [
            {'name': 'A', 'start': '09:00', 'end': '15:00'},
            {'name': 'B', 'start': '10:00', 'end': '11:00'},
            {'name': 'C', 'start': '12:00', 'end': '13:00'}]}]}
        errors = validate(d)['errors']
        self.assertEqual(sum('overlap' in e for e in errors), 2)

    def test_strict_date(self):
        self.assertFalse(validate({'timezone': 'UTC', 'days': [{'date': '20261201', 'activities': []}]})['valid'])

    def test_boolean_exclusion(self):
        with self.assertRaises(ValueError):
            score({'places': [{'id': 'x', 'name': 'X', 'category': 'cafes', 'excluded': 'false'}]})

    def test_budget_overflow(self):
        with self.assertRaises(ValueError):
            calculate({'participants': 2, 'currency': 'INR', 'items': [{'name': 'X', 'amount': 1e308, 'quantity': 10, 'basis': 'group'}]})

    def test_ranked_fixture_matches(self):
        data = json.loads((ROOT / 'examples/goa-group-input.json').read_text(encoding='utf-8'))
        expected = json.loads((ROOT / 'examples/sample-ranked-output.json').read_text(encoding='utf-8'))
        self.assertEqual(score(data), expected)


if __name__ == '__main__':
    unittest.main()
