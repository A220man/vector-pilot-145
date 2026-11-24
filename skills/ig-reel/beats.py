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
import pathlib

# Concrete number words and digits
# Fixed: removed (?![\w\s]) lookahead that prevented matching numbers followed by space
# Changed to (?=[\s.,;!?]|$) - number must be followed by sentence boundary or end
CONCRETE_NUM_RE = re.compile(
    r"(?<![.!?]\s)"
    r"(?:one|two|three|four|five|six|seven|eight|nine|ten"
    r"|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen"
    r"|eighteen|nineteen|twenty|thirty|forty|fifty|sixty"
    r"|seventy|eighty|ninety|hundred|thousand|million)"
    r"(?=[\s.,;!?]|$)", re.IGNORECASE
)

# Proper name: capitalized word NOT at start of sentence (after . ! ?)
# Fixed: added (?<!\A) to also exclude words at the very start of the string
# The (?<![.!?]\s) lookbehind already prevents matching after period+space
PROPER_RE = re.compile(
    r"(?<![.!?]\s)(?<!\A)[A-Z][a-z]+"
)

CONCRETE_RE = re.compile(
    CONCRETE_NUM_RE.pattern + "|" + PROPER_RE.pattern
)


def count_concrete(text: str) -> int:
    """Count concrete markers in text."""
    return len(CONCRETE_RE.findall(text))


def analyze_beat(beat_text: str) -> dict:
    """Analyze a single beat and return its concretely score."""
    concrete = count_concrete(beat_text)
    total = len(re.findall(CONCRETE_RE, beat_text))
    if concrete > 0:
        status = "CONCRETE"
    else:
        status = "ABSTRACT"
    return {
        "beat": beat_text,
        "concrete": concrete,
        "total": total,
        "is_concrete": concrete > 0,
        "status": status,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: beats.py <file> [--json]")
        sys.exit(1)

    path = pathlib.Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    text = path.read_text()
    beats_list = text.split("\n")
    results = []
    for i, beat in enumerate(beats_list, start=1):
        r = analyze_beat(beat)
        prop = ""
        if r["is_concrete"]:
            prop = " (concrete)"
        elif r["total"] > 0:
            prop = " (abstract)"
        results.append((i, r["beat"], r["status"], prop))

    total_beats = len(results)
    total_concrete = sum(
        1 for _, _, _, prop in results if " (concrete)" in prop
    )

    print(f"Total beats: {total_beats}")
    print(f"Concrete markers: {total_concrete}")
    print(f"Abstract runs: {total_beats - total_concrete}")
    for beat_num, beat_text, status, prop in results:
        print(f"  Beat {beat_num}: {beat_text!r} -> {status}{prop}")


if __name__ == "__main__":
    main()
