"""Content data model for the LOTH interlinear.

Three kinds of stored content, all keyed so that adding a new language is
"add more rows," never a schema change:

1. Bible corpus - the full text of scripture (psalms, canticles, readings),
   keyed by (language, book, chapter_or_psalm_number, verse). Numbering is
   always canonical Vulgate numbering internally; a source using a different
   convention (e.g. Hebrew/Masoretic numbering for the Psalms) must be
   converted at ingestion time, once, never at query time.

2. Proper texts - antiphons, collects, and other texts proper to a specific
   liturgical unit (not scripture quotations), keyed by (unit_tag, language,
   text_type).

3. Hymn pools - a hymn is its own unit type because it's chosen from a pool
   (not fixed to a single day) and aligned line-by-line rather than as one
   block. Keyed by (hymn_id, language) -> ordered list of lines, plus a
   separate "applicability" tag list (which hour/season/context it may be
   sung in).

A "unit" for display purposes (the thing that gets one side-by-side block in
the interlinear view) is either: a Citation into the Bible corpus (psalmody,
canticle, short reading), a proper-text tag (antiphon, collect, responsory),
or a chosen hymn_id (rendered line-by-line instead of as one block).
"""
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

CONTENT_ROOT = Path(__file__).resolve().parent.parent.parent / "content"

# --- Citations into the Bible corpus -----------------------------------

# A citation is book + one or more semicolon-joined segments (canticles like
# "Rev 4:11;5:9,10,12" span multiple chapters of the same book). Each segment
# is either "<chapter>", "<chapter>:<verse-spec>", or a cross-chapter range
# "<chapter>:<verse>-<chapter>:<verse>" (e.g. "61:10-62:5"), which is split
# into two segments internally (rest of the first chapter + start of the next).
_BOOK_RE = re.compile(r"^(?P<book>[0-9A-Za-z]+?)\s+(?P<rest>.+)$")
_CROSS_CHAPTER_SEGMENT_RE = re.compile(
    r"^(?P<ch1>\d+):(?P<v1>\d+)[a-z]?-(?P<ch2>\d+):(?P<v2>\d+)[a-z]?$"
)
_SEGMENT_RE = re.compile(r"^(?P<chapter>\d+)(:(?P<verses>[\d,\-a-z]+))?$")


@dataclass
class Citation:
    book: str      # e.g. "Ps" (canonical Vulgate psalm numbering), "1Chr", "Rom"
    segments: list  # list of (chapter:int, verse_ranges) - verse_ranges is a list of
                     # (start, end) inclusive int tuples (end=None means "to the end of
                     # the chapter"), or None to mean "whole chapter"

    @staticmethod
    def parse(text: str) -> "Citation":
        """Parse citations like 'Ps 109:1-5', 'Ps 108:1-4,6' (verse 5 excluded),
        'Ps 29' (whole chapter), 'Isa 61:10-62:5' (crosses a chapter boundary),
        or 'Rev 4:11;5:9,10,12' (multiple chapters of the same book)."""
        bm = _BOOK_RE.match(text.strip())
        if not bm:
            raise ValueError(f"Unrecognized citation format: {text!r}")
        book = bm.group("book")
        segments = []
        for raw_seg in bm.group("rest").split(";"):
            seg = raw_seg.strip()
            cross = _CROSS_CHAPTER_SEGMENT_RE.match(seg)
            if cross:
                ch1, v1, ch2, v2 = (int(cross.group(g)) for g in ("ch1", "v1", "ch2", "v2"))
                segments.append((ch1, [(v1, None)]))
                segments.append((ch2, [(1, v2)]))
                continue
            sm = _SEGMENT_RE.match(seg)
            if not sm:
                raise ValueError(f"Unrecognized citation segment: {seg!r} in {text!r}")
            chapter = int(sm.group("chapter"))
            if not sm.group("verses"):
                segments.append((chapter, None))
                continue
            ranges = []
            for part in sm.group("verses").split(","):
                if "-" in part:
                    start, end = part.split("-")
                    ranges.append((int(re.sub(r"\D", "", start)), int(re.sub(r"\D", "", end))))
                else:
                    ranges.append((int(re.sub(r"\D", "", part)), int(re.sub(r"\D", "", part))))
            segments.append((chapter, ranges))
        return Citation(book=book, segments=segments)

    @property
    def is_multi_chapter(self) -> bool:
        return len({chapter for chapter, _ in self.segments}) > 1


