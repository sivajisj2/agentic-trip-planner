#!/usr/bin/env python3
"""Static itinerary consistency checks, not live travel verification."""
import argparse
from datetime import date, datetime
import json
import sys
import math
from pathlib import Path


def validate(data):
    if not isinstance(data, dict):
        raise ValueError('input must be a JSON object')
    errors, warnings = [], []
    if not isinstance(data.get('timezone'), str) or not data['timezone'].strip():
        errors.append('timezone is required')
    days = data.get('days')
    if not isinstance(days, list) or not days:
        return {'valid': False, 'errors': errors + ['days must be a nonempty list'], 'warnings': warnings}
    dates = set()
    for i, day in enumerate(days):
        if not isinstance(day, dict):
            errors.append(f'days[{i}] must be an object')
            continue
        d = day.get('date')
        try:
            if not isinstance(d, str):
                raise ValueError()
            if date.fromisoformat(d).isoformat() != d:
                raise ValueError()
            if d in dates:
                errors.append(f'duplicate date: {d}')
            dates.add(d)
        except ValueError:
            errors.append(f'days[{i}].date must be YYYY-MM-DD')
        acts = day.get('activities')
        if not isinstance(acts, list):
            errors.append(f'days[{i}].activities must be a list')
            continue
        intervals = []
        for j, a in enumerate(acts):
            prefix = f'days[{i}].activities[{j}]'
            if not isinstance(a, dict) or not isinstance(a.get('name'), str) or not a['name'].strip():
                errors.append(f'{prefix}.name is required')
                continue
            try:
                start, end = [datetime.strptime(a[k], '%H:%M') for k in ('start', 'end')]
                if start.strftime('%H:%M') != a['start'] or end.strftime('%H:%M') != a['end']:
                    raise ValueError()
                if end <= start:
                    errors.append(f'{prefix} end must be after start; overnight activities require separate dates')
                else:
                    intervals.append((start, end, a['name']))
            except (KeyError, TypeError, ValueError):
                errors.append(f'{prefix} start/end must be valid HH:MM')
            if 'cost' in a:
                v = a['cost']
                if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0:
                    errors.append(f'{prefix}.cost must be a nonnegative finite number')
            if not a.get('source_url'):
                warnings.append(f'{prefix}: no source URL; venue facts and opening hours unverified')
        intervals.sort()
        latest = None
        for current in intervals:
            if latest is not None and current[0] < latest[1]:
                errors.append(f'{d}: overlap between {latest[2]} and {current[2]}')
            if latest is None or current[1] > latest[1]:
                latest = current
    warnings.append('Travel times, venue opening hours, bookings and accessibility are not validated by this script')
    return {'valid': not errors, 'errors': errors, 'warnings': warnings}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output')
    a = ap.parse_args()
    try:
        result = validate(json.loads(sys.stdin.read() if a.input == "-" else Path(a.input).read_text(encoding='utf-8-sig')))
        encoded = json.dumps(result, indent=2) + '\n'
        if a.output:
            Path(a.output).write_text(encoded, encoding='utf-8')
        else:
            print(encoded, end='')
        if not result['valid']:
            raise SystemExit(1)
    except (OSError, ValueError, TypeError, OverflowError) as e:
        ap.exit(1, f'ERROR: {e}\n')


if __name__ == '__main__':
    main()
