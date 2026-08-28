"""Renderer: date -> interactive HTML page for Lauds/Vespers/Compline.

Each side of the interlinear view has its own language dropdown (any
language on either side; picking the same language on both collapses to a
single block) and there's a shared Hour dropdown (Lauds/Vespers/Compline
implemented now, other Hours shown as disabled placeholders). All data for
every implemented hour/language is embedded as JSON and rendered client-side
with vanilla JS, so switching dropdowns doesn't require regenerating the page.

The left dropdown is the "main" language and drives EVERYTHING in the UI
chrome - control labels, Hour names, the Date picker, the page heading - not
just the liturgical content's structural labels (Hymn/Antiphon/etc.). The
right dropdown is a translation of that content: its own label reads
"Vernacular" when the main language is Latin, or "Translation" otherwise.
Liturgical content itself keeps the same sourcing-status distinctions as
before (real vs. "[not yet sourced]").
"""
import json
import re
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_ROOT / "calendar"))
sys.path.insert(0, str(APP_ROOT / "content"))

from resolver import (resolve_ferial_ordinary_time, resolve_ordinary_time_sunday,  # noqa: E402
                       resolve_advent, resolve_lent, resolve_easter, resolve_christmas,
                       most_holy_trinity, baptism_of_the_lord, mary_mother_of_the_church,
                       corpus_christi, sacred_heart_of_jesus, immaculate_heart_of_mary,
                       resolve_triduum, palm_sunday, holy_thursday, transferred_solemnity_date,
                       first_sunday_of_advent, christ_the_king, seventh_sunday_of_easter)
from schema import Citation, BibleCorpus, ProperTextLibrary  # noqa: E402
from i18n import (UNIT_LABELS, HOUR_LABELS, IMPLEMENTED_HOURS, ALL_HOURS_ORDER,  # noqa: E402
                   day_description, advent_day_description, lent_day_description,
                   easter_day_description, christmas_day_description, triduum_day_description,
                   date_human, CHROME_LABELS, TZ_REGION_NAMES)

sys.path.insert(0, str(APP_ROOT.parent / "_recovered_scripts"))
from breviarium_core_resolver import get_resolved  # noqa: E402
from citation_convert import convert_citation  # noqa: E402

CONTENT_ROOT = APP_ROOT.parent / "content"
LANGUAGES = ["la", "es"]  # available now; UI is built to support more later

# Gospel canticles are fixed (not day/week-varying) so they're not in the
# psalter distribution tables - cited directly here instead.
GOSPEL_CANTICLE_CITATIONS = {
    "gospel_canticle_magnificat": "Luke 1:46-55",
    "gospel_canticle_benedictus": "Luke 1:68-79",
}
NUNC_DIMITTIS_CITATION = "Luke 2:29-32"


def load_calendar_day(d: date) -> dict:
    """Returns the cached calendar entry for d (from content/calendar/{year}.json),
    or None if no cache exists for that year or that date isn't in it."""
    path = CONTENT_ROOT / "calendar" / f"{d.year}.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("days", {}).get(d.isoformat())


SANCTORALE_ROOT = CONTENT_ROOT / "sanctorale"
RANK_PRECEDENCE = {"SOLLEMNITAS": 4, "FESTUM": 3, "MEMORIA_OBLIGATORIA": 2, "MEMORIA_AD_LIBITUM": 1}

# GILH SS240 / GIRM: on a Saturday in Ordinary Time with no obligatory
# memorial, an optional Memorial of the Blessed Virgin Mary may be
# observed. This USED TO BE 23 separate sanctorale files, each hardcoded to
# one specific 2026 Saturday's date - correct for that one year only, wrong
# for 2027/2028/2029 (different Saturdays), and prone to an arbitrary
# tie-break against a same-day named Optional Memorial (found via testing:
# St Norbert's own June 6 memorial was being silently displaced by this
# because Python's max() picks whichever file the filesystem happened to
# list first when two records tie on rank). Replaced with a single record
# applied dynamically to ANY qualifying Saturday, and only as a fallback
# when nothing else - not even another Optional Memorial - is already
# proper to that date, which also fixes the tie-break by construction.
MARIAN_SATURDAY_RECORD = {
    "id": "memoria_sanctae_mariae_in_sabbato",
    "titulus": "Memoria Sanctæ Mariæ in Sabbato",
    "gradus": "MEMORIA_AD_LIBITUM",
    "color": "ALBUS",
    "commune_subsidiarium": "COMMON_BVM",
}

_sanctorale_index_cache = None


def load_sanctorale_index() -> dict:
    """Scans content/sanctorale/<Rank>/*.json once and indexes by "dies" (MM-DD).
    A date can have multiple optional memorials competing (e.g. two saints on the
    same day) - callers pick the highest-ranking one via resolve_sanctorale_for_date."""
    global _sanctorale_index_cache
    if _sanctorale_index_cache is not None:
        return _sanctorale_index_cache
    index = {}
    for fp in SANCTORALE_ROOT.glob("*/*.json"):
        with open(fp, encoding="utf-8") as f:
            record = json.load(f)
        index.setdefault(record["dies"], []).append(record)
    _sanctorale_index_cache = index
    return index


MARY_MOTHER_OF_THE_CHURCH_RECORD = {
    "id": "mary_mother_of_the_church",
    "titulus": "Beátæ Maríæ Vírginis, Ecclésiæ Matris",
    "gradus": "MEMORIA_OBLIGATORIA",
    "color": "ALBUS",
    "commune_subsidiarium": "COMMON_BVM",
    "collecta": ("Deus, misericordiárum Pater, cujus Unigénitus, cruci affíxus, beátam Maríam Vírginem, "
                 "Genetrícem suam, Matrem quoque nostram constítuit: concéde, quǽsumus; ut, ejus cooperánte "
                 "caritáte, Ecclésia tua, in dies fecúndior, prolis sanctitáte exsúltet et in grémium suum "
                 "cunctas attráhat famílias populórum."),
    "breviarium_id": "mary_mother_of_the_church",
}

IMMACULATE_HEART_OF_MARY_RECORD = {
    "id": "immaculate_heart_of_mary",
    "titulus": "Immaculáti Cordis Beátæ Maríæ Vírginis",
    "gradus": "MEMORIA_AD_LIBITUM",
    "color": "ALBUS",
    "commune_subsidiarium": "COMMON_BVM",
    "collecta": ("Deus, qui in Corde beátæ Maríæ Vírginis dignum Sancti Spíritus habitáculum præparásti: "
                 "concéde propítius; ut, ejúsdem Vírginis intercessióne, tuæ glóriæ templum inveníri mereámur."),
    "breviarium_id": "immaculate_heart_of_mary",
}


def _all_sollemnitas_records():
    """Every fixed-date Solemnity-grade record across the whole sanctorale
    index - small (11 entries as of this writing), scanned fresh each call
    since resolve_sanctorale_for_date only runs once per rendered day. Used
    both to drop an impeded one from its normal date and to add it back in
    on its transferred date (see transferred_solemnity_date)."""
    index = load_sanctorale_index()
    return [r for candidates in index.values() for r in candidates if r["gradus"] == "SOLLEMNITAS"]


def resolve_sanctorale_for_date(d: date):
    """Returns the highest-precedence content/sanctorale/ record for d's month-day,
    or None if nothing is on the calendar that day. Does not apply Sunday/season
    precedence itself - the caller (resolve_and_build_day) decides whether a
    Sunday or a higher season overrides it.

    Also checks two movable Marian memorials that can't live in the fixed-date
    index at all (Mary, Mother of the Church - Monday after Pentecost; the
    Immaculate Heart of Mary - the Saturday after the Sacred Heart) - both
    were entirely absent before this, found via the same 'compare against
    romcal' audit that caught Holy Family. The two movable SOLEMNITIES in
    this same family (Corpus Christi, the Sacred Heart itself) are handled
    separately in resolve_and_build_day since they need a full Lauds+Vespers
    takeover, not just this memorial-precedence merge.

    Finally applies UNLY SS60's fixed-Solemnity transfer rule: a Solemnity
    impeded that year by a Privileged Sunday or by Holy Week/the Triduum/the
    Easter Octave is dropped from its normal date and re-added on its actual
    (transferred) date instead - see transferred_solemnity_date's docstring
    for the two concrete cases this project's 2026-2029 window actually
    hits (St Joseph 2028, the Annunciation 2027 and 2029). A Feast or
    Memorial impeded the same way is NOT transferred - per GILH it simply
    doesn't happen that year, which the existing precedence pick above
    already achieves without any special-casing."""
    index = load_sanctorale_index()
    candidates = list(index.get(d.strftime("%m-%d"), []))
    if d.year and d == mary_mother_of_the_church(d.year):
        # Inserted FIRST, not appended: the CDW's own Notification on this
        # memorial's institution (11 Feb 2018) explicitly states "the
        # Memorial of the Blessed Virgin Mary is to prevail" whenever it
        # coincides with another Saint's Memorial (obligatory or optional) -
        # a genuine Marian pre-eminence rule, not just an ordinary same-rank
        # coincidence. max()'s key= picks the FIRST candidate achieving the
        # max RANK_PRECEDENCE value on a tie (confirmed: max([('a',2),
        # ('b',2)], key=...) picks 'a'), so this must lead the list, not
        # trail it - found via the same festivals-audit pattern already
        # fixed once before for the Saturday-BVM-memorial/St-Norbert case
        # above (that fix's own comment already names this exact failure
        # mode: "Python's max() picks whichever file happened to list
        # first"). Still correctly loses to a same-day Feast/Solemnity
        # (higher RANK_PRECEDENCE), since the rule is pre-eminence AMONG
        # memorials specifically, not an outright override of everything.
        candidates.insert(0, MARY_MOTHER_OF_THE_CHURCH_RECORD)
    if d.year and d == immaculate_heart_of_mary(d.year):
        candidates.append(IMMACULATE_HEART_OF_MARY_RECORD)

    candidates = [r for r in candidates if not (
        r["gradus"] == "SOLLEMNITAS"
        and transferred_solemnity_date(d.year, int(r["dies"][:2]), int(r["dies"][3:])) is not None)]
    for r in _all_sollemnitas_records():
        if transferred_solemnity_date(d.year, int(r["dies"][:2]), int(r["dies"][3:])) == d:
            candidates.append(r)

    if not candidates:
        return None
    return max(candidates, key=lambda r: RANK_PRECEDENCE.get(r["gradus"], 0))


_baptism_record_cache = None


def load_baptism_of_the_lord_record():
    """The Baptism of the Lord is a MOVABLE date (the Sunday after Epiphany,
    or the following Monday if Epiphany itself is a Sunday - see
    resolver.baptism_of_the_lord), but its record's own 'dies' field was
    filed under a fixed '01-11' (only actually correct for the specific
    year it was first sourced). Looked up here by content instead of
    through the fixed-date index, and applied on the DYNAMICALLY computed
    date each year in resolve_and_build_day - without this, most years'
    real Baptism of the Lord date had no matching record at all (a
    genuinely blank day), found via Christmas-season testing."""
    global _baptism_record_cache
    if _baptism_record_cache is None:
        path = SANCTORALE_ROOT / "Festum" / "in_festo_baptismatis_domini_01_11.json"
        with open(path, encoding="utf-8") as f:
            _baptism_record_cache = json.load(f)
    return _baptism_record_cache


def apply_sanctorale_memorial(hours_data: dict, record: dict, hours=("lauds", "vespers")):
    """Per GILH SS235: on a Memorial, psalms and their antiphons stay ferial. Only
    the Magnificat antiphon (Vespers) and Benedictus antiphon (Lauds) swap in, if
    the sanctorale record has them. The hymn isn't swapped (the dropdown always
    keeps every hour-applicable hymn selectable) but its default *recommendation*
    is re-pointed at the saint's Common category here, same idea as the antiphon
    swap, just softer. The concluding prayer is always proper to the individual
    saint; if
    sourced, its real text is used, otherwise the label is annotated with the
    saint's name as a marker for that gap. `hours` restricts which of the day's
    hours actually belong to this weekday's Office (e.g. on a Saturday, "vespers"
    in hours_data is Sunday's First Vespers, not this weekday's).

    When the record's own collect/antiphon isn't individually sourced, falls
    back to its commune_subsidiarium's generic Common text (content/proper_
    texts/commons.json) rather than leaving a gap - this is liturgically
    correct (GILH SS235: an unsourced-proper Memorial genuinely is supposed to
    borrow from its Common), not a stand-in for missing work."""
    common = load_common(record.get("commune_subsidiarium"))
    ga = record.get("antiphonae_evangelicae", {})
    swaps = {
        "vespers": ("gospel_canticle_magnificat",
                    ga.get("magnificat") or (common or {}).get("magnificat_ant"),
                    ga.get("magnificat_es") or (common or {}).get("magnificat_ant_es")),
        "lauds": ("gospel_canticle_benedictus",
                  ga.get("benedictus") or (common or {}).get("benedictus_ant"),
                  ga.get("benedictus_es") or (common or {}).get("benedictus_ant_es")),
    }
    for hour in hours:
        if hour not in swaps:
            continue
        canticle_label, ant_text, ant_text_es = swaps[hour]
        if not ant_text:
            continue
        units = hours_data.get(hour, [])
        idx = next((i for i, u in enumerate(units) if u["label"] == canticle_label), None)
        if idx is None:
            continue
        new_ant = {lang: (ant_text if lang == "la" else ant_text_es) for lang in LANGUAGES}
        for offset in (-1, 1):
            if 0 <= idx + offset < len(units) and units[idx + offset]["kind"] == "ant":
                units[idx + offset]["content"] = new_ant

    hymn_occasion = hymn_occasion_for_commune(record.get("commune_subsidiarium"))
    if hymn_occasion:
        for hour in hours:
            for unit in hours_data.get(hour, []):
                if unit.get("kind") == "hymn_choice":
                    recommended = recommend_hymn_id(unit["hour"], [hymn_occasion])
                    if recommended:
                        unit["recommended"] = recommended

    # The Common's collect templates carry a literal 'N.' placeholder for the
    # saint's own name (Latin liturgical convention) - past code used the
    # template as-is, rendering the placeholder literally ('beáti N.
    # Mártyris...') instead of the saint's actual name. Our own titulus field
    # is already in the correct Latin genitive case for this exact slot
    # ('Sancti Norberti, episcopi' -> 'Norberti'), so no separate declension
    # step is needed - just strip the 'Sancti '/'Sanctæ '/etc. prefix and the
    # trailing role descriptor. The same stripped name is reused for the
    # Spanish 'N.' slot below - not grammatically localized, but it correctly
    # identifies the saint, which is what matters.
    name = record["titulus"]
    for prefix in ("Sanctorum ", "Sanctarum ", "Sancti ", "Sanctæ ", "Sanctae ", "S. "):
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    name = name.split(",")[0].strip()

    collect = record.get("collecta")
    if not collect and common and common.get("collecta"):
        collect = common["collecta"].replace("N.", name, 1) if name else common["collecta"]
    collect_es = record.get("collecta_es")
    breviarium_id = record.get("breviarium_id")
    for hour in hours:
        breviarium_index = "all_laudes" if hour == "lauds" else "all_vesperae"
        extras = breviarium_extras(breviarium_id, breviarium_index) if breviarium_id else {}
        spanish_collect = collect_es or extras.get("oracion_final")
        if not spanish_collect and common and common.get("collecta_es"):
            # No Spanish source for this saint (no breviarium_id/collecta_es),
            # whether or not the record has its own proper Latin collect -
            # previously this left whatever ferial/seasonal collect was
            # already in the Spanish slot untouched, which silently paired
            # the saint's actual Latin collect (proper or Common-fallback)
            # with an unrelated day's Spanish prayer. Falling back to the
            # Common's own Spanish collect (same commune_subsidiarium
            # category as the antiphons above) is thematically coherent and
            # at least names the right saint, unlike the ferial mismatch.
            spanish_collect = common["collecta_es"].replace("N.", name, 1) if name else common["collecta_es"]
        for unit in hours_data.get(hour, []):
            if unit["label"] == "concluding_prayer":
                unit["ref"] = record["titulus"]
                # Non-destructive: a proper Latin/Spanish collect for this
                # saint always wins, but if one language isn't sourced,
                # whatever the ferial fallback (fill_latin_collect /
                # breviarium's own oracion_final) already put there is left
                # alone rather than being blanked out.
                if collect:
                    unit["content"]["la"] = collect
                if spanish_collect:
                    unit["content"]["es"] = spanish_collect

    # GILH SS235: the short reading, responsory, and intercessions ALSO come
    # from the saint's own Proper text if it exists, otherwise the Common of
    # Saints - only the psalms themselves (and their antiphons) stay ferial.
    # Previously this function stopped at the antiphon+collect swap above,
    # leaving reading/responsory/intercessions on the ferial fallback
    # unconditionally - discovered as a real, calendar-wide mismatch source
    # via a live comparison against universalis.com for Aug 28 (St
    # Augustine): this project's Latin was independently correct (a
    # Doctor-specific responsory/preces, matching Universalis word for word)
    # while the Spanish showed unrelated ferial-day content, because only
    # the Latin overlay tables happened to have saint-specific data wired in
    # this far. No sanctorale record has ever used a "proper" reading/
    # responsory/intercessions of its own (record.get(...) below is there so
    # one could be added later per GILH's actual priority order), so in
    # practice this always means "Common, if the Common has it" today.
    common_reading = (common or {}).get("short_reading") or {}
    reading_la = record.get("short_reading_la") or common_reading.get("text")
    reading_es = record.get("short_reading_es") or (common or {}).get("short_reading_es")
    reading_citation = record.get("short_reading_citation") or common_reading.get("citation")

    # Responsory is hour-specific too (Lauds and Vespers each have their own
    # short responsory in the real breviary, confirmed while sourcing the
    # Common's texts) - scoped by hour just like intercessions, not a single
    # value shared across both hours.
    common_responsory = (common or {}).get("responsory") or {}

    common_intercessions = (common or {}).get("intercessions") or {}

    # Require BOTH languages together before swapping any of these three in:
    # the Common's Latin has often been in this file for a while, but its
    # Spanish translation gets sourced separately and later - swapping Latin
    # alone would pair it with whatever ferial Spanish content was already
    # there, creating exactly the kind of La/Es mismatch this whole fix
    # exists to remove, instead of just leaving a gap (honest and harmless).
    reading_ready = bool(reading_la and reading_es)

    for hour in hours:
        hour_responsory = record.get("responsory_" + hour) or common_responsory.get(hour) or {}
        hour_intercessions = record.get("intercessions_" + hour) or common_intercessions.get(hour) or {}
        for unit in hours_data.get(hour, []):
            if unit["label"] == "reading" and reading_ready:
                # The Common's short reading is a single unnumbered paragraph
                # (matching how it's actually printed), not verse-tuples -
                # switch kind to "plain" to match, same as the ferial
                # fallback already does when a citation can't be resolved to
                # individual verses (see fill_reading_unit-style call sites).
                unit["kind"] = "plain"
                unit["content"] = {l: None for l in LANGUAGES}
                unit["content"]["la"] = reading_la
                unit["content"]["es"] = reading_es
                if reading_citation:
                    unit["ref"] = reading_citation
            elif unit["label"] == "responsory" and hour_responsory.get("la") and hour_responsory.get("es"):
                unit["content"]["la"] = hour_responsory["la"]
                unit["content"]["es"] = hour_responsory["es"]
            elif unit["label"] == "intercessions" and hour_intercessions.get("la") and hour_intercessions.get("es"):
                unit["content"]["la"] = hour_intercessions["la"]
                unit["content"]["es"] = hour_intercessions["es"]


