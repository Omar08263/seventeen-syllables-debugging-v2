"""Seventeen Syllables of Debugging — make.fun entry (v2 attack wave).

Writes one haiku about debugging (three lines, 5-7-5 syllables,
at most 200 characters) to /output/entry.txt.

Deterministic: the same bytes on every run.
Standard library only, no network, no randomness.
"""

import os
import re
import sys

HAIKU = (
    "At three the stack trace\n"
    "spells my name in every frame\n"
    "I signed every frame\n"
)

# Expected syllable counts per line (5-7-5), verified by hand and by
# program: At(1) three(1) the(1) stack(1) trace(1);
# spells(1) my(1) name(1) in(1) every(2) frame(1);
# I(1) signed(1) every(2) frame(1). Total: 76 characters incl. newline.
EXPECTED_SYLLABLES = (5, 7, 5)

# Words the plain vowel-group rule miscounts: "every" is two syllables
# (ev-ery) but has three vowel groups, and the same holds for its
# family (everyone, everything, everybody).
_SPECIAL = {"every": 2, "everyone": 3, "everything": 3, "everybody": 4}


def _syllables(word: str) -> int:
    """Small vowel-group syllable count for the plain words of this haiku."""
    w = word.strip(".,!?'\"").lower().replace("'", "")
    if not w:
        return 0
    if w in _SPECIAL:
        return _SPECIAL[w]
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and n > 1:
        n -= 1
    if w.endswith("ed") and n > 1 and not w.endswith(("ted", "ded")):
        n -= 1
    return max(1, n)


def _counts(text: str) -> tuple:
    """Per-line syllable counts, for self-test output."""
    lines = text.rstrip("\n").split("\n")
    return tuple(
        sum(_syllables(w) for w in line.split()) for line in lines
    )


def _validate(text: str) -> None:
    """Fail loudly unless the haiku meets the competition's gate."""
    assert 1 <= len(text) <= 200, "haiku must be 1-200 characters"
    lines = text.rstrip("\n").split("\n")
    assert len(lines) == 3, "haiku must be exactly three lines"
    counts = _counts(text)
    assert counts == EXPECTED_SYLLABLES, (
        f"syllable shape must be 5-7-5, got {counts}"
    )
    assert text.strip(), "haiku must not be only white space"


def main() -> None:
    if "--self-test" in sys.argv[1:]:
        print("lines:", len(HAIKU.rstrip("\n").split("\n")))
        print("syllables:", _counts(HAIKU))
        print("chars:", len(HAIKU))
        _validate(HAIKU)
        print("self-test: OK")
        return
    _validate(HAIKU)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(HAIKU)
    # Read-back check: fail loudly on any difference.
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        assert f.read() == HAIKU, "read-back mismatch"


if __name__ == "__main__":
    main()
