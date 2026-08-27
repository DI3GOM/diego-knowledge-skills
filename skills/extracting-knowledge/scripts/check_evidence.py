#!/usr/bin/env python3
"""Grounding lint for Knowledge/ notes. Report-only; never modifies files.

For every note (*.md outside raw/, excluding README.md and log.md) that links
raw files in its `raw:` frontmatter, extract high-signal literals from the note
body and grep each verbatim into the linked raws. High-signal candidate set
(kept narrow on purpose — small plain integers are left to the write-time
locate-before-write rule):
  - quoted spans of 15+ chars ("..." and blockquoted lines)
  - ISO dates (YYYY-MM-DD, YYYY-MM)
  - specific numbers: thousands-grouped (10,000), dotted (2.1.80, 3.14),
    suffixed (42K, 99.9%, 3M), or 4+ digits (2026)

Also reports: notes with no raw links, raw links that don't resolve or escape
raw/, and raw files no note references.

Usage: python3 check_evidence.py /path/to/Knowledge
"""
import re
import sys
from pathlib import Path

DATE_RE = re.compile(r'\b\d{4}-\d{2}(?:-\d{2})?\b')
NUM_RE = re.compile(r'\b\d{1,3}(?:,\d{3})+\b|\b\d+\.\d[\d.]*\b|\b\d+(?:\.\d+)?\s?[KkMmBb%]\b|\b\d{4,}\b')
QUOTE_RE = re.compile(r'"([^"\n]{15,})"')


def literals(body: str) -> set[str]:
    out = set()
    for line in body.splitlines():
        if line.lstrip().startswith('>') and len(line.lstrip('> ').strip()) >= 15:
            out.add(line.lstrip('> ').strip())
        out.update(QUOTE_RE.findall(line))
        out.update(DATE_RE.findall(line))
        out.update(NUM_RE.findall(line))
    return out


def frontmatter_raws(text: str) -> list[str]:
    m = re.match(r'^---\n(.*?)\n---', text, re.S)
    if not m:
        return []
    raws, in_raw = [], False
    for line in m.group(1).splitlines():
        if re.match(r'^raw:\s*$', line):
            in_raw = True
        elif in_raw and re.match(r'^\s+-\s+', line):
            raws.append(line.split('-', 1)[1].strip())
        elif not line.startswith(' '):
            in_raw = False
    return raws


def main(root: Path) -> None:
    notes = [p for p in root.rglob('*.md')
             if 'raw' not in p.parent.parts and p.name not in ('README.md', 'log.md')]
    all_raws = {p for p in root.rglob('raw/*.md')}
    referenced = set()
    problems = 0

    for note in notes:
        text = note.read_text(encoding='utf-8')
        rel = note.relative_to(root)
        raws = frontmatter_raws(text)
        if not raws:
            print(f'[no raw links]  {rel}')
            problems += 1
            continue
        raw_texts = []
        for r in raws:
            rp = (note.parent / r).resolve()
            if not rp.is_file() or 'raw' not in rp.parts:
                print(f'[bad raw link]  {rel}: {r}')
                problems += 1
            else:
                referenced.add(rp)
                raw_texts.append(rp.read_text(encoding='utf-8'))
        corpus = '\n'.join(raw_texts)
        body = re.sub(r'^---\n.*?\n---', '', text, flags=re.S)
        for lit in sorted(literals(body)):
            if lit not in corpus:
                print(f'[not in raw]    {rel}: {lit!r}')
                problems += 1

    for rp in sorted(all_raws - {p.resolve() for p in referenced}):
        print(f'[orphan raw]    {rp.relative_to(root)}')

    print(f'\n{len(notes)} notes checked, {problems} problems.')


if __name__ == '__main__':
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_dir():
        sys.exit(__doc__)
    main(Path(sys.argv[1]).resolve())