def load_static(key: str) -> dict:
    with open(CONTENT_ROOT / "proper_texts" / "static.json", encoding="utf-8") as f:
        return json.load(f)[key]


def _static_content(entry: dict) -> dict:
    """Builds the {lang: text} dict for a load_static() result, always
    including a real (non-machine-translated) 'en' key when the source entry
    has one - static.json's universal, invariant texts (Deus in Adiutorium,
    the Our Father, Compline's fixed formulas) are the one place genuine
    English has actually been sourced; everywhere else in the app 'en' is a
    client-side-only, live-translated beta feature (see template.js)."""
    content = {l: entry[l] for l in LANGUAGES}
    if "en" in entry:
        content["en"] = entry["en"]
    return content


def load_breviarium_latin_antiphons() -> dict:
    """This project's own in-house Latin sourcing for breviarium-core-driven
    seasons (Advent/Lent/Triduum/Easter/Christmas), which breviarium-core
    itself only ever supplies in Spanish. Keyed by breviarium_id -> hour
    ('lauds'/'vespers') -> slot ('primer'/'segundo'/'tercer'/'gospel') ->
    Latin antiphon text. Entries not yet sourced are simply absent, same as
    every other progressive-sourcing table in this project."""
    path = CONTENT_ROOT / "proper_texts" / "breviarium_latin_antiphons.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    data.pop("_note", None)
    return data


def load_common(commune_subsidiarium: str):
    """commune_subsidiarium is e.g. 'COMMON_VIRGINS' -> commons.json's 'virgins'
    category, used as a fallback for a Memorial whose own record doesn't have
    a proper collect/antiphon sourced yet. Returns None if there's no such
    category or no commune_subsidiarium at all (some entries are fully proper
    despite being a Memorial, and apostles have no generic common collect -
    see fetch_common_collects.py)."""
    if not commune_subsidiarium or not commune_subsidiarium.startswith("COMMON_"):
        return None
    key = commune_subsidiarium[len("COMMON_"):].lower()
    with open(CONTENT_ROOT / "proper_texts" / "commons.json", encoding="utf-8") as f:
        commons = json.load(f)
    return commons.get(key)


def build_hymn_pools() -> dict:
    """Groups content/proper_texts/hymns.json by 'applicability' context, for the
    hymn-choice dropdown (and the Hymnal browsing screen). A hymn's
    'original_language' is the language it's actually sung in; any other
    language present in 'lines' defaults to being purely a translation for
    following along (driven by rightLang like every other unit), NOT a
    second genuine sung version - every hymn currently in this file is a
    Latin composition with a Spanish comprehension translation, matching
    the file's own _note policy. The optional 'also_sung_in' array (rare -
    none of the current entries use it) names additional languages that
    are ALSO a genuine, separately-attested sung setting of the hymn, not
    just a translation - this is what the Hymnal screen's "multi-language"
    vs "single-language" filter actually keys on (see hymnLangCount() in
    template.js), not merely how many languages happen to have text.

    Builds a pool for every hour tag actually present in the data, not a
    fixed list - previously hardcoded to ("vespers", "lauds", "compline"),
    which silently dropped any hymn tagged with another hour (e.g. the
    existing veni_creator_spiritus's "terce"/"special" tags never appeared
    in any pool). Only lauds/vespers/compline currently have a rendering
    call site that creates a hymn_choice unit, so this mainly future-proofs
    the pool-building itself and feeds the Hymnal screen's "by hour" filter,
    which reads every tag regardless of what's implemented yet."""
    with open(CONTENT_ROOT / "proper_texts" / "hymns.json", encoding="utf-8") as f:
        all_hymns = json.load(f)
    all_hymns.pop("_note", None)
    contexts = sorted({ctx for h in all_hymns.values() for ctx in h.get("applicability", [])})
    pools = {}
    for ctx in contexts:
        pools[ctx] = [
            {"id": hid, "title": h["title"], "original_language": h["original_language"],
             "also_sung_in": h.get("also_sung_in", []),
             "lines": {l: h["lines"].get(l, []) for l in LANGUAGES}}
            for hid, h in all_hymns.items()
            if ctx in h.get("applicability", [])
        ]
    return pools


_hymn_library_cache = None


def _load_hymn_library() -> dict:
    """content/proper_texts/hymns.json, cached, '_note' stripped - the raw
    per-id records (with 'occasions'), not the per-hour pools build_hymn_
    pools() produces. Used only to pick a recommended default (see
    recommend_hymn_id below); the actual content shown still comes from
    DATA.hymn_pools client-side, same as always."""
    global _hymn_library_cache
    if _hymn_library_cache is None:
        with open(CONTENT_ROOT / "proper_texts" / "hymns.json", encoding="utf-8") as f:
            data = json.load(f)
        data.pop("_note", None)
        _hymn_library_cache = data
    return _hymn_library_cache


# Maps a sanctorale record's commune_subsidiarium (see load_common) to the
# occasion tag hymns.json's "occasions" field uses for that Common - GILH
# SS235 already takes the antiphon/reading/responsory/intercessions from the
# saint's own Proper or Common when it's a Memorial (see
# apply_sanctorale_memorial); the hymn recommendation follows the same
# real-practice rule (a martyr's hymn on a martyr's day, etc.), just as a
# soft default rather than a swap - the dropdown is never restricted, this
# only decides what's pre-selected. pastors_doctors reuses the plain
# "pastors" hymn tag (no Doctor-specific hymn sourced yet); holy_men_women
# has no dedicated tag yet, so it simply falls through to the next
# priority level (season, then weekday) rather than a wrong guess.
HYMN_OCCASION_BY_COMMUNE_KEY = {
    "apostles": "apostles", "martyrs": "martyrs", "virgins": "virgins",
    "pastors": "pastors", "pastors_doctors": "pastors", "bvm": "marian",
}


def hymn_occasion_for_commune(commune_subsidiarium) -> str:
    if not commune_subsidiarium or not commune_subsidiarium.startswith("COMMON_"):
        return None
    key = commune_subsidiarium[len("COMMON_"):].lower()
    return HYMN_OCCASION_BY_COMMUNE_KEY.get(key)


def hymn_occasion_for_cycle_key(cycle_key) -> str:
    """Derives a seasonal occasion tag from a breviarium-core-style id
    prefix (e.g. 'advent_3_wednesday' -> 'advent'), for the ferial days
    breviarium_primary_hour_units renders (the only seasons breviarium-core
    supplies psalmody for at all - Ordinary Time has its own weekday-cycle
    tagging instead, applied at its own call site)."""
    if not cycle_key:
        return None
    for prefix, occ in (("advent_", "advent"), ("christmas_", "christmas"),
                        ("lent_", "lent"), ("easter_time_", "easter"), ("easter_", "easter")):
        if cycle_key.startswith(prefix):
            return occ
    return None


def recommend_hymn_id(hour: str, occasions) -> str:
    """Given an ordered list of occasion tags to try (most specific first,
    None/falsy entries skipped), returns the id of the first hymn tagged
    for `hour` that carries one of them - or None if nothing matches, in
    which case the client keeps its existing fallback (the pool's own
    first entry), same as before this feature existed. Never narrows or
    filters what's selectable, only what's pre-selected by default."""
    library = _load_hymn_library()
    for occ in occasions:
        if not occ:
            continue
        for hid, h in library.items():
            if hour in h.get("applicability", []) and occ in h.get("occasions", []):
                return hid
    return None


def load_distribution_entry(hour: str, psalter_week: int, weekday: str) -> dict:
    with open(CONTENT_ROOT / "tables" / "ferial_psalter_distribution.json", encoding="utf-8") as f:
        table = json.load(f)
    if hour == "compline":
        return table[hour][weekday.lower()]
    return table[hour][f"week{psalter_week}"][weekday.lower()]


def load_short_reading_citation(hour: str, psalter_week: int, weekday: str):
    """Ferial (Mon-Sat) Ordinary Time short reading citation for Lauds/Vespers,
    from content/tables/ferial_short_reading_citations.json. Returns None if
    not covered (Sunday/feast readings aren't part of this 4-week table)."""
    if hour not in ("lauds", "vespers"):
        return None
    with open(CONTENT_ROOT / "tables" / "ferial_short_reading_citations.json", encoding="utf-8") as f:
        table = json.load(f)
    return table.get(hour, {}).get(f"week{psalter_week}", {}).get(weekday.lower())


def load_sunday_entry(hour_variant: str, psalter_week: int) -> dict:
    """hour_variant: 'vespers_i' | 'vespers_ii' | 'lauds'"""
    with open(CONTENT_ROOT / "tables" / "sunday_psalter_distribution.json", encoding="utf-8") as f:
        table = json.load(f)
    return table[hour_variant][f"week{psalter_week}"]


def psalm_lines(citation_text: str, corpora: dict) -> dict:
    citation = Citation.parse(citation_text)
    out = {}
    for lang in LANGUAGES:
        verses = corpora[lang].text_for(citation)
        out[lang] = verses if verses else None
    return out


def ant(proper: dict, tag: str) -> dict:
    return {lang: proper[lang].get(tag, "antiphon") for lang in LANGUAGES}


def breviarium_extras(entry_id: str, day_index_name: str) -> dict:
    """Looks up responsory/preces/Spanish-reading/Spanish-collect from the
    breviarium-core database (see memory note 'main extract sources' /
    _recovered_scripts/breviarium_core_resolver.py) for a given day-index id
    (e.g. 'ordinary_time_5_tuesday', or a sanctorale record's own id). Returns
    an empty dict if the id isn't present in that day-index file - callers
    treat every key as optional."""
    resolved = get_resolved(day_index_name, entry_id)
    return resolved or {}


_latin_seasonal_tables_cache = {}


def _load_latin_seasonal_table(name: str) -> dict:
    """Loads one of content/tables/latin_{responsories,preces,oratio_seasonal}.json
    - real Latin text extracted from Universalis' official-text Latin ePub
    editions of the Liturgy of the Hours (see _recovered_scripts/
    build_latin_tables.py), keyed the same way breviarium-core's own ids
    work (e.g. 'advent_1_monday', 'ordinary_time_15_saturday'). These are a
    supplement to breviarium-core (which is Spanish-only for these 3
    categories - see responsory_unit/intercessions_unit), not a
    replacement; only covers cycle positions that don't collide with a
    sanctorale record in the one reference year they were harvested from,
    so coverage is real but not necessarily total."""
    if name not in _latin_seasonal_tables_cache:
        path = CONTENT_ROOT / "tables" / f"latin_{name}.json"
        with open(path, encoding="utf-8") as f:
            _latin_seasonal_tables_cache[name] = json.load(f)
    return _latin_seasonal_tables_cache[name]


_SHORT_RESPONSORY_V_RE = re.compile(r"^℣\.\s*(.+?)[,.]?\s*\*\s*(.+?)\.\s*(.+?)\.\s*$")
_SHORT_RESPONSORY_R_RE = re.compile(r"^℟\.\s*(.+?)[,.]?\s*\*\s*(.+?)\.\s*Gl[oó]ria Patri\.\s*(.+?)\.\s*$")