# Psalms whose Vulgate text numbers the Hebrew superscription itself
# ("In finem, in carminibus. Psalmus David.", "Intellectus David...", etc.)
# as verse 1 - real scholarly apparatus, never actually recited in the
# Liturgy of the Hours. This project's Spanish corpus (Torres Amat) doesn't
# translate or number these headings at all, so a "whole psalm" citation
# resolved verse-for-verse against both corpora previously showed the Latin
# side with one extra opening line the Spanish side had no counterpart for -
# not just an academic numbering quirk but a real row-misalignment bug in
# the parallel display (found via a project-wide La/Es consistency scan,
# confirmed against every one of these 58 psalms' own verse-1 text).
PSALM_SUPERSCRIPTION_CHAPTERS = frozenset({
    "3", "4", "5", "6", "7", "8", "9", "10", "11", "18", "20", "21", "29",
    "30", "33", "35", "37", "38", "39", "40", "41", "44", "45", "46", "47",
    "48", "50", "51", "52", "53", "54", "56", "57", "60", "61", "62", "63",
    "66", "67", "68", "69", "74", "75", "76", "79", "80", "82", "83", "84",
    "87", "88", "91", "101", "107", "125", "135", "139", "141",
})


class BibleCorpus:
    """Loads content/bible/<language>/<book>.json, shaped as
    {"<chapter>": {"<verse>": "text", ...}, ...}."""

    def __init__(self, language: str):
        self.language = language
        self._books = {}

    def _load_book(self, book: str) -> dict:
        if book not in self._books:
            path = CONTENT_ROOT / "bible" / self.language / f"{book.lower()}.json"
            if not path.exists():
                raise FileNotFoundError(f"No corpus file for {self.language}/{book}: {path}")
            with open(path, encoding="utf-8") as f:
                self._books[book] = json.load(f)
        return self._books[book]

    def text_for(self, citation: Citation) -> list:
        """Returns a list of (label, text) for every verse in the citation that
        exists in the corpus, in citation order. Missing verses are silently
        skipped (so a verse-exclusion citation like 'Ps 108:1-4,6' works without
        special-casing). label is the plain verse number ("5") for ordinary
        single-chapter citations - unchanged from before - or "chapter:verse"
        ("62:5") when the citation spans more than one chapter, so verse numbers
        that repeat across chapters don't collide."""
        book_data = self._load_book(citation.book)
        multi = citation.is_multi_chapter
        skip_superscription = (
            self.language == "la" and citation.book.lower() == "ps"
        )
        result = []
        for chapter, verse_ranges in citation.segments:
            chapter_data = book_data.get(str(chapter), {})
            if verse_ranges is None:
                verse_numbers = sorted((int(v) for v in chapter_data if v.isdigit()))
            else:
                verse_numbers = []
                for start, end in verse_ranges:
                    if end is None:
                        end = max((int(v) for v in chapter_data if v.isdigit()), default=start)
                    verse_numbers.extend(range(start, end + 1))
            if skip_superscription and str(chapter) in PSALM_SUPERSCRIPTION_CHAPTERS:
                verse_numbers = [v for v in verse_numbers if v != 1]
            for v in verse_numbers:
                if str(v) in chapter_data:
                    label = f"{chapter}:{v}" if multi else str(v)
                    result.append((label, chapter_data[str(v)]))
        return result


# --- Proper texts (antiphons, collects, responsories) -------------------

class ProperTextLibrary:
    """Loads content/proper_texts/<language>.json, shaped as
    {"<unit_tag>": {"<text_type>": "text", ...}, ...}."""

    def __init__(self, language: str):
        self.language = language
        self._data = None

    def _load(self) -> dict:
        if self._data is None:
            path = CONTENT_ROOT / "proper_texts" / f"{self.language}.json"
            if not path.exists():
                raise FileNotFoundError(f"No proper-texts file for {self.language}: {path}")
            with open(path, encoding="utf-8") as f:
                self._data = json.load(f)
        return self._data

    def get(self, unit_tag: str, text_type: str) -> Optional[str]:
        return self._load().get(unit_tag, {}).get(text_type)


# --- Hymn pools -----------------------------------------------------------

class HymnPool:
    """Loads content/proper_texts/hymns.json, shaped as
    {"<hymn_id>": {"applicability": ["compline", ...],
                   "lines": {"<language>": ["line 1", "line 2", ...]}}}."""

    def __init__(self):
        self._data = None

    def _load(self) -> dict:
        if self._data is None:
            path = CONTENT_ROOT / "proper_texts" / "hymns.json"
            with open(path, encoding="utf-8") as f:
                self._data = json.load(f)
        return self._data

    def options_for(self, context: str) -> list:
        return [hid for hid, h in self._load().items() if context in h.get("applicability", [])]

    def lines(self, hymn_id: str, language: str) -> list:
        return self._load().get(hymn_id, {}).get("lines", {}).get(language, [])
