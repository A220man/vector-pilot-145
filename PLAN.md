# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

beats-concrete-numbers

## Roadmap

### beats-concrete-numbers — Beats should count spoken numbers as concrete

Status: planned

Acceptance:
- spoken numbers like 'five hours' are counted as concrete beats
- PROPER regex uses lookbehind to avoid counting capitalized start-of-sentence words as proper names
- swipe --out works with bare filenames without crashing

Implementation: `skills/ig-reel/beats.py`, `scripts/beats_fix.py`

Tests: `tests/test_beats_concrete.py`

### swipe-bare-filename — swipe.py --out crash on bare filename

Status: planned

Acceptance:
- python3 skills/ig-reel/swipe.py captured.tsv --out swipe.md works with any filename
- no FileNotFoundError on os.makedirs(os.path.dirname(path))

Implementation: `scripts/swipe.py`

Tests: `tests/test_swipe_bare.py`