def _expand_short_responsory(la_lines):
    """This project's curated Latin responsories are stored in the
    traditional compact 2-line printed convention (verse,* refrain. cue. /
    response,* refrain. Glória Patri. cue.), while breviarium-core's
    Spanish responsories are already pre-expanded into 6 separate lines -
    side by side these render with mismatched row counts, reading as
    unrelated content even when the underlying text is correct (found via
    a user report on ordinary_time_21_thursday, though the format mismatch
    is universal, not specific to that entry). Expands the Latin into the
    same 6-line structure Spanish already uses: the full verse, its
    repeat, the second verse, the refrain alone, the doxology, and the
    full verse repeated again. The parsing regexes were verified against
    all 811 responsory entries in the project before relying on them here
    (100% match after handling both '.' and ',' before the asterisk, and
    multi-word repeat-cues) - anything that still doesn't match (none
    currently) is left as the original 2-line form rather than guessed."""
    if not la_lines or len(la_lines) != 2:
        return la_lines
    m1 = _SHORT_RESPONSORY_V_RE.match(la_lines[0])
    m2 = _SHORT_RESPONSORY_R_RE.match(la_lines[1])
    if not m1 or not m2:
        return la_lines
    a, b, _cue1 = m1.groups()
    c, b2, _cue2 = m2.groups()
    full = f"{a}, {b}."
    return [
        f"℣. {full}",
        f"℟. {full}",
        f"℣. {c}.",
        f"℟. {b2}.",
        "℣. Glória Patri, et Fílio, et Spirítui Sancto.",
        f"℟. {full}",
    ]


def responsory_unit(extras: dict, cycle_key: str = None, hour: str = None) -> dict:
    lines = extras.get("responsorios") or []
    la_lines = None
    if cycle_key and hour:
        la_lines = _load_latin_seasonal_table("responsories").get(cycle_key, {}).get(hour)
        la_lines = _expand_short_responsory(la_lines)
    return {"kind": "lines", "label": "responsory",
            "content": {l: (la_lines if l == "la" else (lines if l == "es" else None)) for l in LANGUAGES}}


def _normalize_latin_preces(la_lines):
    """This project's curated Latin preces are stored in the traditional
    printed format: an intro line, then the refrain shown alone, then
    repeating triples of [petition part A, petition part B, refrain
    repeated] for each intercession - while the Spanish side (built just
    below, from breviarium-core's preces_contenido/preces_respuesta) is
    already flattened into one combined line per petition (the petition
    text with the refrain appended), giving 1+N total lines for N
    petitions. Side by side these have mismatched row counts even when
    the underlying content is correct (same class of issue as
    _expand_short_responsory, found via the same user report). Reshapes
    the Latin into that same 1+N structure: intro unchanged, then for each
    petition its two halves joined with the refrain appended - matching
    Spanish's own combination convention exactly. Leaves anything that
    doesn't cleanly fit either the [intro, refrain, (A, B, refrain)*N] or
    the [intro, refrain, (petition, refrain)*N] shape (a second, smaller
    sub-convention found where each petition is already a single line)
    untouched rather than guess."""
    if not la_lines or len(la_lines) < 2:
        return la_lines
    intro, refrain, *body = la_lines
    combined = [intro]
    if body and len(body) % 3 == 0:
        for i in range(0, len(body), 3):
            a, b, r = body[i], body[i + 1], body[i + 2]
            r = re.sub(r"^[–-]\s*", "", r).strip()
            combined.append(f"{a} {b} {r}".strip())
        return combined
    if body and len(body) % 2 == 0:
        for i in range(0, len(body), 2):
            a, r = body[i], body[i + 1]
            r = re.sub(r"^[–-]\s*", "", r).strip()
            combined.append(f"{a} {r}".strip())
        return combined
    return la_lines


def intercessions_unit(extras: dict, cycle_key: str = None, hour: str = None) -> dict:
    intro = extras.get("preces_intro")
    resp = extras.get("preces_respuesta")
    content = extras.get("preces_contenido") or []
    lines = []
    if intro:
        lines.append(intro)
    for petition in content:
        lines.append(petition + (f" {resp}" if resp else ""))
    la_lines = None
    if cycle_key and hour:
        la_lines = _load_latin_seasonal_table("preces").get(cycle_key, {}).get(hour)
        la_lines = _normalize_latin_preces(la_lines)
    return {"kind": "lines", "label": "intercessions",
            "content": {l: (la_lines if l == "la" else (lines if l == "es" else None)) for l in LANGUAGES}}


def fill_latin_seasonal_collect(unit: dict, cycle_key: str, hour: str) -> None:
    """Latin-fill counterpart to fill_spanish_collect, for the seasons whose
    ferial Oratio has no other Latin source (Advent/Lent/Easter/Christmas -
    Ordinary Time already has fill_latin_collect's Missale Romanum table).
    Never overwrites a real sourced Latin text if one's already there."""
    if not cycle_key or unit["content"].get("la") is not None:
        return
    la = _load_latin_seasonal_table("oratio_seasonal").get(cycle_key, {}).get(hour)
    if la:
        unit["content"]["la"] = la


def fill_spanish_collect(unit: dict, extras: dict) -> None:
    """Adds breviarium-core's Spanish collect into an existing concluding_prayer
    unit's 'es' slot, without disturbing whatever's already there (a sourced
    Latin text, or None)."""
    oracion = extras.get("oracion_final")
    if oracion and unit["content"].get("es") is None:
        unit["content"]["es"] = oracion


_ordinary_time_sunday_collects_cache = None


def load_ordinary_time_sunday_collect(ot_week_number: int):
    """The Ordinary Time weekday Office reuses that week's own Sunday collect
    (a standard GILH option) - content/tables/ordinary_time_sunday_collects.json
    has the real Missale Romanum Latin text for weeks 2-34 (week 1 has none in
    the modern calendar, replaced by the Baptism of the Lord)."""
    global _ordinary_time_sunday_collects_cache
    if _ordinary_time_sunday_collects_cache is None:
        path = CONTENT_ROOT / "tables" / "ordinary_time_sunday_collects.json"
        with open(path, encoding="utf-8") as f:
            _ordinary_time_sunday_collects_cache = json.load(f)
    return _ordinary_time_sunday_collects_cache.get(str(ot_week_number))


def fill_latin_collect(unit: dict, ot_week_number: int) -> None:
    if not ot_week_number or unit["content"].get("la") is not None:
        return
    collect = load_ordinary_time_sunday_collect(ot_week_number)
    if collect:
        unit["content"]["la"] = collect


_MANUAL_READING_LATIN_OVERRIDES = {
    # breviarium-core's citation dialect can't express a half-verse suffix
    # ("3b"), so convert_citation() correctly declines rather than guessing
    # (resolving whole verse 3 would wrongly include the "3a" clause, which
    # isn't part of this reading). Latin sourced directly (Nova Vulgata Rom
    # 8:3b-4), split at the same point as the already-correct Spanish.
    "Rom 8, 3b-4": "Deus Fílium suum mittens in similitúdinem carnis peccáti et de peccáto, damnávit peccátum in carne, et iustificátio legis implerétur in nobis, qui non secúndum carnem ambulámus, sed secúndum spíritum.",
}


def breviarium_reading_unit(extras: dict, corpora: dict):
    """Builds a proper bilingual 'reading' unit from breviarium-core's own
    citation (converted into this project's Citation format), so a reading
    sourced this way gets real verse-aligned Latin+Spanish from this
    project's own corpus - not just breviarium's raw Spanish prose. Falls
    back to Spanish-only plain text if the citation doesn't convert/resolve
    (e.g. a bare alternate-reading 'X / Y' citation). Returns None if
    breviarium has nothing usable for this hour at all."""
    cita = extras.get("lectura_biblica_cita")
    texto = extras.get("lectura_biblica")
    if not texto:
        return None
    manual_la = _MANUAL_READING_LATIN_OVERRIDES.get((cita or "").strip())
    if manual_la:
        return {"kind": "plain", "label": "reading", "content": {"la": manual_la, "es": texto}, "ref": cita}
    converted = convert_citation(cita) if cita else None
    if converted:
        try:
            lines = psalm_lines(converted, corpora)
        except ValueError:
            lines = None
        if lines and (lines.get("la") or lines.get("es")):
            # A citation that resolves real Latin but fails to resolve
            # Spanish (a verse missing/misaligned in this project's own
            # Spanish corpus - found happening for Isaiah 9:5/Dec 30) must
            # not suppress breviarium-core's own already-good raw Spanish
            # prose just because the verse-aligned lookup came back partial.
            if not lines.get("es"):
                lines = {**lines, "es": texto}
            return {"kind": "psalm", "label": "reading", "ref": converted, "content": lines}
    return {"kind": "plain", "label": "reading", "content": {"la": None, "es": texto}, "ref": cita}


def breviarium_psalm_unit(cita: str, antifona: str, antifona_la: str, texto: str, corpora: dict) -> list:
    """Builds the antiphon/psalm-or-canticle/antiphon triple for one of
    breviarium-core's primer/segundo/tercer_salmo entries. Converts the
    citation into this project's own format and resolves bilingual verses
    from this project's corpus where possible (matching how every other
    psalm/canticle in the project is sourced); falls back to breviarium's
    own Spanish-only prose (as a single 'lines' block, not verse-numbered -
    breviarium doesn't key its raw psalm text by verse number) only when the
    citation doesn't convert or doesn't resolve. Returns [] if there's
    nothing here at all (some entries have only 2 of the 3 slots filled).
    antifona_la is this project's own in-house Latin sourcing, layered on top
    of breviarium-core (which is Spanish-only) - see
    content/proper_texts/breviarium_latin_antiphons.json; None until sourced."""
    if not cita:
        return []
    ant_content = {"es": antifona, "la": antifona_la}
    converted = convert_citation(cita)
    unit = None
    if converted:
        try:
            lines = psalm_lines(converted, corpora)
        except ValueError:
            lines = None
        if lines and (lines.get("la") or lines.get("es")):
            label = "psalm" if converted.startswith("Ps ") else "canticle"
            unit = {"kind": "psalm", "label": label, "ref": converted, "content": lines}
    if unit is None and texto:
        unit = {"kind": "lines", "label": "canticle", "ref": cita,
                "content": {"la": None, "es": texto.split("\n")}}
    if unit is None:
        return []
    ant_unit = {"kind": "ant", "label": "antiphon", "content": ant_content}
    return [ant_unit, unit, {**ant_unit, "repeated": True}]


# The 7th Sunday of Easter (between Ascension and Pentecost) is breviarium-
# core's one genuine content gap in the whole Easter season - every other
# day has an entry, this Sunday alone doesn't. Sourced by hand from
# Universalis' official-text Latin ePub edition of the Liturgy of the Hours
# (see _recovered_scripts/build_latin_tables.py's harvest of the SAME
# source for this day's Responsorium/Preces/Oratio, already in content/
# tables/latin_*.json under the 'easter_time_7_sunday' key - reused below
# rather than duplicated). Psalm/reading CITATIONS resolve bilingually
# through this project's own Bible corpus like every other citation-based
# unit; the antiphons themselves are liturgical compositions, not Scripture,
# so needed their own Spanish sourced separately (ant_es below - original
# in-house translations, not copied from any site, per project policy).
EASTER_7_SUNDAY_CONTENT = {
    "lauds": {
        "psalms": [
            {"cita": "Ps 92:1-5", "ant_la": "Dóminus regnávit, decórem indútus est, allelúia.",
             "ant_es": "El Señor reina, vestido de majestad, aleluya."},
            {"cita": "Dan 3:57-88,56",
             "ant_la": "Liberábitur creatúra in libertátem glóriæ filiórum Dei, allelúia.",
             "ant_es": "La creación será liberada para participar en la libertad y la gloria de los hijos de Dios, aleluya."},
            {"cita": "Ps 148:1-14", "ant_la": "Exaltátum est nomen Dómini super cælum et terram, allelúia.",
             "ant_es": "Exaltado es el nombre del Señor sobre el cielo y la tierra, aleluya."},
        ],
        "reading_cita": "Acts 10:40-43",
        "gospel_canticle_ant_la": ("Pater, ego te clarificávi super terram; opus consummávi, quod dedísti "
                                    "mihi ut fáciam, allelúia."),
        "gospel_canticle_ant_es": ("Padre, yo te he glorificado en la tierra; he llevado a cabo la obra "
                                    "que me encomendaste realizar, aleluya."),
    },
    "vespers": {
        "psalms": [
            {"cita": "Ps 109:1-5,7",
             "ant_la": "Purgatiónem peccatórum fáciens, sedet ad déxteram maiestátis in excélsis, allelúia.",
             "ant_es": "Después de purificarnos de los pecados, se sentó a la derecha de la majestad en las alturas, aleluya."},
            {"cita": "Ps 110:1-10", "ant_la": "Redemptiónem misit Dóminus pópulo suo, allelúia.",
             "ant_es": "El Señor envió la redención a su pueblo, aleluya."},
        ],
        "reading_cita": "Heb 10:12-14",
        "gospel_canticle_ant_la": ("Cum vénerit Paráclitus, quem ego mittam vobis, Spíritum veritátis, qui a "
                                    "Patre procédit, ille testimónium perhibébit de me, allelúia."),
        "gospel_canticle_ant_es": ("Cuando venga el Paráclito, que yo os enviaré de parte del Padre, el "
                                    "Espíritu de la verdad, que procede del Padre, él dará testimonio de mí, aleluya."),
    },
}

EASTER_7_SUNDAY_COLLECT_ES = (
    "Atiende, Señor, propicio a nuestras súplicas, para que, así como creemos que el "
    "Salvador del género humano está contigo en tu majestad, sintamos también que "
    "permanece con nosotros, como él mismo prometió, hasta el fin de los siglos. "
    "Por nuestro Señor Jesucristo, tu Hijo, que contigo vive y reina en la unidad "
    "del Espíritu Santo, y es Dios, por los siglos de los siglos. Amén."
)


def build_easter_7_sunday_units(hour: str, corpora: dict, proper: dict) -> list:
    """Lauds or Vespers for the 7th Sunday of Easter - see EASTER_7_SUNDAY_
    CONTENT's comment for why this needs its own builder instead of
    breviarium_primary_hour_units (that function assumes breviarium-core's
    Spanish-only antiphon convention, which doesn't apply to this
    Latin-sourced content)."""
    data = EASTER_7_SUNDAY_CONTENT[hour]
    units = []
    deus = load_static("deus_in_adiutorium")
    units.append({"kind": "static", "label": "deus", "content": _static_content(deus)})
    hymn_recommended = recommend_hymn_id(hour, ["easter", "sunday"])
    units.append({"kind": "hymn_choice", "label": "hymn", "hour": hour, "recommended": hymn_recommended})

    for p in data["psalms"]:
        ant_content = {"la": p["ant_la"], "es": p.get("ant_es")}
        lines = psalm_lines(p["cita"], corpora)
        label = "psalm" if p["cita"].startswith("Ps ") else "canticle"
        units.append({"kind": "ant", "label": "antiphon", "content": ant_content})
        units.append({"kind": "psalm", "label": label, "ref": p["cita"], "content": lines})
        units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": ant_content})

    reading_lines = psalm_lines(data["reading_cita"], corpora)
    units.append({"kind": "psalm", "label": "reading", "ref": data["reading_cita"], "content": reading_lines})
    units.append(responsory_unit({}, "easter_time_7_sunday", hour))

    gospel_key = "gospel_canticle_benedictus" if hour == "lauds" else "gospel_canticle_magnificat"
    gospel_ant = {"la": data["gospel_canticle_ant_la"], "es": data.get("gospel_canticle_ant_es")}
    gospel_ref = GOSPEL_CANTICLE_CITATIONS[gospel_key]
    units.append({"kind": "ant", "label": "antiphon", "content": gospel_ant})
    units.append({"kind": "psalm", "label": gospel_key, "ref": gospel_ref, "content": psalm_lines(gospel_ref, corpora)})
    units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": gospel_ant})

    units.append(intercessions_unit({}, "easter_time_7_sunday", hour))
    our_father = load_static("our_father")
    units.append({"kind": "lines", "label": "our_father", "content": _static_content(our_father)})
    concluding_unit = {"kind": "plain", "label": "concluding_prayer", "content": {l: None for l in LANGUAGES}}
    fill_latin_seasonal_collect(concluding_unit, "easter_time_7_sunday", hour)
    concluding_unit["content"]["es"] = EASTER_7_SUNDAY_COLLECT_ES
    units.append(concluding_unit)
    dismissal = load_static("dismissal_vespers_lauds")
    units.append({"kind": "static", "label": "dismissal", "content": _static_content(dismissal)})

    return units


