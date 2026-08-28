# -*- coding: utf-8 -*-
"""Converts a breviarium-core Spanish-book-abbreviation citation (e.g.
'2 Ts 2, 13-14', 'Salmo 62, 2-9: El alma sedienta de Dios') into this
project's own Citation.parse()-compatible format ('2thess 2:13-14'), so
readings sourced from breviarium-core can be resolved bilingually against
this project's own Latin+Spanish Bible corpus instead of only showing
breviarium's raw Spanish prose. Shared by build_sanctorale_psalmody.py and
render_day.py - originally only lived in the former.
"""
import re

BOOK_MAP = {
    "Gn": "gen", "Ex": "exod", "Lv": "lev", "Nm": "num", "Dt": "deut",
    "Jos": "jos", "Jc": "judg", "Jue": "judg", "Rt": "ruth",
    "1 S": "1sam", "2 S": "2sam", "1 R": "1kgs", "2 R": "2kgs",
    "1 Cro": "1chr", "2 Cro": "2chr", "1 Cr": "1chr", "2 Cr": "2chr",
    "Esd": "ezra", "Ne": "neh", "Tb": "tob", "Jdt": "jdt", "Est": "esth",
    "Jb": "job", "Sal": "ps", "Pr": "prov", "Qo": "eccl", "Ct": "song",
    "Sb": "wis", "Si": "sir", "Eclo": "sir", "Is": "isa", "Jr": "jer",
    "Lm": "lam", "Ba": "bar", "Ez": "ezek", "Dn": "dan", "Daniel": "dan",
    "Os": "hos", "Jl": "joel", "Am": "amos", "Ab": "obad", "Jon": "jon",
    "Mi": "mic", "Na": "nah", "Ha": "hab", "So": "zeph", "Ag": "hag",
    "Za": "zech", "Ml": "mal", "1 M": "1macc", "2 M": "2macc",
    "Mt": "matt", "Mc": "mark", "Lc": "luke", "Jn": "john",
    "Hch": "acts", "Rm": "rom", "1 Co": "1cor", "2 Co": "2cor",
    "Ga": "gal", "Ef": "eph", "Efesios": "eph", "Flp": "phil", "Col": "col",
    "Filipenses": "phil", "Colosenses": "col",
    "1 Ts": "1thess", "2 Ts": "2thess", "1 Tm": "1tim", "2 Tm": "2tim",
    "Tt": "titus", "Flm": "phlm", "Hb": "heb", "St": "jas",
    "1 P": "1pet", "2 P": "2pet", "1 Jn": "1john", "2 Jn": "2john",
    "3 Jn": "3john", "Jud": "jude", "Ap": "rev", "Apocalipsis": "rev",
    # breviarium-core's OT canticle citations (used for Lauds during
    # Advent/Lent/Easter, sourced independently of the abbreviated-book-code
    # readings above) spell books out in full Spanish rather than
    # abbreviating - same target books, just a different citation dialect.
    "Genesis": "gen", "Exodo": "exod", "Éxodo": "exod",
    "Levitico": "lev", "Levítico": "lev", "Numeros": "num",
    "Números": "num", "Deuteronomio": "deut", "Josue": "jos",
    "Josué": "jos", "Jueces": "judg", "Rut": "ruth",
    "1 Samuel": "1sam", "2 Samuel": "2sam", "1 Reyes": "1kgs", "2 Reyes": "2kgs",
    "1 Cronicas": "1chr", "1 Crónicas": "1chr",
    "2 Cronicas": "2chr", "2 Crónicas": "2chr", "Esdras": "ezra",
    "Nehemias": "neh", "Nehemías": "neh", "Tobias": "tob",
    "Tobías": "tob", "Judit": "jdt", "Ester": "esth",
    "Job": "job", "Proverbios": "prov", "Eclesiastes": "eccl",
    "Eclesiastés": "eccl",
    "Sabiduria": "wis", "Sabiduría": "wis",
    "Eclesiastico": "sir", "Eclesiástico": "sir", "Siracide": "sir",
    "Sirácide": "sir",
    "Isaias": "isa", "Isaías": "isa",
    "Jeremias": "jer", "Jeremías": "jer", "Lamentaciones": "lam",
    "Baruc": "bar", "Ezequiel": "ezek", "Oseas": "hos", "Joel": "joel",
    "Amos": "amos", "Amós": "amos", "Abdias": "obad",
    "Abdías": "obad", "Jonas": "jon", "Jonás": "jon",
    "Miqueas": "mic", "Nahum": "nah", "Nahúm": "nah",
    "Habacuc": "hab", "Sofonias": "zeph", "Sofonías": "zeph",
    "Ageo": "hag", "Zacarias": "zech",
    "Zacarías": "zech", "Malaquias": "mal", "Malaquías": "mal",
    "1 Macabeos": "1macc", "2 Macabeos": "2macc", "Mateo": "matt",
    "Marcos": "mark", "Lucas": "luke",
    "Juan": "john", "Hechos": "acts", "Romanos": "rom",
    "1 Corintios": "1cor", "2 Corintios": "2cor", "Galatas": "gal",
    "Gálatas": "gal",
    "Filemon": "phlm", "Filemón": "phlm", "Hebreos": "heb",
    "Santiago": "jas",
    "1 Pedro": "1pet", "2 Pedro": "2pet", "1 Juan": "1john",
    "2 Juan": "2john", "3 Juan": "3john", "Judas": "jude",
    "1 Tesalonicenses": "1thess", "2 Tesalonicenses": "2thess",
    "1 Timoteo": "1tim", "2 Timoteo": "2tim", "Tito": "titus",
}
BOOK_KEYS = sorted(BOOK_MAP, key=len, reverse=True)

