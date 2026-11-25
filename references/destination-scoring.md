# TripSync AI scoring model

Derived from `apps/api/src/smart.rs` (`score_place`, `plan_score`). Formula:

`score = 100 * (0.30*R + 0.30*P + 0.25*V + 0.15*L)`

- R: rating/5, clamped 0..1; missing rating → 0.5.
- P: category preference/5, clamped 0..1; missing category preference → 0.5.
- V: min(votes,10)/10; zero recorded votes → 0.0.
- L: 1.0 when both latitude and longitude exist, else 0.5.

The coordinate component is a completeness bonus, **not** a proximity or travel-time score. Scores are rounded to 2 decimals. Tie-breaking: score descending, rating descending where available, name ascending, ID ascending. A destination violating hard constraints must be filtered out before scoring; the script accepts `excluded: true` and omits such places. Vote counts should come from actual participants; when missing, do not imply that zero reflects an actual ballot. Use a neutral zero-vote baseline for numerical compatibility with the original code and flag missing vote evidence.

Example input: `examples/goa-group-input.json`. Invoke `python3 scripts/score_destinations.py --input examples/goa-group-input.json --output /tmp/ranked.json`. Output is JSON with `ranked_places`, `scoring_model`, and `warnings`.

This scoring is a prioritization heuristic, not an ML model or LLM. It does not prove destination suitability or itinerary feasibility.