_YEAR_VARIANT_RE = re.compile(
    r"\$\s*A[ñn]o\s*A\s*:\s*\$(?P<a>.*?)\$\s*A[ñn]o\s*B\s*:\s*\$(?P<b>.*?)\$\s*A[ñn]o\s*C\s*:\s*\$(?P<c>.*)$",
    re.S)


def year_letter_for_date(d: date) -> str:
    """Sunday-lectionary cycle letter (A/B/C) for a given date - the 3-year
    cycle is conventionally named after the calendar year most of it falls
    in (e.g. the liturgical year beginning Advent 2025 is "Year A" since it
    mostly runs through 2026); remainder 1->A, 2->B, 0->C (verified against
    known reference years: 2023->A, 2024->B, 2025->C, 2026->A)."""
    cycle_year = d.year + 1 if d >= first_sunday_of_advent(d.year) else d.year
    return {1: "A", 2: "B", 0: "C"}[cycle_year % 3]


_TRAILING_SOURCING_NOTE_RE = re.compile(r"\s*\([^()]*\)\s*$")


def _strip_trailing_sourcing_note(text: str) -> str:
    """The Año A/B/C gospel-antiphon segments this file curates sometimes
    carry an internal provenance/confidence note in trailing parentheses
    (e.g. '...non moriétur in ætérnum. (Io 11,25-26 - live fetch, VERBATIM
    matches...)') - documentation for whoever maintains this content, never
    meant to be prayed. _YEAR_VARIANT_RE's segment match has no way to tell
    that note apart from the real text (both just end at the next '$Año X:
    $' marker), so without this it renders straight to the page. Strips at
    most one such trailing note; safe no-op on any segment that doesn't end
    in one (most don't)."""
    return _TRAILING_SOURCING_NOTE_RE.sub("", text)


def _select_year_variant(text, year_letter: str):
    """breviarium-core stores some Sunday-cycle-dependent text (mostly
    Ordinary Time Sunday gospel-canticle antiphons, ids ~2400-2513, but
    found affecting Advent Sundays too) as a single string shaped
    '$ Año A: $<text A>\\n$Año B: $<text B>\\n$Año C: $<text C>' rather than
    three separate fields - the client-side mdLite() markdown-lite renderer
    has no notion of this format and was rendering all three concatenated
    as one bolded blob. Reduces to just the current cycle's segment (still
    wrapped in whatever _emphasis_/$bold$ markup it already had) - returns
    the input unchanged if it doesn't match this format, so this is always
    safe to apply to any string."""
    if not isinstance(text, str) or "$" not in text:
        return text
    m = _YEAR_VARIANT_RE.match(text.strip())
    if not m:
        return text
    return _strip_trailing_sourcing_note(m.group(year_letter.lower()).strip())


def _apply_year_variant_selection(extras: dict, year_letter: str) -> dict:
    def transform(v):
        if isinstance(v, str):
            return _select_year_variant(v, year_letter)
        if isinstance(v, list):
            return [transform(x) for x in v]
        return v
    return {k: transform(v) for k, v in extras.items()}


def _apply_advent_sunday_o_antiphon_override(vespers_units: list, advent_tag) -> None:
    """GILH SS213's 'O Antiphons' (Dec 17-23) apply to whichever Vespers
    falls on that date, Sunday included - and Advent 4 Sunday, which always
    falls Dec 18-24, therefore carries a DIFFERENT Magnificat antiphon every
    year depending on which specific date it lands on (confirmed via live
    cross-check: 2026's Advent 4 = Dec 20 = 'O Clavis David', 2027's = Dec 19
    = 'O Radix Iesse' - not a single fixed 'Advent 4 Sunday' antiphon as the
    single hardcoded breviarium-core id for that Sunday would otherwise give
    every year). Advent 3 (Gaudete) can rarely land on Dec 17 too (whenever
    Christmas Day itself is a Sunday), so this checks both Sundays rather
    than hardcoding week 4.

    Dec 24 has no O-Antiphon of its own (the series only runs 17-23) but
    still needs handling here: confirmed by direct testing that the
    sanctorale First-Vespers-of-Christmas overlay does NOT reach this case
    (its is_privileged_sunday guard correctly leaves a privileged Sunday's
    own Vespers in place, and Advent 4 Sunday is exactly such a Sunday - see
    resolve_and_build_day's docstring), so without this, Dec-24-as-Advent-4-
    Sunday would fall back to the generic hardcoded 'advent_4_sunday'
    antiphon (itself just a leftover copy of Dec 22's O Rex Gentium).
    Sourced instead from content/sanctorale/Sollemnitas/
    in_nativitate_domini_12_25.json's own magnificat_i/magnificat_i_es
    (First Vespers of Christmas' proper antiphon, 'Cum ortus fuerit sol de
    caelo...') - confirmed via a live Wayback Machine capture of a real
    computed Dec-24-Sunday Vespers page (2017) that this exact text is what
    every source actually shows for this date, regardless of whether one
    labels the evening 'Advent 4 Sunday's Vespers II' or 'Christmas' First
    Vespers' - the two framings disagree on the label but not the text.

    Mutates vespers_units in place; a no-op if this Sunday's date isn't Dec
    17-24 or the source entry is missing either language's text."""
    if advent_tag.weekday != "Sunday" or advent_tag.week_number not in (3, 4):
        return
    day = advent_tag.date.day
    if day < 17 or day > 24:
        return
    if day == 24:
        christmas_record = resolve_sanctorale_for_date(date(advent_tag.date.year, 12, 25))
        ga = (christmas_record or {}).get("antiphonae_evangelicae", {})
        es_text = ga.get("magnificat_i_es") or ga.get("magnificat_es")
        la_text = ga.get("magnificat_i") or ga.get("magnificat")
    else:
        o_antiphon_id = f"advent_december_{day}"
        extras = get_resolved("all_vesperae", o_antiphon_id)
        es_text = extras.get("cantico_evangelico_antifona") if extras else None
        la_text = load_breviarium_latin_antiphons().get(o_antiphon_id, {}).get("vespers", {}).get("gospel")
    if not es_text and not la_text:
        return
    o_ant = {"es": es_text, "la": la_text}
    for i, unit in enumerate(vespers_units):
        if unit.get("label") == "gospel_canticle_magnificat":
            for j in (i - 1, i + 1):
                if 0 <= j < len(vespers_units) and vespers_units[j].get("label") == "antiphon":
                    vespers_units[j]["content"] = o_ant
            break


def _apply_pre_epiphany_psalter_override(units: list, hour: str, weekday: str, corpora: dict, proper: dict) -> None:
    """The 3 psalm-antiphon slots breviarium-core stores for Jan 3/4/5
    (christmas_time_january_N, the ferial days between the Octave of
    Christmas and Epiphany) are WRONG for most years: real GILH rubrics
    have these days run the ORDINARY weekday psalter (the same one
    Ordinary Time ferial days use, which depends on which weekday the date
    falls on - genuinely different year to year), but breviarium-core
    stores one fixed psalm set apparently captured from whatever single
    reference year this data was originally scraped in. Only the short
    reading and Gospel-canticle antiphon are genuinely date-fixed for
    these days (independently confirmed correct against a live source) -
    this leaves those untouched and replaces just the 3 psalm-antiphon
    triples.

    Confirmed empirically (not assumed) which psalter week these days
    actually use: live-fetched 2026-01-03 (Saturday) and 2026-01-05
    (Monday) both matched content/tables/ferial_psalter_distribution.json's
    WEEK 2 entries exactly (and no other week), for both dates - i.e. a
    FIXED week 2, not the normal rotating cycle (which would never give
    the same week for a Saturday and the following Monday). Reuses the
    exact same content/proper_texts/ antiphon keys and psalm citations
    already correctly populated for ordinary Week-2 Saturday/Monday/etc
    (build_hour_units's own data), so no new antiphon text needed - only
    the reading/collect/gospel-canticle stay sourced from breviarium-core.

    Mutates units in place; replaces the span from just after the 'hymn'
    unit up to (not including) the first 'reading' unit. A no-op for
    Saturday Vespers: the ordinary ferial distribution table has no such
    entry at all (Saturday evening is always First Vespers of the
    following Sunday instead, a different concept this override doesn't
    attempt to model) - leaves whatever breviarium-core already had rather
    than crash on a lookup that structurally can't exist."""
    PRE_EPIPHANY_PSALTER_WEEK = 2
    if hour == "vespers" and weekday == "Saturday":
        return
    entry = load_distribution_entry(hour, PRE_EPIPHANY_PSALTER_WEEK, weekday)
    day_tag = f"{hour}_wk{PRE_EPIPHANY_PSALTER_WEEK}_{weekday.lower()}"

    def triple(ant_content, ref):
        label = "psalm" if ref.startswith("Ps") else "canticle"
        return [
            {"kind": "ant", "label": "antiphon", "content": ant_content},
            {"kind": "psalm", "label": label, "ref": ref, "content": psalm_lines(ref, corpora)},
            {"kind": "ant", "label": "antiphon", "repeated": True, "content": ant_content},
        ]

    new_units = triple(ant(proper, f"{day_tag}_ant1"), entry["psalm1"])
    if hour == "vespers":
        new_units += triple(ant(proper, f"{day_tag}_ant2"), entry["psalm2"])
        new_units.append({"kind": "psalm", "label": "canticle", "ref": entry["canticle"],
                           "content": psalm_lines(entry["canticle"], corpora)})
    else:
        new_units += triple(ant(proper, f"{day_tag}_ant2"), entry["canticle"])
        new_units += triple(ant(proper, f"{day_tag}_ant3"), entry["psalm3"])

    start = next((i for i, u in enumerate(units) if u.get("label") == "hymn"), None)
    end = next((i for i, u in enumerate(units) if u.get("label") == "reading"), None)
    if start is None or end is None:
        return
    units[start + 1:end] = new_units


def breviarium_primary_hour_units(hour: str, entry_id: str, corpora: dict, proper: dict, d: date = None) -> list:
    """Builds a full Vespers/Lauds hour DIRECTLY from breviarium-core, used
    for seasons where breviarium-core is the ONLY source of psalmody (Advent,
    Lent, Easter - there's no equivalent to Ordinary Time's
    ferial_psalter_distribution.json for these). Reuses
    responsory_unit/intercessions_unit/breviarium_reading_unit unchanged,
    since they already operate on a get_resolved()-shaped dict regardless of
    which day-index it came from; only the hymn and psalmody are new here,
    since Ordinary Time sources those from this project's own tables
    instead. Returns None if entry_id isn't in breviarium-core's index.
    d (the actual calendar date being rendered), when given, resolves any
    Año A/B/C cycle-variant text (see _select_year_variant) to just the
    current cycle's segment - omit only for callers that can't supply a
    real date (there are none left; kept optional for caution)."""
    day_index_name = "all_vesperae" if hour == "vespers" else "all_laudes"
    extras = get_resolved(day_index_name, entry_id)
    if not extras:
        return None
    if d is not None:
        extras = _apply_year_variant_selection(extras, year_letter_for_date(d))
    latin_ants = load_breviarium_latin_antiphons().get(entry_id, {}).get(hour, {})

    units = []
    deus = load_static("deus_in_adiutorium")
    units.append({"kind": "static", "label": "deus", "content": _static_content(deus)})
    hymn_occasions = [hymn_occasion_for_cycle_key(entry_id)]
    if entry_id and entry_id.endswith("_sunday"):
        hymn_occasions.append("sunday")
    hymn_recommended = recommend_hymn_id(hour, hymn_occasions)
    units.append({"kind": "hymn_choice", "label": "hymn", "hour": hour, "recommended": hymn_recommended})

    for n in ("primer", "segundo", "tercer"):
        units.extend(breviarium_psalm_unit(
            extras.get(f"{n}_salmo_cita"), extras.get(f"{n}_salmo_antifona"), latin_ants.get(n),
            extras.get(f"{n}_salmo_texto"), corpora))

    units.append(breviarium_reading_unit(extras, corpora) or
                 {"kind": "plain", "label": "reading", "content": {l: None for l in LANGUAGES}})
    units.append(responsory_unit(extras, entry_id, hour))

    gospel_key = "gospel_canticle_benedictus" if hour == "lauds" else "gospel_canticle_magnificat"
    gospel_ant_text = extras.get("cantico_evangelico_antifona")
    gospel_ant_latin = latin_ants.get("gospel")
    if d is not None:
        gospel_ant_latin = _select_year_variant(gospel_ant_latin, year_letter_for_date(d))
    gospel_ant = {"es": gospel_ant_text, "la": gospel_ant_latin}
    gospel_ref = GOSPEL_CANTICLE_CITATIONS[gospel_key]
    units.append({"kind": "ant", "label": "antiphon", "content": gospel_ant})
    units.append({"kind": "psalm", "label": gospel_key, "ref": gospel_ref,
                  "content": psalm_lines(gospel_ref, corpora)})
    units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": gospel_ant})

    units.append(intercessions_unit(extras, entry_id, hour))
    our_father = load_static("our_father")
    units.append({"kind": "lines", "label": "our_father", "content": _static_content(our_father)})
    concluding_unit = {"kind": "plain", "label": "concluding_prayer", "content": {l: None for l in LANGUAGES}}
    fill_spanish_collect(concluding_unit, extras)
    fill_latin_seasonal_collect(concluding_unit, entry_id, hour)
    units.append(concluding_unit)
    dismissal = load_static("dismissal_vespers_lauds")
    units.append({"kind": "static", "label": "dismissal", "content": _static_content(dismissal)})

    return units


def memorial_proper_hour_units(hour: str, record: dict, corpora: dict, proper: dict, d: date = None):
    """A Memorial's own breviarium-core entry is normally 'cycle': ANY/
    MEMORY_FERIAL* - no proper psalms of its own (-1 placeholders), meaning
    it's meant only for apply_sanctorale_memorial's antiphon/collect swap on
    top of the day's real ferial content (GILH SS235). A handful (7, as of
    this writing - e.g. Ss Basil & Gregory, Jan 2) are instead 'cycle':
    MEMORY_PROPER, with genuinely full proper psalmody of their own; this
    matters because Jan 2 has no OTHER content at all - breviarium-core's
    Christmastide day-index has entries for Jan 3-5 but not Jan 2, a real
    gap that would otherwise sink the whole day (found via the 2026-2029
    audit). Returns full hour units sourced from the record's own entry, but
    ONLY when it's genuinely MEMORY_PROPER - never for the ordinary case,
    where doing this would silently produce a psalm-less hour instead of
    correctly falling through to real ferial content."""
    entry_id = record.get("breviarium_id") if record else None
    if not entry_id:
        return None
    day_index_name = "all_vesperae" if hour == "vespers" else "all_laudes"
    extras = get_resolved(day_index_name, entry_id)
    if not extras or extras.get("cycle") != "MEMORY_PROPER":
        return None
    return breviarium_primary_hour_units(hour, entry_id, corpora, proper, d)


