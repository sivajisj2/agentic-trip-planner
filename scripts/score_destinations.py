#!/usr/bin/env python3
"""Transparent TripSync AI destination scoring. Standard library only."""
import argparse
import json
import sys
import math
from pathlib import Path

WEIGHTS = {'rating': .30, 'preference': .30, 'votes': .25, 'coordinates': .15}


def number(value, field, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f'{field} must be a finite number between {low} and {high}')
    return float(value)


def score(data):
    if not isinstance(data, dict):
        raise ValueError('input must be a JSON object')
    preferences = data.get('preferences', {})
    if not isinstance(preferences, dict):
        raise ValueError('preferences must be an object')
    for category, value in preferences.items():
        number(value, f'preferences.{category}', 0, 5)
    places = data.get('places')
    if not isinstance(places, list):
        raise ValueError('places must be a list')
    ranked, warnings, ids = [], [], set()
    for p in places:
        if not isinstance(p, dict):
            raise ValueError('each place must be an object')
        pid, name, category = p.get('id'), p.get('name'), p.get('category')
        if not all(isinstance(v, str) and v.strip() for v in (pid, name, category)):
            raise ValueError('each place requires nonempty id, name and category')
        if pid in ids:
            raise ValueError(f'duplicate place id: {pid}')
        ids.add(pid)
        if not isinstance(p.get('excluded', False), bool):
            raise ValueError(f'{name}.excluded must be a boolean')
        if p.get('excluded', False):
            warnings.append(f'{name}: excluded by hard constraint')
            continue
        rating = p.get('rating')
        r = .5 if rating is None else number(rating, f'{name}.rating', 0, 5) / 5
        pref = number(preferences.get(category, 2.5), f'{name}.preference', 0, 5) / 5
        votes = p.get('votes', 0)
        if isinstance(votes, bool) or not isinstance(votes, int) or votes < 0:
            raise ValueError(f'{name}.votes must be a nonnegative integer')
        if 'votes' not in p:
            warnings.append(f'{name}: votes missing; zero-vote baseline used, not verified consensus')
        v = min(votes, 10) / 10
        lat, lon = p.get('latitude'), p.get('longitude')
        if lat is not None:
            number(lat, f'{name}.latitude', -90, 90)
        if lon is not None:
            number(lon, f'{name}.longitude', -180, 180)
        loc = 1 if lat is not None and lon is not None else .5
        value = round(100 * (WEIGHTS['rating'] * r + WEIGHTS['preference'] * pref + WEIGHTS['votes'] * v + WEIGHTS['coordinates'] * loc) + 1e-9, 2)
        explanations = [f'Rating: {rating}/5' if rating is not None else 'Rating unavailable: neutral 0.5', f'Category preference: {pref * 5:g}/5', f'Votes: {votes} (capped at 10 for scoring)', 'Coordinates available' if loc == 1 else 'Coordinates unavailable: neutral 0.5']
        ranked.append({'id': pid, 'name': name, 'category': category, 'score': value, 'rating': rating, 'votes': votes, 'source_url': p.get('source_url'), 'verified_at': p.get('verified_at'), 'explanations': explanations})
    ranked.sort(key=lambda p: (-p['score'], -(p['rating'] if p['rating'] is not None else -1), p['name'], p['id']))
    return {'scoring_model': {'weights': WEIGHTS, 'score_range': [0, 100], 'note': 'Coordinates represent data completeness, not route distance'}, 'ranked_places': ranked, 'warnings': warnings}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output')
    a = ap.parse_args()
    try:
        result = score(json.loads(sys.stdin.read() if a.input == "-" else Path(a.input).read_text(encoding='utf-8-sig')))
        encoded = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
        if a.output:
            Path(a.output).write_text(encoded, encoding='utf-8')
        else:
            print(encoded, end='')
    except (OSError, ValueError, TypeError, OverflowError) as e:
        ap.exit(1, f'ERROR: {e}\n')


if __name__ == '__main__':
    main()
