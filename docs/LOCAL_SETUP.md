# Run locally

GroupTrip Planner Pro is an AI agent skill, not a web application. There is no local server, localhost URL, database, Docker setup, npm installation or API key needed for offline helpers.

## Prerequisites

- Git (or download and extract the repository ZIP).
- Python 3.10 or later.
- Optional: VS Code and an AI agent that can read local files and execute Python.

## Windows PowerShell

Open PowerShell. Run each command separately.

For a new clone:

```powershell
git clone https://github.com/sivajisj2/agentic-trip-planner.git
cd agentic-trip-planner
```

If you already cloned the repository, enter that directory instead and update it:

```powershell
cd "$HOME\agentic-trip-planner"
git pull --ff-only origin main
```

Adjust the path if your clone lives elsewhere.

```powershell
python --version
Get-ChildItem
python -m unittest discover -s tests -v
python scripts/score_destinations.py --input examples/goa-group-input.json
python scripts/calculate_budget.py --input examples/goa-budget.json
python scripts/validate_itinerary.py --input examples/goa-itinerary.json
```

If `python` is unavailable but the Windows Python launcher is installed, use `py -3` in its place. No pip install or virtual environment is required.

## Linux/macOS

For a new clone:

```bash
git clone https://github.com/sivajisj2/agentic-trip-planner.git
cd agentic-trip-planner
```

For an existing clone, change into its actual directory and run `git pull --ff-only origin main`.

```bash
python3 --version
ls
python3 -m unittest discover -s tests -v
python3 scripts/score_destinations.py --input examples/goa-group-input.json
python3 scripts/calculate_budget.py --input examples/goa-budget.json
python3 scripts/validate_itinerary.py --input examples/goa-itinerary.json
```

## Expected results

The v1.1.1 suite contains 20 tests; expect `OK` after all pass. This is an expected result, not a claim that the expanded suite has been run on your machine.

| Check | Expected fixture result |
| --- | --- |
| Ranking | Sample Beach Viewpoint, 79.5/100 |
| Group budget | INR 18,000 |
| Equal split | INR 4,500 for four people |
| Remaining budget | INR 6,000 |
| Schedule | valid: true, with warnings about unverified real-world details |

All example places, votes and costs are illustrative. Do not interpret them as live travel information.

## Run with your own JSON

Copy the corresponding example into a separate personal working directory and edit its fields. Do not commit private trip data. Pass the actual file path to the helper.

For example, from the repository root, after creating your own `my-trip.json` based on the scoring example:

```powershell
python scripts/score_destinations.py --input my-trip.json --output my-ranked.json
```

Use `python3` on Linux/macOS. Choose a fresh output filename: the scripts overwrite an existing output file if explicitly supplied. Each helper also supports `--input -` to read JSON from stdin. See [input formats](../README.md#input-and-output).

## Use the actual AI skill

The Python helpers alone do not generate a conversational travel plan. Open the repository folder in a compatible AI agent (for example, Codex in VS Code), or use your host's supported skill installation process.

If VS Code and its command-line launcher are installed, run `code .` from the repository root. In the agent chat, enter:

> Read SKILL.md and its referenced files. Act as GroupTrip Planner Pro. Plan a three-day Goa trip for four travelers with a total INR 24,000 budget. Ask for missing preferences and constraints, distinguish supplied data from estimates, use the bundled Python scripts, and return a reviewable itinerary. Do not invent votes or research, modify source code, or make bookings. Do not use paid tools without approval.

Confirm the agent reads the skill, invokes the correct helpers, reports missing inputs and produces a draft. Local agent execution requires that agent's own installation and authentication.

## Test the Agensi integration separately

Open [the live listing](https://www.agensi.io/skills/grouptrip-planner-pro) and follow its host-specific installation instructions. Check that the two documented search tools are available. Approve any tool charges before running live research. Do not assume that cloning GitHub installs marketplace tools or grants access to paid services.

GitHub source and the marketplace package are independently versioned; check the installed version. Local Python tests do not verify live Agensi calls.

## Troubleshooting

If tests cannot find `tests`, check the current directory (`Get-Location` on Windows or `pwd` on Linux/macOS). It must contain SKILL.md and the tests directory. See [troubleshooting](TROUBLESHOOTING.md) for other errors.