def build_hour_units(hour: str, psalter_week: int, weekday: str, corpora: dict, proper: dict,
                      ot_week_number: int = None) -> list:
    entry = load_distribution_entry(hour, psalter_week, weekday)
    day_tag = f"{hour}_{weekday.lower()}" if hour == "compline" else f"{hour}_wk{psalter_week}_{weekday.lower()}"
    units = []
    breviarium_id = f"ordinary_time_{ot_week_number}_{weekday.lower()}" if ot_week_number else None

    if hour in ("vespers", "lauds"):
        deus = load_static("deus_in_adiutorium")
        units.append({"kind": "static", "label": "deus", "content": _static_content(deus)})
        hymn_recommended = recommend_hymn_id(hour, [f"ot_{weekday.lower()}"])
        units.append({"kind": "hymn_choice", "label": "hymn", "hour": hour, "recommended": hymn_recommended})

        ant1 = ant(proper, f"{day_tag}_ant1")
        units.append({"kind": "ant", "label": "antiphon", "content": ant1})
        units.append({"kind": "psalm", "label": "psalm", "ref": entry["psalm1"],
                      "content": psalm_lines(entry["psalm1"], corpora)})
        units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": ant1})

        if hour == "vespers":
            ant2 = ant(proper, f"{day_tag}_ant2")
            units.append({"kind": "ant", "label": "antiphon", "content": ant2})
            units.append({"kind": "psalm", "label": "psalm", "ref": entry["psalm2"],
                          "content": psalm_lines(entry["psalm2"], corpora)})
            units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": ant2})
            units.append({"kind": "psalm", "label": "canticle", "ref": entry["canticle"],
                          "content": psalm_lines(entry["canticle"], corpora)})
        else:
            ant2 = ant(proper, f"{day_tag}_ant2")
            units.append({"kind": "ant", "label": "antiphon", "content": ant2})
            units.append({"kind": "psalm", "label": "canticle", "ref": entry["canticle"],
                          "content": psalm_lines(entry["canticle"], corpora)})
            units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": ant2})

            ant3 = ant(proper, f"{day_tag}_ant3")
            units.append({"kind": "ant", "label": "antiphon", "content": ant3})
            units.append({"kind": "psalm", "label": "psalm", "ref": entry["psalm3"],
                          "content": psalm_lines(entry["psalm3"], corpora)})
            units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": ant3})

        day_index_name = "all_vesperae" if hour == "vespers" else "all_laudes"
        extras = breviarium_extras(breviarium_id, day_index_name) if breviarium_id else {}

        reading_citation = load_short_reading_citation(hour, psalter_week, weekday)
        if reading_citation:
            reading_unit = {"kind": "psalm", "label": "reading", "ref": reading_citation,
                             "content": psalm_lines(reading_citation, corpora)}
        else:
            reading_unit = (breviarium_reading_unit(extras, corpora) or
                             {"kind": "plain", "label": "reading", "content": {l: None for l in LANGUAGES}})
        units.append(reading_unit)
        units.append(responsory_unit(extras, breviarium_id, hour))

        gospel_key = "gospel_canticle_magnificat" if hour == "vespers" else "gospel_canticle_benedictus"
        gospel_ant_tag = f"{day_tag}_magnificat_ant" if hour == "vespers" else f"{day_tag}_benedictus_ant"
        gospel_ant = ant(proper, gospel_ant_tag)
        gospel_ref = GOSPEL_CANTICLE_CITATIONS[gospel_key]
        units.append({"kind": "ant", "label": "antiphon", "content": gospel_ant})
        units.append({"kind": "psalm", "label": gospel_key, "ref": gospel_ref,
                      "content": psalm_lines(gospel_ref, corpora)})
        units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": gospel_ant})

        units.append(intercessions_unit(extras, breviarium_id, hour))
        our_father = load_static("our_father")
        units.append({"kind": "lines", "label": "our_father", "content": _static_content(our_father)})
        concluding_unit = {"kind": "plain", "label": "concluding_prayer", "content": {l: None for l in LANGUAGES}}
        fill_latin_collect(concluding_unit, ot_week_number)
        fill_latin_seasonal_collect(concluding_unit, breviarium_id, hour)
        fill_spanish_collect(concluding_unit, extras)
        units.append(concluding_unit)
        dismissal = load_static("dismissal_vespers_lauds")
        units.append({"kind": "static", "label": "dismissal", "content": _static_content(dismissal)})

    elif hour == "compline":
        deus = load_static("deus_in_adiutorium")
        units.append({"kind": "static", "label": "deus", "content": _static_content(deus)})
        units.append({"kind": "hymn_choice", "label": "hymn", "hour": "compline"})

        ant1 = ant(proper, f"{day_tag}_ant1")
        units.append({"kind": "ant", "label": "antiphon", "content": ant1})
        units.append({"kind": "psalm", "label": "psalm", "ref": entry["psalm1"],
                      "content": psalm_lines(entry["psalm1"], corpora)})
        if "psalm2" in entry:
            units.append({"kind": "psalm", "label": "psalm", "ref": entry["psalm2"],
                          "content": psalm_lines(entry["psalm2"], corpora)})
        units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": ant1})

        reading_citation = entry.get("reading")
        if reading_citation:
            units.append({"kind": "psalm", "label": "reading", "ref": reading_citation,
                          "content": psalm_lines(reading_citation, corpora)})
        else:
            units.append({"kind": "plain", "label": "reading", "content": {l: None for l in LANGUAGES}})
        compline_responsory = load_static("compline_responsory")
        units.append({"kind": "static", "label": "responsory",
                      "content": _static_content(compline_responsory)})

        nunc_ant = ant(proper, "compline_nunc_dimittis_ant")
        units.append({"kind": "ant", "label": "antiphon", "content": nunc_ant})
        units.append({"kind": "psalm", "label": "nunc_dimittis", "ref": NUNC_DIMITTIS_CITATION,
                      "content": psalm_lines(NUNC_DIMITTIS_CITATION, corpora)})
        units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": nunc_ant})

        compline_prayer = load_static("compline_concluding_prayer")[weekday.lower()]
        units.append({"kind": "static", "label": "concluding_prayer",
                      "content": _static_content(compline_prayer)})
        compline_dismissal = load_static("compline_dismissal")
        units.append({"kind": "static", "label": "dismissal",
                      "content": _static_content(compline_dismissal)})

    return units


def build_sunday_units(hour_variant: str, psalter_week: int, corpora: dict, proper: dict,
                        ot_week_number: int = None) -> list:
    """hour_variant: 'vespers_i' | 'vespers_ii' | 'lauds' (Sunday Lauds)."""
    entry = load_sunday_entry(hour_variant, psalter_week)
    # A handful of Ordinary Time Sundays carry their own special id in
    # breviarium-core instead of the plain 'ordinary_time_N_sunday' pattern
    # (verified against its day-index: week 3 = Sunday of the Word of God,
    # week 34 = Christ the King, the last Sunday of the liturgical year).
    SUNDAY_ID_OVERRIDES = {3: "sunday_of_the_word_of_god", 34: "our_lord_jesus_christ_king_of_the_universe"}
    breviarium_id = (SUNDAY_ID_OVERRIDES.get(ot_week_number) or
                      (f"ordinary_time_{ot_week_number}_sunday" if ot_week_number else None))
    breviarium_index = "all_laudes" if hour_variant == "lauds" else "all_vesperae"
    extras = breviarium_extras(breviarium_id, breviarium_index) if breviarium_id else {}
    day_tag = "vespers_i" if hour_variant == "vespers_i" else ("vespers_ii" if hour_variant == "vespers_ii" else "lauds_sunday")
    day_tag = f"{day_tag}_wk{psalter_week}"
    units = []

    deus = load_static("deus_in_adiutorium")
    units.append({"kind": "static", "label": "deus", "content": _static_content(deus)})
    hymn_context = "lauds" if hour_variant == "lauds" else "vespers"
    hymn_recommended = recommend_hymn_id(hymn_context, ["sunday"])
    units.append({"kind": "hymn_choice", "label": "hymn", "hour": hymn_context, "recommended": hymn_recommended})

    ant1 = ant(proper, f"{day_tag}_ant1")
    units.append({"kind": "ant", "label": "antiphon", "content": ant1})
    units.append({"kind": "psalm", "label": "psalm", "ref": entry["psalm1"],
                  "content": psalm_lines(entry["psalm1"], corpora)})
    units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": ant1})

    ant2 = ant(proper, f"{day_tag}_ant2")
    units.append({"kind": "ant", "label": "antiphon", "content": ant2})
    second_ref = entry["psalm2"] if hour_variant != "lauds" else entry["canticle"]
    second_label = "psalm" if hour_variant != "lauds" else "canticle"
    units.append({"kind": "psalm", "label": second_label, "ref": second_ref,
                  "content": psalm_lines(second_ref, corpora)})
    units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": ant2})

    ant3 = ant(proper, f"{day_tag}_ant3")
    if hour_variant == "lauds":
        units.append({"kind": "ant", "label": "antiphon", "content": ant3})
        units.append({"kind": "psalm", "label": "psalm", "ref": entry["psalm3"],
                      "content": psalm_lines(entry["psalm3"], corpora)})
        units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": ant3})
    else:
        # Vespers I/II: 3rd antiphon (if sourced) belongs to the NT canticle
        units.append({"kind": "ant", "label": "antiphon", "content": ant3})
        units.append({"kind": "psalm", "label": "canticle", "ref": entry["canticle"],
                      "content": psalm_lines(entry["canticle"], corpora)})
        units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": ant3})

    reading_unit = (breviarium_reading_unit(extras, corpora) or
                     {"kind": "plain", "label": "reading", "content": {l: None for l in LANGUAGES}})
    units.append(reading_unit)
    # The Latin seasonal tables only distinguish 'lauds'/'vespers' (Universalis'
    # own page structure has one "Ad Vesperas" per Sunday, not separate First/
    # Second Vespers entries) - vespers_i and vespers_ii both look up under
    # 'vespers', reusing the same real sourced text for both rather than
    # leaving vespers_i without Latin at all.
    latin_hour = "lauds" if hour_variant == "lauds" else "vespers"
    units.append(responsory_unit(extras, breviarium_id, latin_hour))

    gospel_key = "gospel_canticle_magnificat" if hour_variant != "lauds" else "gospel_canticle_benedictus"
    gospel_tag = f"{day_tag}_magnificat_ant" if hour_variant != "lauds" else f"{day_tag}_benedictus_ant"
    gospel_ant = ant(proper, gospel_tag)
    gospel_ref = GOSPEL_CANTICLE_CITATIONS[gospel_key]
    units.append({"kind": "ant", "label": "antiphon", "content": gospel_ant})
    units.append({"kind": "psalm", "label": gospel_key, "ref": gospel_ref,
                  "content": psalm_lines(gospel_ref, corpora)})
    units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": gospel_ant})

    units.append(intercessions_unit(extras, breviarium_id, latin_hour))
    our_father = load_static("our_father")
    units.append({"kind": "lines", "label": "our_father", "content": _static_content(our_father)})
    concluding_unit = {"kind": "plain", "label": "concluding_prayer", "content": {l: None for l in LANGUAGES}}
    fill_latin_collect(concluding_unit, ot_week_number)
    fill_latin_seasonal_collect(concluding_unit, breviarium_id, latin_hour)
    fill_spanish_collect(concluding_unit, extras)
    units.append(concluding_unit)
    dismissal = load_static("dismissal_vespers_lauds")
    units.append({"kind": "static", "label": "dismissal", "content": _static_content(dismissal)})

    return units


SANCTORALE_PSALMODY_KEY = {
    "lauds": "psalmodia_laudum",
    "vespers_i": "psalmodia_primarum_vesperarum",
    "vespers_ii": "psalmodia_secundarum_vesperarum",  # not yet sourced for any record
    "vespers": "psalmodia_vesperarum",                # Feast's single Vespers - not yet sourced either
}


def build_sanctorale_hour_units(hour_key: str, record: dict, corpora: dict, proper: dict) -> list:
    """Constructs a Feast/Solemnity's Lauds or Vespers from content/sanctorale/,
    per GILH SS225-231: psalmody is proper (never ferial) for these ranks. Uses
    real sourced psalmody where the record has it; where it doesn't (Vespers II
    of a Solemnity, or a Feast's only Vespers - not sourced in this pass), the
    psalm/antiphon units are simply absent rather than filled with ferial
    substitutes, since that would misrepresent what's actually proper here.
    hour_key: 'lauds' | 'vespers_i' | 'vespers_ii' | 'vespers'."""
    units = []
    deus = load_static("deus_in_adiutorium")
    units.append({"kind": "static", "label": "deus", "content": _static_content(deus)})
    hymn_context = "lauds" if hour_key == "lauds" else "vespers"
    hymn_recommended = recommend_hymn_id(hymn_context, [hymn_occasion_for_commune(record.get("commune_subsidiarium"))])
    units.append({"kind": "hymn_choice", "label": "hymn", "hour": hymn_context, "recommended": hymn_recommended})

    props = record.get("propria", {})
    psalmody = props.get(SANCTORALE_PSALMODY_KEY.get(hour_key, ""), [])
    if not psalmody:
        # Don't just silently skip straight to the reading - that reads as a
        # rendering bug, not the sourcing gap it actually is. This hour's own
        # proper psalmody genuinely hasn't been sourced yet for this record
        # (see task #21); say so instead of leaving a blank gap.
        units.append({"kind": "plain", "label": "psalmody_gap", "content": {l: True for l in LANGUAGES}})
    for item in psalmody:
        citation = item["citatio"]
        label = "psalm" if citation.startswith("Ps") else "canticle"
        ant_text = item.get("antiphona")
        ant_text_es = item.get("antiphona_es")
        ant_content = {l: (ant_text if l == "la" else ant_text_es) for l in LANGUAGES}
        units.append({"kind": "ant", "label": "antiphon", "content": ant_content})
        units.append({"kind": "psalm", "label": label, "ref": citation,
                      "content": psalm_lines(citation, corpora)})
        units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": ant_content})

    is_lauds = (hour_key == "lauds")
    breviarium_id = record.get("breviarium_id")
    breviarium_index = "all_laudes" if is_lauds else "all_vesperae"
    extras = breviarium_extras(breviarium_id, breviarium_index) if breviarium_id else {}

    reading_key = "lectio_brevis_laudum" if is_lauds else "lectio_brevis_vesperarum"
    reading_citation = props.get(reading_key)
    if reading_citation:
        units.append({"kind": "psalm", "label": "reading", "ref": reading_citation,
                      "content": psalm_lines(reading_citation, corpora)})
    else:
        reading_unit = (breviarium_reading_unit(extras, corpora) or
                         {"kind": "plain", "label": "reading", "content": {l: None for l in LANGUAGES}})
        units.append(reading_unit)
    # Universalis' page structure only distinguishes 'lauds'/'vespers', not
    # First/Second Vespers separately - same simplification as build_sunday_units.
    latin_hour = "lauds" if is_lauds else "vespers"
    units.append(responsory_unit(extras, record.get("id"), latin_hour))

    gospel_key = "gospel_canticle_benedictus" if is_lauds else "gospel_canticle_magnificat"
    ga = record.get("antiphonae_evangelicae", {})
    if is_lauds:
        gospel_ant_text = ga.get("benedictus")
        gospel_ant_text_es = ga.get("benedictus_es")
    elif hour_key == "vespers_i":
        gospel_ant_text = ga.get("magnificat_i") or ga.get("magnificat")
        gospel_ant_text_es = ga.get("magnificat_i_es") or ga.get("magnificat_es")
    else:
        gospel_ant_text = ga.get("magnificat_ii") or ga.get("magnificat")
        gospel_ant_text_es = ga.get("magnificat_ii_es") or ga.get("magnificat_es")
    gospel_ant = {l: (gospel_ant_text if l == "la" else gospel_ant_text_es) for l in LANGUAGES}
    gospel_ref = GOSPEL_CANTICLE_CITATIONS[gospel_key]
    units.append({"kind": "ant", "label": "antiphon", "content": gospel_ant})
    units.append({"kind": "psalm", "label": gospel_key, "ref": gospel_ref,
                  "content": psalm_lines(gospel_ref, corpora)})
    units.append({"kind": "ant", "label": "antiphon", "repeated": True, "content": gospel_ant})

    units.append(intercessions_unit(extras, record.get("id"), latin_hour))
    our_father = load_static("our_father")
    units.append({"kind": "lines", "label": "our_father", "content": _static_content(our_father)})
    collect_text = record.get("collecta")
    collect_content = {l: (collect_text if l == "la" else None) for l in LANGUAGES}
    units.append({"kind": "plain", "label": "concluding_prayer", "ref": record["titulus"],
                  "content": collect_content})
    fill_latin_seasonal_collect(units[-1], record.get("id"), latin_hour)
    fill_spanish_collect(units[-1], extras)
    dismissal = load_static("dismissal_vespers_lauds")
    units.append({"kind": "static", "label": "dismissal", "content": _static_content(dismissal)})

    return units


