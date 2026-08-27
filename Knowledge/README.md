# Knowledge

Distilled, grounded notes produced by the
[`extracting-knowledge`](../skills/extracting-knowledge/SKILL.md) skill,
grouped by theme:

```
Knowledge/
├── log.md                         # append-only ingest log
└── <theme-slug>/                  # e.g. demand-graph/
    ├── raw/YYYY-MM-DD-<slug>.md   # immutable source snapshots (never edited)
    ├── <topic-slug>.md            # topic notes: essentials of a subject
    └── pipeline-<slug>.md         # pipeline notes: registered processes
```

Every number, date, and quote in a note must exist verbatim in its linked `raw/`
files — verify the whole corpus with:

```bash
python3 ../skills/extracting-knowledge/scripts/check_evidence.py .
```

## Index

<!-- One "### Theme" section per theme folder; table: | Note | One-line summary | Updated | -->

*(empty — add your first note with the extracting-knowledge skill)*
