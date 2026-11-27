# Contributing

Report issues with a minimal reproducible example and expected versus actual behavior. Do not include credentials, personal trip details or paid tool responses containing private information.

For proposed changes, use a branch and pull request. Preserve the documented TripSync scoring weights unless explicitly proposing a model change. Keep scripts standalone and standard-library-only, update relevant fixtures and tests, and run:

```sh
python -m unittest discover -s tests -v
```

Review the [release checklist](docs/RELEASE_CHECKLIST.md). Public visibility is not an open-source license; contact the repository owner before redistribution.