def _resolve_and_build_day_inner(d: date, corpora: dict, proper: dict):
    """Given any date, returns (hours_data, description_tag) where description_tag
    carries whatever's needed for the meta line. Dispatches by rank: a Solemnity
    or Feast from content/sanctorale/ takes over Lauds+Vespers entirely (proper
    psalmody, GILH SS225-231); a Memorial keeps ferial psalms and only swaps the
    Magnificat/Benedictus antiphon and collect (GILH SS235); a plain day falls
    through to ferial/Sunday. Handles the Saturday-evening-is-Sunday's-First-
    Vespers rule. A weekday Solemnity's own First Vespers (on the PRECEDING
    evening) is NOT built here - see resolve_and_build_day, which wraps this
    function and overlays that afterward, since it can require overwriting
    whatever branch below produced today's Vespers rather than being another
    branch itself."""
    is_sunday = d.weekday() == 6
    is_saturday = d.weekday() == 5
    hours_data = {}

    if d == baptism_of_the_lord(d.year):
        # A movable Feast (see load_baptism_of_the_lord_record's docstring)
        # checked before the fixed-date sanctorale lookup, whose own index
        # only has this record filed under a fixed, mostly-wrong date.
        record = load_baptism_of_the_lord_record()
        hours_data["lauds"] = build_sanctorale_hour_units("lauds", record, corpora, proper)
        hours_data["vespers"] = build_sanctorale_hour_units("vespers", record, corpora, proper)
        hours_data["compline"] = build_hour_units("compline", 1, "Sunday", corpora, proper)
        return hours_data, ("festum", None, None, record["titulus"], record)

    # Easter Time's highest-ranking days (the Octave, Divine Mercy Sunday,
    # Ascension, Pentecost) outrank every ordinary Feast/Memorial in the
    # fixed-date sanctorale calendar below - checked first so a saint whose
    # own feast happens to land here (e.g. St Matthias, May 14) can never
    # silently displace the Ascension just because Ascension itself isn't in
    # that fixed-date system. No Memorial overlay applies on any of these
    # (per GILH, the Octave admits none at all; Ascension/Pentecost are
    # Solemnities of the Lord; Divine Mercy is a Sunday) - unlike the
    # regular Easter weeks 2-7 handled further below, which do allow one.
    HIGH_RANK_EASTER_IDS = {
        "easter_sunday", "easter_monday", "easter_tuesday", "easter_wednesday",
        "easter_thursday", "easter_friday", "easter_saturday",
        "divine_mercy_sunday", "ascension_of_the_lord", "pentecost_sunday",
    }
    easter_tag = resolve_easter(d)
    if easter_tag is not None and easter_tag.breviarium_id in HIGH_RANK_EASTER_IDS:
        lauds_units = breviarium_primary_hour_units("lauds", easter_tag.breviarium_id, corpora, proper, d)
        vespers_units = breviarium_primary_hour_units("vespers", easter_tag.breviarium_id, corpora, proper, d)
        if lauds_units is not None and vespers_units is not None:
            hours_data["lauds"] = lauds_units
            hours_data["vespers"] = vespers_units
            hours_data["compline"] = build_hour_units("compline", 1, easter_tag.weekday, corpora, proper)
            return hours_data, ("easter", None, easter_tag.breviarium_id, easter_tag.weekday, None)

    if d == most_holy_trinity(d.year):
        # Also a movable day that must win before the sanctorale lookup -
        # its date otherwise falls inside Ordinary Time Part 2's range and
        # would be wrongly claimed as that part's first Sunday.
        lauds_units = breviarium_primary_hour_units("lauds", "most_holy_trinity", corpora, proper, d)
        vespers_units = breviarium_primary_hour_units("vespers", "most_holy_trinity", corpora, proper, d)
        if lauds_units is not None and vespers_units is not None:
            hours_data["lauds"] = lauds_units
            hours_data["vespers"] = vespers_units
            hours_data["compline"] = build_hour_units("compline", 1, "Sunday", corpora, proper)
            return hours_data, ("sollemnitas", None, None, "Sunday",
                                 {"titulus": "Sanctissimæ Trinitatis"})

    if d == christ_the_king(d.year):
        # The last Sunday of Ordinary Time - found completely missing from
        # the sanctorale/special-case system during the 2026-2029 audit
        # against content/calendar/'s synced cache (it was silently
        # rendering as a plain numbered OT Sunday). Same movable-Solemnity-
        # on-a-Sunday pattern as Trinity Sunday above, and needs the same
        # early check for the same reason: its date otherwise falls inside
        # resolve_ordinary_time_sunday's normal range and would be claimed
        # as an ordinary numbered Sunday without this override.
        lauds_units = breviarium_primary_hour_units("lauds", "our_lord_jesus_christ_king_of_the_universe", corpora, proper, d)
        vespers_units = breviarium_primary_hour_units("vespers", "our_lord_jesus_christ_king_of_the_universe", corpora, proper, d)
        if lauds_units is not None and vespers_units is not None:
            hours_data["lauds"] = lauds_units
            hours_data["vespers"] = vespers_units
            hours_data["compline"] = build_hour_units("compline", 1, "Sunday", corpora, proper)
            return hours_data, ("sollemnitas", None, None, "Sunday",
                                 {"titulus": "Domini Nostri Iesu Christi Universorum Regis"})

    if d == corpus_christi(d.year):
        # Thursday after Trinity Sunday - same "movable, not in the fixed-
        # date sanctorale index" situation as Trinity itself, so it needs
        # the same full breviarium-core takeover before the sanctorale
        # lookup below (which knows nothing about this date).
        lauds_units = breviarium_primary_hour_units("lauds", "most_holy_body_and_blood_of_christ", corpora, proper, d)
        vespers_units = breviarium_primary_hour_units("vespers", "most_holy_body_and_blood_of_christ", corpora, proper, d)
        if lauds_units is not None and vespers_units is not None:
            hours_data["lauds"] = lauds_units
            hours_data["vespers"] = vespers_units
            hours_data["compline"] = build_hour_units("compline", 1, "Sunday", corpora, proper)
            return hours_data, ("sollemnitas", None, None, "Thursday",
                                 {"titulus": "Sanctíssimi Córporis et Sánguinis Christi"})

    if d == sacred_heart_of_jesus(d.year):
        # Friday in the third week after Pentecost - same treatment.
        lauds_units = breviarium_primary_hour_units("lauds", "most_sacred_heart_of_jesus", corpora, proper, d)
        vespers_units = breviarium_primary_hour_units("vespers", "most_sacred_heart_of_jesus", corpora, proper, d)
        if lauds_units is not None and vespers_units is not None:
            hours_data["lauds"] = lauds_units
            hours_data["vespers"] = vespers_units
            hours_data["compline"] = build_hour_units("compline", 1, "Sunday", corpora, proper)
            return hours_data, ("sollemnitas", None, None, "Friday",
                                 {"titulus": "Sacratíssimi Cordis Iesu"})

    record = resolve_sanctorale_for_date(d)
    if is_sunday and (not record or record["gradus"] != "SOLLEMNITAS"):
        record = None  # Sunday outranks Feast/Memorial; only a Solemnity can override Sunday (GILH 237)

    # Palm Sunday through Holy Saturday outrank EVERY sanctorale record, even
    # a Solemnity - UNLY Table #59: PrivilegedSunday_2/WeekdayOfHolyWeek_2/
    # Triduum_1 all sit above GeneralSolemnity_3. No saint, however highly
    # ranked, is ever commemorated on these 6 days. (In practice this mostly
    # matters as a safety net: the only fixed Solemnities that can even land
    # here - St Joseph, the Annunciation - are already turned away upstream
    # by resolve_sanctorale_for_date's transfer logic, but a Feast/Memorial
    # has no transfer and must still be blanked here rather than leaking
    # through, which is what the now-fixed dead is_holy_week flag on
    # resolve_lent's Holy Monday-Wednesday days was meant to prevent.)
    _hw_palm = palm_sunday(d.year)
    _hw_sat = holy_thursday(d.year) + timedelta(days=2)
    if _hw_palm <= d <= _hw_sat:
        record = None

    if record is None and is_saturday and resolve_ferial_ordinary_time(d) is not None:
        record = MARIAN_SATURDAY_RECORD  # see its own comment above

    # A Feast never outranks a Sunday, so on a Saturday its VESPERS
    # correctly falls through below to the following Sunday's First
    # Vespers (is_saturday excludes it from the full-takeover branch just
    # below). A Solemnity is different: per GILH 237 its own Vespers (First
    # or Second) displaces an ordinary Sunday's First Vespers, so it must
    # NOT be excluded on a Saturday - without this, a Solemnity landing on
    # a Saturday (e.g. the Assumption) fell all the way through to plain
    # ferial Lauds AND had its own Vespers silently replaced, discarding
    # its proper texts for the whole day.
    is_overriding_solemnity = record and record["gradus"] == "SOLLEMNITAS"
    if record and record["gradus"] in ("FESTUM", "SOLLEMNITAS") and (not is_saturday or is_overriding_solemnity):
        hours_data["lauds"] = build_sanctorale_hour_units("lauds", record, corpora, proper)
        vespers_key = "vespers_ii" if record.get("habet_primas_vesperas") else "vespers"
        hours_data["vespers"] = build_sanctorale_hour_units(vespers_key, record, corpora, proper)
        hours_data["compline"] = build_hour_units("compline", 1, "Sunday", corpora, proper)
        kind = "sollemnitas" if record["gradus"] == "SOLLEMNITAS" else "festum"
        return hours_data, (kind, None, None, record["titulus"], record)

    # Reaching here with a FESTUM record means exactly one case: it's a
    # Saturday (the branch above already returned for every other case).
    # Its VESPERS correctly defers to the following Sunday's First Vespers,
    # but LAUDS has nothing to do with that Saturday-evening-anticipates-
    # Sunday rule and must still be this Feast's own proper Lauds - without
    # this override, whichever season branch below fills in today's Lauds
    # would silently show plain ferial content instead (found via Dec 26
    # sometimes landing on a Saturday: St Stephen's own Lauds was being
    # dropped even though his Vespers was correctly deferred).
    festum_lauds_pending = (build_sanctorale_hour_units("lauds", record, corpora, proper)
                             if record and record["gradus"] == "FESTUM" else None)

    christmas_tag = resolve_christmas(d)
    if christmas_tag is not None:
        # Same scope note as Advent/Lent/Easter: no Saturday-evening-
        # anticipates-Sunday handling. Christmas Day, Mary Mother of God,
        # and Epiphany are already fixed-date Solemnities in sanctorale and
        # never reach here (see resolve_christmas' docstring); this only
        # fills the ferial gaps around them.
        lauds_units = breviarium_primary_hour_units("lauds", christmas_tag.breviarium_id, corpora, proper, d)
        vespers_units = breviarium_primary_hour_units("vespers", christmas_tag.breviarium_id, corpora, proper, d)
        # Jan 3/4/5's 3 psalm-antiphon slots are year-dependent in the real
        # rubric (ordinary weekday psalter, week 2 fixed - confirmed via
        # live cross-check) but breviarium-core stores one fixed set from
        # whatever reference year it was scraped in; only the reading and
        # Gospel-canticle antiphon are genuinely date-fixed for these days.
        # See _apply_pre_epiphany_psalter_override's docstring.
        if christmas_tag.breviarium_id.startswith("christmas_time_january_") and christmas_tag.date.day in (3, 4, 5):
            if lauds_units is not None:
                _apply_pre_epiphany_psalter_override(lauds_units, "lauds", christmas_tag.weekday, corpora, proper)
            if vespers_units is not None:
                _apply_pre_epiphany_psalter_override(vespers_units, "vespers", christmas_tag.weekday, corpora, proper)
        # Jan 2 has no ferial Christmastide entry in breviarium-core at all
        # (unlike Jan 3-5) - but its fixed Memorial, Ss Basil & Gregory,
        # carries genuinely full proper psalmody of its own that year (see
        # memorial_proper_hour_units), so use that instead of failing the
        # whole day.
        if lauds_units is None:
            lauds_units = memorial_proper_hour_units("lauds", record, corpora, proper, d)
        if vespers_units is None:
            vespers_units = memorial_proper_hour_units("vespers", record, corpora, proper, d)
        if (festum_lauds_pending is None and lauds_units is None) or vespers_units is None:
            return None, None
        hours_data["lauds"] = festum_lauds_pending if festum_lauds_pending is not None else lauds_units
        hours_data["vespers"] = vespers_units
        hours_data["compline"] = build_hour_units("compline", 1, christmas_tag.weekday, corpora, proper)
        if record and record["gradus"] in ("MEMORIA_OBLIGATORIA", "MEMORIA_AD_LIBITUM"):
            apply_sanctorale_memorial(hours_data, record, hours=("lauds", "vespers"))
        return hours_data, ("christmas", None, christmas_tag.breviarium_id, christmas_tag.weekday, record)

    advent_tag = resolve_advent(d)
    if advent_tag is not None:
        # Advent has no equivalent to Ordinary Time's Saturday-evening-is-
        # Sunday's-First-Vespers handling here (see breviarium_primary_hour_units'
        # docstring) - each day, Saturday included, uses its own breviarium-core
        # entry for both Lauds and Vespers. A Memorial still only swaps the
        # Magnificat/Benedictus antiphon and collect (GILH 235), same as Ordinary Time.
        lauds_units = breviarium_primary_hour_units("lauds", advent_tag.breviarium_id, corpora, proper, d)
        vespers_units = breviarium_primary_hour_units("vespers", advent_tag.breviarium_id, corpora, proper, d)
        if (festum_lauds_pending is None and lauds_units is None) or vespers_units is None:
            return None, None
        _apply_advent_sunday_o_antiphon_override(vespers_units, advent_tag)
        hours_data["lauds"] = festum_lauds_pending if festum_lauds_pending is not None else lauds_units
        hours_data["vespers"] = vespers_units
        hours_data["compline"] = build_hour_units("compline", 1, advent_tag.weekday, corpora, proper)
        if record and record["gradus"] in ("MEMORIA_OBLIGATORIA", "MEMORIA_AD_LIBITUM"):
            apply_sanctorale_memorial(hours_data, record, hours=("lauds", "vespers"))
        # desc_tag's 3rd slot (normally ot_week_number) carries day-of-month
        # instead, but only for the December 17-24 'greater ferias' (where
        # week_number is None) - see build_day_description's advent branch.
        day_of_month = advent_tag.date.day if advent_tag.week_number is None else None
        return hours_data, ("advent", advent_tag.week_number, day_of_month, advent_tag.weekday, record)

    lent_tag = resolve_lent(d)
    if lent_tag is not None:
        # Same scope note as Advent: no Saturday-evening-anticipates-Sunday
        # handling here, each day (Saturday included) uses its own
        # breviarium-core entry for both Lauds and Vespers.
        lauds_units = breviarium_primary_hour_units("lauds", lent_tag.breviarium_id, corpora, proper, d)
        vespers_units = breviarium_primary_hour_units("vespers", lent_tag.breviarium_id, corpora, proper, d)
        if (festum_lauds_pending is None and lauds_units is None) or vespers_units is None:
            return None, None
        hours_data["lauds"] = festum_lauds_pending if festum_lauds_pending is not None else lauds_units
        hours_data["vespers"] = vespers_units
        hours_data["compline"] = build_hour_units("compline", 1, lent_tag.weekday, corpora, proper)
        if record and record["gradus"] in ("MEMORIA_OBLIGATORIA", "MEMORIA_AD_LIBITUM"):
            apply_sanctorale_memorial(hours_data, record, hours=("lauds", "vespers"))
        # desc_tag's 3rd slot (normally ot_week_number) carries breviarium_id
        # instead, but only for the named non-numbered-week days (Ash
        # Wednesday, Palm Sunday, Holy Week) - see build_day_description's
        # lent branch.
        named_id = lent_tag.breviarium_id if lent_tag.week_number is None else None
        return hours_data, ("lent", lent_tag.week_number, named_id, lent_tag.weekday, record)

    triduum_tag = resolve_triduum(d)
    if triduum_tag is not None:
        # record was already forced to None for this whole span above (Palm
        # Sunday through Holy Saturday outrank every sanctorale record - see
        # that check's comment), so unlike every other season branch here,
        # there's no apply_sanctorale_memorial call: no saint, however
        # highly ranked, is ever commemorated during the Triduum.
        lauds_units = breviarium_primary_hour_units("lauds", triduum_tag.breviarium_id, corpora, proper, d)
        if lauds_units is None:
            return None, None
        hours_data["lauds"] = lauds_units
        if triduum_tag.has_vespers:
            vespers_units = breviarium_primary_hour_units("vespers", triduum_tag.breviarium_id, corpora, proper, d)
            if vespers_units is None:
                return None, None
            hours_data["vespers"] = vespers_units
        else:
            # Holy Saturday has no Evening Prayer at all - the Easter Vigil
            # takes its place structurally (GILH SS208-209 name only
            # Thursday and Friday as having a Vespers that can be skipped;
            # Saturday's simply doesn't exist to skip). Say so explicitly
            # rather than leave a blank gap that reads as an unsourced-
            # content bug (see TriduumTag's docstring).
            hours_data["vespers"] = [{"kind": "plain", "label": "vespers_omitted_holy_saturday",
                                       "content": {lang: True for lang in LANGUAGES}}]
        hours_data["compline"] = build_hour_units("compline", 1, triduum_tag.weekday, corpora, proper)
        return hours_data, ("triduum", None, triduum_tag.breviarium_id, triduum_tag.weekday, None)

    if easter_tag is not None and easter_tag.breviarium_id == "easter_time_7_sunday":
        # breviarium-core's one genuine content gap in Easter Time - see
        # EASTER_7_SUNDAY_CONTENT's comment. record was already blanked
        # above unless it's a Solemnity (is_sunday check) - none of our
        # fixed Solemnities ever fall in this narrow window, so no memorial
        # overlay logic belongs here.
        hours_data["lauds"] = build_easter_7_sunday_units("lauds", corpora, proper)
        hours_data["vespers"] = build_easter_7_sunday_units("vespers", corpora, proper)
        hours_data["compline"] = build_hour_units("compline", 1, "Sunday", corpora, proper)
        return hours_data, ("easter", None, "easter_time_7_sunday", "Sunday", None)

    if easter_tag is not None:
        # Reaching here means easter_tag is NOT one of the high-rank ids
        # (those already returned above, before the sanctorale lookup) - so
        # this only handles the regular numbered Easter weeks 2-6, where a
        # Sunday still can't be overridden (is_sunday already blanked
        # `record` above unless it's a Solemnity) but a weekday Feast/
        # Memorial applies the same as any other season. Same
        # Saturday-evening scope note as Advent/Lent otherwise.
        lauds_units = breviarium_primary_hour_units("lauds", easter_tag.breviarium_id, corpora, proper, d)
        vespers_units = breviarium_primary_hour_units("vespers", easter_tag.breviarium_id, corpora, proper, d)
        if (festum_lauds_pending is None and lauds_units is None) or vespers_units is None:
            return None, None
        hours_data["lauds"] = festum_lauds_pending if festum_lauds_pending is not None else lauds_units
        hours_data["vespers"] = vespers_units
        hours_data["compline"] = build_hour_units("compline", 1, easter_tag.weekday, corpora, proper)
        if record and record["gradus"] in ("MEMORIA_OBLIGATORIA", "MEMORIA_AD_LIBITUM"):
            apply_sanctorale_memorial(hours_data, record, hours=("lauds", "vespers"))
        # desc_tag's 3rd slot (normally ot_week_number) carries breviarium_id
        # instead, but only for the named non-numbered-week days (the
        # Octave, Divine Mercy, Ascension, Pentecost) - see
        # build_day_description's easter branch.
        named_id = easter_tag.breviarium_id if easter_tag.week_number is None else None
        return hours_data, ("easter", easter_tag.week_number, named_id, easter_tag.weekday, record)

    if is_sunday:
        sun_tag = resolve_ordinary_time_sunday(d)
        if sun_tag is None:
            return None, None
        hours_data["lauds"] = build_sunday_units("lauds", sun_tag.psalter_week, corpora, proper,
                                                  ot_week_number=sun_tag.ot_week_number)
        hours_data["vespers"] = build_sunday_units("vespers_ii", sun_tag.psalter_week, corpora, proper,
                                                    ot_week_number=sun_tag.ot_week_number)
        hours_data["compline"] = build_hour_units("compline", sun_tag.psalter_week, "Sunday", corpora, proper)
        return hours_data, ("sunday", sun_tag.psalter_week, sun_tag.ot_week_number, "Sunday", None)

    if is_saturday:
        # Saturday evening = following Sunday's First Vespers; Compline
        # stays ferial Saturday. Lauds is ferial UNLESS festum_lauds_pending
        # is set (a FESTUM-grade saint's own Lauds, captured above).
        ferial_tag = resolve_ferial_ordinary_time(d)
        next_sunday_tag = resolve_ordinary_time_sunday(d + timedelta(days=1))
        # The very last Saturday of Ordinary Time Part 2 anticipates ADVENT's
        # First Sunday, not another Ordinary Time Sunday -
        # resolve_ordinary_time_sunday(d+1) correctly returns None there
        # (Advent 1 isn't Ordinary Time), which without this check made the
        # whole day wrongly fall through to a full out-of-scope result
        # instead of just needing Advent's own Vespers source.
        advent1_follows = (d + timedelta(days=1) == first_sunday_of_advent(d.year))
        if ferial_tag is None or (next_sunday_tag is None and not advent1_follows):
            return None, None
        hours_data["lauds"] = festum_lauds_pending if festum_lauds_pending is not None else build_hour_units(
            "lauds", ferial_tag.psalter_week, ferial_tag.weekday, corpora, proper,
            ot_week_number=ferial_tag.ot_week_number)
        if advent1_follows:
            # Year-letter must be computed from tomorrow's date (Advent 1
            # Sunday), not today's (d), since tomorrow is where the new
            # lectionary cycle year actually begins - year_letter_for_date(d)
            # here would still return the OLD cycle's letter.
            vespers_units = breviarium_primary_hour_units(
                "vespers", "advent_1_sunday", corpora, proper, d + timedelta(days=1))
            if vespers_units is None:
                return None, None
            hours_data["vespers"] = vespers_units
        else:
            hours_data["vespers"] = build_sunday_units("vespers_i", next_sunday_tag.psalter_week, corpora, proper,
                                                        ot_week_number=next_sunday_tag.ot_week_number)
        hours_data["compline"] = build_hour_units("compline", ferial_tag.psalter_week, ferial_tag.weekday, corpora, proper)
        if record and record["gradus"] in ("MEMORIA_OBLIGATORIA", "MEMORIA_AD_LIBITUM"):
            apply_sanctorale_memorial(hours_data, record, hours=("lauds",))
        return hours_data, ("ferial", ferial_tag.psalter_week, ferial_tag.ot_week_number, ferial_tag.weekday, record)

    ferial_tag = resolve_ferial_ordinary_time(d)
    if ferial_tag is None:
        return None, None
    for hour in IMPLEMENTED_HOURS:
        hours_data[hour] = build_hour_units(hour, ferial_tag.psalter_week, ferial_tag.weekday, corpora, proper,
                                             ot_week_number=ferial_tag.ot_week_number)
    if record and record["gradus"] in ("MEMORIA_OBLIGATORIA", "MEMORIA_AD_LIBITUM"):
        apply_sanctorale_memorial(hours_data, record, hours=("lauds", "vespers"))
    return hours_data, ("ferial", ferial_tag.psalter_week, ferial_tag.ot_week_number, ferial_tag.weekday, record)