VULGATE_CHAPTER_REMAP = {
    ("Ml", "3", "23-24"): "mal 4:5-6",
}

ALTERNATE_OVERRIDES = {
    "Apocalipsis 19 / Apocalipsis 15": "Apocalipsis 19, 1-2. 5-7",
    # breviarium-core cites the "a child is born to us" prophecy as Is 9,5
    # (Nova Vulgata/Hebrew-aligned numbering); this project's own Latin/
    # Spanish Isaiah corpus follows the older Vulgate numbering, where the
    # same text is verse 6 (v5 there is instead "every warrior's boot...",
    # a different verse entirely - confirmed by fetching both and comparing
    # content, not just assuming a constant offset). Used by 3 real
    # breviarium-core entries: christmas_octave_day_6, monday_after_epiphany,
    # tuesday_after_epiphany.
    "Is 9, 5": "Is 9, 6",
}

KNOWN_SPLITS = {
    ("26", "I"): "1-6", ("26", "II"): "7-14",
    ("44", "I"): "2-10", ("44", "II"): "11-18",
    ("48", "I"): "2-13", ("48", "II"): "14-21",
    ("71", "I"): "2-11", ("71", "II"): "12-19",
    ("131", "I"): "1-10", ("131", "II"): "11-18",
    ("134", "I"): "1-12", ("134", "II"): "13-21",
    ("18", "A"): "2-7",
    # verse ranges confirmed against this project's own
    # sunday_psalter_distribution.json / ferial_psalter_distribution.json,
    # where these same split psalms are already sourced under plain "Ps N"
    # citations (Vulgate numbering).
    ("113", "A"): "1-8", ("113", "B"): "9-26",
    ("135", "I"): "1-9", ("135", "II"): "10-26",
    ("143", "I"): "1-8", ("143", "II"): "9-15",
    ("144", "A"): "1-13a", ("144", "B"): "13b-21",
}


def strip_descriptive_title(raw: str) -> str:
    return raw.split(":", 1)[0].strip()


