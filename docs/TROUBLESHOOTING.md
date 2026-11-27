# Troubleshooting

| Symptom | Resolution |
| --- | --- |
| Start directory is not importable: tests | Change into the cloned repository; check that tests/ exists. |
| python3 not recognized on Windows | Use python --version, then python instead of python3. |
| Set-Location positional parameter error | Execute cd and Python commands separately; do not concatenate them. |
| ERROR: input must be a JSON object | Supply a JSON object, not an array or null. |
| Invalid date or time | Use YYYY-MM-DD and HH:MM; split overnight activities across dates. |
| Overlap reported | Review the conflicting activities and adjust the schedule. |
| Over-budget result | Review quantity and group/per_person basis, then revise the draft. |
| No research tools | Use supplied candidates or clearly label research as unavailable. |
| Agensi tool unavailable | Check the host connection, tool selection, permissions and charges. Do not invent results. |

Run the tests from the repository root after updates:

```powershell
git pull origin main
python -m unittest discover -s tests -v
```

For bug reports, include the Python version, operating system, commit SHA and a minimal sanitized JSON example. Remove private traveler details and credentials.