def _load_page_template() -> str:
    """The static page shell (app/renderer/template.html) - kept as a real
    .html file rather than an inline Python string so its CSS/JS can be
    edited with normal editor tooling and never needs brace-escaping for
    .format(). Placeholders (__DATE__, __DATA_JSON__, __APP_JS__) are filled
    in via plain string replacement in render_for_date_range, not .format()."""
    return (Path(__file__).resolve().parent / "template.html").read_text(encoding="utf-8")


def _load_page_script() -> str:
    """The page's client-side JS (app/renderer/template.js), substituted into
    template.html's __APP_JS__ placeholder. Kept as a real .js file for the
    same reason as _load_page_template above."""
    return (Path(__file__).resolve().parent / "template.js").read_text(encoding="utf-8")



_COLLECT_FULL_ENDING_FATHER = (
    "Per Dóminum nostrum Iesum Christum, Fílium tuum, qui tecum vivit et regnat "
    "in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum."
)
_COLLECT_FULL_ENDING_SON_TECUM = "qui tecum vivit et regnat in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum."
_COLLECT_FULL_ENDING_SON_VIVIS = "Qui vivis et regnas cum Deo Patre in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum."

# Real printed breviaries traditionally end most collects with one of these
# short abbreviations (the reader silently supplies the full conclusion
# aloud) - ordered longest-first so e.g. "Per Dóminum nostrum Iesum Christum,
# Fílium tuum" is matched whole rather than falling through to the shorter
# "Per Dóminum" and leaving a dangling fragment unreplaced.
_COLLECT_ABBREVIATIONS = sorted([
    ("Per eúndem Christum Dóminum nostrum", _COLLECT_FULL_ENDING_FATHER),
    ("Per eundem Christum Dominum nostrum", _COLLECT_FULL_ENDING_FATHER),
    ("Per eúndem Dóminum nostrum", _COLLECT_FULL_ENDING_FATHER),
    ("Per eundem Dominum nostrum", _COLLECT_FULL_ENDING_FATHER),
    ("Per Dóminum nostrum Iesum Christum, Fílium tuum", _COLLECT_FULL_ENDING_FATHER),
    ("Per Dominum nostrum Iesum Christum, Filium tuum", _COLLECT_FULL_ENDING_FATHER),
    ("Per Christum Dóminum nostrum", _COLLECT_FULL_ENDING_FATHER),
    ("Per Christum Dominum nostrum", _COLLECT_FULL_ENDING_FATHER),
    ("Per eúndem", _COLLECT_FULL_ENDING_FATHER),
    ("Per eundem", _COLLECT_FULL_ENDING_FATHER),
    ("Per Dóminum", _COLLECT_FULL_ENDING_FATHER),
    ("Per Dominum", _COLLECT_FULL_ENDING_FATHER),
    ("Qui tecum", _COLLECT_FULL_ENDING_SON_TECUM),
    ("Qui vivis", _COLLECT_FULL_ENDING_SON_VIVIS),
], key=lambda pair: -len(pair[0]))


def _expand_latin_collect_ending(text: str) -> str:
    """Expands a Latin collect's traditional printed-abbreviation ending
    ('Per Dominum.', 'Qui vivis.', etc. - see _COLLECT_ABBREVIATIONS) into
    the full Trinitarian conclusion, since this project renders text as
    given rather than relying on the reader to supply it aloud. A collect
    already ending in a full conclusion is left untouched (detected by the
    presence of 'unitate Spiritus Sancti' near the end); one missing any
    conclusion at all gets the standard Father-addressed ending appended,
    correct for the overwhelming majority of Roman collects (the rarer
    'Qui vivis'/'Qui tecum' - Son-addressed - forms are only ever produced
    here when the source text itself already ends that way)."""
    if not text:
        return text
    stripped = text.rstrip()
    tail_window = stripped[-160:]
    if "unitáte Spíritus Sancti" in tail_window or "unitate Spiritus Sancti" in tail_window:
        return text
    # A lone trailing '$' is a stray, unclosed emphasis marker left over from
    # the source scan (e.g. "...mereamur. $Per eundem") - not meaningful
    # content, so drop it before matching the abbreviation itself.
    dollar_idx = stripped.rfind("$")
    working = (stripped[:dollar_idx] + stripped[dollar_idx + 1:]).rstrip() if dollar_idx != -1 and dollar_idx >= len(stripped) - 40 else stripped
    for abbr, full in _COLLECT_ABBREVIATIONS:
        if working.endswith(abbr + "."):
            return working[: -(len(abbr) + 1)].rstrip() + " " + full
        if working.endswith(abbr):
            return working[: -len(abbr)].rstrip() + " " + full
    if working.endswith((":", ";")):
        working = working[:-1] + "."
    elif not working.endswith("."):
        working += "."
    return working + " " + _COLLECT_FULL_ENDING_FATHER


def _expand_all_collect_endings(hours_data: dict) -> None:
    """Applied once, centrally, to every hour's concluding_prayer unit before
    a built day is handed back - there are half a dozen separate code paths
    that populate a Latin collect (sanctorale records, seasonal ferial
    tables, the Ordinary-Time-Sunday-reuse table, movable Solemnities...);
    normalizing here instead of at each source avoids having to find and
    patch every one of them individually, and guarantees nothing new can
    slip through un-expanded."""
    for hour_units in hours_data.values():
        if not hour_units:
            continue
        for unit in hour_units:
            if unit.get("label") == "concluding_prayer" and unit.get("content"):
                la = unit["content"].get("la")
                if la:
                    unit["content"]["la"] = _expand_latin_collect_ending(la)


