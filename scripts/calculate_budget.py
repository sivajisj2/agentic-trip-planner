#!/usr/bin/env python3
"""Group budget totals; all amounts are user-provided, not researched prices."""
import argparse
import json
import sys
import math
from pathlib import Path


def amount(value, field):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError(f'{field} must be a finite nonnegative number')
    return float(value)


def calculate(data):
    if not isinstance(data, dict):
        raise ValueError('input must be a JSON object')
    n = data.get('participants')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError('participants must be a positive integer')
    currency = data.get('currency')
    if not isinstance(currency, str) or not currency.strip():
        raise ValueError('currency is required')
    items = data.get('items')
    if not isinstance(items, list):
        raise ValueError('items must be a list')
    total = 0
    breakdown = []
    for i, item in enumerate(items):
        if not isinstance(item, dict) or not isinstance(item.get('name'), str) or not item['name'].strip():
            raise ValueError(f'items[{i}].name is required')
        price = amount(item.get('amount'), f'items[{i}].amount')
        qty = amount(item.get('quantity', 1), f'items[{i}].quantity')
        basis = item.get('basis')
        if basis not in ('group', 'per_person'):
            raise ValueError(f'items[{i}].basis must be group or per_person')
        status = item.get('status', 'estimate')
        if status not in ('estimate', 'verified'):
            raise ValueError(f'items[{i}].status must be estimate or verified')
        group_cost = round(price * qty * (n if basis == 'per_person' else 1), 2)
        if not math.isfinite(group_cost):
            raise ValueError(f'items[{i}] group cost exceeds numeric range')
        total += group_cost
        if not math.isfinite(total):
            raise ValueError('group total exceeds numeric range')
        breakdown.append({'name': item['name'], 'group_cost': group_cost, 'basis': basis, 'status': status})
    total = round(total, 2)
    limit = data.get('group_limit')
    if limit is not None:
        limit = amount(limit, 'group_limit')
    return {'currency': currency, 'participants': n, 'group_total': total, 'per_person_if_evenly_split': round(total / n, 2), 'group_limit': limit, 'remaining_budget': round(limit - total, 2) if limit is not None else None, 'over_budget': total > limit if limit is not None else None, 'contains_estimates': any(x['status'] == 'estimate' for x in breakdown), 'items': breakdown}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output')
    a = ap.parse_args()
    try:
        result = json.dumps(calculate(json.loads(sys.stdin.read() if a.input == "-" else Path(a.input).read_text(encoding='utf-8-sig'))), indent=2) + '\n'
        if a.output:
            Path(a.output).write_text(result, encoding='utf-8')
        else:
            print(result, end='')
    except (OSError, ValueError, TypeError, OverflowError) as e:
        ap.exit(1, f'ERROR: {e}\n')


if __name__ == '__main__':
    main()
