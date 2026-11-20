"""Tests for beats.py concrete number detection."""

import sys
sys.path.insert(0, '/var/lib/alan-portfolio/workspaces/ryan/vector-pilot-145')

from skills.ig_reel.beats import count_concrete, analyze_beat


def test_spoken_numbers_counted():
    """Test that spoken numbers like 'five hours' are counted as concrete."""
    # Bug #1 fix: "five hours" should be counted
    result = count_concrete("Proposals took me five hours.\nI cut them to twenty minutes.\nThree pages, one template.")
    assert result >= 2, f"Expected at least 2 concrete numbers, got {result}"
    # "five" and "twenty" should be found; "Three" at start may or may not depend on lookbehind


def test_capitalized_not_counted_as_proper_if_start_of_sentence():
    """Test that capitalized word starting a sentence is NOT counted as proper name."""
    # Bug #2 fix: "Proposals took forever. Now they do not." -> "Now" should NOT be counted
    result = count_concrete("Proposals took forever. Now they do not.")
    # "Proposals" at start should not count as proper; "Now" at start of second sentence should not either
    # The lookbehind (?<![.!?]\s) should prevent this
    assert result == 0, f"Expected 0 concrete (no numbers, 'Now' should not count as proper), got {result}"


def test_mixed_sentences():
    """Test mixed sentence capitalization."""
    # "This is a line. Never mind the rest." - "Never" at start of sentence should not count
    result = count_concrete("This is a line. Never mind the rest.")
    # Should be 0 since "Never" starts a new sentence after "."
    assert result == 0, f"Expected 0, got {result}"


def test_beats_with_concrete():
    """Test beat analysis with concrete numbers."""
    beat = "I cut them to twenty minutes."
    result = analyze_beat(beat)
    assert result["concrete"] >= 1, f"Expected at least 1 concrete number in '{beat}', got {result['concrete']}"
    assert result["is_concrete"] is True


def test_beats_without_concrete():
    """Test beat analysis without concrete numbers."""
    beat = "Honestly nothing much happened."
    result = analyze_beat(beat)
    assert result["concrete"] == 0, f"Expected 0 concrete, got {result['concrete']}"
    assert result["is_concrete"] is False


def test_json_output():
    """Test --json output format."""
    import json
    from skills.ig_reel.beats import main
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        # Create a temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            tmp.write("Proposals took me five hours.\nI cut them to twenty minutes.")
            tmp_path = tmp.name
        try:
            main(["--json", tmp_path])
            output = json.loads(f.getvalue())
            assert output["total_beats"] == 2
            assert output["total_concrete"] >= 1
        finally:
            pass  # temp file cleanup
