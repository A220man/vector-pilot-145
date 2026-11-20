#!/usr/bin/env python3
"""
beats.py - Beat analysis for Instagram Reel hook scoring.

Counts "concrete" beats in a text script. A beat is concrete if it contains
a spoken number (e.g., "five hours") or a capitalized proper name (not at start
of sentence).

Usage:
    python3 skills/ig-reel/beats.py s.txt
    python3 skills/ig-reel/beats.py s.txt --json
"""

import re
import sys
import json

# Concrete number words and digits
CONCRETE_NUM_RE = re.compile(
    r'(?<![.!?]\s)(?:one|two|three|four|five|six|seven|eight|nine|ten'
    r'|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen'
    r'|eighteen|nineteen|twenty|thirty|forty|fifty|sixty'
    r'|seventy|eighty|ninety|hundred|thousand|million)'
    r'(?![\w\s])', re.IGNORECASE
)

# Proper name: capitalized word NOT at start of sentence (after . ! ?)
PROPER_RE = re.compile(
    r'(?<![.!?]\s)[A-Z][a-z]+'
)

CONCRETE_RE = re.compile(
    CONCRETE_NUM_RE.pattern + r'|' + PROPER_RE.pattern
)


def count_concrete(text: str) -> int:
    """Count concrete markers in text."""
    return len(CONCRETE_RE.findall(text))


def analyze_beat(beat_text: str) -> dict:
    """Analyze a single beat and return its concretely score."""
    concrete = count_concrete(beat_text)
    has_proper = bool(PROPER_RE.search(beat_text))
    return {
        "beat": beat_text.strip(),
        "concrete": concrete,
        "has_proper": has_proper,
        "is_concrete": concrete > 0 or has_proper,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: beats.py <file> [--json]")
        sys.exit(1)

    filepath = sys.argv[1]
    use_json = "--json" in sys.argv

    with open(filepath, 'r') as f:
        text = f.read()

    # Split into beats (non-empty lines)
    lines = [l.strip() for l in text.split('\n') if l.strip()]

    results = []
    for i, line in enumerate(lines, 1):
        result = analyze_beat(line)
        result["beat_number"] = i
        results.append(result)

    total_concrete = sum(r["concrete"] for r in results)
    total_beats = len(results)
    abstract_runs = sum(
        1 for r in results
        if not r["is_concrete"]
    )

    if use_json:
        output = {
            "total_beats": total_beats,
            "total_concrete": total_concrete,
            "abstract_runs": abstract_runs,
            "beats": [{"n": r["beat_number"], "concrete": r["concrete"], "has_proper": r["has_proper"], "beat": r["beat"]} for r in results],
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Total beats: {total_beats}")
        print(f"Concrete markers: {total_concrete}")
        if abstract_runs > 0:
            print(f"Abstract runs: {abstract_runs}")
        for r in results:
            status = "CONCRETE" if r["is_concrete"] else "abstract"
            prop = " (proper name)" if r["has_proper"] else ""
            print(f"  Beat {r['beat_number']}: {r['beat']!r} -> {status}{prop}")


if __name__ == "__main__":
    main()