def convert_citation(raw: str):
    """Returns a citation string in this project's format, or None if the
    citation can't be safely/confidently converted - None means 'skip this
    one', never a guess."""
    if not raw:
        return None
    if raw.strip() in ALTERNATE_OVERRIDES:
        raw = ALTERNATE_OVERRIDES[raw.strip()]
    raw = strip_descriptive_title(raw)
    raw = re.sub(r"\s*\([^)]*\)", "", raw).strip()
    if "/" in raw:
        return None

    if raw.startswith("Salmo "):
        rest = raw[len("Salmo "):].strip()
        m = re.match(r"^(\d+)[\s-]([IVA-Z]+)$", rest)
        if m and not re.search(r"\d", m.group(2)):
            num, suf = m.group(1), m.group(2)
            verses = KNOWN_SPLITS.get((num, suf))
            if verses is None:
                return None
            return f"Ps {num}:{verses}"
        chapter, _, verses = rest.partition(",")
        chapter = chapter.strip()
        if not chapter.isdigit():
            return None
        if not verses.strip():
            return f"Ps {chapter}"
        verses = verses.replace(".", ",")
        verses = re.sub(r"\s+", "", verses)
        verses = re.sub(r"[a-zA-Z]", "", verses)
        verses = verses.strip(",")
        if not verses:
            return f"Ps {chapter}"
        return f"Ps {chapter}:{verses}"

    book_es = None
    rest = None
    for key in BOOK_KEYS:
        if raw.startswith(key + " "):
            book_es = key
            rest = raw[len(key):].strip()
            break
    if book_es is None:
        return None
    remap_chapter, _, remap_verses = rest.partition(",")
    remap_key = (book_es, remap_chapter.strip(), remap_verses.strip())
    if remap_key in VULGATE_CHAPTER_REMAP:
        return VULGATE_CHAPTER_REMAP[remap_key]
    book = BOOK_MAP[book_es]
    # Cross-chapter range spelled "61, 10-62, 5" (ch1, v1-ch2, v2) rather
    # than this project's own "61:10-62:5" - convert directly, since the
    # general comma/semicolon splitting below assumes everything stays
    # within one chapter.
    cross = re.match(r"^(\d+)\s*,\s*(\d+)\s*-\s*(\d+)\s*,\s*(\d+)$", rest)
    if cross:
        ch1, v1, ch2, v2 = cross.groups()
        return f"{book} {ch1}:{v1}-{ch2}:{v2}"
    # Semicolons here are ambiguous in breviarium-core's own data: usually a
    # genuine new-chapter separator (Citation's own convention, e.g. "Rev
    # 4:11;5:9,10,12"), but occasionally just another verse-range-within-the-
    # same-chapter separator used interchangeably with the period elsewhere
    # (e.g. "Isaias 38, 10-14;17-20" means Isaiah 38:10-14 AND 38:17-20, not
    # a bare "chapter 17-20"). Distinguish by checking whether the part
    # before the first comma is a real chapter number; if not, it's a
    # continuation of the previous segment's verses, not a new chapter.
    parts = [p.strip() for p in rest.split(";")]
    out_segments = []
    for part in parts:
        chapter, _, verses = part.partition(",")
        chapter = chapter.strip()
        verses = verses.strip()
        if not chapter.isdigit() and out_segments:
            extra = verses if verses else chapter
            extra = extra.replace(".", ",")
            extra = re.sub(r"\s+", "", extra)
            extra = re.sub(r"[a-zA-Z]", "", extra)
            extra = extra.strip(",")
            if extra:
                out_segments[-1] = out_segments[-1] + "," + extra
            continue
        if not verses:
            out_segments.append(chapter)
            continue
        verses = verses.replace(".", ",")
        verses = re.sub(r"\s+", "", verses)
        verses = re.sub(r"[a-zA-Z]", "", verses)
        verses = verses.strip(",")
        out_segments.append(f"{chapter}:{verses}" if verses else chapter)
    return f"{book} " + ";".join(out_segments)