def resolve_and_build_day(d: date, corpora: dict, proper: dict):
    """Wraps _resolve_and_build_day_inner to overlay a Solemnity's First
    Vespers onto the PRECEDING evening (GILH SS141-143): 'habet_primas_
    vesperas' sanctorale records (Christmas, the Annunciation, the
    Assumption, St Joseph, the Nativity of John the Baptist, etc. - 11 as of
    this writing) only ever got their Vespers built on their OWN day before
    this; nothing rendered Vespers I on the evening before, so e.g. Dec 24
    never showed Christmas's First Vespers.

    Overlaying (rather than making this its own branch in the inner
    function) is deliberate: it must be able to override whatever ANY of
    that function's branches already produced for today, and only when
    today doesn't itself outrank a First Vespers eve per UNLY's Table of
    Liturgical Days: a Solemnity/Festum record, and the Triduum, keep their
    own (second) Vespers or omission; a privileged Sunday (of Advent, Lent,
    or Easter - Table item "2-I") outranks a General Solemnity's First
    Vespers (Table item "2-II", a lower sub-tier of the same rank 2 - not a
    different rank entirely) so also keeps its own, confirmed by direct
    testing for the one case this can actually arise in practice (Advent 4
    Sunday landing on Dec 24, since every OTHER habet_primas_vesperas
    Solemnity's eve is a fixed date that can coincide with at most an
    Ordinary Time Sunday, never a privileged one - see
    _apply_advent_sunday_o_antiphon_override for how that specific case's
    Magnificat antiphon is still sourced correctly despite the Sunday
    keeping its own Vespers); every other day - ferial, an unprivileged
    (Ordinary Time) Sunday, a non-Sunday Advent/Lent/Easter day - yields to
    it."""
    hours_data, desc_tag = _resolve_and_build_day_inner(d, corpora, proper)
    if hours_data is None:
        return hours_data, desc_tag

    tomorrow_record = resolve_sanctorale_for_date(d + timedelta(days=1))
    if (tomorrow_record and tomorrow_record["gradus"] == "SOLLEMNITAS"
            and tomorrow_record.get("habet_primas_vesperas")):
        kind, weekday = desc_tag[0], desc_tag[3]
        is_privileged_sunday = weekday == "Sunday" and kind in ("advent", "lent", "easter")
        if kind not in ("sollemnitas", "festum", "triduum") and not is_privileged_sunday:
            hours_data["vespers"] = build_sanctorale_hour_units("vespers_i", tomorrow_record, corpora, proper)
            _expand_all_collect_endings(hours_data)
            return hours_data, desc_tag

    # Sanctorale records and the movable Solemnities of the Lord are disjoint
    # date sets, so falling through here (rather than an elif) is safe - at
    # most one of the two overlays can ever apply to a given "tomorrow".
    hours_data = _overlay_movable_solemnity_first_vespers(d, hours_data, desc_tag, corpora, proper)
    _expand_all_collect_endings(hours_data)
    return hours_data, desc_tag


# breviarium_id (see breviarium_primary_hour_units) for each movable Solemnity
# of the Lord's own First-Vespers-eve entry - these have no sanctorale/
# record at all (they're the hardcoded-date special cases above, resolved
# by year via resolver.py, never entered into resolve_sanctorale_for_date's
# system), so the habet_primas_vesperas overlay above never sees them and
# the evening before each one silently fell through to a plain ferial/
# ordinary-numbered-Sunday day until this was added.
MOVABLE_SOLEMNITY_FIRST_VESPERS_IDS = {
    "most_holy_trinity": "most_holy_trinity_1v",
    "most_holy_body_and_blood_of_christ": "most_holy_body_and_blood_of_christ_1v",
    "most_sacred_heart_of_jesus": "most_sacred_heart_of_jesus_1v",
    "our_lord_jesus_christ_king_of_the_universe": "our_lord_jesus_christ_king_of_the_universe_1v",
}


def _overlay_movable_solemnity_first_vespers(d: date, hours_data: dict, desc_tag, corpora: dict, proper: dict):
    """Same GILH SS141-143 First-Vespers-eve overlay as resolve_and_build_day's
    sanctorale one above, for the 4 movable Solemnities of the Lord (Trinity,
    Corpus Christi, Sacred Heart, Christ the King), which aren't sanctorale
    records so the other overlay never triggers for them."""
    tomorrow = d + timedelta(days=1)
    tomorrow_id = None
    if tomorrow == most_holy_trinity(tomorrow.year):
        tomorrow_id = "most_holy_trinity"
    elif tomorrow == corpus_christi(tomorrow.year):
        tomorrow_id = "most_holy_body_and_blood_of_christ"
    elif tomorrow == sacred_heart_of_jesus(tomorrow.year):
        tomorrow_id = "most_sacred_heart_of_jesus"
    elif tomorrow == christ_the_king(tomorrow.year):
        tomorrow_id = "our_lord_jesus_christ_king_of_the_universe"
    if tomorrow_id is None:
        return hours_data

    kind, weekday = desc_tag[0], desc_tag[3]
    is_privileged_sunday = weekday == "Sunday" and kind in ("advent", "lent", "easter")
    if kind in ("sollemnitas", "festum", "triduum") or is_privileged_sunday:
        return hours_data

    vespers_i_units = breviarium_primary_hour_units(
        "vespers", MOVABLE_SOLEMNITY_FIRST_VESPERS_IDS[tomorrow_id], corpora, proper, tomorrow)
    if vespers_i_units is not None:
        hours_data["vespers"] = vespers_i_units
    return hours_data


LITURGICAL_COLOR_MAP = {
    "ALBUS": "white", "VIRIDIS": "green", "VIOLACEUS": "violet", "RUBER": "red", "ROSEUS": "rose",
}

GRADUS_LABELS = {
    "SOLLEMNITAS": {"en": "Solemnity", "es": "Solemnidad", "la": "Sollemnitas"},
    "FESTUM": {"en": "Feast", "es": "Fiesta", "la": "Festum"},
    "MEMORIA_OBLIGATORIA": {"en": "Memorial", "es": "Memoria", "la": "Memoria"},
    "MEMORIA_AD_LIBITUM": {"en": "Optional Memorial", "es": "Memoria libre", "la": "Memoria ad libitum"},
}


def liturgical_color_key(desc_tag) -> str:
    """Best-effort liturgical color for the Settings tab's Liturgical Color
    Sync + the main page's color badge. A sanctorale record's own `color`
    field always wins when present (GILH's color rules are keyed to the
    specific celebration, not just the season); otherwise falls back to the
    season's standard color, including the Gaudete/Laetare rose exception
    (Advent week 3 Sunday / Lent week 4 Sunday - `psalter_week` is repurposed
    as week_number for both of those kinds, see build_day_description)."""
    kind, psalter_week, ot_week_number, weekday, feast = desc_tag
    if feast and feast.get("color") in LITURGICAL_COLOR_MAP:
        return LITURGICAL_COLOR_MAP[feast["color"]]
    if kind in ("christmas", "easter"):
        return "white"
    if kind == "advent":
        return "rose" if (weekday == "Sunday" and psalter_week == 3) else "violet"
    if kind == "lent":
        return "rose" if (weekday == "Sunday" and psalter_week == 4) else "violet"
    if kind == "triduum":
        if ot_week_number == "holy_thursday":
            return "white"
        if ot_week_number == "friday_of_the_passion_of_the_lord":
            return "red"
        return "violet"  # Holy Saturday: no true Mass color, violet is the safe default
    return "green"  # Ordinary Time (Sunday or ferial)


def build_liturgical_meta(desc_tag) -> dict:
    """{color, rank, title} for the main page's Liturgical Calendar Hero
    banner and the Settings tab's Liturgical Color Sync. `title`/`rank` are
    only populated when a sanctorale record is actually being celebrated
    (a named saint) - for a plain ferial/season day, build_day_description's
    own text already fully describes the day, so the caller falls back to
    that instead of duplicating it here."""
    kind, psalter_week, ot_week_number, weekday, feast = desc_tag
    color = liturgical_color_key(desc_tag)
    if feast:
        rank = GRADUS_LABELS.get(feast.get("gradus"), {"en": "", "es": "", "la": ""})
        title = {lang: feast["titulus"] for lang in ("en", "es", "la")}
    else:
        rank = {"en": "", "es": "", "la": ""}
        title = None
    return {"color": color, "rank": rank, "title": title}


def build_day_description(desc_tag) -> dict:
    kind, psalter_week, ot_week_number, weekday, feast = desc_tag
    is_sunday = (kind == "sunday")
    if kind in ("sollemnitas", "festum"):
        return {lang: feast["titulus"] for lang in ("en", "es", "la")}
    if kind == "christmas":
        # ot_week_number is repurposed here as breviarium_id - see
        # resolve_and_build_day's christmas branch.
        day_desc = {
            lang: christmas_day_description(weekday, ot_week_number, lang)
            for lang in ("en", "es", "la")
        }
        if feast:
            note = f" &mdash; {feast['titulus']}"
            for lang in day_desc:
                day_desc[lang] += note
        return day_desc
    if kind == "advent":
        # psalter_week/ot_week_number are repurposed here as week_number/
        # day_of_month - see resolve_and_build_day's advent branch.
        day_desc = {
            lang: advent_day_description(weekday, psalter_week, ot_week_number, lang, is_sunday=(weekday == "Sunday"))
            for lang in ("en", "es", "la")
        }
        if feast:
            note = f" &mdash; {feast['titulus']}"
            for lang in day_desc:
                day_desc[lang] += note
        return day_desc
    if kind == "lent":
        # psalter_week/ot_week_number are repurposed here as week_number/
        # named breviarium_id - see resolve_and_build_day's lent branch.
        day_desc = {
            lang: lent_day_description(weekday, psalter_week, ot_week_number, lang, is_sunday=(weekday == "Sunday"))
            for lang in ("en", "es", "la")
        }
        if feast:
            note = f" &mdash; {feast['titulus']}"
            for lang in day_desc:
                day_desc[lang] += note
        return day_desc
    if kind == "easter":
        # psalter_week/ot_week_number are repurposed here as week_number/
        # named breviarium_id - see resolve_and_build_day's easter branch.
        day_desc = {
            lang: easter_day_description(weekday, psalter_week, ot_week_number, lang, is_sunday=(weekday == "Sunday"))
            for lang in ("en", "es", "la")
        }
        if feast:
            note = f" &mdash; {feast['titulus']}"
            for lang in day_desc:
                day_desc[lang] += note
        return day_desc
    if kind == "triduum":
        # ot_week_number is repurposed here as breviarium_id - see
        # resolve_and_build_day's triduum branch. No feast/record possible
        # here (always None - the Triduum outranks every sanctorale entry).
        return {lang: triduum_day_description(ot_week_number, lang) for lang in ("en", "es", "la")}
    day_desc = {
        lang: day_description(weekday, ot_week_number, psalter_week, lang, is_sunday=is_sunday)
        for lang in ("en", "es", "la")
    }
    if feast:
        note = f" &mdash; {feast['titulus']}"
        for lang in day_desc:
            day_desc[lang] += note
    return day_desc


def build_date_payload(d: date, corpora: dict, proper: dict):
    """The {date_human, day_description, hours} shape for a single date, or None
    if d is out of Phase 1 scope. Shared by the static generator (render_for_date_range)
    and dev_server.py's /api/day endpoint, so both go through the exact same
    resolution logic - dev_server.py never re-implements this in JS."""
    hours_data, desc_tag = resolve_and_build_day(d, corpora, proper)
    if hours_data is None:
        return None
    return {
        "date_human": {lang: date_human(d, lang) for lang in ("en", "es", "la")},
        "day_description": build_day_description(desc_tag),
        "liturgical_meta": build_liturgical_meta(desc_tag),
        "hours": hours_data,
    }


def render_for_date_range(center_date: date, days_before: int, days_after: int, out_name):
    """Builds every date from center_date - days_before to center_date + days_after
    and embeds all of them in one page. Without dev_server.py running, a client can't
    ask for a day outside this window - but baking in a wide-enough window lets the
    page pick the right day for whatever timezone the viewer is actually in (the
    generator's own "today" won't match every viewer's "today" 1:1), rather than
    just statically showing one fixed day and warning when it's stale.
    out_name: a single filename, or a list/tuple of filenames to write the exact
    same computed page to more than once (e.g. "demo_today.html" AND
    "index.html", so GitHub Pages - which needs docs/index.html as the landing
    page - always stays in sync with the rolling demo without a separate copy
    step)."""
    corpora = {lang: BibleCorpus(lang) for lang in LANGUAGES}
    proper = {lang: ProperTextLibrary(lang) for lang in LANGUAGES}

    dates_data = {}
    for offset in range(-days_before, days_after + 1):
        d = center_date + timedelta(days=offset)
        payload = build_date_payload(d, corpora, proper)
        if payload is None:
            continue  # out of Phase 1 scope for this date; simply omitted from the picker
        dates_data[d.isoformat()] = payload

    if not dates_data:
        raise SystemExit(f"No dates in range around {center_date} are in Phase 1 scope")

    data = {
        "languages": LANGUAGES,
        "hour_order": ALL_HOURS_ORDER,
        "implemented_hours": IMPLEMENTED_HOURS,
        "default_hour": "vespers",
        "hour_labels": HOUR_LABELS,
        "unit_labels": UNIT_LABELS,
        "chrome_labels": CHROME_LABELS,
        "tz_region_names": TZ_REGION_NAMES,
        "hymn_pools": build_hymn_pools(),
        "our_father_bread_variants": load_static("our_father_bread_variants"),
        "dates": dates_data,
        "date_order": sorted(dates_data.keys()),
        "generated_date": center_date.isoformat(),
    }

    html = _load_page_template()
    html = html.replace("__APP_JS__", _load_page_script())
    html = html.replace("__DATE__", center_date.isoformat())
    html = html.replace("__DATA_JSON__", json.dumps(data, ensure_ascii=False))

    out_names = [out_name] if isinstance(out_name, str) else list(out_name)
    for name in out_names:
        out_path = APP_ROOT.parent / "docs" / name
        out_path.write_text(html, encoding="utf-8")
        print(f"Wrote {out_path} ({len(dates_data)} dates: {min(dates_data)} to {max(dates_data)})")


def render_for_date(demo_date: date, out_name: str):
    """Single-date convenience wrapper - a range of exactly one day."""
    render_for_date_range(demo_date, 0, 0, out_name)


def copy_docs_assets():
    """Mirrors the handful of files docs/*.html reference by a docs-relative
    path (see the "Locally-supplied liturgical typefaces" comment in
    template.html and the hymns.json fetch in template.js) into docs/ itself,
    so those references resolve correctly both under GitHub Pages (which
    serves docs/ AS the site root - a project-root-relative path 404s there)
    and under the local dev server (which serves the whole project root, so
    a docs-relative path still lands on the same real files one level up).
    Cheap to just overwrite every time rather than diffing first."""
    project_root = APP_ROOT.parent
    docs = project_root / "docs"

    fonts_dst = docs / "fonts"
    fonts_dst.mkdir(parents=True, exist_ok=True)
    for font_file in (project_root / "fonts").glob("*.ttf"):
        shutil.copy2(font_file, fonts_dst / font_file.name)

    hymns_src = project_root / "content" / "proper_texts" / "hymns.json"
    hymns_dst = docs / "content" / "proper_texts" / "hymns.json"
    hymns_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(hymns_src, hymns_dst)

    print(f"Copied fonts + hymns.json into {docs}")


if __name__ == "__main__":
    render_for_date(date(2026, 7, 30), "demo_vespers.html")       # ferial Thursday (regression check)
    render_for_date(date(2026, 8, 2), "demo_sunday.html")          # Sunday (new)
    render_for_date(date(2026, 1, 21), "demo_memorial.html")       # St Agnes, Wed - Common of Virgins override
    render_for_date(date(2026, 8, 1), "demo_saturday.html")        # Saturday -> Sunday's First Vespers (new)
    # 3 days before today through a full week ahead, so viewers in any timezone
    # land inside the window and the page can auto-select their actual "today".
    # Also written to index.html - GitHub Pages serves docs/ as the site root
    # and needs that exact filename for the bare domain to load anything.
    render_for_date_range(date.today(), 3, 7, ["demo_today.html", "index.html"])
    copy_docs_assets()
