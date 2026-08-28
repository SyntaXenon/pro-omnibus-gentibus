# -*- coding: utf-8 -*-
"""Walks every in-scope day across the given years and flags places where
Latin and Spanish content for the SAME unit look structurally or lengthwise
mismatched, even though both are present (i.e. NOT the gap-detection that
content_completeness_check.py already does). Three checks:
  1. list-vs-list length mismatch (responsory/preces/hymn row-count bugs -
     same class already found and fixed several times this session).
  2. psalm-kind verse-label-set mismatch (citation resolves to a different
     set of verses in la vs es - e.g. Nova-Vulgata-vs-Clementina numbering
     drift, or a missing verse in one corpus).
  3. plain-text length-ratio outliers (a crude heuristic: la/es character
     count ratio far from the corpus-wide typical range suggests one side
     is truncated, wrong, or an unrelated text - not proof, just a flag).
Dedupes by (hour, label, content-signature) since most content repeats
across many days via shared ferial/seasonal tables - reports a count of
affected dates and one example per unique mismatch, not 1461 raw rows."""
import sys, json, hashlib
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(r"C:\Omnium Gentium LOTH\_recovered_scripts")))
sys.path.insert(0, str(Path(r"C:\Omnium Gentium LOTH\app")))
sys.path.insert(0, str(Path(r"C:\Omnium Gentium LOTH\app\renderer")))

from render_day import resolve_and_build_day, LANGUAGES
from schema import BibleCorpus, ProperTextLibrary

corpora = {lang: BibleCorpus(lang) for lang in LANGUAGES}
proper = {lang: ProperTextLibrary(lang) for lang in LANGUAGES}

YEARS = [2026, 2027, 2028, 2029]

structural = {}   # key -> {hour,label,la_len,es_len,la_sample,es_sample,dates:[]}
psalm_verse = {}  # key -> {hour,label,la_labels,es_labels,dates:[]}
ratios = []       # list of dicts: hour,label,date,la_len,es_len,ratio,la_sample,es_sample

def sig(obj):
    return hashlib.sha1(repr(obj).encode("utf-8", "ignore")).hexdigest()[:16]

for year in YEARS:
    d = date(year, 1, 1)
    end = date(year, 12, 31)
    while d <= end:
        hours_data, desc_tag = resolve_and_build_day(d, corpora, proper)
        if hours_data:
            for hour, units in hours_data.items():
                for unit in units:
                    content = unit.get("content")
                    if not isinstance(content, dict):
                        continue
                    la = content.get("la")
                    es = content.get("es")
                    if not la or not es:
                        continue
                    label = unit.get("label")
                    kind = unit.get("kind")

                    if isinstance(la, list) and isinstance(es, list):
                        if kind == "psalm":
                            # each element is [label, text] after JSON round-trip / tuple in-memory
                            def get_label(x):
                                try:
                                    return x[0]
                                except Exception:
                                    return None
                            la_labels = tuple(sorted(str(get_label(x)) for x in la))
                            es_labels = tuple(sorted(str(get_label(x)) for x in es))
                            if la_labels != es_labels:
                                key = (hour, label, sig((la_labels, es_labels)))
                                if key not in psalm_verse:
                                    psalm_verse[key] = {
                                        "hour": hour, "label": label,
                                        "la_labels": la_labels, "es_labels": es_labels,
                                        "ref": unit.get("ref"),
                                        "dates": [],
                                    }
                                psalm_verse[key]["dates"].append(d.isoformat())
                        else:
                            if len(la) != len(es):
                                key = (hour, label, sig((la, es)))
                                if key not in structural:
                                    structural[key] = {
                                        "hour": hour, "label": label, "kind": kind,
                                        "la_len": len(la), "es_len": len(es),
                                        "la_sample": la[:2], "es_sample": es[:2],
                                        "dates": [],
                                    }
                                structural[key]["dates"].append(d.isoformat())
                    elif isinstance(la, str) and isinstance(es, str):
                        la_n, es_n = len(la), len(es)
                        if la_n > 0 and es_n > 0:
                            ratio = la_n / es_n
                            ratios.append({
                                "hour": hour, "label": label, "date": d.isoformat(),
                                "la_len": la_n, "es_len": es_n, "ratio": round(ratio, 3),
                                "la_sample": la[:80], "es_sample": es[:80],
                            })
        d += (date(year, d.month % 12 + 1, 1) - d) if False else __import__("datetime").timedelta(days=1)

out = {
    "structural_mismatches": sorted(structural.values(), key=lambda x: -len(x["dates"])),
    "psalm_verse_mismatches": sorted(psalm_verse.values(), key=lambda x: -len(x["dates"])),
}
with open("_recovered_scripts/la_es_scan_structural.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

with open("_recovered_scripts/la_es_scan_ratios_raw.json", "w", encoding="utf-8") as f:
    json.dump(ratios, f, ensure_ascii=False, indent=2)

print("structural:", len(structural), "psalm_verse:", len(psalm_verse), "ratio_samples:", len(ratios))
