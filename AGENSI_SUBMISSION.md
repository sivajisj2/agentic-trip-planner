# Agensi submission checklist

Listing name: GroupTrip Planner Pro

Summary: Turn competing traveler preferences into an explainable shared itinerary, ranked options, and a checked budget.

Description: Coordinate group travel with transparent preference and vote scoring, destination research, draft review, schedule conflict detection, and group/per-person cost calculations. The portable skill derives its ranking methodology from TripSync AI and works with supplied data when research tools are unavailable. No bookings or payments are made by the skill.

Suggested tags: travel, itinerary, group-planning, productivity, budgeting, collaboration.

Tools to select: `agensi:google.serp.maps`, `agensi:google.serp.organic`. These IDs are documented by Agensi. Confirm availability, pricing and response schemas in the creator account before publishing. Tool fees are separate from the listing price.

Published listing: https://www.agensi.io/skills/grouptrip-planner-pro

The creator reports a $6 introductory price. Verify current pricing and payout settings in Creator Studio; no pricing or licensing changes are made by this repository.

## Submission steps

1. Create or sign in to your Agensi account and enable Creator Mode.
2. Verify the tool IDs and run a small real search with approval for costs.
3. Install the skill in a supported agent and run the acceptance scenarios below.
4. Upload the marketplace ZIP. Select the documented tools and describe Python execution as optional (required for deterministic helper verification). No third-party API keys are required by the skill.
5. Set pricing and payout options if paid. Submit for automated and manual review.
6. After approval, load your own skill and test the buyer workflow.

## Acceptance scenarios (manual, not yet executed)

- Four travelers, conflicting budgets and interests: ask only for missing essentials, show conflicts, and never invent votes.
- No search tools: use supplied places or mark research unavailable; do not invent venue facts.
- Agensi tools connected: quote cost, approve limited searches, normalize results, cite evidence, report any missing fields.
- Invalid schedule: run the validator and revise overlapping activities.
- Over-budget group: propose alternatives and show unresolved choices, not a false final plan.

Official references: https://www.agensi.io/docs/packaging and https://www.agensi.io/docs/skills-that-use-tools

Status: the creator reports that the original listing is live and the original 14 helper tests passed on Windows. This repository patch is v1.1.1; upload the updated skill through Creator Studio separately. Live agent acceptance and Agensi calls remain unverified.
