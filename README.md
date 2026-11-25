# GroupTrip Planner Pro

A portable, tool-agnostic AI agent skill for group travel planning. Inspired by the deterministic destination ranking and draft-review workflow in [TripSync AI](https://github.com/sivajisj2/tripsync-ai).

## Features

- Collect multiple travelers' preferences and hard constraints
- Research places with tools available to the host agent (no embedded API credentials)
- Transparent TripSync-style destination ranking with explanations
- Distinguish real votes from proposed ballots; handle disagreements
- Budget arithmetic with per-person and group totals
- Validate time overlaps, negative costs, and missing itinerary details
- Generate an editable, evidence-labeled itinerary before approval

## Install

Copy this entire directory to your AI agent's supported skills location, then follow that agent's skill-discovery instructions. Skill installation conventions vary by host; this ZIP does not install Agensi tools automatically.

The root `SKILL.md` is the agent entry point. `references/` contains detailed rules; `scripts/` contains Python standard-library helpers. No server, database, API key, or pip install is required for the offline scoring and validation examples.

## Run examples

From this directory:

```bash
python3 scripts/score_destinations.py --input examples/goa-group-input.json --output /tmp/grouptrip-ranked.json
python3 scripts/calculate_budget.py --input examples/goa-budget.json
python3 scripts/validate_itinerary.py --input examples/goa-itinerary.json
python3 -m unittest discover -s tests -v
```

The Goa data is **illustrative**, not live-researched. Scores do not assert that any place is currently open, bookable, or priced as shown.

## Input and output

Scoring accepts `preferences` (category → weight 0..5) and `places` with `id`, `name`, `category`, `rating` (0..5 or null), `latitude`/`longitude` (both or neither), `votes` (nonnegative integer), and optional `source_url`/`verified_at`. It outputs a sorted JSON list with score and explanations.

Budget accepts `participants`, `currency`, optional `group_limit`, and `items` with `name`, `amount`, `quantity`, `basis` (`group` or `per_person`), and `status` (`estimate` or `verified`).

Itinerary validator accepts `days` containing `date` and `activities` with `name`, `start`, `end` (`HH:MM`), and optional `cost` and `source_url`. It detects overlapping activities and invalid values; it does not infer travel time or check real opening hours.

## Provenance and limitations

The score uses the exact four weights documented in TripSync AI's `apps/api/src/smart.rs`: rating 0.30, category preference 0.30, capped group votes 0.25, coordinate availability 0.15. Missing rating/preference/location signals are neutral (0.5); vote signal is zero when no votes are recorded, matching the original code. The agent instructions distinguish **no vote data** from a verified zero-vote result and must not claim that consensus was reached.

The Rust app's `order_plan` uses squared coordinate differences for rough ordering. This skill does **not** represent that as route travel time. The helpers are offline validation tools, not live search or booking integrations. Agensi tool IDs are documented in SKILL.md; live calls and marketplace acceptance must be verified separately. All helper CLIs accept `--input -` for JSON via standard input.

## Packaging

Zip this folder with `SKILL.md` at the top level inside the package folder. Inspect marketplace-specific requirements before submitting. Never include `.env`, API keys, private data, or unlicensed third-party content.

## License

No open-source license is granted by this package. Public visibility does not grant redistribution rights. The owner should choose a distribution license before commercial publication; this package does not assert a license for the upstream TripSync AI repository.
