# Release checklist

- [ ] Review changes and update SKILL.md version for behavior-changing releases.
- [ ] Update CHANGELOG.md and examples when behavior changes.
- [ ] Run python -m unittest discover -s tests -v from the repository root.
- [ ] Check Windows and Ubuntu CI results.
- [ ] Run all three CLI helpers on the example inputs.
- [ ] Test a conflicting-preference trip in a compatible agent.
- [ ] Verify missing-tool fallback and no fabricated votes or prices.
- [ ] Verify live Agensi tools with approved costs and actual host permissions.
- [ ] Build a marketplace ZIP containing SKILL.md, references/, scripts/ and examples/.
- [ ] Inspect ZIP contents; exclude secrets, private data, caches and Git metadata.
- [ ] Check current marketplace packaging rules and tool selection.
- [ ] Upload through Creator Studio; verify price, version and public listing.
- [ ] Test the published buyer experience after approval.

The GitHub repository and marketplace package are separate releases. A Git push does not update Agensi. Documentation-only changes need not alter the skill version if the distributed behavior is unchanged. See [submission notes](../AGENSI_SUBMISSION.md).
