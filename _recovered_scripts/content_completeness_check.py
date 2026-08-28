# -*- coding: utf-8 -*-
"""Walks every in-scope day of a year through resolve_and_build_day and
tallies any unit whose content is None/empty in either language, broken
down by unit label. A regression check that nothing in today's bible
re-scrape / boundary work broke a psalm_lines() lookup or similar."""
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(r"C:\Omnium Gentium LOTH\_recovered_scripts")))
sys.path.insert(0, str(Path(r"C:\Omnium Gentium LOTH\app")))
sys.path.insert(0, str(Path(r"C:\Omnium Gentium LOTH\app\renderer")))

from render_day import resolve_and_build_day, LANGUAGES  # noqa: E402
from schema import BibleCorpus, ProperTextLibrary  # noqa: E402

corpora = {lang: BibleCorpus(lang) for lang in LANGUAGES}
proper = {lang: ProperTextLibrary(lang) for lang in LANGUAGES}

YEAR = int(sys.argv[1]) if len(sys.argv) > 1 else 2026

gaps = Counter()
examples = {}

d = date(YEAR, 1, 1)
end = date(YEAR, 12, 31)
while d <= end:
    hours_data, desc_tag = resolve_and_build_day(d, corpora, proper)
    if hours_data:
        for hour, units in hours_data.items():
            for unit in units:
                content = unit.get("content")
                if not isinstance(content, dict):
                    continue
                for lang, text in content.items():
                    if text is None or (isinstance(text, str) and not text.strip()):
                        key = (hour, unit.get("label"), lang)
                        gaps[key] += 1
                        examples.setdefault(key, d.isoformat())
    d += timedelta(days=1)

print(f"Year {YEAR}: {len(gaps)} distinct (hour, label, lang) gap patterns")
for key, count in sorted(gaps.items(), key=lambda x: -x[1]):
    print(f"  {key}: {count} days (e.g. {examples[key]})")
