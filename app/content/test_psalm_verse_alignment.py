"""Regression check: content/bible/la/ps.json and content/bible/es/ps.json
must have matching verse-number keys per chapter, except where the Latin
superscription is counted as its own verse 1 and the Spanish source has no
separate line for it (that specific, one-verse gap is the only allowed
divergence - see the _source note in ps.json for how this was audited)."""
import json
from pathlib import Path

CONTENT_ROOT = Path(__file__).resolve().parent.parent.parent / "content"

with open(CONTENT_ROOT / "bible" / "la" / "ps.json", encoding="utf-8") as f:
    la = json.load(f)
with open(CONTENT_ROOT / "bible" / "es" / "ps.json", encoding="utf-8") as f:
    es = json.load(f)

failures = []
for chapter in la:
    if chapter == "_source" or chapter not in es:
        continue
    la_keys = set(la[chapter].keys())
    es_keys = set(es[chapter].keys())
    if la_keys == es_keys:
        continue
    if la_keys - es_keys == {"1"} and not (es_keys - la_keys):
        continue  # allowed: Latin-only title verse
    failures.append((chapter, sorted(la_keys - es_keys, key=int), sorted(es_keys - la_keys, key=int)))

if failures:
    print(f"FAIL: {len(failures)} chapters with unexplained verse-key mismatches:")
    for chapter, la_only, es_only in failures:
        print(f"  Ps {chapter}: LA-only {la_only}, ES-only {es_only}")
else:
    print(f"OK: all {len([k for k in la if k != '_source'])} psalm chapters have matching verse numbering")
