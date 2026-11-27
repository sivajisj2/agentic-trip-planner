# Quick start

For detailed OS-specific commands, custom inputs and expected outputs, see [Run locally](LOCAL_SETUP.md).

## 1. Get the skill

Clone the repository:

```sh
git clone https://github.com/sivajisj2/agentic-trip-planner.git
cd agentic-trip-planner
```

Use Python 3.10 or later. On Windows use `python`; on Linux/macOS use `python3`. Run commands from the repository root.

## 2. Check the helpers

```powershell
python -m unittest discover -s tests -v
python scripts/score_destinations.py --input examples/goa-group-input.json
python scripts/calculate_budget.py --input examples/goa-budget.json
python scripts/validate_itinerary.py --input examples/goa-itinerary.json
```

The sample budget is INR 18,000 for four travelers, with INR 6,000 remaining. This is fixture data, not a travel quote.

## 3. Try the agent workflow

Open this directory in a compatible agent and explicitly ask it to read SKILL.md, or install the package using the host's skill instructions.

Example prompt:

> Plan a three-day Goa trip for four adults with a shared INR 24,000 budget. Collect preferences first, identify constraints, research only with available tools, and use the bundled scoring, budget and validation helpers. Do not invent votes or prices. Present a draft for review.

Review the ranked options, evidence labels, cost estimates, schedule and unresolved decisions. No booking or payment is made.

## 4. Marketplace version

Visit [GroupTrip Planner Pro on Agensi](https://www.agensi.io/skills/grouptrip-planner-pro) and follow the listing's installation instructions. Marketplace tool availability, pricing and host compatibility must be checked in your account. Local tests alone do not verify live tool calls.
